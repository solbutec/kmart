{
    "name": "Stock Picking BackDate",
    "summary": "Change stock picking effective date by schedule date",
    "description": "Stock Picking with backdate for Reciept, Deliver and Transfer",
    "version": "12.0.6",
    "author": "Matrix",
    "category": "Warehouse Management",
    "depends": [
        "stock", "account", "purchase",
    ],
    "data": [
        "views/stock_account_views.xml",
        "views/stock_picking_views.xml",
        "views/purchase_order_view.xml"

    ],
    'price': 120,
    'sequence': 1,
    'license': 'OPL-1',
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
