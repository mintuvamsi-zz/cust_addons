# -*- coding: utf-8 -*-
from odoo import http

class Sea(http.Controller):
    @http.route('/sea/sea/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/sea/sea/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('sea.listing', {
            'root': '/sea/sea',
            'objects': http.request.env['sea.sea'].search([]),
        })

    @http.route('/sea/sea/objects/<model("sea.sea"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('sea.object', {
            'object': obj
        })