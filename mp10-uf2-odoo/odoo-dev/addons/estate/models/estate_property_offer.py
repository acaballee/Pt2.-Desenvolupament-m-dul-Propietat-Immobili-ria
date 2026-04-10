from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Preu")
    status = fields.Selection(
        string="Estat",
        selection=[
            ("accepted", "Acceptada"),
            ("refused", "Refusada"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Comprador", required=True)
    property_id = fields.Many2one("estate.property", string="Propietat", required=True)
