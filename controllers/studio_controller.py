from controllers.generic_controller import GenericController
from services.studio_service import studio_service

studio_controller = GenericController(studio_service, "studio").blueprint
