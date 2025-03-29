from controllers.generic_controller import GenericController
from services.acting_service import acting_service

acting_controller = GenericController(acting_service, "Acting").blueprint
