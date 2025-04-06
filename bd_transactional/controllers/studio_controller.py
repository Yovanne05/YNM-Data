from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.studio_service import studio_service

studio_controller = GenericController(studio_service, "studio").blueprint
