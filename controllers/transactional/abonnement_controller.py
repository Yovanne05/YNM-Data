from controllers.transactional.generic_controller import GenericController
from services.transactional.abonnement_service import abonnement_service

abonnement_controller = GenericController(abonnement_service, "abonnement").blueprint
