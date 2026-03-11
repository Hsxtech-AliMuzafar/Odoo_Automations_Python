# Target Model: account.move
# Trigger: On Update (Trigger Fields: payment_state)

TARGET_TAG_NAME = "Paid"

def post_to_chatter(record, body):
    """Post an HTML message using the user's proven creation method."""
    env['mail.message'].create({
        'model': record._name,
        'res_id': record.id,
        'message_type': 'comment',
        'body': body,
        'subtype_id': env.ref('mail.mt_note').id,
        'author_id': env.user.partner_id.id,
    })

def record_link(rec):
    """Generate a clickable record link."""
    rid = rec.id or (hasattr(rec, '_origin') and rec._origin.id)
    name = rec.name or rec.display_name or "Document"
    if not rid:
        return "<b>{}</b>".format(name)
    base_url = rec.get_base_url()
    url = "{}/odoo/{}/{}".format(base_url.rstrip('/'), rec._name, rid)
    return "<a href='{}'>{}</a>".format(url, name)

try:
    # 1. Triggered on payment_state update. Check if it's now 'paid' or 'in_payment'
    if record.payment_state in ['paid', 'in_payment']:
        
        # 2. Find associated CRM Lead(s)
        # Sequence: account.move -> sale.order (via line_ids.sale_line_ids) -> crm.lead (opportunity_id)
        sale_orders = record.line_ids.mapped('sale_line_ids.order_id')
        leads = sale_orders.mapped('opportunity_id').filtered(lambda l: l.active or not l.active)
        
        if leads:
            # 3. Ensure 'Paid' and 'Unpaid' tags exist/are found
            Tag = env['crm.tag']
            paid_tag = Tag.search([('name', '=', TARGET_TAG_NAME)], limit=1)
            unpaid_tag = Tag.search([('name', '=', 'Unpaid')], limit=1)
            
            if not paid_tag:
                paid_tag = Tag.create({'name': TARGET_TAG_NAME})
            
            for lead in leads:
                # 4. Add the 'Paid' tag and remove 'Unpaid' tag
                vals = {}
                updates = []
                
                # Add 'Paid' tag if not present
                if paid_tag.id not in lead.tag_ids.ids:
                    updates.append((4, paid_tag.id))
                
                # Remove 'Unpaid' tag if present
                if unpaid_tag and unpaid_tag.id in lead.tag_ids.ids:
                    updates.append((3, unpaid_tag.id))
                
                if updates:
                    lead.write({'tag_ids': updates})
                    
                    # 5. Log in chatter
                    invoice_doc = record_link(record)
                    tag_change_desc = "'<b>%s</b>' added" % TARGET_TAG_NAME
                    if unpaid_tag and unpaid_tag.id in lead.tag_ids.ids: # Check if it was actually removed (though logic above handles it)
                         tag_change_desc += " and '<b>Unpaid</b>' removed"
                    
                    body = "Automation: Tag %s because related Invoice %s is now Paid." % (tag_change_desc, invoice_doc)
                    post_to_chatter(lead, body)
                    
                    # 6. UI Notification Popup (Odoo 19)
                    try:
                        env['bus.bus']._sendone(env.user.partner_id, 'simple_notification', {
                            'title': 'CRM Lead Updated',
                            'message': 'Lead "%s" updated to Paid status.' % lead.name,
                            'type': 'success',
                            'sticky': False,
                        })
                    except:
                        pass
        else:
            # Optional: Log on invoice if no lead found (debug)
            # post_to_chatter(record, "Automation Note: No linked CRM Opportunity found to tag as Paid.")
            pass

except Exception as e:
    try:
        post_to_chatter(record, "Automation Error (CRM Tag Update): %s" % str(e))
    except:
        pass
