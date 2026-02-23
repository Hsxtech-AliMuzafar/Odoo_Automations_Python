# Field-wise Computed Field Snippets for account.move (Invoice)
# Pulling data from related Sale Order fields in Odoo 19

# ==========================================
# 1. Job Unit Location
# ==========================================
# Field Name: x_studio_job_unit_location
# Dependency: invoice_line_ids.sale_line_ids.order_id.x_studio_related_unit_location

for record in self:
    sale_orders = record.invoice_line_ids.mapped('sale_line_ids.order_id')
    record['x_studio_job_unit_location'] = sale_orders[0].x_studio_related_unit_location if sale_orders else False


# ==========================================
# 2. Job Unit Number
# ==========================================
# Field Name: x_studio_job_unit_number
# Dependency: invoice_line_ids.sale_line_ids.order_id.x_studio_related_unit_number

for record in self:
    sale_orders = record.invoice_line_ids.mapped('sale_line_ids.order_id')
    record['x_studio_job_unit_number'] = sale_orders[0].x_studio_related_unit_number if sale_orders else False


# ==========================================
# 3. Installation Date
# ==========================================
# Field Name: x_studio_job_installation_date_1
# Dependency: invoice_line_ids.sale_line_ids.order_id.x_studio_related_installation

for record in self:
    sale_orders = record.invoice_line_ids.mapped('sale_line_ids.order_id')
    record['x_studio_job_installation_date_1'] = sale_orders[0].x_studio_related_installation if sale_orders else False


# ==========================================
# 4. Job/Unit Name
# ==========================================
# Field Name: x_studio_job_unit_name
# Dependency: invoice_line_ids.sale_line_ids.order_id.x_studio_related_job_name

for record in self:
    sale_orders = record.invoice_line_ids.mapped('sale_line_ids.order_id')
    record['x_studio_job_unit_name'] = sale_orders[0].x_studio_related_job_name if sale_orders else False

## Powered By HSx Tech
