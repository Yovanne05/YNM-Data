from models.serie_model import Serie
from flask import Blueprint, jsonify, request, Response
from services.serie_service import get_all_series

series_controller = Blueprint('serie_controller', __name__,url_prefix='/series')

@series_controller.route("/series", methods=["GET"])
def get_series() -> tuple[Response, int] :
    series = get_all_series()
    return jsonify([serie.as_dict() for serie in series]), 200
