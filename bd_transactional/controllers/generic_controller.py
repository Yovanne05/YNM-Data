from flask import Blueprint, jsonify, request, Response
from typing import Any, Tuple
from http import HTTPStatus


class GenericController:
    def __init__(self, service: Any, prefix: str):
        self.service = service
        self.blueprint = Blueprint(f'{prefix}_controller', __name__, url_prefix=f'/{prefix}')

        @self.blueprint.route("/", methods=["GET"])
        def get_all() -> Tuple[Response, int]:
            """Récupère tous les éléments ou les éléments filtrés"""
            try:
                filters = request.args.to_dict()
                items = self.service.get_with_filters(filters) if filters else self.service.get_all()

                if not items:
                    return jsonify([]), 200

                if hasattr(items[0], 'as_dict'):
                    return jsonify([item.as_dict() for item in items]), 200
                return jsonify(items), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["GET"])
        def get_by_id(id: int) -> Tuple[Response, int]:
            """Récupère un élément par son ID"""
            try:
                item = self.service.get_by_id(id)
                if not item:
                    return jsonify({"error": "Resource not found"}), 404

                return jsonify(item.as_dict() if hasattr(item, 'as_dict') else item), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/", methods=["POST"])
        def create() -> Tuple[Response, int]:
            """Crée un nouvel élément"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400

                required_fields = self.service.model_class.__annotations__.keys() - {'id'}
                if not all(field in data for field in required_fields):
                    return jsonify({"error": "Missing required fields"}), 400

                item = self.service.create(data)
                return jsonify({
                    "id": item.id,
                    **(item.as_dict() if hasattr(item, 'as_dict') else data)
                }), 201

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["PUT"])
        def update(id: int) -> Tuple[Response, int]:
            """Met à jour un élément existant"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "No data provided"}), 400

                item = self.service.update(id, data)
                if not item:
                    return jsonify({"error": "Resource not found"}), 404

                return jsonify(item.as_dict() if hasattr(item, 'as_dict') else data), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["DELETE"])
        def delete(id: int) -> Tuple[Response, int]:
            """Supprime un élément existant"""
            try:
                if not self.service.delete(id):
                    return jsonify({"error": "Resource not found"}), 404

                return jsonify({"message": "Resource deleted successfully"}), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/schema", methods=["GET"])
        def get_schema() -> Tuple[Response, int]:
            """Récupère le schéma complet de la table"""
            try:
                schema = self.service.get_table_schema()
                return jsonify(schema), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/structure", methods=["GET"])
        def get_structure() -> Tuple[Response, int]:
            """Récupère la structure de la table (noms des colonnes)"""
            try:
                structure = self.service.get_table_structure()
                return jsonify(structure), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
