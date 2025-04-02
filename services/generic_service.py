from typing import Type, List, Any, Dict, Optional
from databases import db

def snake_to_camel(text: str) -> str:
    """
    Convertit un texte en snake_case en camelCase.
    Exemple : 'id_langue_disponible' -> 'idLangueDisponible'
    """
    components = text.lower().split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

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
                id_column = snake_to_camel(f"id_{self.table_name}")
                print(id_column)
                print(self.table_name)
                cursor.execute(f"SELECT * FROM {self.table_name} WHERE {id_column}=%s", (id,))
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

    def get_table_schema(self) -> Dict[str, Dict[str, str]]:
        """Retourne le schéma complet avec les infos nécessaires pour les filtres"""
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        COLUMN_NAME,
                        DATA_TYPE,
                        COLUMN_TYPE,
                        IS_NULLABLE,
                        COLUMN_KEY,
                        EXTRA
                    FROM INFORMATION_SCHEMA.COLUMNS 
                    WHERE TABLE_SCHEMA = 'entrepot_netflix'
                    AND TABLE_NAME = %s
                """, (self.table_name,))

                schema = {}
                for col in cursor.fetchall():
                    schema[col['COLUMN_NAME']] = {
                        'type': col['DATA_TYPE'],
                        'nullable': col['IS_NULLABLE'] == 'YES',
                        'is_key': 'PRI' in col['COLUMN_KEY'],
                        'extra': col['EXTRA']
                    }
                return schema
        except Exception as e:
            raise Exception(f"Erreur récupération schéma: {str(e)}")
        finally:
            con.close()

    def get_with_filters(self, filters: dict) -> List[Any]:
        """
        Récupère les enregistrements avec filtres avancés
        Format des filtres: nom_champ__operateur=valeur
        """
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                base_query = f"SELECT * FROM {self.table_name}"
                where_clauses = []
                params = []

                for filter_key, value in filters.items():
                    if "__" in filter_key:
                        column, operator = filter_key.split("__")
                    else:
                        column = filter_key
                        operator = "eq"

                    sql_operator = {
                        'eq': '=',
                        'ne': '!=',
                        'gt': '>',
                        'lt': '<',
                        'gte': '>=',
                        'lte': '<=',
                        'like': 'LIKE',
                        'not_like': 'NOT LIKE'
                    }.get(operator, '=')

                    if operator in ['like', 'not_like']:
                        value = f"%{value}%"

                    where_clauses.append(f"{column} {sql_operator} %s")
                    params.append(value)

                if where_clauses:
                    base_query += " WHERE " + " AND ".join(where_clauses)

                cursor.execute(base_query, params)
                result = cursor.fetchall()

            return [self.model_class.from_db(row) for row in result]
        except Exception as e:
            raise Exception(f"Erreur lors du filtrage: {str(e)}")
        finally:
            con.close()

    def get_table_structure(self) -> Dict[str, List[str]]:
        """
        Retourne la structure de la table (noms des colonnes)
        Returns:
            Dictionnaire avec le nom de la table comme clé et la liste des colonnes comme valeur
        Raises:
            Exception: Si une erreur survient lors de l'accès à la base
        """
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(f"DESCRIBE `{self.table_name}`")
                columns = [column['Field'] for column in cursor.fetchall()]
                return {self.table_name.lower(): columns}
        except Exception as e:
            raise Exception(f"Erreur lors de la récupération de la structure: {str(e)}")
        finally:
            con.close()