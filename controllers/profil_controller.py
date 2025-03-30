from controllers.generic_controller import GenericController
from services.profil_service import profil_service

profil_controller = GenericController(profil_service, "profil").blueprint
