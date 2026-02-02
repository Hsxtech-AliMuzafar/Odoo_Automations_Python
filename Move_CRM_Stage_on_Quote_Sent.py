# Target Model: sale.order
# Trigger: On Update (When 'state' becomes 'sent')

TARGET_STAGE_NAME = "Quote Issued"

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

try:
    # 1. Check if the Sale Order is linked to an Opportunity
    if record.opportunity_id:
        Lead = record.opportunity_id
        Stage = env['crm.stage']
        
        # 2. Find the "Quote Issued" stage
        target_stage = Stage.search([('name', '=', TARGET_STAGE_NAME)], limit=1)
        
        if not target_stage:
            post_to_chatter(Lead, "<b>Automation Note:</b> Could not find a stage named '%s'." % TARGET_STAGE_NAME)
        else:
            # 3. Update Stage if needed
            if Lead.stage_id.id != target_stage.id:
                old_stage_name = Lead.stage_id.name
                Lead.write({'stage_id': target_stage.id})
                
                # 4. Generate Internal Links (User's proven pattern)
                quote_link = "<a href='#' data-oe-model='sale.order' data-oe-id='%d'>%s</a>" % (record.id, record.name)
                
                # 5. Log the transition in the Lead's chatter
                body = "Automation: Stage automatically moved from '%s' to '%s' because Quotation %s was sent." % (old_stage_name, TARGET_STAGE_NAME, quote_link)
                
                # Use the ultra-robust creation method
                env['mail.message'].create({
                    'model': Lead._name,
                    'res_id': Lead.id,
                    'message_type': 'comment',
                    'body': body,
                    'subtype_id': env.ref('mail.mt_note').id,
                    'author_id': env.user.partner_id.id,
                })
                
                # 6. UI Notification Popup (Odoo 19)
                try:
                    env['bus.bus']._sendone(env.user.partner_id, 'simple_notification', {
                        'title': 'CRM Updated',
                        'message': 'Opportunity moved to %s.' % TARGET_STAGE_NAME,
                        'type': 'success',
                        'sticky': False,
                    })
                except:
                    pass

except Exception as e:
    post_to_chatter(record, "Automation Error (CRM Stage Update): %s" % str(e))
