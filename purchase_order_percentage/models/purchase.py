from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    sale_price = fields.Float(string='Sale Price', related="product_id.lst_price")
    markup_percent = fields.Float(string="Mark Up (%)", compute='_compute_amount')

    @api.depends('product_qty', 'price_unit', 'taxes_id')
    def _compute_amount(self):
        for line in self:
            vals = line._prepare_compute_all_values()
            taxes = line.taxes_id.compute_all(
                vals['price_unit'],
                vals['currency_id'],
                vals['product_qty'],
                vals['product'],
                vals['partner'])
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

            if line.price_unit > 0:
                line.markup_percent = ((line.sale_price - line.price_unit) / line.price_unit) * 100.0
