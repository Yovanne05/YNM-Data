from controllers.generic_controller import GenericController
from services.titregenre_service import titregenre_service

titregenre_controller = GenericController(titregenre_service, "titregenre").blueprint
