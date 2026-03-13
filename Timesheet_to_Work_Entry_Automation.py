# Target Model: account.analytic.line (This is the technical name for "Timesheet" in Odoo)
# Trigger: On Creation & Update

def post_to_chatter(record, body):
    """Post an HTML message to the record's chatter."""
    try:
        record.message_post(body=body)
    except Exception:
        # Fallback to mail.message if message_post fails or isn't available on analytic line
        env['mail.message'].create({
            'model': record._name,
            'res_id': record.id,
            'message_type': 'comment',
            'body': body,
            'subtype_id': env.ref('mail.mt_note').id,
        })

# Use 'records' if available, otherwise fallback to 'record'
target_records = records if records else record

# Odoo Logging: Use log() to write to the 'Logging' tab of the Automated Action
log("Starting Timesheet to Work Entry automation for %s records" % len(target_records))

for line in target_records:
    try:
        # 1. Ensure it's a timesheet entry for an employee
        # Filter for entries that have a valid employee and non-zero duration
        if line.employee_id and line.unit_amount > 0:
            
            # 2. Check if a work entry already exists for this analytic line to prevent duplicates
            # (Assuming we might log a unique ID or check dates/type/employee)
            existing_entry = env['hr.work.entry'].search([
                ('employee_id', '=', line.employee_id.id),
                ('name', 'like', line.name or 'Timesheet'),
                ('date_start', '>=', datetime.combine(line.date, datetime.min.time())),
                ('date_stop', '<=', datetime.combine(line.date, datetime.max.time())),
            ], limit=1)
            
            if existing_entry:
                log("Work entry already exists for line %s, skipping." % line.id)
                continue

            # 3. Find Work Entry Type (Defaulting to "Work")
            WorkEntryType = env['hr.work.entry.type']
            work_type = WorkEntryType.search([('code', '=', 'WORK100')], limit=1)
            if not work_type:
                work_type = WorkEntryType.search([('name', 'ilike', 'Work')], limit=1)

            if work_type:
                # 4. Calculate Start and End Datetimes
                # Set a default start time of 08:00 AM on that date
                start_dt = datetime.combine(line.date, datetime.min.time()).replace(hour=8)
                end_dt = start_dt + timedelta(hours=line.unit_amount)

                # 5. Create the Work Entry record
                work_entry_vals = {
                    'name': f"Work Entry: {line.name or 'Timesheet'}",
                    'employee_id': line.employee_id.id,
                    'work_entry_type_id': work_type.id,
                    'date_start': start_dt,
                    'date_stop': end_dt,
                }
                
                # Fetch contract
                contract = line.employee_id.contract_id if hasattr(line.employee_id, 'contract_id') else False
                if not contract:
                    contract = env['hr.contract'].search([
                        ('employee_id', '=', line.employee_id.id),
                        ('state', '=', 'open')
                    ], limit=1)
                
                if contract:
                    work_entry_vals['contract_id'] = contract.id

                new_work_entry = env['hr.work.entry'].create(work_entry_vals)

                if new_work_entry:
                    # 6. Validate the Work Entry
                    if hasattr(new_work_entry, 'action_validate'):
                        new_work_entry.action_validate()
                    
                    # 7. Success notification in chatter
                    msg = f"Automation: Created and validated Work Entry: <a href='/odoo/hr.work.entry/{new_work_entry.id}'>{new_work_entry.name}</a>"
                    post_to_chatter(line, msg)
                    log("Successfully created work entry %s for line %s" % (new_work_entry.id, line.id))
            else:
                log("Could not find 'Work' entry type (code WORK100) for line %s" % line.id)
        else:
            log("Skipping record %s: No employee or unit_amount is 0." % line.id)

    except Exception as e:
        log("Error processing record %s: %s" % (line.id, str(e)))
        try:
            post_to_chatter(line, f"Automation Error (Timesheet to Work Entry): {str(e)}")
        except:
            pass
