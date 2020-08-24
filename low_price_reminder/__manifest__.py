# -*- coding: utf-8 -*-
{
    'name': "Product Sale Price Alert",
    'summary': """
Alert email product lists that sale price is lower than cost price.
""",
    'description': """
This module will send product list email that the sale price lower then the cost price using schedule action.
    """,
    "version": "12.0.1",
    "category": "Warehouse",
    'author': "Matrix",
    'license': 'Other proprietary',
    "depends": [
        'product','stock','base',
    ],
    "data": [
        'data/cron.xml',
        'report/report_view.xml',
        'data/email_template.xml',
        'views/res_company_view.xml',
    ],
    'price': 100,
    'sequence': 1,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    "application": True,
    'installable': True,
}
