# Automation to prevent users from adding products in Stock Quant window
# Model: stock.quant
# Trigger: On Creation & Update
# Trigger Fields: product_id (watch for product changes)
#
# Purpose: Only allow specific users to add products/lines to inventory adjustment

# Define the list of ALLOWED user IDs (all others will be blocked)
allowed_user_ids = [18, 20, 22, 2, 17, 23, 19]

# Check if the current user is NOT in the allowed list
if env.user.id not in allowed_user_ids:
    raise UserError("You are not allowed to add new lines.")
