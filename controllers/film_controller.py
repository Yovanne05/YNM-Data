from controllers.generic_controller import GenericController
from services.film_service import film_service

film_controller = GenericController(film_service, "film").blueprint
