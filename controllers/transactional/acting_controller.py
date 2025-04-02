from controllers.transactional.generic_controller import GenericController
from services.transactional.acting_service import acting_service

acting_controller = GenericController(acting_service, "acting").blueprint
