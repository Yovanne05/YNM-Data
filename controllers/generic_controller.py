from flask import Blueprint, jsonify, Response, request
from typing import Type, Any, Dict


class GenericController:
    """
    Contrôleur générique qui crée automatiquement des routes CRUD
    pour n'importe quel modèle de données
    """

    def __init__(self, service: Any, prefix: str):
        """
        Initialise le contrôleur avec un service et un préfixe d'URL

        Args:
            service: Le service qui gère les opérations sur les données
            prefix: Préfixe pour les URL
        """
        self.service = service
        self.blueprint = Blueprint(f'{prefix}_controller', __name__, url_prefix=f'/{prefix}')

        @self.blueprint.route("/", methods=["GET"])
        def get_all() -> tuple[Response, int]:
            """
            Récupère tous les éléments ou les éléments filtrés
            """
            try:
                filters = request.args.to_dict()  # Récupère ?age=19 etc.

                if filters:
                    # Si filtres présents, utilisez get_with_filters
                    items = self.service.get_with_filters(filters)
                else:
                    # Sinon récupère tout
                    items = self.service.get_all()

                # Convertit en dictionnaire seulement si ce sont des objets
                if items and hasattr(items[0], 'as_dict'):
                    return jsonify([item.as_dict() for item in items]), 200
                return jsonify(items), 200

            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["GET"])
        def get_by_id(id: int) -> tuple[Response, int]:
            """
            Récupère un élément spécifique par son ID
            Args:
                id: L'identifiant de l'élément à récupérer
            Retourne:
                - Code 200 avec l'élément si trouvé
                - Code 404 si l'élément n'existe pas
                - Code 500 en cas d'erreur
            """
            try:
                item = self.service.get_by_id(id)
                if not item:
                    return jsonify({"error": "Ressource inexistante"}), 404
                return jsonify(item.as_dict()), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/", methods=["POST"])
        def create() -> tuple[Response, int]:
            """
            Crée un nouvel élément
            Attend les données en JSON dans le corps de la requête
            Retourne:
                - Code 201 avec l'ID du nouvel élément si succès
                - Code 400 si des champs requis sont manquants
                - Code 500 en cas d'erreur
            """
            try:
                data = request.get_json()

                # Vérifie que tous les champs requis sont présents
                # __annotations__ : Récupère le dictionnaire des annotations de type ex : {'id': int, 'nom': str, 'email': str, 'age': int}
                required_fields = self.service.model_class.__annotations__.keys() - {'id'}
                if not all(field in data for field in required_fields):
                    return jsonify({"error": "Tous les champs requis doivent être fournis"}), 400

                item_id = self.service.create(data)
                # Retourne l'ID du nouvel élément et les données
                return jsonify({"id": item_id, **data}), 201 # ** : déplie le dictionnaire en clé-valeur
            except Exception as e:
                return jsonify({"error": str(e)}), 500

        @self.blueprint.route("/<int:id>", methods=["PUT"])
        def update(id: int) -> tuple[Response, int]:
            """
            Met à jour un élément existant
            Args:
                id: L'identifiant de l'élément à mettre à jour
            Retourne:
                - Code 200 avec les données mises à jour si succès
                - Code 404 si l'élément n'existe pas
                - Code 500 en cas d'erreur
            """
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
        def delete(id: int) -> tuple[Response, int]:
            """
            Supprime un élément existant
            Args:
                id: L'identifiant de l'élément à supprimer
            Retourne:
                - Code 200 avec un message de confirmation si succès
                - Code 404 si l'élément n'existe pas
                - Code 500 en cas d'erreur
            """
            try:
                item = self.service.get_by_id(id)
                if not item:
                    return jsonify({"error": "Ressource inexistante"}), 404

                self.service.delete(id)
                return jsonify({"message": "Suppression effectuée"}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500


        @self.blueprint.route("/schema", methods=["GET"])
        def get_schema():
            try:
                schema = self.service.get_table_schema()
                return jsonify(schema), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
