# Automation Rule for project.project
# Model: Project (project.project)
# Trigger: On Deletion
#
# Description:
# When a project is deleted, this script finds the related CRM Lead 
# using the 'x_studio_linked' field and archives it.

# Search for the lead that links to this project
lead = env['crm.lead'].search([
    ('x_studio_linked', '=', record.id),
    ('active', '=', True)
], limit=1)

if lead:
    # Log the action in chatter before archiving
    lead.message_post(body="Archived automatically because the related Project '%s' was deleted." % record.name)
    # Archive the lead
    lead.write({'active': False})

## Powered By HSx Tech
