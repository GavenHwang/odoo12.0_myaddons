# -*- coding: utf-8 -*-
import pytz
from odoo import models, fields, api, _
from odoo.tools import float_round
from odoo.exceptions import ValidationError
import base64
import xlsxwriter
import datetime
from io import BytesIO


# 员工信息表
class MailEmployeeInformationReport(models.TransientModel):
    _name = 'ml.employee.information.report'
    _description = 'Mail Employee Information Report'
    _report_name = '员工信息表'

    # 二进制文件用于打印
    file = fields.Binary('文件')
    # 公司
    company_id = fields.Many2one('res.company', '公司', default=lambda self: self.env.user.company_id, required=True)
    # 报表类型
    report_type = fields.Selection(selection=[("excel", "EXCEL")], string='报表类型', required=True, default='excel')

    # 获取报表数据
    def get_excel_data(self):
        company_id = self.company_id.id
        sql = """
            select name, gender, birthday, marital, salary, mobile_phone, address from ml_employee
        """
        self.env.cr.execute(sql)
        result = self.env.cr.fetchall()
        return result

    def open_table(self):
        context = {}
        date = datetime.datetime.strftime(datetime.datetime.now(tz=pytz.timezone("Asia/Shanghai")),
                                          "%Y{n}%m{y}%d{d}").format(n='年', y='月', d='日')
        context['data'] = {
            'company_name': self.company_id.name,
            'date': date,
            'lines': self.get_excel_data(),
        }
        return {
            'type': 'ir.actions.client',
            'tag': 'employee_information_report_tag',
            'context': context,
            'name': '员工信息表'
        }

    def print_excel(self):
        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet(self._report_name)

        # 获得报表样式方法
        def get_xlswriter_style(workbook, font_size=14, bold=False, border=1, align='center', valign='vcenter',
                                fg_color='#ffffff', num_format=0, text_wrap=False):
            style = workbook.add_format({
                'font_size': font_size,  # 字体大小，默认10
                'bold': bold,  # 字体加粗，默认不加粗
                'border': border,  # 单元格边框宽度，默认1
                'align': align,  # 左右对齐方式，默认居中
                'valign': valign,  # 上下对齐方式，默认居中
                'fg_color': fg_color,  # 背景色，默认白色
                'num_format': num_format,  # 数字、日期格式化  '￥#,##0.00'、'yyyy-m-d h:mm:ss'
            })
            # '\n'自动换行
            if text_wrap:
                style.set_text_wrap()
            return style

        # 写入报表方法
        def write_excel(worksheet, datas, styles, row_begain=0, col_begain=0, nomal_direction=True):
            """
                worksheet: worksheet对象
                datas:  打印数据集 eg:[('小明', 12, '男', '2018-01-12'), ('小红', 10, '女', '2010-01-12'3), ...]
                row_begain: 打印起始行
                col_begain: 打印起始列
                styles: 样式列表, 对应每一列的样式 eg: [text_style, num_style, text_style, date_style]
                nomal_direction：True,从左往右，从上往下的顺序; False 从上往下，从左往右的顺序
            """
            row, col = row_begain, col_begain
            if nomal_direction:
                for row_data in datas:
                    for i in range(len(row_data)):
                        worksheet.write(row, col, row_data[i], styles[i] or text_style)
                        col += 1
                    col = col_begain
                    row += 1
            else:
                for row_data in datas:
                    for i in range(len(row_data)):
                        worksheet.write(row, col, row_data[i], styles[col - col_begain])
                        row += 1
                    row = row_begain
                    col += 1
            return True

        # 设置列宽方法
        def set_excel_col_width(worksheet, col_width, col_begain=0):
            """
                设置excel列宽
                col_width：宽度列表
                col_begain：起始列
            """
            for i in range(len(col_width)):
                worksheet.set_column(i + col_begain, i + col_begain, col_width[i])

        # 标题样式
        title_style = get_xlswriter_style(workbook, font_size=24, bold=True)

        # 子标题样式
        head_style_l = get_xlswriter_style(workbook, font_size=14, bold=True, align='left')
        head_style_r = get_xlswriter_style(workbook, font_size=14, bold=True, align='right')
        head_style_c = get_xlswriter_style(workbook, font_size=14, bold=True, fg_color='#90c3e3')
        # 文本样式
        text_style = get_xlswriter_style(workbook, align='left')
        # 数字样式
        num_style = get_xlswriter_style(workbook, align='right', num_format='#,##0.00')
        # 日期样式
        date_style = get_xlswriter_style(workbook, align='left', num_format='yyyy-m-d')

        # 子标题内容列表
        sub_title_x3 = ['姓名', '性别', '生日', '婚姻', '薪资', '电话', '地址']

        # 打印标题
        row = 0
        col = 0
        width = len(sub_title_x3)
        worksheet.merge_range(row, col, row, width - 1, self._report_name, title_style)

        # 打印查看时间和制单人
        row += 1
        worksheet.merge_range(row, col, row, width // 2, '截止时间：' + str(fields.Date.today()), head_style_l)
        worksheet.merge_range(row, width // 2 + 1, row, width - 1, '制单人：' + self.env.user.name, head_style_r)

        # 打印公司和打印日期
        row += 1
        worksheet.merge_range(row, col, row, width // 2, '公司：' + self.company_id.name, head_style_l)
        worksheet.merge_range(row, width // 2 + 1, row, width - 1, '打印日期：' + str(fields.Datetime.now()), head_style_r)

        # 打印横向子标题
        row += 1
        head_styles_x = [head_style_c] * 7  # 横向标题样式
        write_excel(worksheet, [sub_title_x3], head_styles_x, row, col)

        # 获取报表数据
        datas = self.get_excel_data()

        # 打印报表数据
        row += 1
        col_line_styles = [text_style, text_style, date_style, text_style, num_style, text_style, text_style] # 报表数据样式列表
        write_excel(worksheet, datas, col_line_styles, row, col)

        # 冻结行和列
        worksheet.freeze_panes(4, 0)
        # 设置列宽
        set_excel_col_width(worksheet, [24, 32, 32, 32, 32, 32, 32])
        # 在上一行和左列上分割窗格
        # worksheet.split_panes(45, 5)
        # 默认筛选列
        # worksheet.autofilter('A3:O3')

        workbook.close()
        self.write({'file': base64.b64encode(buffer.getvalue())})
        value = {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': '/web/content?model=%s&id=%s&field=file&download=true&filename=%s.xlsx' % (self._name, self.id,
                                                                                              self._report_name),
        }
        return value

    @api.model
    def jump_test(self, params):
        tree_view_id = self.env.ref('hrp_account_gl.hrp_account_gl_account_move_line_tree')
        return {
            'name': '跳转测试',
            'type': 'ir.actions.act_window',
            'view_type': 'tree',
            'view_mode': 'tree',
            'views': [[tree_view_id.id, 'list']],
            'view_id': tree_view_id.id,
            'domain': [('id', 'in', [1, 2])],
            'res_model': 'ml.employee',
            'target': 'current',
            'context': self.env.context.copy()
        }