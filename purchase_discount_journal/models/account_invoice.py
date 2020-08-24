# -*- coding: utf-8 -*-
# --- Correct Accounting Flow For Invoice
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.tools import float_is_zero
from odoo.exceptions import UserError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"
   # NEW ADD FIELD ZNL
    picking_number = fields.Char(string="Picking Number")

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'discount_type', 'discount_rate', 'tax_type', 'invoice_line_ids', 'is_tax')
    def _compute_amount(self):

        for inv in self:
            amount_untaxed = self.amount_discount = self.amount_tax = line_discount = amount_global_discount = after_global_amt_total = 0.0
            for line in inv.invoice_line_ids:
                if line.discount_line_type == 'fixed':
                    line_discount += (line.dis_amount * line.quantity)
                elif line.discount_line_type == 'percent':
                    line_discount += ((line.quantity * line.price_unit) * line.dis_amount) / 100
                else:
                    line_discount = line_discount
                if inv.discount_type == 'fixed':
                    amount_untaxed += line.price_subtotal
                    self.amount_untaxed = amount_untaxed
                    line.discount = 0.0

                elif inv.discount_type == 'percent':
                    amount_untaxed += line.quantity * line.price_unit
                    self.amount_untaxed = amount_untaxed

                else:
                    amount_untaxed += line.price_subtotal
                    self.amount_untaxed = amount_untaxed
                    self.amount_discount = 0.0
        amount_tax = 0.0
        self.amount_discount = line_discount
        self.disc_sub_total = self.amount_untaxed - self.amount_discount

        if self.discount_type == 'fixed':
            amount_global_discount = self.discount_rate
        elif self.discount_type == 'percent':
            amount_global_discount = (self.disc_sub_total * self.discount_rate) / 100
        else:
            amount_global_discount = 0.0
            self.discount_rate = 0.0

        self.amount_global_discount = amount_global_discount
        after_global_amt_total = self.disc_sub_total - self.amount_global_discount
        # ***************For global_tax***************
        if self.company_id.global_tax == True and self.is_tax == True:
            if self.company_id.account_purchase_tax_id:
                amount_tax = (after_global_amt_total * self.company_id.account_purchase_tax_id.amount) / 100
            #else:
               # raise UserError(_('Please check purchase account tax.'))
        else:
            amount_tax = 0.0
        # **********************************************
        self.amount_tax = amount_tax
        self.amount_global_dis_total = after_global_amt_total
        self.amount_total = after_global_amt_total + amount_tax

        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign


    discount_type = fields.Selection([('percent', 'Percentage'), ('fixed', 'Fixed')], string='Type', readonly=True,
                                     states={'draft': [('readonly', False)]}, default='fixed')
    discount_rate = fields.Float('Amount', digits=(16, 1), readonly=True, states={'draft': [('readonly', False)]},
                                 default=0.0)
    amount_discount = fields.Monetary(string='Line Discount', store=True, readonly=True, compute='_compute_amount',
                                      track_visibility='always')
    disc_sub_total = fields.Monetary(string='After Line Discount', store=True, readonly=True,
                                     compute='_compute_amount', track_visibility='always')
    amount_total = fields.Monetary(string='Net Total', store=True, readonly=True, compute='_compute_amount')
    tax = fields.Boolean(string="Global Tax", related="company_id.global_tax", store=True)
    is_tax = fields.Boolean(string="Is Tax", store=True)
    tax_type = fields.Selection([('exclude_tax', "Exclude Tax")], string="Tax Payment Type")
    amount_tax = fields.Monetary(string='Commercial Tax 5%',
                                 store=True, readonly=True, compute='_compute_amount')
    global_tax = fields.Boolean("Global Tax", related="company_id.global_tax", store=True)
    amount_global_discount = fields.Monetary(string='Global Discount', store=True, readonly=True,
                                             compute='_compute_amount')
    amount_global_dis_total = fields.Monetary(string='After Global Discount', store=True, readonly=True,
                                              compute='_compute_amount')

    @api.onchange('discount_type', 'discount_rate', 'invoice_line_ids', 'tax_type', 'is_tax')
    def supply_rate(self):
        for inv in self:
            amount_total = amount_untaxed = amount_discount = line_discount = total = after_global_amt_total = 0.0
            for line in inv.invoice_line_ids:
                if line.discount_line_type == 'fixed':
                    line_discount += (line.dis_amount * line.quantity)
                elif line.discount_line_type == 'percent':
                    line_discount += ((line.quantity * line.price_unit) * line.dis_amount) / 100
                else:
                    line_discount = line_discount
                if inv.discount_type == 'fixed':
                    amount_untaxed += line.price_subtotal
                    self.amount_untaxed = amount_untaxed
                    line.discount = 0.0
                    amount_discount = self.discount_rate
                elif inv.discount_type == 'percent':
                    amount_untaxed += line.quantity * line.price_unit
                    self.amount_untaxed = amount_untaxed
                    amount_discount = ((line.quantity * line.price_unit) * self.discount_rate) / 100
                else:
                    amount_untaxed += line.price_subtotal
                    self.amount_untaxed = amount_untaxed
                    self.amount_discount = 0.0
                    self.discount_rate = 0.0
        amount_tax = 0.0
        self.amount_discount = line_discount
        self.disc_sub_total = self.amount_untaxed - self.amount_discount
        after_global_amt_total = self.amount_untaxed - amount_discount
        # ********************For global_tax***************************
        if self.company_id.global_tax == True and self.is_tax == True:
            if self.company_id.account_purchase_tax_id:
                amount_tax = (after_global_amt_total * self.company_id.account_purchase_tax_id.amount) / 100
            #else:
             #   raise UserError(_('Please check purchase account tax.'))
        else:
            amount_tax = 0.0

        # **************************************************************

        self.amount_tax = amount_tax
        self.amount_global_dis_total = after_global_amt_total
        self.amount_total = after_global_amt_total + amount_tax

    @api.onchange('purchase_id')
    def purchase_order_change(self):
        if not self.purchase_id:
            return {}
        if not self.partner_id:
            self.partner_id = self.purchase_id.partner_id.id

        if not self.invoice_line_ids:
            # as there's no invoice line yet, we keep the currency of the PO
            self.currency_id = self.purchase_id.currency_id
        new_lines = self.env['account.invoice.line']
        for line in self.purchase_id.order_line - self.invoice_line_ids.mapped('purchase_line_id'):
            data = self._prepare_invoice_line_from_po_line(line)
            new_line = new_lines.new(data)
            new_line._set_additional_fields(self)
            new_lines += new_line

        self.invoice_line_ids += new_lines
        self.payment_term_id = self.purchase_id.payment_term_id
        self.discount_type = self.purchase_id.discount_type
        self.discount_rate = self.purchase_id.discount_rate
        self.is_tax = self.purchase_id.is_tax
        self.amount_tax = self.purchase_id.amount_tax
        self.env.context = dict(self.env.context, from_purchase_order_change=True)
        self.purchase_id = False
        return {}

    def _prepare_invoice_line_from_po_line(self, line):

        invoice_line = self.env['account.invoice.line']
        date = self.date or self.date_invoice
        data = {
            'purchase_line_id': line.id,
            'name': line.order_id.name + ': ' + line.name,
            'origin': line.order_id.origin,
            'uom_id': line.product_uom.id,
            'product_id': line.product_id.id,
            'account_id': invoice_line.with_context(
                {'journal_id': self.journal_id.id, 'type': 'in_invoice'})._default_account(),
            'price_unit': line.order_id.currency_id._convert(
                line.price_unit, self.currency_id, line.company_id, date or fields.Date.today(), round=False),
            'quantity': line.product_qty,
            'discount': 0.0,
            'discount_line_type': line.discount_line_type,
            'dis_amount': line.dis_amount,
            'account_analytic_id': line.account_analytic_id.id,
            'analytic_tag_ids': line.analytic_tag_ids.ids,
        }
        account = invoice_line.get_invoice_line_account('in_invoice', line.product_id, line.order_id.fiscal_position_id,
                                                        self.env.user.company_id)
        if account:
            data['account_id'] = account.id
        return data

    @api.model
    def invoice_line_move_line_get(self):  # 08/08/2019
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        if self.amount_discount + self.amount_global_discount > 0:
            name = "Discount"
            if self.discount_type == 'percent':
                name = name + " (" + str(self.discount_rate) + "%)"
            name = name + " for " + (self.origin if self.origin else ("Invoice # " + str(self.id)))
            if self.type in ["out_invoice", "out_refund"]:
                sale_discount = self.company_id.sale_discount
                if not sale_discount:
                    raise UserError(_('Please check sale account ID'))
                dis_account_id = sale_discount.id
                val = {
                    'invl_id': self.number,
                    'type': 'src',
                    'name': name,
                    'price_unit': self.amount_discount + self.amount_global_discount,
                    'quantity': 1,
                    'price': -(self.amount_discount + self.amount_global_discount,),
                    'account_id': dis_account_id,
                    'invoice_id': self.id,
                }
                res.append(val)

            elif self.type in ["in_invoice", "in_refund"]:
                purchase_discount = self.company_id.purchase_discount
                if not purchase_discount:
                    raise UserError(_('Please check purchase account ID'))
                dis_account_id = purchase_discount.id
                val = {
                    'invl_id': self.number,
                    'type': 'src',
                    'name': name,
                    'price_unit': (self.amount_discount + self.amount_global_discount),
                    'quantity': 1,
                    'price': -(self.amount_discount + self.amount_global_discount),
                    'account_id': dis_account_id,
                    'invoice_id': self.id,
                }
                res.append(val)
        if self.company_id.global_tax == True or self.is_tax == True:
            name = "Global Tax"
            name = name + " for " + (self.origin if self.origin else ("Invoice # " + str(self.id)))
            if self.type in ("out_invoice", "out_refund"):
                tax_id = self.company_id.account_sale_tax_id.account_id.id
                if not tax_id:
                    raise UserError(_('Please check Sale account tax.'))
                val = {
                    'invl_id': self.number,
                    'type': 'src',
                    'name': name,
                    'price_unit': self.amount_tax,
                    'quantity': 1,
                    'price': -self.amount_tax,
                    'account_id': tax_id,
                    'invoice_id': self.id,
                }
                res.append(val)
            if self.type in ("in_invoice", "in_refund"):
                tax_id = self.company_id.account_purchase_tax_id.account_id.id
                if not tax_id:
                    raise UserError(_('Please check Purchase account tax.'))
                val = {
                    'invl_id': self.number,
                    'type': 'src',
                    'name': name,
                    'price_unit': self.amount_tax,
                    'quantity': 1,
                    'price': self.amount_tax,
                    'account_id': tax_id,
                    'invoice_id': self.id,
                }
                res.append(val)
        return res

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discount_line_type = fields.Selection([('fixed', "Fixed"), ('percent', "Percentage")], string="Discount Type",
                                          default='percent')
    dis_amount = fields.Float(string='Discount', digits=(16, 2), invisible="[('discount_line_type','=','fixed')]",
                              store=True)

    def _set_taxes(self):  # 08/08/2019
        super(AccountInvoiceLine, self)._set_taxes()
        """ Used in on_change to set taxes and price"""
        self.ensure_one()
        invoice_id = self.invoice_id
        if invoice_id.is_tax and invoice_id.type in (
                "in_invoice", "in_refund"):
            self.invoice_line_tax_ids = False


class res_company(models.Model):
    _inherit = "res.company"

    sale_discount = fields.Many2one("account.account", string="Sale Discount")
    purchase_discount = fields.Many2one("account.account", string="Purchase Discount")
    global_tax = fields.Boolean("Global Tax", default=False)


class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'
    _inherit = 'res.config.settings'

    @api.one
    @api.depends('company_id')
    def _get_sale_journal_id(self):
        self.sale_discount = self.company_id.sale_discount

    @api.one
    @api.depends('company_id')
    def _get_purchase_journal_id(self):
        self.purchase_discount = self.company_id.purchase_discount

    @api.one
    @api.depends('company_id')
    def _get_global_tax(self):
        self.global_tax = self.company_id.global_tax

    sale_discount = fields.Many2one('account.account', related="company_id.sale_discount", readonly=False,
                                    string='Sale Journal', help="Sale Discount of the company.")
    purchase_discount = fields.Many2one('account.account', related="company_id.purchase_discount", readonly=False,
                                        string='Sale Journal', help="Sale Discount of the company.")
    global_tax = fields.Boolean(readonly=False, string='Global Tax', related="company_id.global_tax",
                                help="Global Tax of the company.")

    @api.onchange('company_id')
    def onchange_company_id(self):
        self.sale_discount = self.company_id.sale_discount
        self.purchase_discount = self.company_id.purchase_discount
        self.global_tax = self.company_id.global_tax


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.multi
    def reconcile(self, writeoff_acc_id=False, writeoff_journal_id=False):
        # Empty self can happen if the user tries to reconcile entries which are already reconciled.
        # The calling method might have filtered out reconciled lines.
        if not self:
            return True

        # Perform all checks on lines
        company_ids = set()
        all_accounts = []
        partners = set()
        for line in self:
            company_ids.add(line.company_id.id)
            all_accounts.append(line.account_id)
            if (line.account_id.internal_type in ('receivable', 'payable')):
                partners.add(line.partner_id.id)
            if line.reconciled:
                raise UserError(_('You are trying to reconcile some entries that are already reconciled.'))
        if len(company_ids) > 1:
            raise UserError(_('To reconcile the entries company should be the same for all entries.'))
        if len(set(all_accounts)) > 2:
            raise UserError(_('Entries are not from the same account.'))
        if not (all_accounts[0].reconcile or all_accounts[0].internal_type == 'liquidity'):
            raise UserError(_(
                'Account %s (%s) does not allow reconciliation. First change the configuration of this account to allow it.') % (
                                all_accounts[0].name, all_accounts[0].code))

        # reconcile everything that can be
        remaining_moves = self.auto_reconcile_lines()

        writeoff_to_reconcile = self.env['account.move.line']

        if writeoff_acc_id and writeoff_journal_id and remaining_moves:
            all_aml_share_same_currency = all([x.currency_id == self[0].currency_id for x in self])
            writeoff_vals = {
                'account_id': writeoff_acc_id.id,
                'journal_id': writeoff_journal_id.id
            }
            if not all_aml_share_same_currency:
                writeoff_vals['amount_currency'] = False
            writeoff_to_reconcile = remaining_moves._create_writeoff([writeoff_vals])
            # add writeoff line to reconcile algorithm and finish the reconciliation
            remaining_moves = (remaining_moves + writeoff_to_reconcile).auto_reconcile_lines()
        # Check if reconciliation is total or needs an exchange rate entry to be created
        (self + writeoff_to_reconcile).check_full_reconcile()
        return True
