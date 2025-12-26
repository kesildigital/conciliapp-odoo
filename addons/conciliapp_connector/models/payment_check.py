import json
import requests

from odoo import models, fields, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class ConciliappPaymentCheck(models.Model):
    _name = "conciliapp.payment.check"
    _description = "Conciliapp Payment Check"
    _order = "create_date desc"

    reference = fields.Char(string="Referencia", required=True)
    amount = fields.Float(string="Monto", required=True)

    bank_id = fields.Many2one(
        "conciliapp.bank",
        string="Banco destino",
        required=True,
        domain=[("active", "=", True)],
    )

    status = fields.Selection(
        [
            ("pending", "Pendiente"),
            ("reconciled", "Conciliado"),
            ("failed", "Fallido"),
        ],
        default="pending",
        string="Estado",
        required=True,
    )

    api_message = fields.Char(string="Mensaje API")
    api_payload = fields.Text(string="Respuesta API (JSON)")
    reconciled_at = fields.Datetime(string="Fecha conciliación", readonly=True)

    def action_validate_payment(self):
        self.ensure_one()

        # Config (System Parameters)
        base_url = (
            self.env["ir.config_parameter"].sudo().get_param("conciliapp.api_base_url") or ""
        ).strip()

        if not base_url:
            raise UserError(
                _("Falta configurar 'conciliapp.api_base_url' en Settings > Technical > System Parameters.")
            )

        payload = {
            "reference": self.reference,
            "amount": self.amount,
            "bank_code": self.bank_id.code,
        }

        try:
            url = f"{base_url.rstrip('/')}/payments/validate"
            _logger.warning("Conciliapp validate URL => %s", url)   
            resp = requests.post(
                f"{base_url.rstrip('/')}/payments/validate",
                json=payload,
                timeout=20,
            )
        except Exception as e:
            self.status = "failed"
            raise UserError(_("No se pudo conectar con Conciliapp: %s") % str(e))

        # Parse JSON
        try:
            data = resp.json()
        except Exception:
            data = {"ok": False, "message": "Respuesta no-JSON", "raw": resp.text}

        self.api_payload = json.dumps(data, ensure_ascii=False, indent=2)
        self.api_message = data.get("message") or ""

        # Errores HTTP
        if resp.status_code >= 400:
            self.status = "failed"
            raise UserError(self.api_message or _("Error al validar el pago."))

        # Regla de éxito (asumimos que tu API responde { ok: true/false, message: ... })
        if not data.get("ok"):
            self.status = "failed"
            raise UserError(self.api_message or _("Pago no conciliado."))

        # OK
        self.status = "reconciled"
        self.reconciled_at = fields.Datetime.now()

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Conciliado"),
                "message": self.api_message or _("Pago conciliado correctamente."),
                "sticky": False,
                "type": "success",
            },
        }
