# _*_ Character coding UTF-8 _*_
from odoo import api,models,fields


class CarBookingAddress(models.Model):
    _name='car.booking.address'
    _description=' Booking Address with latlong'

    address_type=fields.Selection(
            selection=[
                ('origin', 'Origin'),
                ('destination', 'Destination'),
                ('drop', 'Drop'),
                ]
            )

    # address fields
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict', domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    booking_latitude = fields.Float(string='Geo Latitude', digits=(16, 5))
    booking_longitude = fields.Float(string='Geo Longitude', digits=(16, 5))



class CarBooking(models.Model):
    _name = 'car.booking'
    _description = 'Car booking Order'

    user = fields.Many2one('res.users', ondelete='cascade')
    luxury_service_id = fields.Many2one('luxury.service', ondelete='cascade', string="Service Type")
    booking_datetime = fields.Datetime()
    origin = fields.Many2one(comodel_name='car.booking.address', ondelete='set null')
    destination = fields.Many2one(comodel_name='car.booking.address', ondelete='set null')
    total_distance = fields.Float()
    total_time = fields.Float()
    passengers = fields.Integer(default=1)
    luggage = fields.Integer(default=0)
    sellist1 = fields.Many2one("luxury.service", "Luxury Type")
    status = fields.Char("Booking Status", default="Available")
    from_date = fields.Datetime("From Date Time")
    from_time = fields.Datetime("To Date")
    cars = fields.Many2one("product.template","Car Enganged",domain="[('booking_status', '=', 'Available')]")
    txtSource = fields.Char("Source Location")
    txtDestination = fields.Char("Destination")
    @api.model
    def create(self, values):
        ## Definition
        query ="UPDATE product_template SET booking_status ='Booked' WHERE id =%s"
        product=values['cars']
        vars = (product,)
        self.env.cr.execute(query, vars)
        return super(models.Model, self).create(values)
    
    



