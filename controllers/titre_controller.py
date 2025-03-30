from controllers.generic_controller import GenericController
from services.titre_service import titre_service

titre_controller = GenericController(titre_service, "titre").blueprint
