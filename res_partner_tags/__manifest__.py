# -*- coding: utf-8 -*-
{
    'name': "Res Partner Tags",

    'summary': """Unhide create and edit in tags field in partner form""",

    'description': """
       * Unhide create and edit in tags field in partner form and add tag menu in
       account configuration.
    """,

    'website': "http://www.asiamatrixsoftware.com",
    'category': 'Sale and Purchase',
    'version': '12.0.2',
    'depends': ['base','account'],
    'data': [
        'views/res_partner_tags.xml',
    ],
}