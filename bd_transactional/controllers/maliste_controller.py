from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.maliste_service import maliste_service

maliste_controller = GenericController(maliste_service, "maliste").blueprint
