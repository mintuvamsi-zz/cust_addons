# -*- coding: utf-8 -*-
from odoo import http

class profitlossqweb(http.Controller):

    @http.route('/pl/home', auth='public')
    def home(self, **kw):
        return 'qweb working fine.....'

    @http.route('/profit/loss', type='http', auth='public', website='True')
    def profitloss_data(self, **kw):
        data = http.request.env['profit.loss'].sudo().search([])
        return http.request.render('profit_loss.pl_page',{'pldata':data})

# class ProfitLoss(http.Controller):
#     @http.route('/profit_loss/profit_loss/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/profit_loss/profit_loss/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('profit_loss.listing', {
#             'root': '/profit_loss/profit_loss',
#             'objects': http.request.env['profit_loss.profit_loss'].search([]),
#         })

#     @http.route('/profit_loss/profit_loss/objects/<model("profit_loss.profit_loss"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('profit_loss.object', {
#             'object': obj
#         })
#########################################################

