from dateutil.relativedelta import relativedelta
from odoo import fields, models

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Model per estate_property'

    name = fields.Char('Propietat Inmobiliaria', required=True)
    date_availability = fields.Date('Data Disponibilitat', default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False)
    bedrooms = fields.Integer('Habitacions', readonly=True)
    active = fields.Boolean('Active', default=True)