# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import api, fields, models, _


class StockRepackaging(models.Model):
    _name = "stock.repackaging"
    _order = "id desc"

    @api.model
    def _default_dest_location_id(self):
        location_obj = self.env['stock.location']
        stock_location_id = location_obj.search([('name', '=',
                                                  'Virtual Locations')])
        location_id = None
        if stock_location_id:
            location_id = location_obj.search([('is_repackaging', '=', True)])
            if location_id:
                if len(location_id) > 1:
                    raise UserError(
                        _("Repackaging location must have  the one location."))
            if not location_id:
                location_id = location_obj.create({
                    'name':
                    'Repackaging',
                    'location_id':
                    stock_location_id.id,
                    'usage':
                    'inventory',
                    'is_repackaging':
                    True,
                })
            return location_id

    @api.model
    def _default_location_id(self):
        company_user = self.env.user.company_id
        warehouse = self.env['stock.warehouse'].search(
            [('company_id', '=', company_user.id)], limit=1)
        if warehouse:
            return warehouse.lot_stock_id.id
        else:
            raise UserError(
                _('You must define a warehouse for the company: %s.') %
                (company_user.name, ))

    name = fields.Char('Repackaging Reference',
                       default="New",
                       readonly=True,
                       store=True)
    location_id = fields.Many2one("stock.location",
                                  "Locations",
                                  default=_default_location_id,
                                  required=True,
                                  store=True)
    destination_location_id = fields.Many2one(
        "stock.location",
        "Location",
        default=_default_dest_location_id,
        required=True,
        store=True)
    date = fields.Datetime("Date",
                       default=fields.Datetime.now,
                       required=True,
                       store=True)
    stockrepackagingline_id = fields.One2many("stock.repackaging.line",
                                              "repackaging_id",
                                              "Stock Repackaging Lines")
    company_id = fields.Many2one('res.company',
                                 'Company',
                                 readonly=True,
                                 index=True,
                                 required=True,
                                 states={'draft': [('readonly', False)]},
                                 default=lambda self: self.env['res.company'].
                                 _company_default_get('stock.repackaging'))
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Repackage'),
                              ('done', 'Done')],
                             "Status",
                             default="draft")

    def action_done(self):
        self._action_done()
        self.write({'state': 'done'})

    def _action_done(self):
        self.get_move_line_value()

    def get_move_line_value(self):
        for package in self.filtered(lambda x: x.state not in ('done')):
            for line in self.stockrepackagingline_id:
                move_to = move_from = []
                qty = reqty = 0
                if line.quantity < 0:
                    qty = line.quantity * (-1)
                else:
                    qty = line.quantity
                if line.quantity >= 1:
                    reqty = line.quantity * (-1)
                else:
                    reqty = line.quantity
                val = {
                    'name': line.repackaging_id.name,
                    'product_id': line.product_id.id,
                    'product_uom': line.uom_id.id,
                    'product_uom_qty': qty,
                    'date': line.repackaging_id.date,
                    'company_id': line.env.user.company_id.id,
                    'state': 'confirmed',
                    'location_id': line.location_id.id,
                    'location_dest_id': line.dest_location_id.id,
                    'move_line_ids': [(0, 0, {'product_id':  line.product_id.id,
                                                'product_uom_qty': 0,
                                                'product_uom_id': line.uom_id.id,
                                                'date': line.repackaging_id.date,
                                                'qty_done': qty,
                                                'location_id': line.location_id.id,
                                                'location_dest_id': line.dest_location_id.id,
                                        })]
                }
                move_id = self.env['stock.move'].create(val)
                line.post_inventory()
                move_id.with_context(force_period_date=self.date)._action_done()
                line.write({'move_id': move_id.id, 'state': 'done'})

    def action_confirm(self):
        num = 0
        for line in self.stockrepackagingline_id:
            if line.product_id.child_id:
                if line.quantity:
                    num += 1
                    line.write({'sequence_number': num})
                    copy_id = line.copy()
                    num += 1
                    copy_id.write({'sequence_number': num})
                else:
                    raise UserError(_("Product quantity is equal 0."))
            else:
                raise UserError(_("Repackage product does not exist."))
        self.write({'state': 'confirm'})

    def action_resettodraft(self):
        if self.stockrepackagingline_id:
            for line in self.stockrepackagingline_id:
                if not line.is_repackage:
                    line.unlink()
        self.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.repackaging') or 'New'
        result = super(StockRepackaging, self).create(vals)
        return result

    def unlink(self):
        if any(pack.state not in ('draft') for pack in self):
            raise UserError(_('You can only delete in draft state.'))
        return super(StockRepackaging, self).unlink()


class StockRepackingLine(models.Model):
    _name = "stock.repackaging.line"
    _order = 'sequence_number'

    def _default_location_id(self):
        if self.repackaging_id:
            return self.repackaging_id.location_id

    def _default_dest_location_id(self):
        if self.repackaging_id:
            return self.repackaging_id.destination_location_id

    name = fields.Char("Product Name",
                       related="product_id.name",
                       store=True,
                       readonly=True)
    product_id = fields.Many2one("product.product",
                                 "Internal Reference",
                                 readonly=False,
                                 store=True)
    onhand_qty = fields.Float("On Hand",
                              digits=(16, 0),
                              readonly=True,
                              compute="_compute_amount",
                              store=True)
    quantity = fields.Float("Quantity", digits=(16, 0), store=True)
    balance = fields.Float("Balance",
                           compute="_compute_amount",
                           readonly=True,
                           store=True)
    uom_id = fields.Many2one("uom.uom",
                             "UOM",
                             related="product_id.uom_id",
                             readonly=True,
                             store=True)
    unit_cost = fields.Float("Unit Cost",
                             compute="_compute_amount",
                             readonly=False,
                             digits=(16, 0),
                             store=True)
    amount = fields.Float("Amount",
                          compute="_compute_amount",
                          digits=(16, 0),
                          readonly=True,
                          store=True)
    repackaging_id = fields.Many2one("stock.repackaging",
                                     "Repackage",
                                     ondelete='cascade',
                                     index=True,
                                     store=True)
    is_repackage = fields.Boolean("Repackage?", default=True)
    location_id = fields.Many2one("stock.location",
                                  "Location",
                                  default=_default_location_id)
    dest_location_id = fields.Many2one("stock.location",
                                       "Destination Location",
                                       default=_default_dest_location_id)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Package'),
                              ('done', 'Done')],
                             "Status",
                             default="draft")
    move_id = fields.Many2one("stock.move", "Stock Move")
    sequence_number = fields.Integer("No")

    def action_get_stock_move_lines(self):
        for res in self.move_id:
            res.date = self.repackaging_id.date
            res.move_line_ids.date = self.repackaging_id.date
        action = self.env.ref('stock.stock_move_line_action').read([])[0]
        action['domain'] = [('move_id', '=', self.move_id.id)]
        return action

    @api.one
    @api.depends('product_id', 'onhand_qty', 'unit_cost', 'quantity',
                 'balance')
    def _compute_amount(self):
        self.amount = 0
        self.balance = 0
        self.onhand_qty = self.onhand_qty
        equ_qty = 0
        if self.is_repackage and self.product_id:
            self.unit_cost = self.product_id.standard_price
        else:
            if not self.unit_cost and self.product_id:
                product_id = self.env['product.template'].search([
                    ('child_id', '=', self.product_id.id)
                ])
                if product_id.equvalent_qty < 0:
                    equ_qty = (-1) * product_id.equvalent_qty
                    self.unit_cost = round(product_id.standard_price * equ_qty,
                                           2)
                else:
                    self.unit_cost = round(
                        product_id.standard_price / product_id.equvalent_qty,
                        2)
        amount = round(self.unit_cost * self.quantity, 2)
        self.amount = amount
        if not self.onhand_qty:
            if self.product_id:
                stock_quant_ids = self.env['stock.quant'].search([
                    ('product_id', '=', self.product_id.id),
                    ('location_id', '=', self.repackaging_id.location_id.id)
                ])
                if stock_quant_ids:
                    self.onhand_qty = stock_quant_ids.quantity
        if self.onhand_qty and self.quantity:
            self.balance = self.onhand_qty + self.quantity
        if self.repackaging_id:
            if not self.dest_location_id:
                if self.repackaging_id.destination_location_id:
                    self.dest_location_id = self.repackaging_id.destination_location_id.id
            if not self.location_id:
                if self.repackaging_id.location_id:
                    self.location_id = self.repackaging_id.location_id.id

    @api.model
    def create(self, values):
        res = super(StockRepackingLine, self).create(values)
        return res

    def copy(self, default=None):
        default = dict(default or {})
        if self.product_id.child_id:
            product_id = self.product_id.child_id
            default['name'] = product_id.name
            default['product_id'] = product_id.id
            onhand = 0
            if product_id:
                stock_quant_ids = self.env['stock.quant'].search([
                    ('product_id', '=', product_id.id),
                    ('location_id', '=',
                     self.repackaging_id.destination_location_id.id)
                ])
                if stock_quant_ids:
                    onhand = stock_quant_ids.quantity
            default['onhand_qty'] = onhand
            if self.product_id.equvalent_qty < 0:
                default[
                    'quantity'] = self.quantity / self.product_id.equvalent_qty
            else:
                default['quantity'] = (
                    -1) * self.quantity * self.product_id.equvalent_qty
            if self.is_repackage:
                default['is_repackage'] = False
            if self.product_id.equvalent_qty > 0:
                default['unit_cost'] = self.unit_cost / default['quantity']
            elif self.product_id.equvalent_qty < 0:
                default['unit_cost'] = self.unit_cost / default['quantity']
            else:
                UserError(
                    _("Please set sub equvalent quantity of sub product."))
            if self.repackaging_id:
                if self.repackaging_id.destination_location_id:
                    default[
                        'location_id'] = self.repackaging_id.destination_location_id.id
                if self.repackaging_id.location_id:
                    default[
                        'dest_location_id'] = self.repackaging_id.location_id.id
        return super(StockRepackingLine, self).copy(default)

    def post_inventory(self):
        # The inventory is posted as a single step which means quants cannot be moved from an internal location to another using an inventory
        # as they will be moved to inventory loss, and other quants will be created to the encoded quant location. This is a normal behavior
        # as quants cannot be reuse from inventory location (users can still manually move the products before/after the inventory if they want).
        self.mapped('move_id').filtered(
            lambda move: move.state != 'done')._action_done()


class Location(models.Model):
    _inherit = "stock.location"

    is_repackaging = fields.Boolean("Is Repackaging", defualt=False)
