import pytz
from datetime import datetime

from odoo import api, fields, models

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    @api.multi
    def do_scrap(self):
        for scrap in self:
            move = self.env['stock.move'].create(scrap._prepare_move_values())
            move.with_context(is_scrap=True, force_period_date=self.date_expected)._action_done()
            scrap.write({'move_id': move.id, 'state': 'done'})
        return True

    def action_get_stock_move_lines(self):
        for res in self.move_id:
            res.date = self.date_expected
            res.move_line_ids.date = self.date_expected
        action = self.env.ref('stock.stock_move_line_action').read([])[0]
        action['domain'] = [('move_id', '=', self.move_id.id)]
        return action

