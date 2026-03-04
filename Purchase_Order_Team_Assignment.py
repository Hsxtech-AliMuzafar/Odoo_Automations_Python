# Target Model: purchase.order
# Trigger: On Creation
# Purpose: Auto-assign Purchase Representative + Create Buyer Activity

# Mapping: Sales Team ID -> Purchaser User ID
TEAM_TO_PURCHASER = {
    4:  9,  # Commercial -> Rohan
    5:  8,  # CCS -> Chintan
    15: 30, # SWEP -> Nagi
    16: 32, # ITES OPEN Mkt Bid -> Ben
    17: 32, # ITES OPEN Mkt Bid -> Ben
    19: 32, # ITES OPEN Mkt Bid -> Ben
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
    
    unique_team_ids = []
    for so in sale_orders:
        if so.team_id:
            unique_team_ids.append(so.team_id.id)
            
    # Fallback: Check creator (if not OdooBot, and only if no SO found)
    if not unique_team_ids:
        creator = record.create_uid or env.user
        if creator.id != 1:
            try:
                if creator.team_id: 
                    unique_team_ids.append(creator.team_id.id)
            except: 
                pass
            search_teams = env['crm.team'].search(['|', ('member_ids', 'in', [creator.id]), ('user_id', '=', creator.id)])
            unique_team_ids.extend(search_teams.ids)

    # Dedup Team IDs
    final_team_ids = []
    for t_id in unique_team_ids:
        if t_id not in final_team_ids: 
            final_team_ids.append(t_id)

    assigned_purchaser_id = None
    matched_team_name = ""

    # 2. Check for matches in the mapping
    for t_id in final_team_ids:
        if t_id in TEAM_TO_PURCHASER:
            assigned_purchaser_id = TEAM_TO_PURCHASER[t_id]
            matched_team = env['crm.team'].browse(t_id)
            matched_team_name = matched_team.name or "Unknown"
            break

    # 3. Apply the assignment & Create Activity
    if assigned_purchaser_id:
        purchaser = env['res.users'].browse(assigned_purchaser_id)
        if purchaser.exists():
            # Set the "Purchase Representative" field
            record.write({'user_id': assigned_purchaser_id})
            
            # Post to chatter
            post_to_chatter(record, "<b>Automation:</b> Assigned Purchase Representative <b>%s</b> based on Sales Team <b>%s</b>." % (purchaser.name, matched_team_name))
            
            # Create Activity
            try:
                # Get the "To-Do" activity type
                todo_type = env.ref('mail.mail_activity_data_todo', raise_if_not_found=False)
                todo_id = todo_type.id if todo_type else False
                
                # Deadline is today - using record.create_date as it's safe in the sandbox
                deadline = record.create_date or time.strftime('%Y-%m-%d')
                
                env['mail.activity'].create({
                    'res_model_id': env['ir.model']._get_id('purchase.order'),
                    'res_id': record.id,
                    'activity_type_id': todo_id,
                    'summary': 'New PO Assigned (Team: %s)' % matched_team_name,
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
        # Trace log if no match found
        debug_msg = "<b>Automation Trace:</b> No match for Team IDs: %s" % (str(final_team_ids))
        post_to_chatter(record, debug_msg)

except Exception as e:
    try:
        # Log error
        post_to_chatter(record, "<b>Automation Error:</b> %s" % str(e))
    except:
        pass
