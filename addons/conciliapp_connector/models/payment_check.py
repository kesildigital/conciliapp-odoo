from odoo import api, fields, models
import json
import logging, os

_logger = logging.getLogger(__name__)
_logger.warning("CONCILIAPP DEBUG: loading payment_check.py from %s", os.path.abspath(__file__))

class ConciliappPaymentCheck(models.Model):
    _name = "conciliapp.payment.check"
    _description = "Conciliapp - Validación de Pagos"
    _order = "create_date desc"

    name = fields.Char(string="Referencia", required=True)
    amount = fields.Monetary(string="Monto", currency_field="currency_id")
    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        default=lambda self: self.env.company.currency_id.id,
        required=True,
    )
    payment_date = fields.Date(string="Fecha")
    customer_name = fields.Char(string="Cliente (opcional)")

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("checking", "Validando"),
            ("found", "Encontrado"),
            ("not_found", "No encontrado"),
            ("mismatch", "No coincide"),
            ("error", "Error"),
        ],
        default="draft",
        string="Estado",
        tracking=True,
        required=True,
    )

    result_message = fields.Char(string="Resultado")
    response_json = fields.Text(string="Respuesta (raw)")

    def action_check(self):
        """
        MVP: por ahora NO llama API real.
        Solo simula respuesta para que el flujo UI quede listo.
        En el siguiente paso conectamos tu endpoint real.
        """
        for rec in self:
            rec.state = "checking"

            # Simulación simple: si la referencia termina en "1" => found
            if (rec.name or "").strip().endswith("1"):
                payload = {"status": "found", "reference": rec.name, "amount": float(rec.amount or 0)}
                rec.state = "found"
                rec.result_message = "Pago encontrado en Conciliapp (simulado)"
                rec.response_json = json.dumps(payload, ensure_ascii=False)
            else:
                payload = {"status": "not_found", "reference": rec.name}
                rec.state = "not_found"
                rec.result_message = "Pago no encontrado en Conciliapp (simulado)"
                rec.response_json = json.dumps(payload, ensure_ascii=False)
