from flask import Blueprint, jsonify, request, Response
from typing import Any

class GenericController:
    def __init__(self, service: Any, prefix: str):
        self.service = service
        self.blueprint = Blueprint(f'{prefix}_controller', __name__, url_prefix=f'/{prefix}')

        @self.blueprint.route("/", methods=["GET"])
        def get_all():
            """Récupère tous les éléments ou les éléments filtrés avec pagination et tri"""
            try:
                page = request.args.get('page', default=1, type=int)
                per_page = request.args.get('per_page', default=5, type=int)
                filters = request.args.to_dict()

                sort_params = []
                for key in list(filters.keys()):
                    if key.startswith('sort_'):
                        sort_params.append((key[5:], filters.pop(key)))

                filters.pop('page', None)
                filters.pop('per_page', None)

                if filters or sort_params:
                    items, total = self.service.get_with_filters_and_sort(
                        filters,
                        sort_params,
                        page=page,
                        per_page=per_page
                    )
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
                    self.service.add_log("CREATE", "FAILED", "Aucune donnée fournie")
                    return jsonify({"error": "Aucune donnée fournie"}), 400

                item = self.service.create_item(data)
                primary_key = self.service.get_primary_key(item)

                self.service.add_log("CREATE", "SUCCESS", f"ID: {getattr(item, primary_key)}")
                return jsonify({
                    "id": getattr(item, primary_key),
                    "message": "Création réussie"
                }), 201

            except Exception as e:
                self.service.add_log("CREATE", "FAILED", str(e))
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["PUT"])
        def update(id: int):
            try:
                item = self.service.get_by_id(id)
                if not item:
                    self.service.add_log("UPDATE", "FAILED", f"ID {id} non trouvé")
                    return jsonify({"error": "Ressource inexistante"}), 404

                data = request.get_json()
                self.service.update(id, data)

                self.service.add_log("UPDATE", "SUCCESS", f"ID: {id}")
                return jsonify(data), 200
            except Exception as e:
                self.service.add_log("UPDATE", "FAILED", f"ID: {id}")
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["DELETE"])
        def delete(id: int):
            try:
                success = self.service.delete(id)
                if not success:
                    self.service.add_log("DELETE", "FAILED", f"ID {id} non trouvé")
                    return jsonify({"error": "Ressource inexistante"}), 404

                self.service.add_log("DELETE", "SUCCESS", f"ID: {id}")
                return jsonify({"message": "Suppression effectuée"}), 200
            except Exception as e:
                self.service.add_log("DELETE", "FAILED", f"ID: {id}")
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

        @self.blueprint.route("/no_pagination", methods=["GET"])
        def get_all_no_pagination():
            """Récupère tous les éléments sans pagination avec filtres et tri"""
            try:
                params = request.args.to_dict()

                filters = {}
                sort_params = []
                for key, value in params.items():
                    if key.startswith("sort_"):
                        column = key.replace("sort_", "")
                        sort_params.append((column, value))
                    elif "__" in key:
                        filters[key] = value
                    else:
                        filters[f"{key}__eq"] = value
                print(filters, sort_params)
                if filters or sort_params:
                    items = self.service.get_with_filters_and_sort_no_pagination(filters, sort_params)
                else:
                    items = self.service.get_all()

                if items and hasattr(items[0], 'as_dict'):
                    return jsonify([item.as_dict() for item in items]), 200
                return jsonify(items), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500