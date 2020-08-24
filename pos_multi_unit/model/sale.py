# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Sale(models.Model):
    _inherit = "sale.order.line"
    
    multi_uom_id = fields.Many2one(
        'product.multi.uom',
        string="UOM(s)"
    )
    product_categ_id = fields.Many2one(
        'product.template',
        related="product_id.product_tmpl_id",
        string="Product Template"
    )

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        super(Sale, self).product_uom_change()
        if not self.multi_uom_id:
            multi_uom_id = self.multi_uom_id.filtered(
                lambda m: m.uom_id == self.product_uom
            )
            if multi_uom_id:
                self.multi_uom_id = multi_uom_id[0]

    @api.onchange('multi_uom_id')
    def product_multi_uom_change(self):
        if self.multi_uom_id:
            self.product_uom = self.multi_uom_id.uom_id
            self.price_unit = self.multi_uom_id.price
#             self.product_uom_qty = self.product_uom_qty * self.multi_uom_id.ratio
            new_list_price = self.multi_uom_id.price
            price = self.multi_uom_id.price
            if new_list_price != 0:
                currency = self.order_id.company_id.currency_id
                if self.order_id.pricelist_id.currency_id != currency:
                    # we need new_list_price in the same currency as price, which is in the SO's pricelist's currency
                    new_list_price = currency._convert(
                        new_list_price, self.order_id.pricelist_id.currency_id,
                        self.order_id.company_id or self.env.user.company_id,
                        self.order_id.date_order or fields.Date.today()
                    )
                discount = (new_list_price - price) / new_list_price * 100
                self.price_unit = new_list_price
                if (discount > 0 and new_list_price > 0) or (discount < 0 and new_list_price < 0):
                    self.discount = discount