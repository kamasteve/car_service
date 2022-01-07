from odoo import models, fields, api


class ProductsChange(models.Model):
    _inherit = "product.template"
    _description = 'Add alternative products to product template'
    alternative_products = fields.Many2many('product.product', 'alternative_id')
    booking_status = fields.Selection([
    ('Booked', 'Booked'),
    ('Available', 'Available'),
    ('Not Available', 'Not Available')], default='Available',string='Booking Status')


class AlternativeProduct(models.Model):
    _name = "alternative.car"
    _description = "Model for storing alternative cars for suggesting to user if the preferred car is not visible"
    car = fields.Many2one("product.template", "Alternative product")
    description = fields.Char('Description')
