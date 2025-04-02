from controllers.transactional.generic_controller import GenericController
from services.transactional.serie_service import serie_service

serie_controller = GenericController(serie_service, "serie").blueprint
