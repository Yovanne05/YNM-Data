from bd_transactional.controllers.generic_controller import GenericController
from bd_transactional.services.paiement_service import paiement_service

paiement_controller = GenericController(paiement_service, "paiement").blueprint
