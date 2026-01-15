# Automation Rule for product.template
# Model: product.template
# Trigger: On Creation & Update
# Trigger Fields: barcode, default_code
#
# Description:
# Prevents duplicate barcodes and internal references by searching across product.template
# and the custom barcode line model product.template.barcode.
# Ensures that barcode and default_code are unique across all models.

# Check barcode field
if record.barcode:
    barcode_to_check = record.barcode
    
    # 1. Check for duplicates in product.template (other records)
    domain = [
        ('id', '!=', record.id),
        '|', ('barcode', '=', barcode_to_check), ('default_code', '=', barcode_to_check)
    ]
    duplicate_product = env['product.template'].search(domain, limit=1)
    
    if duplicate_product:
        raise UserError("This barcode/reference is already used on product: %s" % duplicate_product.display_name)
    
    # 2. Check for duplicates in product.template.barcode
    duplicate_line = env['product.template.barcode'].search([('name', '=', barcode_to_check)], limit=1)
    
    if duplicate_line:
        p_name = "another product"
        if 'product_tmpl_id' in duplicate_line._fields and duplicate_line.product_tmpl_id:
            p_name = duplicate_line.product_tmpl_id.display_name
        raise UserError("This barcode is already used as a barcode line on: %s" % p_name)

# Check default_code field (Internal Reference)
if record.default_code:
    ref_to_check = record.default_code
    
    # 1. Check for duplicates in product.template (other records)
    domain = [
        ('id', '!=', record.id),
        '|', ('barcode', '=', ref_to_check), ('default_code', '=', ref_to_check)
    ]
    duplicate_product = env['product.template'].search(domain, limit=1)
    
    if duplicate_product:
        raise UserError("This reference/barcode is already used on product: %s" % duplicate_product.display_name)
    
    # 2. Check for duplicates in product.template.barcode
    duplicate_line = env['product.template.barcode'].search([('name', '=', ref_to_check)], limit=1)
    
    if duplicate_line:
        p_name = "another product"
        if 'product_tmpl_id' in duplicate_line._fields and duplicate_line.product_tmpl_id:
            p_name = duplicate_line.product_tmpl_id.display_name
        raise UserError("This reference is already used as a barcode line on: %s" % p_name)

## Powered By HSx Tech
