from odoo import models, fields

class ConciliappBank(models.Model):
    _name = "conciliapp.bank"
    _description = "Conciliapp Bank"
    _order = "name asc"

    name = fields.Char(string="Banco", required=True)
    code = fields.Char(string="Código", required=True)
    active = fields.Boolean(default=True)
