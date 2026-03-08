# Server Action: Block Vendor Bill Confirmation Until Landed Costs Are Added
# Model: account.move
# Trigger: Before Update Filter
#          Before Update Filter: state = draft  AND  move_type = in_invoice
#          Filter (After Update): state = posted
#
# WHY THIS MODEL (not purchase.order):
#   purchase.order.invoice_status is a COMPUTED field updated by the ORM internally
#   when pickings are validated — this bypasses Odoo's automation trigger system.
#   The ONLY reliable intercept point is account.move when the user clicks "Confirm",
#   which triggers an explicit write({'state': 'posted'}) that automations can catch.
#
# PURPOSE:
#   When the user clicks "Confirm" on a vendor bill, check that every validated
#   shipment on the linked PO has a Landed Cost referencing it.
#   If any shipment is missing a Landed Cost → raise UserError to block posting.
#
# WORKFLOW:
#   PO created → Shipment validated → Bill created (draft)
#   ↓  User clicks "Confirm" on the bill
#   This action fires → navigates bill → PO → done pickings → landed costs
#   → All pickings covered  ✅  allow — bill is confirmed
#   → Any picking missing   ❌  block — bill stays draft, user sees error
#
# CHAIN:
#   account.move (vendor bill)
#       └── purchase_id  (purchase.order)
#               └── picking_ids  (stock.picking, state='done')
#                       └── checked against stock.landed.cost.picking_ids

# ── Step 1: Get the Purchase Order linked to this bill ──────────────────────
purchase_order = record.purchase_id
if not purchase_order:
    # Fallback: derive PO from invoice lines
    purchase_order = record.invoice_line_ids.mapped('purchase_line_id.order_id')[:1]

if purchase_order:
    # ── Step 2: Get all validated (done) shipments on that PO ───────────────
    done_pickings = purchase_order.picking_ids.filtered(lambda p: p.state == 'done')

    if done_pickings:
        # ── Step 3: Find all landed costs that reference those pickings ──────
        landed_costs = env['stock.landed.cost'].search([
            ('picking_ids', 'in', done_pickings.ids),
        ])
        covered_picking_ids = set(landed_costs.mapped('picking_ids').ids)

        # ── Step 4: Block if any shipment has no landed cost ─────────────────
        missing = done_pickings.filtered(lambda p: p.id not in covered_picking_ids)

        if missing:
            missing_names = '\n  • '.join(missing.mapped('name'))
            raise UserError(
                f"⚠️ Cannot confirm this Vendor Bill yet.\n\n"
                f"The following validated shipment(s) on PO {purchase_order.name} "
                f"do not have a Landed Cost entry:\n\n"
                f"  • {missing_names}\n\n"
                f"Please add a Landed Cost for these transfers "
                f"(Inventory → Operations → Landed Costs) before confirming the bill."
            )
