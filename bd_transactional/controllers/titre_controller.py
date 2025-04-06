from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.titre_service import titre_service

titre_controller = GenericController(titre_service, "titre").blueprint
