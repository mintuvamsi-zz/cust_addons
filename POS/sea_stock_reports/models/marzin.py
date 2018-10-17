from odoo import api, fields, models, tools, _

class POSOrder(models.Model):
	_inherit = "pos.order"

	amount_tax = fields.Float(store=True, string='Tax Amount')


class POSOrderLine(models.Model):
	_inherit = "pos.order.line"

	cost = fields.Float(related="product_id.standard_price", store=True, string='Cost')
	tax = fields.Float(related="order_id.amount_tax", store=True, string='Tax')

class MarginReport(models.Model):
	_name = "margin.report"
	_auto = False
	_rec_name = 'product'

	id=fields.Char('ID')
	product=fields.Char('Product')
	tax_rate=fields.Float('Tax Rate')
	qty=fields.Char('Quantity')
	cost=fields.Integer('Cost')
	cost_tax=fields.Integer('Tax')
	cost_total=fields.Integer('Total')
	date=fields.Datetime('Date')
	sale_price=fields.Integer('Sale Price')
	sale_amount_total=fields.Integer('Amount Total')
	margin=fields.Integer('Product Margin')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'margin_report')
		self._cr.execute("""
			CREATE OR REPLACE VIEW public.margin_report AS 
			SELECT 
				row_number() OVER () AS id,
				a.product,
				a.tax_rate,
				a.qty,
				a.cost,
				a.cost_tax,
				a.cost_total,
				a.date,
				a.sale_price,
				a.sale_amount_total,
				a.sale_amount_total - a.cost_total AS margin
			FROM 
				(SELECT 
					pt.name AS product,
					round(pol.tax * 100::numeric / pol.price_unit / pol.qty, 2) AS tax_rate,
					pol.qty,
					pol.cost,
					round(pol.cost * (pol.tax * 100::numeric / pol.price_unit) / pol.qty / 100::numeric * pol.qty, 2) AS cost_tax,
					round(pol.cost * (pol.tax * 100::numeric / pol.price_unit) / pol.qty / 100::numeric * pol.qty + pol.cost * pol.qty, 2) AS cost_total,
					po.date_order AS date,
					pol.price_unit AS sale_price,
					round(pol.price_unit * pol.qty, 2) AS sale_amount_total
				FROM 
					pos_order po,
					pos_order_line pol,
					product_product pp,
					product_template pt
				WHERE
					pp.id = pol.product_id 
					AND pp.product_tmpl_id = pt.id
					AND po.id = pol.order_id) a;

							""")