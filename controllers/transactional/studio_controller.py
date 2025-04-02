from controllers.transactional.generic_controller import GenericController
from services.transactional.studio_service import studio_service

studio_controller = GenericController(studio_service, "studio").blueprint
