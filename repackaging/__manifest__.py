{
    'name':
    'Repackaging',
    'version':
    '1.2',
    'category':
    'inventory',
    'summary':
    'Repackaging for stocks',
    'email':
    'aungmyoswe.dev@gmail.com',
    'author':
    'Aung Myo Swe',
    'company':
    'Asia Matrix Co., Ltd',
    'description':
    """
This module is the repackaging for the stocks in the inventory operation.
    """,
    'depends': ['stock', 'stock_account'],
    'data': [
        'data/repackaging_sequence_data.xml',
        'security/ir.model.access.csv',
        'report/repackaging_report_template.xml',
        'report/repackaging_report.xml',
        'views/stock_repackaging_data.xml',
        'views/product_view.xml',
        'views/stock_location_view.xml',
    ],
    'installable':
    True,
    'auto_install':
    False,
}
