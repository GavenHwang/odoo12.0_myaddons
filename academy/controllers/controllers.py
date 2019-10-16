# -*- coding: utf-8 -*-
from odoo import http


class Academy(http.Controller):
    # 例1：Hello, World!
    @http.route('/academy/example_01/', auth='public')
    def route_example_01(self, **kw):
        return "Hello, world!"

    # 例2：使用模板
    @http.route('/academy/example_02/', auth='public')
    def route_example_02(self, **kw):
        teachers_obj = http.request.env['academy.teachers']
        return http.request.render('academy.template_01', {
            'teachers': teachers_obj.search([]),
        })

    # 例3：嵌套website
    @http.route('/academy/example_03/', auth='public', website=True)
    def route_example_03(self, **kw):
        teachers_obj = http.request.env['academy.teachers']
        return http.request.render('academy.template_02', {
            'teachers': teachers_obj.search([]),
        })

    # 例4：动态路由（字符）
    # @http.route('/academy/<name>/', auth='public', website=True)
    # def route_example_04(self, name):
    #     return '<h1>{}</h1>'.format(name)

    # 例5：动态路由（数字）
    # @http.route('/academy/<int:id>/', auth='public', website=True)
    # def route_example_05(self, id):
    #     return '<h1>{} ({})</h1>'.format(id, type(id).__name__)

    @http.route('/academy/<model("academy.teachers"):teacher>/', auth='public', website=True)
    def route_example_06(self, teacher):
        return http.request.render('academy.biography', {
            'person': teacher
        })
