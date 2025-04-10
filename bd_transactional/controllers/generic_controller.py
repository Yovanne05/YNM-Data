from flask import Blueprint, jsonify, request, Response
from typing import Any

class GenericController:
    def __init__(self, service: Any, prefix: str):
        self.service = service
        self.blueprint = Blueprint(f'{prefix}_controller', __name__, url_prefix=f'/{prefix}')

        @self.blueprint.route("/", methods=["GET"])
        def get_all():
            """Récupère tous les éléments ou les éléments filtrés avec pagination"""
            try:
                page = request.args.get('page', default=1, type=int)
                per_page = request.args.get('per_page', default=5, type=int)
                filters = request.args.to_dict()

                filters.pop('page', None)
                filters.pop('per_page', None)

                if filters:
                    items, total = self.service.get_with_filters(filters, page=page, per_page=per_page)
                else:
                    items, total = self.service.get_paginated(page=page, per_page=per_page)

                response = {
                    'items': [item.as_dict() for item in items] if items and hasattr(items[0], 'as_dict') else items,
                    'total': total,
                    'page': page,
                    'per_page': per_page,
                    'pages': (total + per_page - 1) // per_page
                }
                return jsonify(response), 200
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
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "Aucune donnée fournie"}), 400

                item = self.service.create_item(data)

                primary_key = self.service.get_primary_key(item)
                return jsonify({
                    "id": getattr(item, primary_key),
                    "message": "Création réussie"
                }), 201

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

        @self.blueprint.route("/schema/<column_name>", methods=["GET"])
        def get_column_schema(column_name: str):
            try:
                schema = self.service.get_column_schema(column_name)
                if "error" in schema:
                    return jsonify(schema), 400
                return jsonify(schema)
            except Exception as e:
                return jsonify({"error": str(e)}), 500