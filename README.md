# Project Task Quality Review
## What It Does
- Adds a Quality Inspector to each project.
- Marks tasks as QA-approved with a dedicated button.
- Auto-assigns the inspector when a task enters the review stage.
- Blocks task completion until QA has passed.

## Requirements
- Odoo 19
- A custom addons path containing this module
- Access to the Odoo server source or running environment

## Installation
1. Copy the `project_task_quality_review` folder into your custom addons directory.
2. Add that directory to `addons_path` in your Odoo configuration if it is not already included.
3. Restart the Odoo server.
4. Enable Developer Mode in Odoo.
5. Go to Apps and click Update Apps List.
6. Search for `Project Task Quality Review`.
7. Click Install.

## How to Run
1. Open a Project.
2. Set the `Quality Inspector` field.
3. Open or create a Task under that project.
4. Move the task into the review stage flagged as `Is Review Stage`.
5. The project’s Quality Inspector is automatically added to the task’s assignees.
6. The inspector opens the task and clicks `Mark Review Passed`.
7. The module sets `is_done = True` and records `quality_inspected_date`.
8. After approval, the task can be moved to Done.

## Behavior Notes
- If a task is moved to Done before QA approval, Odoo raises a `ValidationError`.
- The `Mark Review Passed` button is hidden once the task is approved.
- The approval action cannot be executed twice.
- Only the configured inspector or an Administrator can approve the task.

## Example Scenario
1. Project `Website Revamp` assigns `QA Lead` as Quality Inspector.
2. A developer moves task `Checkout Validation` to the review stage.
3. `QA Lead` is auto-assigned to the task.
4. `QA Lead` clicks `Mark Review Passed`.
5. The task stores the QA approval timestamp.
6. The team moves the task to Done successfully.

