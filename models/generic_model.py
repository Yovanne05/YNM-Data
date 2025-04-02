from typing import Dict, Any
import re

def camel_to_snake(name: str) -> str:
    """
    Convertit un texte en camelCase en snake_case.
    Exemple : 'idLangueDisponible' -> 'id_langue_disponible'
    """
    return re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower()


class GenericModel:

    """
    Une classe modèle générique qui fournit des méthodes de base pour :
    - Convertir des données de la base de données en objet (from_db)
    - Créer un nouvel objet avec des valeurs par défaut (from_db_add)
    - Convertir un objet en dictionnaire (as_dict)
    """

    @classmethod
    def from_db(cls, data: Dict[str, Any]) -> "T":
        """
        Crée une instance du modèle à partir de données de la base de données
        Args:
            data: Dictionnaire contenant les données de la base (clés = noms des colonnes)
        Returns:
            Une instance de la classe modèle avec les données chargées
        """
        # Convertit les clés en snake_case
        data_snake_case = {camel_to_snake(k): v for k, v in data.items()}
        return cls(**data_snake_case)  # Déballe le dictionnaire en clé-valeur

    @classmethod
    def from_db_add(cls, data: Dict[str, Any]) -> "T":
        """
        Crée une instance pour un nouvel enregistrement, avec un ID temporaire à 0
        Args:
            data: Dictionnaire contenant les données du nouvel objet
        Returns:
            Une instance avec id=0 et les autres données fournies
        """
        # Convertit les clés en snake_case
        data_snake_case = {camel_to_snake(k): v for k, v in data.items()}
        return cls(**{**data_snake_case, 'id': 0})


    def as_dict(self) -> Dict[str, Any]:
        """
        Convertit l'objet en dictionnaire
        Returns:
            Dictionnaire avec toutes les propriétés de l'objet
        """
        return self.__dict__