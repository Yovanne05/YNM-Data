from controllers.generic_controller import GenericController
from services.acteur_service import acteur_service

acteur_controller = GenericController(acteur_service, "acteur").blueprint
