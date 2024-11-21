# -*- coding: utf-8 -*-
{
    'name': 'Somko Environment',
    'version': '17.0.0.0.1',
    'author': 'Somko BV',
    'category': 'Settings',
    'description': """
    Somko environment Module
    """,
    'website': 'https://www.somko.be',
    'images': [],
    'depends': [
        'base',
        'mail'
    ],
    'data': [
        "data/ir.config_parameter.csv",
        "data/ir_cron_email_tpl.xml",

        "views/ir_cron.xml",

        "data/cron.xml",
    ],
    'qweb': [],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': True,
}
