# -*- coding: utf-8 -*-
{
    'name': 'Employee',
    'version': '12.0.1.0',
    'summary': '对员工的基本信息，部门和职位进行管理',
    'description': '''
        员工管理模块
    ''',
    'author': 'misterling',
    'sequence': 15,
    'category': 'Uncategorized',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'pre_init_hook': '',
    # 'post_init_hook': '',
    # 'uninstall_hook': '',
}

#           name: 模块的标题
#        version: 版本号
#        summary: 模块的子标题
#    description: 模块的描述性文字
#         author: 作者
#       sequence: 模块在apps中的排列的序号，影响展示顺序。
#       category: 模块的分类，在设置->用户&公司->群组中"应用"字段中可以看到
#        license: 代表着你的开源协议。
#        depends: 依赖的模块，在安装当前模块时，如果依赖模块未安装，将会自动安装；升级依赖的模块时，所有依赖它的模块也将会跟着升级。
#           data: 加载XML文件。
#           demo: 加载demo文件。
#           qweb: 加载qweb template文件。
#    installable: 是否可以安装。
#    application: 是否是应用，在应用列表中，被应用筛选隔离，好的开发习惯应该谨慎考虑是否是应用。
#   auto_install: 是否自动安装，设为True的应用将在数据库初始化时自动安装
#  pre_init_hook: 顾名思义，模块安装前的钩子，指定方法名即可
# post_init_hook: 模块安装完成后的钩子
# uninstall_hook: 模块卸载时的钩子
