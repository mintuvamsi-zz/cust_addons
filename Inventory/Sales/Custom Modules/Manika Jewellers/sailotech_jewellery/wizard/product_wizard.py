# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import pdb
import psycopg2

class ProjectTemplateWizard(models.TransientModel):
    """
    This wizard will confirm the all the selected draft invoices
    """

    _name = "product.template.wizard"
    _description = "Generate Sequence Number"



    quantity = fields.Integer("Quantity")
    # @api.multi
    # def invoice_transffer(self):
    #     context = dict(self._context or {})
    #     active_ids = context.get('active_ids', []) or []

    #     for record in self.env['account.invoice'].browse(active_ids):
    #         #pdb.set_trace()
    #         if record.invoice_status == 'Ready to Transfer':

    #             raise UserError(_("Selected invoice(s) cannot be confirmed to Transffered as they are not in 'Transffered' state."))
    #         record.invoice_status='Ready to Transfer'
    #     return {'type': 'ir.actions.act_window_close'}
    @api.multi
    def update_sequence(self):
        #pdb.set_trace()
        context = dict(self._context or {})
        active_ids = context.get('active_id', []) or []
        product_template=self.env['product.template']
        company_id=product_template.browse(active_ids).company_id.id
        product_tmpl_id=product_template.browse(active_ids).id
        quantity=self.quantity
        user_id=product_template.browse(active_ids).create_uid.id
        # conn_string = "host='localhost' dbname='Jew' user='karthik' password='odoo'"
        # conn = psycopg2.connect(conn_string)
        # conn.rollback()
        # cursor = conn.cursor()
        
        #end_date=str(self.date_to)
        #cursor.rollback()
        self._cr.execute("SELECT * FROM update_sequence(%s,%s,%s,%s)",
            (company_id,product_tmpl_id,quantity,user_id))
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