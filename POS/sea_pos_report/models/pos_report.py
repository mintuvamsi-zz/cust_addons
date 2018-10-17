from odoo import api, fields, models, tools
class posreport(models.Model):
  _name = "pos.report"
  _auto = False
  _rec_name = 'product_names'

  id=fields.Integer('ID')
  payment_modes=fields.Char('Payment modes')
  short_code=fields.Char('Short code')
  pos_payment_ref=fields.Boolean(string='POS Payment reference' ,help='Allow the payments in the pos payment where the payments are in True or Flase state')
  payment_ref_no=fields.Char('Payment Reference No')
  order_ref=fields.Char('Order Reference')
  product_names=fields.Char('Product Names')
  quantity=fields.Integer('Quantity')
  sales_price=fields.Float('Sales Price' , help='Acutal price of the product')
  total_price=fields.Float('Total price' , help='Total price for the orders at particular session')
  date=fields.Datetime('Date Order')
  pos_reference=fields.Char('Receipt order Reference No')
  session_ref=fields.Char('POS Session Reference No')

  @api.model_cr
  def init(self):
    tools.drop_view_if_exists(self._cr, 'pos_report')
    self._cr.execute("""
        CREATE OR REPLACE VIEW public.pos_report AS
        SELECT row_number() OVER () AS id,
        aj.name AS payment_modes,
        aj.code AS short_code,
        aj.pos_payment_ref,
        abkl.payment_ref as payment_ref_no,
        abkl.name AS order_ref,
        pt.name AS product_names,
        pol.qty AS quantity,
        pol.price_unit AS sales_price,
        am.amount AS total_price,
        am.date,
        po.pos_reference ,
        am.ref as session_ref
        FROM account_journal aj,
        account_bank_statement_line abkl,
        account_move am,
        pos_order po,
        pos_order_line pol,
        product_product pp,
        product_template pt
        WHERE aj.id = abkl.journal_id 
        AND abkl.pos_statement_id = po.id
        AND am.id = po.account_move
        AND pol.order_id = po.id
        AND pol.product_id = pp.id
        AND pp.product_tmpl_id = pt.id
        AND (aj.code::text = ANY (ARRAY['PAY'::character varying, 'C/D'::character varying, 'CSH1'::character varying]::text[]))
        GROUP BY aj.name,aj.code,aj.pos_payment_ref,abkl.payment_ref,abkl.name,pt.name,pol.qty,pol.price_unit,abkl.amount,am.amount,am.date,po.pos_reference,am.ref
        ORDER BY id;
          """)
















