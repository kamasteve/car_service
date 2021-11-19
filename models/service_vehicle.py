from odoo import models, fields

class ServiceVehicle(models.Model):
    _name = "service.vehicle"
    _description = "Vehicle Available for Services"

    car_model = fields.Char("Model", required=True)
    total_seat = fields.Integer("Seat Availability", required=True)
    image = fields.Binary()
    
