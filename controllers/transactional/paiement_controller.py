from controllers.transactional.generic_controller import GenericController
from services.transactional.paiement_service import paiement_service

paiement_controller = GenericController(paiement_service, "paiement").blueprint
