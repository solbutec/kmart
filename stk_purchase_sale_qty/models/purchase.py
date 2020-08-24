from odoo import models, fields, api, _
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    month_sale_qty = fields.Float('Last Monthly Sale', store=True, compute='_compute_month_sale_qty')

    @api.one
    @api.depends('product_id')
    def _compute_month_sale_qty(self):
        if self.product_id:
            date_from = fields.Date.to_string(fields.datetime.now() - relativedelta(months=1))
            print("DATE from", date_from)
            for line in self:
                query = """ SELECT sum(l.qty_delivered) as total FROM sale_report l
                        WHERE l.product_id is not null AND l.product_id='"""+str(self.product_id.id)+"""'
                        AND l.confirmation_date >='"""+str(date_from)+"""';"""
                self.env.cr.execute(query)
                result = self.env.cr.dictfetchall()
                for value in result:
                    line.month_sale_qty = value['total']
