from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import UserError

class Picking(models.Model):

    _inherit = "stock.picking"

    currency_id = fields.Many2one(store=True, string='Currency', readonly=True)
    amount_total = fields.Monetary(string='Total', store=True, readonly=True)
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True)
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True)

    supplier_do = fields.Char(string="Supplier DO No")
    good_receive_date = fields.Date(string="Good Receive Date",default=fields.Date.today())

    @api.multi
    def action_done(self):

        todo_moves = self.mapped('move_lines').filtered(
            lambda self: self.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed'])
        # Check if there are ops not linked to moves yet
        for pick in self:
            # # Explode manually added packages
            # for ops in pick.move_line_ids.filtered(lambda x: not x.move_id and not x.product_id):
            #     for quant in ops.package_id.quant_ids: #Or use get_content for multiple levels
            #         self.move_line_ids.create({'product_id': quant.product_id.id,
            #                                    'package_id': quant.package_id.id,
            #                                    'result_package_id': ops.result_package_id,
            #                                    'lot_id': quant.lot_id.id,
            #                                    'owner_id': quant.owner_id.id,
            #                                    'product_uom_id': quant.product_id.uom_id.id,
            #                                    'product_qty': quant.qty,
            #                                    'qty_done': quant.qty,
            #                                    'location_id': quant.location_id.id, # Could be ops too
            #                                    'location_dest_id': ops.location_dest_id.id,
            #                                    'picking_id': pick.id
            #                                    }) # Might change first element
            # # Link existing moves or add moves when no one is related
            for ops in pick.move_line_ids.filtered(lambda x: not x.move_id):
                # Search move with this product
                moves = pick.move_lines.filtered(lambda x: x.product_id == ops.product_id)
                moves = sorted(moves, key=lambda m: m.quantity_done < m.product_qty, reverse=True)
                if moves:
                    ops.move_id = moves[0].id
                else:
                    new_move = self.env['stock.move'].create({
                        'name': _('New Move:') + ops.product_id.display_name,
                        'product_id': ops.product_id.id,
                        'product_uom_qty': ops.qty_done,
                        'product_uom': ops.product_uom_id.id,
                        'location_id': pick.location_id.id,
                        'location_dest_id': pick.location_dest_id.id,
                        'picking_id': pick.id,
                        'picking_type_id': pick.picking_type_id.id,
                    })
                    ops.move_id = new_move.id
                    new_move._action_confirm()
                    todo_moves |= new_move
                    # 'qty_done': ops.qty_done})
        todo_moves._action_done()

        query = """UPDATE stock_move SET date='"""+str(self.good_receive_date)+"""' WHERE origin='"""+str(self.origin)+"""';"""
        self.env.cr.execute(query)
        if self.partner_id:
            stat = """UPDATE stock_move SET partner_id='"""+str(self.partner_id.id)+"""' WHERE picking_id='"""+str(self.id)+"""';"""
            self.env.cr.execute(stat)
        quer="""SELECT id FROM stock_move WHERE picking_id='"""+str(self.id)+"""';"""
        self.env.cr.execute(quer)
        record = self.env.cr.dictfetchall()
        for res in record:
            move_id = res['id']
            print("MOve ID",move_id)
            que = """UPDATE account_move SET date='"""+str(self.good_receive_date)+"""' WHERE stock_move_id="""+str(move_id)+""";"""
            self.env.cr.execute(que)
        self.write({'date_done': self.scheduled_date})
        self.move_line_ids.write({'date': self.scheduled_date})
        self.move_lines.write({'date': self.scheduled_date})

        return True

    @api.multi
    def button_validate(self):
        self.ensure_one()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))

        # If no lots when needed, raise error
        picking_type = self.picking_type_id
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in self.move_line_ids)
        if no_reserved_quantities and no_quantities_done:
            raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        if picking_type.use_create_lots or picking_type.use_existing_lots:
            lines_to_check = self.move_line_ids
            if not no_quantities_done:
                lines_to_check = lines_to_check.filtered(
                    lambda line: float_compare(line.qty_done, 0,
                                               precision_rounding=line.product_uom_id.rounding)
                )

            for line in lines_to_check:
                product = line.product_id
                if product and product.tracking != 'none':
                    if not line.lot_name and not line.lot_id:
                        raise UserError(_('You need to supply a Lot/Serial number for product %s.') % product.display_name)

        if no_quantities_done:
            view = self.env.ref('stock.view_immediate_transfer')
            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
            view = self.env.ref('stock.view_overprocessed_transfer')
            wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.overprocessed.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        # Check backorder should check for other barcodes
        if self._check_backorder():
            return self.action_generate_backorder_wizard()
        self.action_done()
        query = """UPDATE stock_move SET date='"""+str(self.good_receive_date)+"""' WHERE origin='"""+str(self.origin)+"""';"""
        self.env.cr.execute(query)
        if self.partner_id:
            stat = """UPDATE stock_move SET partner_id='"""+str(self.partner_id.id)+"""' WHERE picking_id='"""+str(self.id)+"""';"""
            self.env.cr.execute(stat)
        quer="""SELECT id FROM stock_move WHERE picking_id='"""+str(self.id)+"""';"""
        self.env.cr.execute(quer)
        record = self.env.cr.dictfetchall()
        for res in record:
            move_id = res['id']
            print("MOve ID",move_id)
            que = """UPDATE account_move SET date='"""+str(self.good_receive_date)+"""' WHERE stock_move_id="""+str(move_id)+""";"""
            self.env.cr.execute(que)
        return

class StockImmediateTransfer(models.TransientModel):
    _name = 'stock.immediate.transfer'
    _inherit = 'stock.immediate.transfer'

    def process(self):
        pick_to_backorder = self.env['stock.picking']
        pick_to_do = self.env['stock.picking']
        for picking in self.pick_ids:
            # If still in draft => confirm and assign
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
            for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty
            if picking._check_backorder():
                pick_to_backorder |= picking
                continue
            pick_to_do |= picking
        # Process every picking that do not require a backorder, then return a single backorder wizard for every other ones.
        if pick_to_do:
            pick_to_do.action_done()
            query = """UPDATE stock_move SET date='"""+str(pick_to_do.good_receive_date)+"""' WHERE origin='"""+str(pick_to_do.origin)+"""';"""
            self.env.cr.execute(query)
            if pick_to_do.partner_id:
                stat = """UPDATE stock_move SET partner_id='"""+str(pick_to_do.partner_id.id)+"""' WHERE picking_id='"""+str(pick_to_do.id)+"""';"""
                self.env.cr.execute(stat)
            quer="""SELECT id FROM stock_move WHERE picking_id='"""+str(pick_to_do.id)+"""';"""
            self.env.cr.execute(quer)
            record = self.env.cr.dictfetchall()
            for res in record:
                move_id = res['id']
                print("MOve ID",move_id)
                que = """UPDATE account_move SET date='"""+str(pick_to_do.good_receive_date)+"""' WHERE stock_move_id="""+str(move_id)+""";"""
                self.env.cr.execute(que)
        if pick_to_backorder:
            return pick_to_backorder.action_generate_backorder_wizard()
        return False    @api.multi
    def button_validate(self):
        self.ensure_one()
        if not self.move_lines and not self.move_line_ids:
            raise UserError(_('Please add some items to move.'))

        # If no lots when needed, raise error
        picking_type = self.picking_type_id
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in self.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
        no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in self.move_line_ids)
        if no_reserved_quantities and no_quantities_done:
            raise UserError(_('You cannot validate a transfer if no quantites are reserved nor done. To force the transfer, switch in edit more and encode the done quantities.'))

        if picking_type.use_create_lots or picking_type.use_existing_lots:
            lines_to_check = self.move_line_ids
            if not no_quantities_done:
                lines_to_check = lines_to_check.filtered(
                    lambda line: float_compare(line.qty_done, 0,
                                               precision_rounding=line.product_uom_id.rounding)
                )

            for line in lines_to_check:
                product = line.product_id
                if product and product.tracking != 'none':
                    if not line.lot_name and not line.lot_id:
                        raise UserError(_('You need to supply a Lot/Serial number for product %s.') % product.display_name)

        if no_quantities_done:
            view = self.env.ref('stock.view_immediate_transfer')
            wiz = self.env['stock.immediate.transfer'].create({'pick_ids': [(4, self.id)]})
            return {
                'name': _('Immediate Transfer?'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.immediate.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        if self._get_overprocessed_stock_moves() and not self._context.get('skip_overprocessed_check'):
            view = self.env.ref('stock.view_overprocessed_transfer')
            wiz = self.env['stock.overprocessed.transfer'].create({'picking_id': self.id})
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'stock.overprocessed.transfer',
                'views': [(view.id, 'form')],
                'view_id': view.id,
                'target': 'new',
                'res_id': wiz.id,
                'context': self.env.context,
            }

        # Check backorder should check for other barcodes
        if self._check_backorder():
            return self.action_generate_backorder_wizard()
        self.action_done()
        query = """UPDATE stock_move SET date='"""+str(self.good_receive_date)+"""' WHERE origin='"""+str(self.origin)+"""';"""
        self.env.cr.execute(query)
        if self.partner_id:
            stat = """UPDATE stock_move SET partner_id='"""+str(self.partner_id.id)+"""' WHERE picking_id='"""+str(self.id)+"""';"""
            self.env.cr.execute(stat)
        quer="""SELECT id FROM stock_move WHERE picking_id='"""+str(self.id)+"""';"""
        self.env.cr.execute(quer)
        record = self.env.cr.dictfetchall()
        for res in record:
            move_id = res['id']
            print("MOve ID",move_id)
            que = """UPDATE account_move SET date='"""+str(self.good_receive_date)+"""' WHERE stock_move_id="""+str(move_id)+""";"""
            self.env.cr.execute(que)
        return

class StockImmediateTransfer(models.TransientModel):
    _name = 'stock.immediate.transfer'
    _inherit = 'stock.immediate.transfer'

    def process(self):
        pick_to_backorder = self.env['stock.picking']
        pick_to_do = self.env['stock.picking']
        for picking in self.pick_ids:
            # If still in draft => confirm and assign
            if picking.state == 'draft':
                picking.action_confirm()
                if picking.state != 'assigned':
                    picking.action_assign()
                    if picking.state != 'assigned':
                        raise UserError(_("Could not reserve all requested products. Please use the \'Mark as Todo\' button to handle the reservation manually."))
            for move in picking.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty
            if picking._check_backorder():
                pick_to_backorder |= picking
                continue
            pick_to_do |= picking
        # Process every picking that do not require a backorder, then return a single backorder wizard for every other ones.
        if pick_to_do:
            pick_to_do.action_done()
            query = """UPDATE stock_move SET date='"""+str(pick_to_do.good_receive_date)+"""' WHERE origin='"""+str(pick_to_do.origin)+"""';"""
            self.env.cr.execute(query)
            if pick_to_do.partner_id:
                stat = """UPDATE stock_move SET partner_id='"""+str(pick_to_do.partner_id.id)+"""' WHERE picking_id='"""+str(pick_to_do.id)+"""';"""
                self.env.cr.execute(stat)
            quer="""SELECT id FROM stock_move WHERE picking_id='"""+str(pick_to_do.id)+"""';"""
            self.env.cr.execute(quer)
            record = self.env.cr.dictfetchall()
            for res in record:
                move_id = res['id']
                print("MOve ID",move_id)
                que = """UPDATE account_move SET date='"""+str(pick_to_do.good_receive_date)+"""' WHERE stock_move_id="""+str(move_id)+""";"""
                self.env.cr.execute(que)
        if pick_to_backorder:
            return pick_to_backorder.action_generate_backorder_wizard()
        return False