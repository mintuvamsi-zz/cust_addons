# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
import psycopg2

class profit_loss(models.Model):
    _name = 'profit.loss'
    _auto  =  False
    #_rec_name  =  'sno'
    #_order  =  'date desc'

    id  =  fields.Integer(string =  'ID')
    # incrownum = fields.Integer()
    # incid = fields.Integer()
    incname = fields.Char(string="Income Name")
    incproductname = fields.Char(string="Income Product Name")
    incentityname = fields.Char(string="Income Entity Name")
    # inccredit = fields.Integer()
    # incdebit = fields.Integer()
    # opincomecredit = fields.Integer()
    # opincomedebit = fields.Integer()
    # grossincomecredit = fields.Integer()
    # grossincomedebit = fields.Integer()
    # totincomecredit = fields.Integer()
    # totincomedebit = fields.Integer()
    totincome = fields.Float(string="Total Income")
    # exprownum = fields.Integer()
    # expid = fields.Integer()
    expname = fields.Char(string="Expense Name")
    expproductname = fields.Char(string="Expense Product Name")
    expentityname = fields.Char(string="Expense Entity Name")
    # expcredit = fields.Integer()
    # expdebit = fields.Integer()
    # opexpensecredit = fields.Integer()
    # opexpensedebit = fields.Integer()
    # grossexpensecredit = fields.Integer()
    # grossexpensedebit = fields.Integer()
    # totexpensecredit = fields.Integer()
    # totexpensedebit = fields.Integer()
    totexpense = fields.Float(string="Total Expenses")
    grossprofit = fields.Float(store=True,string="Net Profit")

    # @api.onchange('login')
    # def on_change_login(self):
    #     self.email = self.login


    # @api.model_cr
    # def init(self):
    #     tools.drop_view_if_exists(self._cr, 'profit_loss')
    #     self._cr.execute('select * from profit_loss')

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'profit_loss')
        self._cr.execute("""CREATE OR REPLACE VIEW profit_loss AS             
            SELECT row_number() OVER (ORDER BY tb1.incrownum) AS id,
            tb1.incrownum,
            tb1.incid,
            tb1.incname,
            tb1.incproductname,
            tb1.incentityname,
            tb1.inccredit,
            tb1.incdebit,
            tb1.opincomecredit,
            tb1.opincomedebit,
            tb1.grossincomecredit,
            tb1.grossincomedebit,
            tb1.totincomecredit,
            tb1.totincomedebit,
            tb1.totincome,
            tb2.exprownum,
            tb2.expid,
            tb2.expname,
            tb2.expproductname,
            tb2.expentityname,
            tb2.expcredit,
            tb2.expdebit,
            tb2.opexpensecredit,
            tb2.opexpensedebit,
            tb2.grossexpensecredit,
            tb2.grossexpensedebit,
            tb2.totexpensecredit,
            tb2.totexpensedebit,
            tb2.totexpense,
            tb1.totincome - tb2.totexpense as grossprofit
           FROM ( SELECT row_number() OVER (ORDER BY x.id) AS incrownum,
                    x.id AS incid,
                    x.name AS incname,
                    x.productname AS incproductname,
                    x.entityname AS incentityname,
                    x.credit AS inccredit,
                    x.debit AS incdebit,
                    sum(x.credit) OVER (PARTITION BY x.name, x.productname ORDER BY x.name, x.productname) AS opincomecredit,
                    sum(x.debit) OVER (PARTITION BY x.name, x.productname ORDER BY x.name, x.productname) AS opincomedebit,
                    sum(x.credit) OVER (PARTITION BY x.name ORDER BY x.name) AS grossincomecredit,
                    sum(x.debit) OVER (PARTITION BY x.name ORDER BY x.name) AS grossincomedebit,
                    sum(x.credit) OVER (PARTITION BY (x.id = ANY (ARRAY[13, 14, 17])) ORDER BY (x.id = ANY (ARRAY[13, 14, 17]))) AS totincomecredit,
                    sum(x.debit) OVER (PARTITION BY (x.id = ANY (ARRAY[13, 14, 17])) ORDER BY (x.id = ANY (ARRAY[13, 14, 17]))) AS totincomedebit,
                    sum(x.credit) OVER (PARTITION BY (x.id = ANY (ARRAY[13, 14, 17])) ORDER BY (x.id = ANY (ARRAY[13, 14, 17]))) + sum(x.debit) OVER (PARTITION BY (x.id = ANY (ARRAY[13, 14, 17])) ORDER BY (x.id = ANY (ARRAY[13, 14, 17]))) AS totincome
                   FROM ( SELECT aat.id,
                            aat.name,
                            aa.code::text || aa.name::text AS productname,
                            aml.name AS entityname,
                            sum(COALESCE(aml.credit, 0::numeric)) AS credit,
                            sum(COALESCE(aml.debit, 0::numeric)) AS debit
                           FROM account_account_type aat
                             LEFT JOIN account_account aa ON aat.id = aa.user_type_id
                             LEFT JOIN account_move_line aml ON aa.user_type_id = aml.user_type_id
                          WHERE aat.id = ANY (ARRAY[13, 14, 17])
                          GROUP BY aat.id, (aa.code::text || aa.name::text), aml.name
                          ORDER BY aat.id) x
                  ORDER BY (row_number() OVER (ORDER BY x.id))) tb1
             FULL JOIN ( SELECT row_number() OVER (ORDER BY x.id) AS exprownum,
                    x.id AS expid,
                    x.name AS expname,
                    x.productname AS expproductname,
                    x.entityname AS expentityname,
                    x.credit AS expcredit,
                    x.debit AS expdebit,
                    sum(x.credit) OVER (PARTITION BY x.name, x.productname ORDER BY x.name, x.productname) AS opexpensecredit,
                    sum(x.debit) OVER (PARTITION BY x.name, x.productname ORDER BY x.name, x.productname) AS opexpensedebit,
                    sum(x.credit) OVER (PARTITION BY x.name ORDER BY x.name) AS grossexpensecredit,
                    sum(x.debit) OVER (PARTITION BY x.name ORDER BY x.name) AS grossexpensedebit,
                    sum(x.credit) OVER (PARTITION BY (x.id = ANY (ARRAY[15, 16])) ORDER BY (x.id = ANY (ARRAY[15, 16]))) AS totexpensecredit,
                    sum(x.debit) OVER (PARTITION BY (x.id = ANY (ARRAY[15, 16])) ORDER BY (x.id = ANY (ARRAY[15, 16]))) AS totexpensedebit,
                    sum(x.credit) OVER (PARTITION BY (x.id = ANY (ARRAY[15, 16])) ORDER BY (x.id = ANY (ARRAY[15, 16]))) + sum(x.debit) OVER (PARTITION BY (x.id = ANY (ARRAY[15, 16])) ORDER BY (x.id = ANY (ARRAY[15, 16]))) AS totexpense
                   FROM ( SELECT aat.id,
                            aat.name,
                            aa.code::text || aa.name::text AS productname,
                            aml.name AS entityname,
                            sum(COALESCE(aml.credit, 0::numeric)) AS credit,
                            sum(COALESCE(aml.debit, 0::numeric)) AS debit
                           FROM account_account_type aat
                             LEFT JOIN account_account aa ON aat.id = aa.user_type_id
                             LEFT JOIN account_move_line aml ON aa.user_type_id = aml.user_type_id
                          WHERE aat.id = ANY (ARRAY[15, 16])
                          GROUP BY aat.id, (aa.code::text || aa.name::text), aml.name
                          ORDER BY aat.id) x
                  ORDER BY (row_number() OVER (ORDER BY x.id))) tb2 ON tb1.incrownum = tb2.exprownum;""")
    
    # @api.model_cr
    # def init(self):
    #     #tools.drop_view_if_exists(self._cr, 'profit_loss')
    #     self._cr.execute(""" select row_number() OVER (ORDER BY incrownum) AS id,incname,totincome,
    # expname,totexpense,
    # grossprofit
    # from profit_loss; """)
    
    # @api.depends('value')
    # def _value_pc(self):
    #     self.value2 = float(self.value) 

    @api.depends('totexpense')
    def _value_pc(self):
        self.grossprofit = float(self.toincome-self.totexpense)



# class profitlossview(models.Model):
#     _name='profit_loss_view'
#     _auto= False

#     id = fields.Integer()
#     incname = fields.Char()
#     totincome = fields.Integer()
#     expname = fields.Char()
#     totexpense = fields.Integer()
#     grossprofit = fields.Integer()

#     @api.model_cr
#     def init(self):
#         tools.drop_view_if_exists(self._cr, 'profit_loss')
#         self._cr.execute(""" select row_number() OVER (ORDER BY incrownum) AS id,incname,totincome,
#     expname,totexpense,
#     grossprofit
#     from profit_loss; """)
#       