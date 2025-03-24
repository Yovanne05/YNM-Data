import db  # Importez votre module de connexion à la base de données

class Delete_Edit_Services:
    @staticmethod
    def get_all_items(table_name):
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table_name}")
                result = cursor.fetchall()


            items = [dict(zip([column[0] for column in cursor.description], row)) for row in result]
            return items

        except Exception as e:
            raise Exception(f"Error fetching items from {table_name}: {str(e)}")

        finally:
            con.close()

    @staticmethod
    def delete_item(table_name, item_id):

        table_primary_keys = {
            "utilisateur": "idUtilisateur",
            "abonnement": "idAbonnement",
            "temps": "idDate",
            "genre": "idGenre",
            "titre": "idTitre",
            "serie": "idSerie",
            "film": "idFilm",
            "langue": "idLangue",
            "langue_Disponible": "idLangueDispo",
            "visionnage": "idVisionnage",
            "evaluation": "idEvaluation",
            "Paiement": "idPaiement",
        }


        allowed_tables = list(table_primary_keys.keys())
        if table_name not in allowed_tables:
            raise ValueError(f"Table '{table_name}' non autorisée")


        primary_key = table_primary_keys.get(table_name)
        if not primary_key:
            raise ValueError(f"Colonne d'identifiant non trouvée pour la table '{table_name}'")


        if not isinstance(item_id, int) or item_id <= 0:
            raise ValueError("item_id doit être un entier positif")

        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:

                query = f"DELETE FROM {table_name} WHERE {primary_key} = %s"
                print(f"Exécution de la requête : {query} avec item_id = {item_id}")
                cursor.execute(query, (item_id,))
                con.commit()

                if cursor.rowcount == 0:
                    raise Exception("Item not found")

                print("Élément supprimé avec succès")
                return {"message": "Item deleted successfully"}

        except Exception as e:
            con.rollback()
            print(f"Erreur lors de la suppression : {str(e)}")
            raise Exception(f"Error deleting item from {table_name}: {str(e)}")

        finally:
            con.close()

    @staticmethod
    def update_item(table_name, item_id, updated_data):
        table_primary_keys = {
            "utilisateur": "idUtilisateur",
            "abonnement": "idAbonnement",
            "temps": "idDate",
            "genre": "idGenre",
            "titre": "idTitre",
            "serie": "idSerie",
            "film": "idFilm",
            "langue": "idLangue",
            "langue_disponible": "idLangueDispo",
            "visionnage": "idVisionnage",
            "evaluation": "idEvaluation",
            "paiement": "idPaiement"
        }

        # 1. Validation des paramètres d'entrée
        if not table_name or not isinstance(table_name, str):
            raise ValueError("Nom de table invalide")

        if table_name.lower() not in table_primary_keys:
            raise ValueError(f"Table '{table_name}' non autorisée")

        if not updated_data or not isinstance(updated_data, dict):
            raise ValueError("Données de mise à jour invalides")

        try:
            item_id = int(item_id)
            if item_id <= 0:
                raise ValueError("ID doit être un entier positif")
        except (ValueError, TypeError):
            raise ValueError("ID invalide - doit être un nombre")

        primary_key = table_primary_keys[table_name.lower()]

        # 2. Construction de la requête
        con = db.get_db_connection()
        try:
            with con.cursor() as cursor:
                # Vérification que l'élément existe
                cursor.execute(
                    f"SELECT 1 FROM {table_name} WHERE {primary_key} = %s",
                    (item_id,)
                )
                if not cursor.fetchone():
                    raise Exception("Élément non trouvé")

                # Construction dynamique de la requête
                set_fields = []
                values = []
                for key, value in updated_data.items():
                    if key != primary_key:  # On ne permet pas de modifier la clé primaire
                        set_fields.append(f"{key} = %s")
                        values.append(value)

                if not set_fields:
                    raise ValueError("Aucun champ valide à mettre à jour")

                query = f"""
                    UPDATE {table_name} 
                    SET {', '.join(set_fields)}
                    WHERE {primary_key} = %s
                """
                values.append(item_id)

                # Exécution
                cursor.execute(query, values)
                con.commit()

                return {
                    "message": "Mise à jour réussie",
                    "affected_rows": cursor.rowcount
                }

        except Exception as e:
            con.rollback()
            raise Exception(f"Erreur lors de la mise à jour : {str(e)}")
        finally:
            con.close()