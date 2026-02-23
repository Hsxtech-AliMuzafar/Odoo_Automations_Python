# Automation Rule for hr.expense
# Model: Expense (hr.expense)
# Trigger: On Save (Creation & Update)
# Before Update Domain: [('state', '=', 'draft')]
# Apply On: [('state', '!=', 'draft')]
#
# Description:
# This script ensures that an expense has a receipt (attachment) before it is 
# moved from the 'draft' state to any other state (e.g., reported, approved).
# If no receipt is found, it raises a UserError to block the transition.

# Check if the record has any attachments
# Odoo's hr.expense model has a field 'nb_attachment' (in recent versions)
# that tracks the number of attachments.
if not record.nb_attachment:
    raise UserError("Please attach a receipt before submitting this expense.")

## Powered By HSx Tech
