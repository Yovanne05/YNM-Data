from controllers.generic_controller import GenericController
from services.temps_service import temps_service

temps_controller = GenericController(temps_service, "temps").blueprint
