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
            "Abonnement": "idAbonnement",
            "Temps": "idDate",
            "Genre": "idGenre",
            "Titre": "idTitre",
            "Serie": "idSerie",
            "Film": "idFilm",
            "Langue": "idLangue",
            "Langue_Disponible": "idLangueDispo",
            "Visionnage": "idVisionnage",
            "Evaluation": "idEvaluation",
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
        con = db.get_db_connection()
        try:
            if not updated_data:
                raise Exception("No data provided")


            set_clause = ", ".join([f"{key} = %s" for key in updated_data.keys()])
            values = list(updated_data.values()) + [item_id]

            with con.cursor() as cursor:
                cursor.execute(
                    f"UPDATE {table_name} SET {set_clause} WHERE id = %s",
                    values
                )
                con.commit()

                if cursor.rowcount == 0:
                    raise Exception("Item not found")

                return {"message": "Item updated successfully"}

        except Exception as e:
            con.rollback()
            raise Exception(f"Error updating item in {table_name}: {str(e)}")

        finally:
            con.close()