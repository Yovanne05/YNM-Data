from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.serie_service import serie_service

serie_controller = GenericController(serie_service, "serie").blueprint
