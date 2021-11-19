from odoo import models, fields

class LuxuryService(models.Model):
    _name = 'luxury.service'
    _description = 'All Luxury Car Services Available'

    name = fields.Char(string='Service Name', required=True)
    service_type = fields.Many2one(comodel_name='service.type', ondelete='cascade')
    description = fields.Html()
    vehicles = fields.Many2many(comodel_name='service.vehicle')
    rate = fields.Float()


