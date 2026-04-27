# Project Task Quality Review

## Module Description
Project Task Quality Review extends Odoo Project with a mandatory quality gate before task completion.

Each project can define a Quality Inspector, and tasks can only be completed after QA approval.

## Core Features
- Adds project-level field: Quality Inspector (quality_inspector_id).
- Adds task-level QA fields:
  - Quality Review Passed (is_done)
  - Quality Inspected On (quality_inspected_date)
- Adds stage-level flag: Is Review Stage (is_review_stage) on task stages.
- Auto-assigns the project inspector to task assignees when task enters a review stage.
- Adds Mark Review Passed button on task form header.
- Blocks task completion if QA has not passed.
- Supports state-based completion and closed-stage completion checks.

## Security Model
- Only the configured project Quality Inspector or an Administrator can execute Mark Review Passed.
- The action cannot be executed twice for the same task.
- No sudo usage in business logic.

## Installation
1. Place module folder project_task_quality_review into your custom addons path.
2. Restart Odoo service.
3. Update Apps List.
4. Install Project Task Quality Review.

## Usage Workflow
1. Open a project and set Quality Inspector.
2. Ensure your review stage is flagged with Is Review Stage.
3. Move a task into a review stage.
4. Module auto-adds the Quality Inspector to task assignees if not already assigned.
5. Inspector (or Administrator) opens the task and clicks Mark Review Passed.
6. Module sets is_done and quality_inspected_date.
7. Task can then move to Done or another closed stage.

## Example Scenario
1. Project Website Revamp sets QA Lead as Quality Inspector.
2. Developer moves task Checkout Validation to Ready for Review.
3. QA Lead is auto-assigned to the task.
4. QA Lead clicks Mark Review Passed.
5. Task stores QA approval date.
6. Task is moved to Done.

If QA approval is missing, completion is blocked with:

Task must pass quality review before being marked as Done.
