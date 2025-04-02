from controllers.transactional.generic_controller import GenericController
from services.transactional.film_service import film_service

film_controller = GenericController(film_service, "film").blueprint
