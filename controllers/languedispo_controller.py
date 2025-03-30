from controllers.generic_controller import GenericController
from services.languedispo_service import languedisponible_service

languedisponible_controller = GenericController(languedisponible_service, "langue_disponible").blueprint
