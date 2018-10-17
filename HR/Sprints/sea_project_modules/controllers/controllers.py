# -*- coding: utf-8 -*-
# Part of Sailotech. See LICENSE file for full copyright and licensing details.
from odoo import http

# class ProjectModules(http.Controller):
#     @http.route('/project_modules/project_modules/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_modules/project_modules/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_modules.listing', {
#             'root': '/project_modules/project_modules',
#             'objects': http.request.env['project_modules.project_modules'].search([]),
#         })

#     @http.route('/project_modules/project_modules/objects/<model("project_modules.project_modules"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_modules.object', {
#             'object': obj
#         })