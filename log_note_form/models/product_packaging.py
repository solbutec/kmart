from odoo import models, fields, api, _


class ProductPackaging(models.Model):
    _name = 'product.item'
    _description = 'to create cut item name'

    name = fields.Char(string="Name")
