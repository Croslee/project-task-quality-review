from odoo import Command, _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError


class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    is_review_stage = fields.Boolean(
        string="Is Review Stage",
        help="If enabled, moving a task to this stage triggers quality inspector auto-assignment.",
    )


class ProjectTask(models.Model):
    _inherit = "project.task"

    is_done = fields.Boolean(
        string="Quality Review Passed",
        default=False,
        copy=False,
        help="Checked when this task has passed quality review.",
    )
    quality_inspected_date = fields.Datetime(
        string="Quality Inspected On",
        copy=False,
        readonly=True,
        help="Date and time when quality review was approved.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        sanitized_vals_list = [self._sanitize_quality_tracking_vals(vals) for vals in vals_list]
        tasks = super().create(sanitized_vals_list)
        tasks._assign_quality_inspector_if_ready_for_review()
        return tasks

    def write(self, vals):
        result = super().write(self._sanitize_quality_tracking_vals(vals))

        if "stage_id" in vals:
            self._assign_quality_inspector_if_ready_for_review()

        return result

    @api.constrains("stage_id", "is_done")
    def _check_done_requires_quality_review(self):
        self._validate_done_requires_quality_review()

    def _validate_done_requires_quality_review(self):
        for task in self:
            if task._is_done_target() and not task.is_done:
                raise ValidationError(
                    _("Task must pass quality review before being marked as Done.")
                )

    def action_mark_review_passed(self):
        user = self.env.user
        is_admin = user.has_group("base.group_system")

        for task in self:
            if task.is_done:
                raise UserError(
                    _("This task has already passed quality review.")
                )

            if not is_admin and task.project_id.quality_inspector_id != user:
                raise AccessError(
                    _(
                        "Only the configured Quality Inspector or an Administrator can mark review as passed."
                    )
                )

        now = fields.Datetime.now()
        self.write({"is_done": True, "quality_inspected_date": now})
        return True

    def _assign_quality_inspector_if_ready_for_review(self):
        tasks_to_update = self.filtered(lambda task: task.project_id and task.stage_id)
        for task in tasks_to_update:
            inspector = task.project_id.quality_inspector_id
            if not inspector:
                continue
            if task._is_ready_for_review_stage(task.stage_id) and inspector not in task.user_ids:
                task.write({"user_ids": [Command.link(inspector.id)]})

    @api.model
    def _sanitize_quality_tracking_vals(self, vals):
        vals = dict(vals)
        if vals.get("is_done") and not vals.get("quality_inspected_date"):
            vals["quality_inspected_date"] = fields.Datetime.now()
        if vals.get("is_done") is False:
            vals["quality_inspected_date"] = False
        return vals

    @api.model
    def _is_ready_for_review_stage(self, stage):
        return bool(
            stage
            and "is_review_stage" in stage._fields
            and stage.is_review_stage
        )

    def _is_done_target(self):
        self.ensure_one()
        return self._is_done_stage(self.stage_id)

    @api.model
    def _is_done_stage(self, stage):
        if not stage:
            return False
        if "is_closed" in stage._fields and stage.is_closed:
            return True
        if "fold" in stage._fields and stage.fold:
            return True
        return False
