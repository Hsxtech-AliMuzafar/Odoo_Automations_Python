# Configurable Constants
TRIGGER_STAGE_IDS = [1]
TRIGGER_STAGE_NAMES = ['Job Request', 'Job Re', 'Project Proposal', 'Won', 'Contract Signed']
FALLBACK_TEMPLATE_NAME = 'Opportunity Template'

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
    Project = env['project.project']
    current_stage_id = record.stage_id.id if record.stage_id else 0
    current_stage_name = record.stage_id.name if record.stage_id else "No Stage"
    
    # 1. Trigger Check
    trigger_names_lower = [n.lower().strip() for n in TRIGGER_STAGE_NAMES]
    is_id_match = current_stage_id in TRIGGER_STAGE_IDS
    is_name_match = current_stage_name.lower().strip() in trigger_names_lower
    
    if is_id_match or is_name_match:
        # 2. Duplicate Check
        existing_project = Project.search([
            ('partner_id', '=', record.partner_id.id),
            ('name', '=', record.name),
            ('active', '=', True)
        ], limit=1)
        
        if existing_project:
            # Inform user it exists
            base_url = record.get_base_url()
            existing_url = "%s/odoo/project.project/%d" % (base_url.rstrip('/'), existing_project.id)
            post_to_chatter(record, "Automation Note: Project already exists: <a href='%s'>%s</a>" % (existing_url, existing_project.name))
        else:
            # 3. Template Selection
            template = Project.search([('is_template', '=', True)], order='write_date desc', limit=1)
            if not template:
                template = Project.search([('name', '=', FALLBACK_TEMPLATE_NAME)], limit=1)
            
            if not template:
                post_to_chatter(record, "Error: Template '%s' not found." % FALLBACK_TEMPLATE_NAME)
            else:
                # 4. Create Project
                copy_vals = {
                    'name': record.name,
                    'partner_id': record.partner_id.id,
                    'user_id': record.user_id.id or env.uid,
                    'description': record.description or "",
                    'is_template': False,
                }
                if record.tag_ids:
                    copy_vals['tag_ids'] = [(6, 0, record.tag_ids.ids)]

                project = template.copy(copy_vals)
                project.write({'is_template': False, 'active': True})
                
                # Link project back to lead (NEW)
                record.write({'x_studio_linked': project.id})

                # 5. Generate Modern Links (Full URL is best for Odoo 19)
                base_url = record.get_base_url()
                project_url = "%s/odoo/project.project/%d" % (base_url.rstrip('/'), project.id)
                lead_url = "%s/odoo/crm.lead/%d" % (base_url.rstrip('/'), record.id)

                # 6. Chatter Notifications (Using user's proven logic)
                post_to_chatter(record, "Project Created: <a href='%s'>%s</a>" % (project_url, project.name))
                
                # Also link back on project
                env['mail.message'].create({
                    'model': 'project.project',
                    'res_id': project.id,
                    'message_type': 'comment',
                    'body': "Created from Lead: <a href='%s'>%s</a>" % (lead_url, record.name),
                    'subtype_id': env.ref('mail.mt_note').id,
                    'author_id': env.user.partner_id.id,
                })

                # 7. Create Activity (Added value)
                try:
                    env['mail.activity'].create({
                        'res_model_id': env['ir.model']._get_id('project.project'),
                        'res_id': project.id,
                        'activity_type_id': env.ref('mail.mail_activity_data_todo').id,
                        'summary': 'New Project setup required',
                        'note': 'Automatically created from Lead: %s' % record.name,
                        'user_id': project.user_id.id or env.uid,
                        'date_deadline': fields.Date.today(),
                    })
                except:
                    pass

                # 8. UI Notification Popup
                try:
                    env['bus.bus']._sendone(env.user.partner_id, 'simple_notification', {
                        'title': 'Success',
                        'message': 'Project "%s" is ready.' % project.name,
                        'type': 'success',
                        'sticky': False, 
                        'link': {'label': 'Open Project', 'url': project_url}
                    })
                except:
                    pass

except Exception as e:
    post_to_chatter(record, "Automation Error: %s" % str(e))
