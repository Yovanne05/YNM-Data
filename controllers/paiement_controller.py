from controllers.generic_controller import GenericController
from services.paiement_service import paiement_service

paiement_controller = GenericController(paiement_service, "paiement").blueprint
