from controllers.transactional.generic_controller import GenericController
from services.transactional.maliste_service import maliste_service

maliste_controller = GenericController(maliste_service, "maliste").blueprint
