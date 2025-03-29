from controllers.generic_controller import GenericController
from services.langue_service import langue_service

langue_controller = GenericController(langue_service, "langue").blueprint
