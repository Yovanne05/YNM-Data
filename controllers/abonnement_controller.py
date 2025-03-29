from controllers.generic_controller import GenericController
from services.abonnement_service import abonnement_service

abonnement_controller = GenericController(abonnement_service, "abonnement").blueprint
