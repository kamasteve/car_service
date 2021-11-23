# -*- Content Encoding - UTF-8 -*-
{
 'name' : 'Car Booking Service',
 'description' : 'Various Car booking Service',
 'summary' : 'Manager Car services and booking',
 'depends' : ['base', 'base_geolocalize', 'web_google_maps'],
 'application' : True,
 'data': ['security/ir.model.access.csv',
          'views/service_type_views.xml',
          'views/service_vehicle_views.xml',
          'views/luxury_service_views.xml',
          'views/car_booking_views.xml',
		  'views/online_booking.xml',
          'views/service_type_menus.xml',
          ],
}
