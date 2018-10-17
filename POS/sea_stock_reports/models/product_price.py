from odoo import api, fields, models, tools, _

class ProductAttributePrice(models.Model):
	_inherit= "product.attribute.line"

	cost = fields.Float(related="product_tmpl_id.standard_price", store=True, string='Cost')

class ProductAttributePrice(models.Model):
	_inherit= "product.attribute"

	cost = fields.Float(related="attribute_line_ids.cost", store=True, string='Cost')

class ProductAttributevalue(models.Model):
	_inherit = "product.attribute.value"

	total_price=fields.Float('Total Cost')
	cost = fields.Float(related="product_tmpl_id.standard_price", store=True, string='Cost')
	


	