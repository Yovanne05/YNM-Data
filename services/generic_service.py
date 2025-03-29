from typing import Type, List, Any, Dict, Optional
import db


class GenericService:
    """
    Service générique fournissant les opérations CRUD
    pour n'importe quelle table de la base de données
    """

    def __init__(self, table_name: str, model_class: Type):
        """
        Initialise le service avec le nom de la table et la classe modèle associée
        Args:
            table_name: Nom de la table en base de données
            model_class: Classe Python représentant le modèle
        """
        self.table_name = table_name
        self.model_class = model_class

    def get_all(self) -> List[Any]:
        """
        Récupère tous les enregistrements de la table
        Returns:
            Liste d'instances du modèle peuplées avec les données de la table
        Raises:
            Exception: Si une erreur survient lors de l'accès à la base
        """
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.table_name}")
                result = cursor.fetchall()
            return [self.model_class.from_db(row) for row in result]
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération des données: {str(e)}")
        finally:
            con.close()

    def get_by_id(self, id: int) -> Optional[Any]:
        """
        Récupère un enregistrement par son identifiant unique
        Args:
            id: Identifiant de l'enregistrement à récupérer
        Returns:
            Une instance du modèle si trouvé, None sinon
        Raises:
            Exception: Si une erreur survient lors de l'accès à la base
        """
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE id{self.table_name}=%s", (id,))
                result = cursor.fetchone()
                if result:
                    return self.model_class.from_db(result)
            return None
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de l'élément: {str(e)}")
        finally:
            con.close()

    def create(self, data: Dict[str, Any]) -> int:
        """
        Crée un nouvel enregistrement dans la table
        Args:
            data: Dictionnaire contenant les données à insérer (clés = noms de colonnes)
        Returns:
            L'identifiant (ID) du nouvel enregistrement
        Raises:
            Exception: Si une erreur survient lors de l'insertion
        """
        con = db.get_db_connection()
        try:
            # Prépare les noms de colonnes et les valeurs à insérer
            columns = ", ".join(data.keys())
            placeholders = ", ".join(["%s"] * len(data))

            with con.cursor() as cursor:

                cursor.execute(
                    f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})",
                    list(data.values())
                )
                con.commit()
                return cursor.lastrowid
        except Exception as e:
            raise Exception(f"Erreur lors de la création: {str(e)}")
        finally:
            con.close()

    def update(self, id: int, data: Dict[str, Any]) -> None:
        """
        Met à jour un enregistrement existant
        Args:
            id: Identifiant de l'enregistrement à mettre à jour
            data: Dictionnaire des champs à modifier (clés = noms de colonnes)
        Raises:
            Exception: Si une erreur survient lors de la mise à jour
        """
        con = db.get_db_connection()
        try:
            # Prépare la clause SET pour la requête UPDATE
            set_clause = ", ".join([f"{key} = %s" for key in data.keys()])

            with con.cursor() as cursor:

                cursor.execute(
                    f"UPDATE {self.table_name} SET {set_clause} WHERE id{self.table_name} = %s",
                    [*data.values(), id] # [*data.values(), id] débale dans une lise (remplacé par les valeurs dans l'ordre de la requête)
                )
                con.commit()
        except Exception as e:
            raise Exception(f"Erreur lors de la mise à jour: {str(e)}")
        finally:
            con.close()

    def delete(self, id: int) -> None:
        """
        Supprime un enregistrement par son identifiant
        Args:
            id: Identifiant de l'enregistrement à supprimer
        Raises:
            Exception: Si une erreur survient lors de la suppression
        """
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(f"DELETE FROM {self.table_name} WHERE id{self.table_name}=%s", (id,))
                con.commit()
        except Exception as e:
            raise Exception(f"Erreur lors de la suppression: {str(e)}")
        finally:
            con.close()