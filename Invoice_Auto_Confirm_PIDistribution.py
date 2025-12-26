# Automation to Confirm Invoices for Specific Company
# Model: account.move
# Trigger: On Creation or On Update (Suggested: On Creation & Update)
# Targeted Company: PI Distribution SRL (ID: 12)

# Ensure 'record' variable is available (Standard in Odoo Automations)
if record:
    # 1. Check if the record belongs to Company ID 12
    if record.company_id.id == 12:
        
        # 2. Check if the record is currently in 'draft' state (to avoid error on re-posting)
        if record.state == 'draft':
            
            # 3. Check if it is an Invoice or Bill (Excluded Journal Entries usually)
            # Types: out_invoice (Customer Invoice), out_refund (Customer Credit Note/Refund), 
            #        in_invoice (Vendor Bill), in_refund (Vendor Credit Note/Refund)
            if record.move_type in ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']:
                
                # 4. Post the Invoice
                record.action_post()
