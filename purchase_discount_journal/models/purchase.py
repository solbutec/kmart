from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.one
    @api.depends('discount_type', 'discount_rate', 'order_line.price_total', 'is_tax')
    def _amount_all(self):
        for order in self:
            amt_total = amount_discount = amount_untaxed = amount_tax = amount_dis_total = self.amount_discount = self.amount_tax = line_discount = amount_global_discount = amount_global_dis_total = after_global_amt_total = 0.0
            for line in order.order_line:
                if line.discount_line_type == 'fixed':
                    line_discount += (line.dis_amount * line.product_qty)
                    line.line_dis_total_amount = (line.dis_amount * line.product_qty)
                elif line.discount_line_type == 'percent':
                    line_discount += ((line.product_qty * line.price_unit) * line.dis_amount) / 100
                    line.line_dis_total_amount = (line.product_qty * line.price_unit * line.dis_amount) / 100
                else:
                    line_discount = line_discount

                if self.discount_type == 'fixed':
                    amount_untaxed += line.price_subtotal
                    self.amount_untaxed = amount_untaxed
                    line.discount = 0.0
                elif self.discount_type == 'percent':
                    amount_untaxed += line.product_qty * line.price_unit
                    self.amount_untaxed = amount_untaxed
                else:
                    amount_untaxed += line.price_subtotal
                    self.amount_untaxed = amount_untaxed
        amount_discount = amount_discount + line_discount
        amount_dis_total = amount_untaxed - amount_discount
        if self.discount_type == 'fixed':
            amount_global_discount = self.discount_rate
        elif self.discount_type == 'percent':
            amount_global_discount = (amount_dis_total * self.discount_rate) / 100
        else:
            amount_global_discount = 0.0
            self.discount_rate = 0.0
        after_global_amt_total = amount_dis_total - amount_global_discount
        # **************************global_tax*****************************
        if self.company_id.global_tax == True and self.is_tax == True:
            if self.company_id.account_purchase_tax_id:
                amount_tax = (after_global_amt_total * self.company_id.account_purchase_tax_id.amount) / 100
            else:
                raise UserError(_('Please check purchase account tax.'))
        else:
            amount_tax = 0.0
        # *****************************************************************
        # **********************constant amount_tax 5%*********************
        # if self.is_tax == True:
        #     amount_tax = after_global_amt_total * 0.05
        # else:
        #     amount_tax = 0.0
        # *****************************************************************
        amt_total = after_global_amt_total + amount_tax
        order.update({
            'amount_untaxed': order.currency_id.round(amount_untaxed),
            'amount_tax': order.currency_id.round(amount_tax),
            'amount_discount': order.currency_id.round(amount_discount),
            'amount_dis_total': order.currency_id.round(amount_dis_total),
            'amount_global_discount': order.currency_id.round(amount_global_discount),
            'amount_global_dis_total': after_global_amt_total,
            'amount_total': amt_total,
        })

    is_tax = fields.Boolean("Is Tax", default=False, store=True)
    global_tax = fields.Boolean("Global Tax", related="company_id.global_tax", store=True)
    discount_type = fields.Selection([('fixed', "Fixed"), ('percent', "Percentage")], default="fixed", string="Type")
    discount_rate = fields.Float("Discount")
    amount_discount = fields.Monetary(string='Line Discount', store=True, readonly=True, compute='_amount_all')
    amount_dis_total = fields.Monetary(string='After Line Discount', store=True, readonly=True, compute='_amount_all')
    amount_global_discount = fields.Monetary(string='Global Discount', store=True, readonly=True, compute='_amount_all')
    amount_global_dis_total = fields.Monetary(string='After Global Discount', store=True, readonly=True,
                                              compute='_amount_all')

    amount_tax = fields.Monetary(string='Commercial Tax 5%',
                                 store=True, readonly=True, compute='_amount_all')
    picking_number = fields.Char(string="Picking Number", compute="get_do_num")

    def get_do_num(self):
        query = """SELECT name FROM stock_picking WHERE origin='"""+str(self.origin)+"""';"""
        self.env.cr.execute(query)
        record = self.env.cr.dictfetchall()
        for rec in record:
            if not self.picking_number:
                self.picking_number = rec['name']

    @api.onchange('discount_type')
    def onchange_discount_type(self):
        self.discount_rate = 0.0

    @api.onchange('date_planned')
    def onchange_set_date_planned(self):
        for order in self:
            order.order_line.update({'date_planned': order.date_planned})

    # FOR PO PICKNUMBER TO CALL IN ACCOUNT INVOICE
    @api.multi
    def action_view_invoice(self):
        action = self.env.ref('account.action_vendor_bill_template')
        result = action.read()[0]
        create_bill = self.env.context.get('create_bill', False)
        # override the context to get rid of the default filtering
        result['context'] = {
            'type': 'in_invoice',
            'default_purchase_id': self.id,
            'default_currency_id': self.currency_id.id,
            'default_company_id': self.company_id.id,
            'default_picking_number': self.picking_number,
            'company_id': self.company_id.id
        }
        # choose the view_mode accordingly
        if len(self.invoice_ids) > 1 and not create_bill:
            result['domain'] = "[('id', 'in', " + str(self.invoice_ids.ids) + ")]"
        else:
            res = self.env.ref('account.invoice_supplier_form', False)
            form_view = [(res and res.id or False, 'form')]
            if 'views' in result:
                result['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
            else:
                result['views'] = form_view
            # Do not set an invoice_id if we want to create a new bill.
            if not create_bill:
                result['res_id'] = self.invoice_ids.id or False
        result['context']['default_origin'] = self.name
        result['context']['default_reference'] = self.partner_ref
        return result


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    discount_line_type = fields.Selection([('fixed', "Fixed"), ('percent', "Percentage")], string="Discount Type",
                                          default='percent')
    dis_amount = fields.Float(string='Discount', digits=(16, 2), store=True)
    line_dis_total_amount = fields.Float(string="Total Discount", digits=(16, 2), store=True)
