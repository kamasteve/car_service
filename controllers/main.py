
from odoo import http, _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
import datetime
from datetime import timedelta
from werkzeug.exceptions import NotFound

class Admission(http.Controller):
    @http.route(['/shop/new-booking',], type='http', auth="public", website=True)
    def op_admission (self, **kw):
        #return "hello"
        country = http.request.env['res.country'].sudo().search([])
        cars = http.request.env['product.template'].sudo().search([])
        luxury_service = http.request.env['luxury.service'].sudo().search([])
        return request.render("car_service.book_car_online", {'country': country,'cars':cars,'luxury_service':luxury_service})

    @http.route('/shop/products/validate', type='http', auth="public", website=True)
    def admission_courses_fetch(self, **kwargs):
        values = {}
        for field_name, field_value in kwargs.items():
            values[field_name] = field_value

        from_date1 = values['from_date']
        duration1 = values['input_duration']
        if duration1:
            duration = int(duration1) / 60
        else:
            duration = 0
        n2 = datetime.datetime.strptime(from_date1, '%Y-%m-%dT%H:%M')
        from_time = n2 + timedelta(minutes=duration) + timedelta(minutes=30)
        cars = int(values['cars'])
        return_string = ""
        #print(from_time)
        from_date = datetime.datetime.strptime(from_date1, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
        date =str(from_time)
        from_time1 = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
        if from_time1 < from_date:
            return_string = "The end date cannot be smaller that the start date"
        check_booking = request.env['car.booking'].sudo().search([('from_date', '>=', from_date),('from_date', '<=', from_time),('cars','=', cars)])
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
    @http.route('/shop/book/car', type="http", auth="public", website='user')
    def admission_submit_application(self, **kwargs):
         values = {}
         for field_name, field_value in kwargs.items():
             values[field_name] = field_value
         sellist1 = values['sellist1']
         from_date1 = values['from_date']
         from_time1 = values['from_date']
         txtSource = values['txtSource']
         duration1 = values['input_duration']
         total_distance = values['input_distance']
         txtDestination = values['txtDestination']
         if duration1:
             duration = int(duration1)/60
         else:
             duration=0
         cars = values['cars']
         quantity = values['quantity']
         from_date= datetime.datetime.strptime(from_date1, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
         n=30
         n2 = datetime.datetime.strptime(from_time1, '%Y-%m-%dT%H:%M')
         from_time = n2 + datetime.timedelta(minutes=n) + datetime.timedelta(minutes=duration)
         print(from_time)
         dict = {'sellist1':sellist1,'from_date':from_date,'txtSource':txtSource,'total_time':duration,'total_distance':total_distance,'status':'Booked','from_time':from_time,
                 'cars':cars,'luggage':quantity,'txtDestination':txtDestination
                 }

         results = request.env['car.booking'].sudo().create(dict)
         query = """
                     UPDATE product_template
                         SET booking_status = 'Booked'
                     WHERE id = %s
                 """
         request.env.cr.execute(query, [tuple(cars)])
         product_id = cars
         add_qty = 1
         set_qty = 0
         #product.update({'lst_price': post['Overdue']})
         # product.lst_price = post['amount']
         request.website.sale_get_order(force_create=1)._cart_update(
             product_id=int(product_id),
             add_qty=float(add_qty),
             set_qty=float(set_qty),
         )
         return request.redirect("/shop/cart")
