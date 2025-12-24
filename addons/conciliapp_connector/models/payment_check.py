from odoo import models, fields

class ConciliappPaymentCheck(models.Model):
    _name = "conciliapp.payment.check"
    _description = "Conciliapp Payment Check"

    name = fields.Char(string="Referencia", required=True)
    amount = fields.Float(string="Monto")
    status = fields.Selection(
        [
            ("pending", "Pendiente"),
            ("validated", "Validado"),
            ("not_found", "No encontrado"),
        ],
        default="pending",
        string="Estado",
    )
