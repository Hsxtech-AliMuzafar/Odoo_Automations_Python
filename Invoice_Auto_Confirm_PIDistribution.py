# Automation to Confirm Invoices for Specific Company
# Model: account.move
# Trigger: On Creation or On Update (Suggested: On Creation & Update)
# Targeted Company: PI Distribution SRL (ID: 12)

# Ensure 'record' variable is available (Standard in Odoo Automations)
if record:
    # 1. Check if the record belongs to Company ID 12
    if record.company_id.id == 12:
        
        # 2. Check if the record is currently in 'draft' state
        if record.state == 'draft':
            
            # 3. Check if it is an Invoice or Bill
            if record.move_type in ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']:
                
                # 4. Partner specific tax assignment
                if record.partner_id.id in [6598, 15]:
                    for line in record.invoice_line_ids:
                        # Using .write() to avoid 'forbidden opcode: STORE_ATTR'
                        line.write({'tax_ids': [(4, 312)]})
                else:
                    # 5. For other partners, check for empty tax lines and add tax 302
                    for line in record.invoice_line_ids:
                        if not line.tax_ids:
                            # Using .write() to avoid 'forbidden opcode: STORE_ATTR'
                            line.write({'tax_ids': [(4, 302)]})
                
                # 6. Post the Invoice
                record.action_post()
