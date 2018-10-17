from odoo import api, fields, models, tools, _
class RackWiseReport(models.Model):
	_name = "rackwise.report"
	_auto = False
	_rec_name = 'name'

	id=fields.Integer('ID')
	name=fields.Char('Product')
	quantity=fields.Integer('Quantity')
	complete_name=fields.Char('Location')
	date=fields.Datetime('Date')

	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'rackwise_report')
		self._cr.execute("""
			CREATE OR REPLACE VIEW public.rackwise_report AS 
			SELECT row_number() OVER () AS id,
				pt.name,
				sq.quantity,
				sl.complete_name,
				sq.create_date as date
				/*to_char(sq.in_date, 'DD-Mon-YYYY'::text)::date AS date*/
			FROM stock_quant sq,
				stock_location sl,
				product_product pp,
				product_template pt
			WHERE sq.location_id = sl.id AND sq.product_id = pp.id
			AND pp.product_tmpl_id = pt.id AND sq.location_id NOT IN(8,9)
				ORDER BY (row_number() OVER ()); """)

		