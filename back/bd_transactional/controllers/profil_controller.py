from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.profil_service import profil_service

profil_controller = GenericController(profil_service, "profil").blueprint
