# Lotto Client Ticket Controller (Ana)

####An Web API controller for the client ticket system

This Web API is built on the [Django REST Framework](https://github.com/tomchristie/django-rest-framework) for the proposal to manage and control a system of client tickets. It allows to the users:

* Create a new ticket for the next Lotto (using Bob)
* Check if a owned ticket is a winner of the related Lotto (using Bob)
* Retrieve information about their tickets
* Retrieve information about a specific owned ticket

## Requirements
* Python (3.4+)
* Django (1.7, 1.9+)
* Django REST framework (3.3.2))

## Special Thanks
Thanks to [ONYO](http://onyo.com/) for giving me the opportunity to study and understand the frameworks mentioned above and also for making this challenge really fun.

## Contributors
* Pedro Amaral (@pedroamaral)

## Web API Documentation
This Project uses [Django REST Framework Swagger](https://github.com/marcgibbons/django-rest-swagger) to generate documentation based on Django REST Framework API code. For more information about API endpoints, please navigate on [api-docs-route](http://onyo-ticket-system-ana.herokuapp.com).