from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    quality_inspector_id = fields.Many2one(
        "res.users",
        string="Quality Inspector",
        help="User responsible for approving task quality before completion.",
    )
