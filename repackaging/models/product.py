# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    child_id = fields.Many2one("product.product", "Child Product")
    equvalent_qty = fields.Float("Equvalent Qty")
