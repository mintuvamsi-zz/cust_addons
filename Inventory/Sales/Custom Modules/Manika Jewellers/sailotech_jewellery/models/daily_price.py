from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.tools import float_is_zero, float_compare, pycompat
import re
import pdb

class DailyPrice(models.Model):
    _name = "daily.price"

    _description = "Define your Day to Day Prices of the Items"

    name = fields.Char(string='Type')
    daily_price_line_id = fields.One2many('daily.price.line','daily_price_id','Daily Price Line')

    @api.multi
    def all_costs_update(self):
        #pdb.set_trace()
        context = dict(self._context or {})
        #active_ids = context.get('active_id', []) or []
        type_id=self.id
        #company_id=product_template.browse(active_ids).company_id.id
        #quantity=self.quantity
        #user_id=product_template.browse(active_ids).create_uid.id
        # conn_string = "host='localhost' dbname='Jew' user='karthik' password='odoo'"
        # conn = psycopg2.connect(conn_string)
        # conn.rollback()
        # cursor = conn.cursor()
        
        #end_date=str(self.date_to)
        #cursor.rollback()
        self._cr.execute("SELECT * FROM all_costs_update("+str(type_id)+")")
        #status=cursor.fetchone()[0]
        #records = cursor.fetchall()
        # get_invoices=self.env['account.invoice'].search([('invoice_status','=','Ready to transffer'),('date_invoice','>=',self.date_from),('date_invoice','<=',self.date_to)])
        # start_date=self.date_from
        # end_date=self.date_to
        # period=self.period
        # gst_in=self.gst_in
        # p_user=self.p_user
        # query_string="select * from test_insert("+"'"+str(gst_in)+"','"+str(start_date)+"','"+str(end_date)+"','"+str(period)+"','"+str(p_user)+"')"
        # self.env.cr.execute(query_string)
        self.env.cr.commit()

class DailyPriceLine(models.Model):
	_name= "daily.price.line"

	name = fields.Float(string='Price Per Unit')
	date= fields.Date(string='Date')
	daily_price_id = fields.Many2one('daily.price','Daily Price ID')