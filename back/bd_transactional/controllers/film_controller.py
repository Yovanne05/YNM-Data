from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.film_service import film_service

film_controller = GenericController(film_service, "film").blueprint
