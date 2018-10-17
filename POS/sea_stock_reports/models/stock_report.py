from odoo import api, fields, models, tools, _
class StockReport(models.Model):
	_name = "stock.report"
	_auto = False
	_rec_name = 'partner'
	_order='scheduled_date'

	id=fields.Integer('ID')
	partner=fields.Char('Partner')
	product=fields.Char('Product')
	recived_qty=fields.Integer('Received Quantity')
	scheduled_date=fields.Datetime('Received Date')
	sold_qty=fields.Integer('Sold Quantity')
	remain_date=fields.Datetime('Date')
	rem_qty=fields.Integer('Remaining Quantity')


	@api.model_cr
	def init(self):
		tools.drop_view_if_exists(self._cr, 'stock_report')
		self._cr.execute("""
			CREATE OR REPLACE VIEW public.stock_report AS
				SELECT row_number() OVER () AS id,
					rp.name AS partner,
					sm.name AS product,
					sm.product_qty AS recived_qty,
					sp.scheduled_date,
					sm.product_qty::double precision + sq.quantity - sm.product_qty::double precision AS sold_qty,
					sp.scheduled_date as remain_date,
					sm.product_qty::double precision - sq.quantity AS rem_qty
				FROM stock_move sm, 
					product_product pp, 
					stock_quant sq, 
					res_partner rp, 
					stock_picking sp
				WHERE sm.picking_type_id =1 
				AND sm.product_id=pp.id 
				AND sq.product_id=pp.id 
				AND sq.location_id=9 
				AND rp.id=sp.partner_id 
				AND sp.id=sm.picking_id;
											""")