from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.langue_service import langue_service

langue_controller = GenericController(langue_service, "langue").blueprint
