{
    'name': 'Purchase Discount Journal',
    'version': '12.5.0',
    'category': 'Sales Management',
    'summary': "Sale/Purchase Discount on total in Invoice with Discount Fixed and Journal Entry",
    'author': 'Kyaw Zin Oo',
    'website': '',
    'email': 'kyawzinoo@asiamatrixsoftware.com',
    'description': """

Sale/Purchase Discount for Total Amount and Journal Entry
==================================================
Module to manage discount on total amount in Sale/Purchase.
        as an specific amount  and journal.
""",
    'depends': ['account','purchase','update_cost_setting'],
    'data': [   'views/account_invoice_view.xml',
                'views/purchase_invoice_view.xml',
                'views/res_config_view.xml',
                'report/purchase_order_report.xml',
                'report/vendor_bill_report.xml',
             ],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
}
