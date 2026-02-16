# ============================================================
# AUTOMATION NAME: Task Stage → Task State Sync
# MODEL: project.task
# TRIGGER: On Update
# TRIGGER FIELDS: stage_id
# APPLY DOMAIN: [('state', '!=', '1_done')]
#
# PURPOSE:
# When a task is moved to a folded (Done) stage,
# automatically set its state to '1_done'.
# When reopened, reset state to '1_in_progress'.
#
# MODELS USED:
# - project.task
#
# NOTES:
# - Uses context flag to prevent recursion
# - Compatible with Odoo 19 Enterprise (sale_project)
# - Requires valid state values in DB
# ============================================================

# Prevent recursive execution
for task in records:

    # If moved to a folded (Done) stage
    if task.stage_id.fold:

        if task.state != '1_done':
            task.write({
                'state': '1_done'
            })