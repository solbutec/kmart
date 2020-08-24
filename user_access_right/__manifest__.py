# -*- coding: utf-8 -*-
{
    'name': "Users Access Right",
    'website': "www.asiamatrixsoftware.com",
    'category': 'base',
    'summary': """User Access Right For Account Finance""",
    'version': '12.2.0',
    'description': """
        This Module Add user access right for Finance User that is same Advisor.
    """,
    'depends': [
        'base',
        'stock',
        'purchase',
        'account',
        'point_of_sale',
        'pos_product_margin',
    ],
    'data': [
        'security/inventory_access_views.xml',
        'security/purchase_access_views.xml',
        'security/pos_access_views.xml',
        'security/account_access_views.xml',
        'views/purchase_views.xml',
        'views/stock_views.xml',
        'views/pos_views.xml',
        'views/account_views.xml',
    ],
    'images': ['static/description/icon.png'],
}
