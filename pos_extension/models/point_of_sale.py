# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.multi
    def refund(self):

        PosOrder = self.env['pos.order']

        for order in self:
            clone = order.copy({
                # ot used, name forced by create
                'name': order.name + _(' REFUND'),
                'session_id': order.session_id.id,
                'date_order': fields.Datetime.now(),
                'pos_reference': order.pos_reference,
                'lines': False,
                'amount_tax': -order.amount_tax,
                'amount_total': -order.amount_total,
                'amount_paid': 0,
            })
            for line in order.lines:
                clone_line = line.copy({
                    # required=True, copy=False
                    'name': line.name + _(' REFUND'),
                    'order_id': clone.id,
                    'qty': -line.qty,
                    'price_subtotal': -line.price_subtotal,
                    'price_subtotal_incl': -line.price_subtotal_incl,
                })
            PosOrder += clone
        return {
            'name': _('Return Products'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pos.order',
            'res_id': PosOrder.ids[0],
            'view_id': False,
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.onchange('price_unit', 'tax_ids', 'qty', 'discount', 'product_id')
    def _onchange_amount_line_all(self):
        for line in self:
            _logger.warning('Working _onchange_amount_line_all >>>>>>>>>>> %s', line.qty)
            res = line._compute_amount_line_all()
            _logger.warning('After Working _onchange_amount_line_all >>>>>>>>>>> %s', res)
            if res:
                line.update(res)

    def _compute_amount_line_all(self):
        self.ensure_one()

        _logger.warning('After _compute_amount_line_all >>>>>>>>>>> %s', self)
        fpos = self.order_id.fiscal_position_id

        _logger.warning('After compute fpos id >>>>>>>>>>> %s', fpos)

        tax_ids_after_fiscal_position = fpos.map_tax(self.tax_ids, self.product_id,
                                                     self.order_id.partner_id) if fpos else self.tax_ids

        _logger.warning('After compute tax amount >>>>>>>>>>> %s', tax_ids_after_fiscal_position)

        price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)

        _logger.warning('After price compute amount in _compute_amount_line_all >>>>>>>>>>>>> %s', price)

        taxes = tax_ids_after_fiscal_position.compute_all(price, self.order_id.pricelist_id.currency_id, self.qty,
                                                          product=self.product_id, partner=self.order_id.partner_id)
        return {
            'price_subtotal_incl': taxes['total_included'],
            'price_subtotal': taxes['total_excluded'],
        }
