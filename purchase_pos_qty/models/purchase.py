from odoo import models, fields, api, _
from datetime import timedelta
from dateutil.relativedelta import relativedelta

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    month_pos_qty = fields.Float('Last Monthly POS', store=True, compute='_compute_month_pos_qty')

    @api.one
    @api.depends('product_id')
    def _compute_month_pos_qty(self):
        if self.product_id:
            date_from = fields.Date.to_string(fields.datetime.now() - relativedelta(months=1))
            print("DATE from", date_from)
            for line in self:
                query = """ SELECT sum(p.product_qty) as total FROM report_pos_order p
                        WHERE p.product_id is not null AND p.product_id='"""+str(self.product_id.id)+"""'
                        AND p.date >='"""+str(date_from)+"""';"""
                self.env.cr.execute(query)
                result = self.env.cr.dictfetchall()
                for value in result:
                    line.month_pos_qty = value['total']
