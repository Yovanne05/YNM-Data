from controllers.generic_controller import GenericController
from services.utilisateur_service import utilisateur_service

utilisateur_controller = GenericController(utilisateur_service, "utilisateur").blueprint
