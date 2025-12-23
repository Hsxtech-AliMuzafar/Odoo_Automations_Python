# Automation to assign current user to Sales Person field
# Model: sale.order
# Trigger: On Creation / Update or Manual Action

if record:
    record['user_id'] = env.user.id
