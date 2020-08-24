# -*- coding: utf-8 -*-
{
    'name': "Logs Notes Form",

    'summary': """
        Log for Partner,Sale,Purchase,Invoice and Stock""",

    'description': """
        Logs for Partner form,Sale form,Purchase form,Invoice form and Stock
    """,

    'author': "THA",
    'website': "http://www.asiamatrixsoftware.com",
    'category': 'Extra',
    'version': '0.4.0',
    'depends': ['stock','mail','purchase','point_of_sale'],
    'data': [
        # 'views/product_template_view_form.xml',
         'views/pos_session_log.xml',
         # 'views/product_template_form.xml',
    ],
}