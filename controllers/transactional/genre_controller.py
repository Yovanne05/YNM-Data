from controllers.transactional.generic_controller import GenericController
from services.transactional.genre_service import genre_service

genre_controller = GenericController(genre_service, "genre").blueprint
