from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.genre_service import genre_service

genre_controller = GenericController(genre_service, "genre").blueprint
