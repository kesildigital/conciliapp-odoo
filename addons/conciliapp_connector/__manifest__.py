{
    "name": "Conciliapp Connector",
    "version": "17.0.1.0.0",
    "summary": "Integración de conciliación de pagos con Conciliapp",
    "description": """
    Integra Odoo Community con Conciliapp para validación/conciliación de pagos.
    """,
    "author": "Kesil Digital",
    "website": "https://kesildigital.com",
    "category": "Tools",
    "license": "GPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/conciliapp_bank_views.xml",
        "views/conciliapp_payment_check_views.xml",
        "views/conciliapp_menu.xml",
    ],
    "installable": True,
    "application": True,
}
