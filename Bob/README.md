# Lotto Result Controller System (Bob)

####An Web API controller for the Lotto Result System

This Web API is built on the [Django REST Framework](https://github.com/tomchristie/django-rest-framework) for the proposal to manage and control a system of Lotto. It allows to the users:

* Generate a random result for the next Lotto
* Retrieve information about the past results
* Retrieve information about a specific past result

For the client APIs, this project allows:
* Match a bet to a specific result for winner ticket verification
* Retrieve information about the next Lotto Result
and also:
* Retrieve information about the past results
* Retrieve information about a specific past result

## Requirements
* Python (3.4+)
* Django (1.7, 1.9+)
* Django REST framework (3.3.2))

## Special Thanks
Thanks to [ONYO](http://onyo.com/) for giving me the opportunity to study and understand the frameworks mentioned above and also for making this challenge really fun.

## Contributors
* Pedro Amaral (@pedro-amaral)

## Web API Documentation
This Project uses [Django REST Framework Swagger](https://github.com/marcgibbons/django-rest-swagger) to generate documentation based on Django REST Framework API code. For more information about API endpoints, please navigate on [api-docs-route](http://onyo-lotto-system-bob.herokuapp.com).