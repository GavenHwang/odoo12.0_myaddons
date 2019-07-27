# -*- coding: utf-8 -*-

import xmlrpc.client

info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
url, db, username, password = info['host'], info['database'], info['user'], info['password']
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
uid = common.authenticate(db, username, password, {})

# url = "http://192.168.99.100:8069"
# db = "odoo12"
# username = 'admin'
# password = 'admin'
# uid = 1

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
models.execute_kw(db, uid, password, 'res.partner', 'check_access_rights', ['read'], {'raise_exception': False})
models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True], ['customer', '=', True]]])
models.execute_kw(db, uid, password, 'res.partner', 'search', [[['is_company', '=', True], ['customer', '=', True]]],
                  {'offset': 10, 'limit': 5})
models.execute_kw(db, uid, password, 'res.partner', 'search_count',
                  [[['is_company', '=', True], ['customer', '=', True]]])
ids = models.execute_kw(db, uid, password, 'res.partner', 'search',
                        [[['is_company', '=', True], ['customer', '=', True]]], {'limit': 1})
[record] = models.execute_kw(db, uid, password, 'res.partner', 'read', [ids])
len(record)
models.execute_kw(db, uid, password, 'res.partner', 'read', [ids], {'fields': ['name', 'country_id', 'comment']})
models.execute_kw(db, uid, password, 'res.partner', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
models.execute_kw(db, uid, password, 'res.partner', 'search_read',
                  [[['is_company', '=', True], ['customer', '=', True]]],
                  {'fields': ['name', 'country_id', 'comment'], 'limit': 5})
id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{'name': "New Partner", }])
models.execute_kw(db, uid, password, 'res.partner', 'write', [[id], {'name': "Newer partner"}])
# get record name after having changed it
models.execute_kw(db, uid, password, 'res.partner', 'name_get', [[id]])
models.execute_kw(db, uid, password, 'res.partner', 'unlink', [[id]])
# check if the deleted record is still in the database
models.execute_kw(db, uid, password, 'res.partner', 'search', [[['id', '=', id]]])
models.execute_kw(db, uid, password, 'ir.model', 'create',
                  [{'name': "Custom Model", 'model': "x_custom_model", 'state': 'manual'}])
models.execute_kw(db, uid, password, 'x_custom_model', 'fields_get', [], {'attributes': ['string', 'help', 'type']})
id = models.execute_kw(db, uid, password, 'ir.model', 'create', [{
    'name': "Custom Model",
    'model': "x_custom",
    'state': 'manual',
}])
models.execute_kw(
    db, uid, password,
    'ir.model.fields', 'create', [{
        'model_id': id,
        'name': 'x_name',
        'ttype': 'char',
        'state': 'manual',
        'required': True,
    }])
record_id = models.execute_kw(
    db, uid, password,
    'x_custom', 'create', [{
        'x_name': "test record",
    }])
models.execute_kw(db, uid, password, 'x_custom', 'read', [[record_id]])
