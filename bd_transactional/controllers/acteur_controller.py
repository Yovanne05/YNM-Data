from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.acteur_service import acteur_service

acteur_controller = GenericController(acteur_service, "acteur").blueprint
