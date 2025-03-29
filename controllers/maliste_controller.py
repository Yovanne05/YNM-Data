from controllers.generic_controller import GenericController
from services.maliste_service import maliste_service

maliste_controller = GenericController(maliste_service, "maliste").blueprint
