from odoo import api, fields, models, _

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    
    @api.depends('price_unit', 'tax_ids', 'qty', 'discount', 'product_id')
    def _compute_amount_line_all_margin(self):
        for line in self:
            factor = 1.0
            if line.product_id:
                query = """SELECT factor FROM uom_uom WHERE id="""+str(line.uom_id.id)+""";"""
                self.env.cr.execute(query)
                result = self.env.cr.dictfetchall()
                for res in result:
                    factor = res['factor']
            margin = (line.price_unit*line.qty) - ((line.product_id.product_tmpl_id.standard_price*(1.0 / factor))*line.qty)
            purchase_price = line.product_id.product_tmpl_id.standard_price*(1.0 / factor)
            if line.price_unit == 0:
                margin = 0 
            line.update({
                'margin': margin,
                'purchase_price': purchase_price,
            })
                         
    margin = fields.Float(compute='_compute_amount_line_all_margin', string='Margin', store=True)
    purchase_price = fields.Float(compute='_compute_amount_line_all_margin',store=True,string='Cost')

    
class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.depends('statement_ids', 'lines.price_subtotal_incl', 'lines.discount')
    def _compute_amount_all(self):
        for order in self:
            order.amount_paid = order.amount_return = order.amount_tax = 0.0
            currency = order.pricelist_id.currency_id
            order.amount_paid = sum(payment.amount for payment in order.statement_ids)
            order.amount_return = sum(payment.amount < 0 and payment.amount or 0 for payment in order.statement_ids)
            order.amount_tax = currency.round(sum(self._amount_line_tax(line, order.fiscal_position_id) for line in order.lines))
            amount_untaxed = currency.round(sum(line.price_subtotal for line in order.lines))
            order.amount_total = order.amount_tax + amount_untaxed
            order.margin = sum(line.margin for line in order.lines)
            
    margin = fields.Float(compute='_compute_amount_all', string='Margin', store=True)