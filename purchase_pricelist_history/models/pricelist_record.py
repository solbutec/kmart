# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.addons import decimal_precision as dp


class PricelistRecord(models.Model):
    _name = 'pricelist.record'
    _description = 'Purchase Order Record based on Pricelist'

    name = fields.Many2one(
        'res.partner', 'Vendor',
        domain=[('supplier', '=', True)], ondelete='cascade', required=True,
        help="Vendor of this product")
    sequence = fields.Integer(
        'Sequence', default=1, help="Assigns the priority to the list of product vendor.")
    price = fields.Float(
        'Price', default=0.0, digits=dp.get_precision('Product Price'),
        required=True, help="The price to purchase a product")
    currency_id = fields.Many2one(
        'res.currency', 'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True)
    product_tmpl_id = fields.Many2one(
        'product.product', 'Product',
        index=True, ondelete='cascade', oldname='product_id')
    ticket_date = fields.Datetime(string="Ticket Date")
    ticket_number = fields.Char(string="PO Number", required=True)
    purchase_qty = fields.Integer(string="Purchase Quantity")


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def button_confirm(self):
        product_supplierinfo = self.env['product.supplierinfo']
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.user.company_id.currency_id._convert(
                        order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                        order.date_order or fields.Date.today())) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})

            for line in order.order_line:
                if line.price_unit != 0:
                    values = {
                        'name': order.partner_id.id,
                        'ticket_number': order.name,
                        'ticket_date': order.date_order,
                        'currency_id': order.currency_id.id,
                        'product_tmpl_id': line.product_id.id,
                        'price': line.price_unit,
                        'purchase_qty': line.product_qty,
                    }
                    print('VALUESS', values)
                    self.env['pricelist.record'].create(values)
                    query = """UPDATE product_supplierinfo SET price=""" + \
                            str(line.price_unit) + """ WHERE name=""" + str(
                        line.partner_id.id) + """ AND product_tmpl_id=""" + \
                            str(line.product_id.product_tmpl_id.id) + """;"""
                    self.env.cr.execute(query)
                    print("Product_id", order.product_id.id)
                    quee = """UPDATE product_template SET final_purchase_price=""" + str(
                        line.price_unit) + """ WHERE id=""" + str(line.product_id.product_tmpl_id.id) + """;"""
                    self.env.cr.execute(quee)

        return True


class ProductTemplate(models.Model):
    _inherit = "product.template"

    final_purchase_price = fields.Float("Final Purchase Price")


class Product(models.Model):
    _inherit = "product.product"

    final_purchase_price = fields.Float("Final Purchase Price", related='product_tmpl_id.final_purchase_price')
