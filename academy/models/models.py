# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Teachers(models.Model):
    _name = 'academy.teachers'

    name = fields.Char()
    biography = fields.Html()
    course_ids = fields.One2many('academy.courses', 'teacher_id', string="Courses")
    product_course_ids = fields.One2many('product.template', 'teacher_id', string="Product Courses")


class Courses(models.Model):
    _name = 'academy.courses'
    _inherit = 'mail.thread'

    name = fields.Char()
    teacher_id = fields.Many2one('academy.teachers', string="Teacher")


class Products(models.Model):
    _inherit = 'product.template'

    teacher_id = fields.Many2one('academy.teachers', string="Teacher")
