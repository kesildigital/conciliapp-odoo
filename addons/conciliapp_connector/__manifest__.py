{
    "name": "Conciliapp Connector",
    "version": "17.0.1.0.0",
    "summary": "Integración de conciliación de pagos con Conciliapp",
    "description": """
        Integra Odoo Community con Conciliapp para conciliación de pagos.
    """,
    "author": "Kesil Digital",
    "website": "https://kesildigital.com",
    "category": "Accounting",
    "license": "LGPL-3",
    "depends": ["base"],  # por ahora sin account
    "data": [
        "security/ir.model.access.csv",
        "views/conciliapp_menu.xml",
        "views/payment_check_views.xml",
    ],
    "installable": True,
    "application": True,
}
