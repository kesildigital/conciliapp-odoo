from odoo import fields, models

class AccountPayment(models.Model):
    _inherit = "account.payment"

    conciliapp_sync_state = fields.Selection(
        [
            ("not_sent", "No enviado"),
            ("sent", "Enviado"),
            ("matched", "Conciliado"),
            ("error", "Error"),
        ],
        string="Conciliapp Estado",
        default="not_sent",
        copy=False,
        tracking=True,
    )

    conciliapp_external_id = fields.Char(
        string="Conciliapp ID",
        copy=False,
        index=True,
        tracking=True,
    )

    conciliapp_last_error = fields.Text(
        string="Conciliapp Último error",
        copy=False,
    )
