from odoo import api, fields, models
from datetime import datetime

# class ProductMake(models.Model):
#     _name = 'product.make'

#     name = fields.Char('Made In', required=True)

#     _sql_constraints = [
#         ('name_uniq', 'unique (name)', 'Already Exists Make In!')
#     ]

class ProductSeasonal(models.Model):
    _name = 'product.seasonal'

    name = fields.Char('Promotion', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Already Exists Seasonal!')
    ]

class ProductPacking(models.Model):
    _name = 'product.packing'

    name = fields.Char('Cut Item', required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Already Exists Packing Size!')
    ]

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # product_make_id = fields.Many2one('product.make', string='Made In', track_visibility='onchange', store=True)
    product_seasonal_id = fields.Many2one('product.seasonal', string='Promotion', track_visibility='onchange', store=True)
    product_packing_id = fields.Many2one('product.packing', string='Cut Item', track_visibility='onchange', store=True)
    product_remark = fields.Text('Remark', track_visibility='onchange', store=True)
