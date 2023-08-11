# -*- coding: utf-8 -*-

{
    'name': 'UAnalyst Company Assets',
    'version': '1.2',
    'category': 'UAnalyst Company Assets',
    'summary': 'UAnalyst Company Assets',
    'description': """
    UAnalyst Company Assets.
    """,
    'author': "Mohamed Nagy",
    'sequence': '-100',
    'depends': ['base',
                'mail',
                'product',
                'hr',
                'account',
                'stock',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/company_assets_views.xml',
        'views/hr_employee_views.xml',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'report/report.xml',
        'report/template_report.xml',
    ],
    'demo': [],
    'application': True,
    'installable': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
