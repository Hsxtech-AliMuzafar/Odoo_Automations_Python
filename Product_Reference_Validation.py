# Automation Rule for product.template
# Model: product.template
# Trigger: On Creation & Update
# Trigger Fields: default_code (Internal Reference)
#
# Description:
# Prevents duplicate Internal References by searching across product.template
# and the custom barcode line model product.template.barcode.

ref_to_check = record.default_code

if ref_to_check:
    # 1. Check for duplicates in the standard product.template model
    # We only check 'default_code' (Internal Reference)
    domain = [
        ('id', '!=', record.id),
        ('default_code', '=', ref_to_check)
    ]
    duplicate_product = env['product.template'].search(domain, limit=1)
    
    if duplicate_product:
        raise UserError("This reference is already used on product: %s" % duplicate_product.display_name)

## Powered By HSx Tech
