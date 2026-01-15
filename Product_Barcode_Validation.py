# Automation Rule for product.template.barcode
# Model: product.template.barcode
# Trigger: On Creation & Update
# Trigger Fields: name (the barcode field)
#
# Description:
# Prevents duplicate barcodes by searching across both product.template (standard barcode and default_code)
# and product.template.barcode (custom multi-barcode lines).

barcode_to_check = record.name

if barcode_to_check:
    # 1. Check for duplicates in the product.template.barcode model (other records)
    # Note: We exclude the current record ID to avoid false positives on update.
    domain = [
        ('name', '=', barcode_to_check),
        ('id', '!=', record.id)
    ]
    duplicate_line = env['product.template.barcode'].search(domain, limit=1)
    
    if duplicate_line:
        # Try to get the product template name from the duplicate line
        p_name = "another product"
        if 'product_tmpl_id' in duplicate_line._fields and duplicate_line.product_tmpl_id:
            p_name = duplicate_line.product_tmpl_id.display_name
        
        raise UserError("This barcode is already used on: %s" % p_name)

    # 2. Check for duplicates in the standard product.template model
    # We check both 'barcode' and 'default_code' (Internal Reference)
    duplicate_product = env['product.template'].search([
        '|', ('barcode', '=', barcode_to_check), ('default_code', '=', barcode_to_check)
    ], limit=1)
    
    if duplicate_product:
        raise UserError("This barcode conflicts with product: %s" % duplicate_product.display_name)

## Powered By HSx Tech
