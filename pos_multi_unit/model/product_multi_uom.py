# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductMultiUOM(models.Model):
    _name = "product.multi.uom"
    _rec_name = 'uom_id'

    product_tmpl_id = fields.Many2one('product.template', 'Product', required=True)
    base_uom_id = fields.Many2one('uom.uom', related='product_tmpl_id.uom_id')
    uom_id = fields.Many2one('uom.uom', 'Uom', required=True)
    price = fields.Float('Price', required=True, default=1.0)

    ratio = fields.Float('Ratio', compute='_compute_ratio', required=True, readonly=True, digits=(16, 6))

    @api.model
    def get_uom_category_id(self, product_tmpl_id):
        product_tmpl = self.env['product.template'].browse(product_tmpl_id)
        uom = product_tmpl.uom_id or product_tmpl.weight_uom_id
        if uom:
            return uom.category_id.id
        else:
            return False

    @api.depends('uom_id', 'product_tmpl_id')
    def _compute_ratio(self):
        for obj in self:
            product_uom_id = obj.product_tmpl_id.uom_id or obj.product_tmpl_id.weight_uom_id
            if product_uom_id:
                obj.ratio = obj.uom_id.factor_inv/product_uom_id.factor_inv


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    enable_multi_uom = fields.Boolean('Multi unit of measure')
    multi_uom_ids = fields.One2many('product.multi.uom', 'product_tmpl_id', string='Units of measure')

