# -*- coding: utf-8 -*-
from odoo import http

# class Ideas(http.Controller):
#     @http.route('/ideas/ideas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ideas/ideas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ideas.listing', {
#             'root': '/ideas/ideas',
#             'objects': http.request.env['ideas.ideas'].search([]),
#         })

#     @http.route('/ideas/ideas/objects/<model("ideas.ideas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ideas.object', {
#             'object': obj
#         })