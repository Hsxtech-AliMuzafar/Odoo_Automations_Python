# ==========================================================
# AUTOMATION: Project Done -> CRM stage "Job Complete"
# Trigger UI:
#   Model: project.project
#   Trigger: On Update
#   Trigger Fields: stage_id
# ==========================================================

TARGET_CRM_STAGE = "Job Complete"

def post_to_chatter(rec, body):
    """Post an HTML message using the user's proven creation method."""
    env['mail.message'].create({
        'model': rec._name,
        'res_id': rec.id,
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
    # 1. Check if the Project is Done
    # We use 'in' for name check to handle variations like "Done" or "Project Done"
    if record.stage_id and "Done" in record.stage_id.name:
        
        # 2. Find the related CRM Lead
        # Linking logic from Create_Projects_from_crm.py uses 'x_studio_linked'
        lead = env['crm.lead'].search([('x_studio_linked', '=', record.id)], limit=1)
        
        # Fallback: check project.sale_order_id.opportunity_id (Standard Odoo link)
        if not lead and hasattr(record, 'sale_order_id') and record.sale_order_id.opportunity_id:
            lead = record.sale_order_id.opportunity_id

        if lead:
            target_stage = env['crm.stage'].search([('name', '=', TARGET_CRM_STAGE)], limit=1)
            
            if not target_stage:
                # Log warning on project if CRM stage is missing
                post_to_chatter(record, "Automation Note: Could not find a CRM stage named '%s'." % TARGET_CRM_STAGE)
            else:
                current_stage = lead.stage_id
                
                # 3. Update if needed and prevent downgrade
                if current_stage.id != target_stage.id:
                    # Downgrade prevention: check sequence
                    if current_stage.sequence > target_stage.sequence:
                        post_to_chatter(lead, "Automation Note: CRM stage change to '%s' skipped (downgrade prevention: current stage follows target)." % TARGET_CRM_STAGE)
                    else:
                        old_name = current_stage.name if current_stage else "None"
                        lead.write({'stage_id': target_stage.id})
                        
                        # 4. Success Notifications
                        project_doc = record_link(record)
                        body = "Automation: Stage automatically moved from '<b>%s</b>' to '<b>%s</b>' because related Project %s is Done." % (old_name, TARGET_CRM_STAGE, project_doc)
                        post_to_chatter(lead, body)
                        
                        # Bus notification for current user
                        try:
                            env['bus.bus']._sendone(env.user.partner_id, 'simple_notification', {
                                'title': 'CRM Updated',
                                'message': 'Opportunity linked to Project "%s" moved to %s.' % (record.name, TARGET_CRM_STAGE),
                                'type': 'success',
                                'sticky': False,
                            })
                        except:
                            pass

except Exception as e:
    try:
        post_to_chatter(record, "Automation Error (Project Group Sync): %s" % str(e))
    except:
        pass
