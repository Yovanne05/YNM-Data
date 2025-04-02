from controllers.transactional.generic_controller import GenericController
from services.transactional.evaluation_service import evaulation_service

evaluation_controller = GenericController(evaulation_service, "evaluation").blueprint
