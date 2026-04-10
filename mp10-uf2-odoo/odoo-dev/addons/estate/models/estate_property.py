from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(string="Nom", required=True)
    description = fields.Text(string="Descripció")
    postcode = fields.Char(string="Codi Postal", required=True, default="00000")
    date_availability = fields.Date(string="Data Disponibilitat", default=lambda self: fields.Date.today() + relativedelta(months=1), copy=False)
    expected_price = fields.Float(string="Preu Esperat", required=True)
    selling_price = fields.Float(string="Preu de Venda Final", readonly=True, copy=False)
    
    best_offer = fields.Float(string="Millor Oferta", compute="_compute_best_offer", readonly=True, store=False)

    state = fields.Selection(
        string="Estat",
        selection=[
            ("new", "Nova"),
            ("offer_received", "Oferta Rebuda"),
            ("offer_accepted", "Oferta Acceptada"),
            ("sold", "Venuda"),
            ("canceled", "Cancel·lada"),
        ],
        default="new",
    )

    bedrooms = fields.Integer(string="Nombre d'habitacions", required=True, default=0)
    property_type_id = fields.Many2one("estate.property.type", string="Tipus")
    tag_ids = fields.Many2many("estate.property.tag", string="Etiquetes")

    elevator = fields.Boolean(string="Ascensor", default=False)
    parking = fields.Boolean(string="Parking", default=False)
    renovated = fields.Boolean(string="Renovat", default=False)
    bathrooms = fields.Integer(string="Banys")
    surface = fields.Integer(string="Superfície", required=True, default=0)

    avgPrice = fields.Float(string="Preu per m2", compute="_compute_avg_price", readonly=True, store=False)

    construction_year = fields.Integer(string="Any de construcció")
    energy_certificate = fields.Selection(
        string="Certificat energètic",
        selection=[
            ("A", "A"), ("B", "B"), ("C", "C"), 
            ("D", "D"), ("E", "E"), ("F", "F"), ("G", "G")
        ]
    )

    active = fields.Boolean(string="Actiu", default=True)
    
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Ofertes")

    buyer_id = fields.Many2one("res.partner", string="Comprador", compute="_compute_buyer", readonly=True, store=False)
    salesperson_id = fields.Many2one("res.users", string="Comercial", default=lambda self: self.env.user)

    @api.depends('expected_price', 'surface')
    def _compute_avg_price(self):
        for record in self:
            if record.surface > 0:
                record.avgPrice = record.expected_price / record.surface
            else:
                record.avgPrice = 0.0

    @api.depends('offer_ids.price', 'offer_ids.status')
    def _compute_best_offer(self):
        for record in self:
            valid_offers = record.offer_ids.filtered(lambda o: o.status != 'refused')
            record.best_offer = max(valid_offers.mapped('price')) if valid_offers else 0.0

    @api.depends('offer_ids.status', 'offer_ids.partner_id')
    def _compute_buyer(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            record.buyer_id = accepted_offer[0].partner_id if accepted_offer else False

    def cancellarPropietat(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'canceled'
            else:
                raise UserError('No es pot cancel·lar una propietat venuda')
        return True
