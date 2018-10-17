# -*- coding: utf-8 -*-
from odoo import http

# class Visitors(http.Controller):
#     @http.route('/visitors/visitors/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/visitors/visitors/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('visitors.listing', {
#             'root': '/visitors/visitors',
#             'objects': http.request.env['visitors.visitors'].search([]),
#         })

#     @http.route('/visitors/visitors/objects/<model("visitors.visitors"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('visitors.object', {
#             'object': obj
#         })