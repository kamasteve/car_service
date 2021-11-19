from odoo import models, fields

class ServiceType(models.Model):
    _name = 'service.type'
    _description = 'Hourly or Kilometer Based'

    name = fields.Char(required=True)
