from flask import Blueprint, jsonify, request, Response
from typing import Any

class GenericController:
    def __init__(self, service: Any, prefix: str):
        self.service = service
        self.blueprint = Blueprint(f'{prefix}_controller', __name__, url_prefix=f'/{prefix}')

        @self.blueprint.route("/", methods=["GET"])
        def get_all():
            """Récupère tous les éléments ou les éléments filtrés"""
            try:
                filters = request.args.to_dict()
                if filters:
                    items = self.service.get_with_filters(filters)
                else:
                    items = self.service.get_all()

                if items and hasattr(items[0], 'as_dict'):
                    return jsonify([item.as_dict() for item in items]), 200
                return jsonify(items), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["GET"])
        def get_by_id(id: int):
            """Récupère un élément par son ID"""
            try:
                item = self.service.get_by_id(id)
                if not item:
                    return jsonify({"error": "Ressource inexistante"}), 404
                return jsonify(item.as_dict()), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/", methods=["POST"])
        def create():
            """Crée un nouvel élément"""
            try:
                data = request.get_json()
                required_fields = self.service.model_class.__annotations__.keys() - {'id'}
                if not all(field in data for field in required_fields):
                    return jsonify({"error": "Champs requis manquants"}), 400

                item = self.service.create(data)
                return jsonify({"id": item.id, **data}), 201
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["PUT"])
        def update(id: int):
            """Met à jour un élément existant"""
            try:
                item = self.service.get_by_id(id)
                if not item:
                    return jsonify({"error": "Ressource inexistante"}), 404

                data = request.get_json()
                self.service.update(id, data)
                return jsonify(data), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["DELETE"])
        def delete(id: int):
            """Supprime un élément existant"""
            try:
                success = self.service.delete(id)
                if not success:
                    return jsonify({"error": "Ressource inexistante"}), 404
                return jsonify({"message": "Suppression effectuée"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/schema", methods=["GET"])
        def get_schema():
            """Récupère le schéma complet de la table"""
            try:
                schema = self.service.get_table_schema()
                return jsonify(schema), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/structure", methods=["GET"])
        def get_structure():
            """Récupère la structure de la table (noms des colonnes)"""
            try:
                structure = self.service.get_table_structure()
                return jsonify(structure), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500