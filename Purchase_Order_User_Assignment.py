# Target Model: purchase.order
# Trigger: On Creation
# Purpose: Auto-assign Purchase Representative based on linked SO Salesperson

# Mapping: Salesperson User ID -> Purchaser User ID
USER_TO_PURCHASER = {
    11: 8,  # Ali -> Chintan
    12: 8,  # Harun -> Chintan
    7:  9,  # Ali Z -> Rohan
    10: 9,  # Kashif -> Rohan
    13: 9,  # SAL -> Rohan
    14: 9,  # Azam -> Rohan
    15: 9,  # Ashwin -> Rohan
    16: 9,  # Usman -> Rohan
    17: 9,  # Bilal -> Rohan
    18: 9,  # Jason -> Rohan
    19: 9,  # Farooq -> Rohan
}

def post_to_chatter(rec, body):
    """Post an HTML message to the chatter."""
    try:
        env['mail.message'].create({
            'model': rec._name,
            'res_id': rec.id,
            'message_type': 'comment',
            'body': body,
            'subtype_id': env.ref('mail.mt_note').id,
            'author_id': env.user.partner_id.id,
        })
    except:
        pass

try:
    # 1. Identify the linked Sales Order(s)
    sale_orders = env['sale.order']
    
    # Priority 1: Search by 'Source Document' (origin) field
    if record.origin:
        # Split by comma or colon and clean up
        potential_names = [n.strip() for n in record.origin.replace(':', ',').split(',')]
        sale_orders = env['sale.order'].search([('name', 'in', potential_names)])

    # Priority 2: Standard Odoo line-item mapping
    if not sale_orders:
        sale_orders = record.order_line.mapped('sale_line_id.order_id')
    
    unique_user_ids = []
    for so in sale_orders:
        if so.user_id:
            unique_user_ids.append(so.user_id.id)
            
    # Fallback: Check creator (if not OdooBot, and only if no SO found)
    if not unique_user_ids:
        creator = record.create_uid or env.user
        if creator.id != 1: # Skip OdooBot
            unique_user_ids.append(creator.id)

    # Dedup User IDs
    final_user_ids = []
    for u_id in unique_user_ids:
        if u_id not in final_user_ids: 
            final_user_ids.append(u_id)

    assigned_purchaser_id = None
    matched_user_name = ""

    # 2. Check for matches in the mapping
    for u_id in final_user_ids:
        if u_id in USER_TO_PURCHASER:
            assigned_purchaser_id = USER_TO_PURCHASER[u_id]
            matched_user = env['res.users'].browse(u_id)
            matched_user_name = matched_user.name or "Unknown"
            break
    

    # 3. Apply the assignment & Create Activity
    if assigned_purchaser_id:
        purchaser = env['res.users'].browse(assigned_purchaser_id)
        if purchaser.exists():
            # Set the "Purchase Representative" field
            record.write({'user_id': assigned_purchaser_id})
            
            # Post to chatter
            post_to_chatter(record, "<b>Automation:</b> Assigned Purchase Representative <b>%s</b> based on Salesperson/User <b>%s</b>." % (purchaser.name, matched_user_name))
            
            # Create Activity
            try:
                # Get the "To-Do" activity type
                todo_type = env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
                todo_id = todo_type.id if todo_type else False
                
                # Deadline is today
                deadline = record.create_date or time.strftime('%Y-%m-%d')
                
                env['mail.activity'].create({
                    'res_model_id': env['ir.model']._get_id('purchase.order'),
                    'res_id': record.id,
                    'activity_type_id': todo_id,
                    'summary': 'New PO Assigned (Source User: %s)' % matched_user_name,
                    'note': 'Please review and process this Purchase Order.',
                    'user_id': assigned_purchaser_id,
                    'date_deadline': deadline,
                })
            except Exception as act_e:
                post_to_chatter(record, "<b>Automation Note:</b> Could not create activity: %s" % str(act_e))

            # UI Popup notification
            try:
                env['bus.bus']._sendone(env.user.partner_id, 'simple_notification', {
                    'title': 'Purchaser Assigned',
                    'message': 'Buyer %s has been set and notified.' % purchaser.name,
                    'type': 'success',
                })
            except:
                pass
    else:
        # Trace log if no user found to map from
        debug_msg = "<b>Automation Trace:</b> No source user found to determine purchaser assignment."
        post_to_chatter(record, debug_msg)

except Exception as e:
    try:
        # Log error
        post_to_chatter(record, "<b>Automation Error:</b> %s" % str(e))
    except:
        pass
