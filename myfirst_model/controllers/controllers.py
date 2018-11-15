# -*- coding: utf-8 -*-
from odoo import http

class MyfirstModel(http.Controller):
    @http.route('/home', auth='public')
    def index(self, **kw):
        return "Hello, world"


    @http.route('/example', type='http',website=True)
    def render_example_page(self,**kw):
        customer = http.request.env['customer'].sudo().search([])
        return http.request.render('myfirst_model.example_page',{'customers':customer})


