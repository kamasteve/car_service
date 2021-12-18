
from odoo import http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
import datetime
from werkzeug.exceptions import NotFound

class Admission(http.Controller):
    @http.route(['/shop/new-booking',], type='http', auth="public", website=True)
    def op_admission (self, **kw):
        #return "hello"
        country = http.request.env['res.country'].sudo().search([])
        cars = http.request.env['product.template'].sudo().search([])
        print(cars)
        return request.render("car_service.book_car_online", {'country': country,'cars':cars})

    @http.route('/shop/products/validate', type='http', auth="public", website=True)
    def admission_courses_fetch(self, **kwargs):
        values = {}
        for field_name, field_value in kwargs.items():
            values[field_name] = field_value
            print(values[field_name])
        from_date1 = values['from_date']
        from_time1 = values['from_date']
        cars = int(values['cars'])
        print(cars)
        return_string = ""
        from_date = datetime.datetime.strptime(from_date1, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
        from_time = datetime.datetime.strptime(from_time1, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
        if from_time < from_date:
            return_string = "The end date cannot be smaller that the start date"
        check_booking = request.env['car.booking'].sudo().search([('from_date', '=', from_date),('cars','=', cars)]).id
        print(check_booking)
        if  check_booking:
           alternative = request.env['product.template'].sudo().search([('id', '=', values['cars'])]).alternative_products
           if alternative:
              return_string += "<img t-att-src='data:image/png;base64,%s' % to_text(alternative.image_1920)/>\n"
              return_string += "<div class=\"form-group\">\n"
              return_string += "  <label class=\"control-label\" for=\"subcategory\">Alternative Cars</label>\n"
              return_string += "  <select class=\"form-control\" id=\"cars\" name=\"cars\">\n"
              for alternative in alternative:
                  return_string += "    <option value=\"" + str(
                  alternative.id) + "\">" + alternative.name + "</option>\n"
                  return_string += "  </select>\n"
                  return_string += "</div>\n"
        return return_string
    # @http.route('/rekrutacja-online/subjects/fetch', type='http', auth="public", website=True)

    @http.route('/shop/book/car', type="http", auth="public", website='user')
    def admission_submit_application(self, **kwargs):
         values = {}

         for field_name, field_value in kwargs.items():
             values[field_name] = field_value
         sellist1 = values['sellist1']
         from_date1 = values['from_date']
         from_time1 = values['from_date']
         txtSource = values['txtSource']
         cars = values['cars']
         quantity = values['quantity']
         from_date= datetime.datetime.strptime(from_date1, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
         from_time = datetime.datetime.strptime(from_time1, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
         print(from_date)
         dict = {'sellist1':sellist1,'from_date':from_date,'txtSource':txtSource,'from_time':from_time,
                 'cars':cars,'luggage':quantity,
                 }

         results = request.env['car.booking'].sudo().create(dict)
         return http.request.render('car_service.booking_success', {})