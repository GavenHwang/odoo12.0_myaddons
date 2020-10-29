# -*- coding: utf-8 -*-
import base64
import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

GENDER = [
    ('male', u'男'),
    ('female', u'女'),
    ('other', u'其他')
]

MARITAL = [
    ('single', u'单身'),
    ('married', '已婚'),
    ('cohabitant', '合法同居'),
    ('widower', '丧偶'),
    ('divorced', '离婚')
]


class Employee(models.Model):
    _name = "ml.employee"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _table = "ml_employee"
    _description = '''
        员工信息
    '''

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return base64.b64encode(open(image_path, 'rb').read())

    name = fields.Char(string=u'姓名')

    # image attachment=True 是否以附件的形式存储，设为True时，将会存储到ir.attachment中
    # image = fields.Binary(string=u"照片", default=_default_image, attachment=True, help=u"上传员工照片，<1024x1024px")
    # image_medium = fields.Binary(string=u"中尺寸照片", attachment=True, help="128x128px照片")
    # image_small = fields.Binary(string=u"小尺寸照片", attachment=True, help="64x64px照片")

    image = fields.Image("照片", default=_default_image)
    image_big = fields.Image("Image 512", related='image', max_width=512, max_height=512, store=True, readonly=False)
    image_medium = fields.Image("Image 256", related='image', max_width=256, max_height=256, store=False, readonly=False)
    image_small = fields.Image("Image 128", related='image', max_width=128, max_height=128, store=False, readonly=False)

    company_id = fields.Many2one('res.company', string=u'公司')

    gender = fields.Selection(GENDER, string=u'性别')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')
    marital = fields.Selection(MARITAL, string=u'婚姻状况', default='single')

    # work
    currency_id = fields.Many2one(related='company_id.currency_id', string='公司币种', readonly=True, store=True,
                                          help='表示货币数量的工具字段')
    salary = fields.Monetary("薪资", currency_field="currency_id")
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    leader_id = fields.Many2one('ml.employee', string=u'所属上级')
    subordinate_ids = fields.One2many('ml.employee', 'leader_id', string=u'下属')
    # age = fields.Integer(states={'draft': [('readonly', '=', False), ('invisible', '=', False), ('required', '=',
    # True)]})
    note = fields.Text(string=u'备注信息')

    color = fields.Integer(u'颜色')
    priority = fields.Selection([('0', 'Low'), ('1', 'Normal'), ('2', 'High')], 'Priority', default='1')
    kanban_state = fields.Selection([('normal', 'In Progress'), ('blocked', 'Blocked'), ('done', 'Ready for next stage')],
                                    'Kanban State', default='normal')

    @api.model
    def default_get(self, fields_list):
        defaults = super(Employee, self).default_get(fields_list)
        defaults['birthday'] = fields.Date.today()
        defaults['company_id'] = self.env.user.company_id.id
        defaults['country_id'] = self.country_id.search([('code', '=', 'CN')], limit=1).id
        return defaults

    @api.model
    def create(self, values):
        # tools.image_resize_images(values)
        return super(Employee, self).create(values)

    def write(self, values):
        # tools.image_resize_images(values)
        return super(Employee, self).write(values)

    # constrains只能在界面层面对字段进行约束，对API调用不起效果
    @api.constrains('company_id')
    def _constrains_company_id(self):
        self.ensure_one()
        if not self.company_id:
            raise ValidationError(u'公司不能为空！')
