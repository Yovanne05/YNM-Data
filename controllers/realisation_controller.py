from controllers.generic_controller import GenericController
from services.realisation_service import realisation_service

realisation_controller = GenericController(realisation_service, "realisation").blueprint
