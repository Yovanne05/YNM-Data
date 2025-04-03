from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.acting_service import acting_service

acting_controller = GenericController(acting_service, "acting").blueprint
