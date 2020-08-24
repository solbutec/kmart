# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    product_filter = fields.Selection(
        selection=[
            ('all', 'All'),
            ('product_categ', 'Product Category'),
            ('product', 'Products')
        ],
        default="all",
        string="Product Filter"
    )
    reminder_product_categ_ids = fields.Many2many(
        'product.category',
        string="Product Category",
    )
    reminder_product_tmpl_ids = fields.Many2many(
        'product.template',
        string="Products",
    )
    reminder_user_ids = fields.Many2many(
        'res.users',
        string="Users",
    )

    @api.model
    def _run_action_price_reminder(self):

        tmpl = False
        try:
            tmpl = self.env.ref('low_price_reminder.email_tmpl_price_alert')
        except:
            pass

        company = self.env.user.company_id

        if tmpl and company.reminder_user_ids:
            if company._get_product_list():
                partner_ids = [
                    (4, u.partner_id.id)
                    for u in company.reminder_user_ids
                ]
                email_values = {'recipient_ids': partner_ids}
                tmpl.send_mail(company.id, email_values=email_values)

    @api.model
    def _get_product_list(self):
        domain = [('company_id', '=', self.id)]
        if self.product_filter == 'product_categ':
            domain.append(('categ_id', 'in', self.reminder_product_categ_ids.ids))
        elif self.product_filter == 'product':
            domain.append(('id', 'in', self.reminder_product_tmpl_ids.ids))
        products = self.env['product.template'].sudo().search(domain)
        products = products.filtered(lambda i: i.lst_price < i.standard_price + ((i.standard_price * 10) / 100))
        return products
