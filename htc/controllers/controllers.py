# -*- coding: utf-8 -*-
from odoo import http

# class Htc(http.Controller):
#     @http.route('/htc/htc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/htc/htc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('htc.listing', {
#             'root': '/htc/htc',
#             'objects': http.request.env['htc.htc'].search([]),
#         })

#     @http.route('/htc/htc/objects/<model("htc.htc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('htc.object', {
#             'object': obj
#         })