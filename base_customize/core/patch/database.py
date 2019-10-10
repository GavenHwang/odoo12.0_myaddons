# -*- coding: utf-8 -*-
import os
import jinja2
import odoo
from odoo import http
from odoo.addons.web import controllers

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

# 更改数据库页面，env环境更改为'my_addons/base_customize/template'
path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'template'))
loader = jinja2.FileSystemLoader(path)
env = jinja2.Environment(loader=loader, autoescape=True)

DBNAME_PATTERN = '^[a-zA-Z0-9][a-zA-Z0-9_.-]+$'

db_monodb = http.db_monodb


def _render_template(self, **d):
    d.setdefault('manage', True)
    d['insecure'] = odoo.tools.config.verify_admin_password('admin')
    d['list_db'] = odoo.tools.config['list_db']
    d['langs'] = odoo.service.db.exp_list_lang()
    d['countries'] = odoo.service.db.exp_list_countries()
    d['pattern'] = DBNAME_PATTERN
    # databases list
    d['databases'] = []
    try:
        d['databases'] = http.db_list()
        d['incompatible_databases'] = odoo.service.db.list_db_incompatible(d['databases'])
    except odoo.exceptions.AccessDenied:
        monodb = db_monodb()
        if monodb:
            d['databases'] = [monodb]
    return env.get_template("database_manager.html").render(d)


def patch_database():
    controllers.main.Database._render_template = _render_template
