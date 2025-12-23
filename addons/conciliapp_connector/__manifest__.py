{
    "name": "Conciliapp Connector",
    "version": "17.0.1.0.0",
    "category": "Accounting",
    "summary": "Conciliación de pagos contra Conciliapp",
    "depends": ["base", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/account_payment_views.xml",
        "views/conciliapp_reconcile_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}