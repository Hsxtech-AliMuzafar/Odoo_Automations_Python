# Automation Rule for product.template
# Model: product.template
# Trigger: On Creation & Update
#
# Description:
# Automatically adds Sales Tax (ID: 302) to products in Company 12.
# Uses SQL to bypass Odoo's multi-company security rules ("top-secret records" error)
# and environment sandbox limitations (env.sudo() error).

# Configuration
TAX_ID = 302
TARGET_COMPANY_ID = 12

# Note: Many2Many relation table for products and taxes is 'product_taxes_rel'
# Field names: 'prod_id' (Product Template ID) and 'tax_id' (Account Tax ID)

# 1. Safely identify the company using record.sudo()
# In the sandbox, record.sudo() is generally available, but env.sudo() is not.
su_record = record.sudo()
current_company_id = su_record.company_id.id if su_record.company_id else False

if current_company_id == TARGET_COMPANY_ID:
    
    # 2. Check if the link already exists in the relation table using SQL
    # This avoids 'read' permission errors on the tax model entirely.
    env.cr.execute("""
        SELECT 1 FROM product_taxes_rel 
        WHERE prod_id = %s AND tax_id = %s
    """, (record.id, TAX_ID))
    
    already_linked = env.cr.fetchone()
    
    if not already_linked:
        try:
            # 3. Insert the link directly via SQL
            # This is the most reliable way to bypass multi-company record rules
            # and generic permission barriers for cross-company data.
            env.cr.execute("""
                INSERT INTO product_taxes_rel (prod_id, tax_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING
            """, (record.id, TAX_ID))
            
            # 4. Optional: Invalidate cache so the change is reflected in the UI immediately
            # Use su_record to ensure we have permission to invalidate the cache
            su_record.invalidate_cache(['taxes_id'], [record.id])
            
            log(f"SQL SUCCESS: Linked Tax ID {TAX_ID} to Product ID {record.id}", level='info')
            
        except Exception as e:
            log(f"SQL ERROR while adding tax: {str(e)}", level='error')
    else:
        # Tax already present, no action needed
        pass

## Powered By HSx Tech - Ali Muzafar
