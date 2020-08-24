import pytz
from datetime import datetime

from odoo import api, fields, models

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

class StockMove(models.Model):
    _inherit = "stock.move"

    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id):
        self.ensure_one()
        AccountMove = self.env['account.move']
        quantity = self.env.context.get('forced_quantity', self.product_qty)
        quantity = quantity if self._is_in() else -1 * quantity

        # Make an informative `ref` on the created account move to differentiate between classic
        # movements, vacuum and edition of past moves.
        ref = self.reference
        if self.env.context.get('force_valuation_amount'):
            if self.env.context.get('forced_quantity') == 0:
                ref = 'Revaluation of %s (negative inventory)' % ref
            elif self.env.context.get('forced_quantity') is not None:
                ref = 'Correction of %s (modification of past move)' % ref

        move_lines = self.with_context(forced_ref=ref)._prepare_account_move_line(quantity, abs(self.value),
                                                                                  credit_account_id, debit_account_id)
        print ("self._context---------------------------",self._context)
        if move_lines:
            # date = self._context.get('force_period_date', self.picking_id.scheduled_date)
            date = self._context.get('force_period_date', False)
            if not date:
                picking_date = self.picking_id.scheduled_date

                local_tz_st = pytz.timezone(self.env.user.tz or 'UTC')
                if picking_date:
                    
                    scheduled_date_only = picking_date
                    start_d = scheduled_date_only.replace(tzinfo=pytz.utc).astimezone(local_tz_st)
                    start_date = datetime.strftime(start_d, DEFAULT_SERVER_DATETIME_FORMAT)
                    scheduled_date_only = datetime.strptime(
                        start_date, '%Y-%m-%d %H:%M:%S'
                    )
                    date = scheduled_date_only.date()
            print ("date 00000000000000000000", date)
            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': self.id,
            })
            new_account_move.post()

    @api.multi
    def write(self, vals): #24/09/2019
        print ("vals -------56------",vals)
        if self._context.get('inventory_date', False):
            if vals.get('state', '') == 'done':
                vals.update({
                    'date': self._context['inventory_date']
                })
        return super(StockMove, self).write(vals)


class StockMoveLine(models.Model): #24/09/2019
    _inherit = "stock.move.line"

    @api.multi
    def write(self, vals): #24/09/2019
        print ("vals -------70------",vals)

        if self._context.get('inventory_date', False):
            if vals.get('date', False) and 'product_uom_qty' in vals:
                vals.update({
                    'date': self._context['inventory_date']
                })
        return super(StockMoveLine, self).write(vals)
