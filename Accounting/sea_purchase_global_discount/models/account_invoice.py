from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'tax_line_ids.amount_rounding',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_tax = sum(line.amount_total for line in self.tax_line_ids)
        self.amount_total = self.amount_untaxed + self.amount_tax

        for inv in self:
            if inv.discount_type == 'percent' and inv.discount_selection=='btd':
                for line in inv.invoice_line_ids:
                    line.discount = inv.discount_rate
                    self.amount_discount = sum((line.quantity * line.price_unit * line.discount)/100 for line in self.invoice_line_ids)

            elif inv.discount_type == 'amount' and inv.discount_selection=='btd':
                total = discount = 0.0
                for line in inv.invoice_line_ids:
                    total += (line.quantity * line.price_unit)
                    line.discount = (inv.discount_rate / total) * 100
                    inv.amount_discount=inv.discount_rate

            elif inv.discount_type == 'amount' and inv.discount_selection=='atd':
                inv.amount_total = inv.amount_untaxed + inv.amount_tax - inv.discount_rate
                inv.amount_discount=inv.discount_rate

            elif inv.discount_type == 'percent' and inv.discount_selection=='atd':
                inv.amount_total=inv.amount_untaxed + inv.amount_tax-(inv.amount_untaxed*inv.discount_rate/100)
                inv.amount_discount=inv.amount_untaxed + inv.amount_tax-(inv.amount_untaxed*inv.discount_rate/100)-(inv.amount_untaxed + inv.amount_tax)
                

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

    discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')], string='Discount Type',
                                     readonly=True, states={'draft': [('readonly', False)]}, default='percent')
    discount_rate = fields.Float('Discount Amount', digits=(16, 2), readonly=True, states={'draft': [('readonly', False)]})
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount',
                                      track_visibility='always')
    discount_selection = fields.Selection([('none','None'), ('atd','ATD'), ('btd','BTD')], default='none',string='Discount Selection', help="ATD=After Tax Discount(Total); BTD= Before Tax Discount(Sub Total)")



    @api.onchange('amount_tax','amount_total','amount_untaxed','discount_type', 'amount_discount', 'discount_selection', 'discount_rate', 'invoice_line_ids')
    def supply_rate(self):
        for inv in self:
            if inv.discount_type == 'percent' and inv.discount_selection=='btd':
                for line in inv.invoice_line_ids:
                    line.discount = inv.discount_rate
                    inv.amount_discount=inv.discount_rate
            elif inv.discount_type == 'amount' and inv.discount_selection=='btd':
                total = discount = 0.0
                for line in inv.invoice_line_ids:
                    total += (line.quantity * line.price_unit)
                    line.discount = (inv.discount_rate / total) * 100
            elif inv.discount_selection=='none':
                inv.discount_rate = 0
                inv.amount_discount=0
                for line in inv.invoice_line_ids:
                    line.discount=0
            elif inv.discount_type == 'amount' and inv.discount_selection=='atd':
                inv.amount_total = inv.amount_untaxed + inv.amount_tax - inv.discount_rate
                inv.amount_discount=inv.discount_rate
            elif inv.discount_type == 'percent' and inv.discount_selection=='atd':
                inv.amount_total=inv.amount_untaxed + inv.amount_tax-(inv.amount_untaxed*inv.discount_rate/100)
                inv.amount_discount=inv.amount_untaxed + inv.amount_tax-(inv.amount_untaxed*inv.discount_rate/100)-(inv.amount_untaxed + inv.amount_tax)

    @api.multi
    def compute_invoice_totals(self, company_currency, invoice_move_lines):
        total = 0
        total_currency = 0
        for line in invoice_move_lines:
            if self.currency_id != company_currency:
                currency = self.currency_id.with_context(date=self.date or self.date_invoice or fields.Date.context_today(self))
                line['currency_id'] = currency.id
                line['amount_currency'] = currency.round(line['price'])
                line['price'] = currency.compute(line['price'], company_currency)
            else:
                line['currency_id'] = False
                line['amount_currency'] = False
                line['price'] = line['price']
            if self.type in ('out_invoice', 'in_refund'):
                total += line['price']
                total_currency += line['amount_currency'] or line['price']
                line['price'] = - line['price']
            else:
                total -= line['price']
                total_currency -= line['amount_currency'] or line['price']
        return total, total_currency, invoice_move_lines

    @api.multi
    def button_dummy(self):
        self.supply_rate()
        return True

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    discount = fields.Float(string='Discount (%)', default=0.0)
