import pytz
from datetime import datetime
from odoo import api, fields, models, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError


class StockInv(models.Model):
    _inherit = "stock.inventory"

    accounting_date = fields.Date(
        'Accounting Date', default=fields.Date.context_today,
        help="Date at which the accounting entries will be created"
             " in case of automated inventory valuation."
             " If empty, the inventory date will be used.")

    date = fields.Datetime(
        states={
            'draft': [('readonly', False)],
        },
    ) #24/09/2019

    @api.onchange('date')
    def onchange_date(self):
        if self.date:
            local_tz_st = pytz.timezone(self.env.user.tz or 'UTC')
            scheduled_date_only = self.date
            start_d = scheduled_date_only.replace(tzinfo=pytz.utc).astimezone(local_tz_st)
            start_date = datetime.strftime(start_d, DEFAULT_SERVER_DATETIME_FORMAT)
            scheduled_date_only = datetime.strptime(
                start_date, '%Y-%m-%d %H:%M:%S'
            )
            date = scheduled_date_only.date()
            self.accounting_date = date

    @api.model
    def create(self, vals):
        inv = super(StockInv, self).create(vals)
        if inv.date:
            local_tz_st = pytz.timezone(self.env.user.tz or 'UTC')
            scheduled_date_only = inv.date
            start_d = scheduled_date_only.replace(tzinfo=pytz.utc).astimezone(local_tz_st)
            start_date = datetime.strftime(start_d, DEFAULT_SERVER_DATETIME_FORMAT)
            scheduled_date_only = datetime.strptime(
                start_date, '%Y-%m-%d %H:%M:%S'
            )
            date = scheduled_date_only.date()
            if inv.accounting_date != date:
                raise UserError(
                    _('Inventory Date and Accounting Date must be same!')
                )
        return inv

    @api.multi
    def write(self, vals):
        res = super(StockInv, self).write(vals)
        if vals.get('date', False):
            for inv in self:
                if inv.date:
                    local_tz_st = pytz.timezone(self.env.user.tz or 'UTC')
                    scheduled_date_only = inv.date
                    start_d = scheduled_date_only.replace(tzinfo=pytz.utc).astimezone(local_tz_st)
                    start_date = datetime.strftime(start_d, DEFAULT_SERVER_DATETIME_FORMAT)
                    scheduled_date_only = datetime.strptime(
                        start_date, '%Y-%m-%d %H:%M:%S'
                    )
                    date = scheduled_date_only.date()
                    if inv.accounting_date != date:
                        raise UserError(
                            _('Inventory Date and Accounting Date must be same!')
                        )
        return res

    def action_start(self):
        for inventory in self.filtered(lambda x: x.state not in ('done','cancel')):
#             vals = {'state': 'confirm', 'date': self.accounting_date} #24/09/2019
            vals = {'state': 'confirm', 'date': self.date} #24/09/2019
            if (inventory.filter != 'partial') and not inventory.line_ids:
                vals.update({'line_ids': [(0, 0, line_values) for line_values in inventory._get_inventory_lines_values()]})
            inventory.write(vals)
        return True

    def post_inventory(self): #24/09/2019
        ctx = self._context.copy()
        ctx.update({'inventory_date': self.date})
        return super(
            StockInv, self.with_context(ctx)
        ).post_inventory()


class InventoryLine(models.Model): #24/09/2019
    _inherit = "stock.inventory.line"

    @api.one
    @api.depends(
        'location_id', 'product_id',
        'package_id', 'product_uom_id',
        'company_id', 'prod_lot_id', 'partner_id'
    )
    def _compute_theoretical_qty(self):
        if not self.product_id:
            self.theoretical_qty = 0
            return
        ctx = self._context.copy()

        if self.inventory_id.date:
            ctx.update({'inventory_date': self.inventory_id.date})

        theoretical_qty = self.product_id.with_context(ctx).get_theoretical_quantity(
            self.product_id.id,
            self.location_id.id,
            lot_id=self.prod_lot_id.id,
            package_id=self.package_id.id,
            owner_id=self.partner_id.id,
            to_uom=self.product_uom_id.id,
        )
        self.theoretical_qty = theoretical_qty


    def _get_move_values(
            self, qty, location_id, location_dest_id, out
        ): #24/09/2019
        
        ctx = self._context.copy()
        ctx.update(my_test=self.inventory_id.date)
        
        vals = super(
            InventoryLine, self.with_context(ctx)
        )._get_move_values(
            qty, location_id, location_dest_id, out
        )
        vals.update({
            'date': self.inventory_id.date
        })
        if vals.get('move_line_ids', []):
            if len(vals['move_line_ids'][0]) == 3:
                if isinstance(vals['move_line_ids'][0][2], dict):
                    vals['move_line_ids'][0][2].update({
                        'date': self.inventory_id.date
                    })
        return vals


class Product(models.Model):
    _inherit = "product.product"
    
    @api.model
    def get_theoretical_quantity(self, product_id, location_id, lot_id=None, package_id=None, owner_id=None, to_uom=None):
        if not self._context.get('inventory_date', False):
            return super(Product, self).get_theoretical_quantity(product_id, location_id, lot_id, package_id, owner_id, to_uom)

        product_id = self.env['product.product'].browse(product_id)
        product_id.check_access_rights('read')
        product_id.check_access_rule('read')

        location_id = self.env['stock.location'].browse(location_id)
        lot_id = self.env['stock.production.lot'].browse(lot_id)
        package_id = self.env['stock.quant.package'].browse(package_id)
        owner_id = self.env['res.partner'].browse(owner_id)
        to_uom = self.env['uom.uom'].browse(to_uom)
        quants = self.env['stock.quant']._gather(product_id, location_id, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=True)

        theoretical_quantity = sum([quant.quantity for quant in quants])
        if self._context.get('inventory_date', False):
            move_lines = self.env['stock.move.line'].search([
                ('product_id', '=', product_id.id),
                '|',
                    ('location_id', '=', location_id.id),
                    ('location_dest_id', '=', location_id.id),
                ('lot_id', '=', lot_id.id),
                '|',
                    ('package_id', '=', package_id.id),
                    ('result_package_id', '=', package_id.id),
                ('date', '<=',  self._context['inventory_date'])
            ])
            move_qty = 0.0
            for l in move_lines:
                if l.location_id.id == location_id.id:
                    move_qty -= l.qty_done
                else:
                    move_qty += l.qty_done
            
            theoretical_quantity = move_qty
        if to_uom and product_id.uom_id != to_uom:
            theoretical_quantity = product_id.uom_id._compute_quantity(theoretical_quantity, to_uom)
        return theoretical_quantity
