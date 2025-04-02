from controllers.transactional.generic_controller import GenericController
from services.transactional.profil_service import profil_service

profil_controller = GenericController(profil_service, "profil").blueprint
