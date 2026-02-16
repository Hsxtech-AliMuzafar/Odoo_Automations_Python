# ============================================================
# AUTOMATION NAME: Project Auto Close / Reopen
# MODEL: project.task
# TRIGGER: On Update
# TRIGGER FIELDS: stage_id
#
# PURPOSE:
# If all tasks of a project are Done (folded),
# automatically move the project to the "Done" stage.
# If any task is reopened, reopen the project.
# Sends notification to Project Manager when closed.
#
# MODELS USED:
# - project.task
# - project.project
# - project.project.stage
# - bus.bus (for notification)
#
# NOTES:
# - Uses context flag to prevent recursion
# - Searches project Done stage by name (ilike 'Done')
# - Requires Done stage to exist
# ============================================================

# Prevent recursion
for task in records:
    project = task.project_id
    if not project:
        continue

    # Count tasks not in Done (folded = False)
    not_done_count = env['project.task'].search_count([
        ('project_id', '=', project.id),
        ('stage_id.fold', '=', False)
    ])

    # Get Done project stage
    done_stage = env['project.project.stage'].search([
        ('name', 'ilike', 'Done')
    ], limit=1)

    if not done_stage:
        continue

    # -------------------------
    # CLOSE PROJECT
    # -------------------------
    if not_done_count == 0 and project.stage_id != done_stage:

        project.write({
            'stage_id': done_stage.id
        })

        # Send notification
        env['bus.bus']._sendone(
            project.user_id.partner_id,
            'simple_notification',
            {
                'title': 'Project Closed',
                'message': f'Project "{project.name}" has been automatically marked as Done.',
                'type': 'success'
            }
        )

    # -------------------------
    # REOPEN PROJECT
    # -------------------------
    elif not_done_count > 0 and project.stage_id == done_stage:

        # Get first non-folded stage (reopen stage)
        reopen_stage = env['project.project.stage'].search([
            ('fold', '=', False)
        ], order="sequence asc", limit=1)

        if reopen_stage:
            project.write({
                'stage_id': reopen_stage.id
            })