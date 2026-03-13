if record.price_unit < 0 and record.tax_ids:
    # Hardcoded 5% VAT adjustment:
    # When Odoo adds a discount of -3 AED with inclusive tax, it sets price_unit to -2.857.
    # We restore it to -3.00 (-2.857 * 1.05) and remove the tax.
    new_price = record.price_unit * 1.05

    if record.price_unit != new_price or record.tax_ids:
        record.write({
            'price_unit': new_price,
            'tax_ids': [(5, 0, 0)]  # Remove taxes
        })
        
        log(f"Discount RESTORED: {record.price_unit} adjusted to {new_price} (Taxes removed)", level='info')

## Powered By HSx Tech - Ali Muzafar
