# Automation Action for Product Template or Product Product
# Trigger: On Creation & Update
# Target Model: product.template or product.product
#
# Description:
# Keeps list_price (Sales Price) and standard_price (Cost) synchronized
# for the product with Internal Reference 'P24K001'.
#
# Note: Since the user added a domain on Odoo's side, this check provides
# an extra layer of safety.

if record.default_code == 'P24K001':
    # LOGIC: Enforce Standard Price (Cost) follows List Price (Sales Price)
    # This assumes List Price is the 'Master' value.
    if record.list_price != record.standard_price:
        record['standard_price'] = record.list_price
        
## Powered By HSx Tech
## Ali and Muneeb
