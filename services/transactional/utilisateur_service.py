from services.transactional.generic_service import GenericService
from models.transactional.utilisateur_model import Utilisateur

utilisateur_service = GenericService(Utilisateur)

# class UtilisateurService(GenericService):
#     def __init__(self):
#         super().__init__(Utilisateur)
#
#     #A décommenter a la fin (verif email)
#
#     # def create(self, data: dict) -> int:
#     #     if 'email' in data:
#     #         self._validate_email_format(data['email'])
#     #         self._validate_unique_email(data['email'])
#     #     return super().create(data)
#     #
#     # def update(self, id: int, data: dict) -> None:
#     #     if 'email' in data:
#     #         self._validate_email_format(data['email'])
#     #
#     #         current_user = self.get_by_id(id)
#     #         if current_user.email != data['email']:
#     #             self._validate_unique_email(data['email'])
#     #
#     #     super().update(id, data)
#     #
#     # def _validate_email_format(self, email: str):
#     #     """Valide le format de l'email"""
#     #     if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
#     #         raise ValueError("Format d'email invalide. L'email doit contenir '@' et un domaine valide")
#     #
#     # def _validate_unique_email(self, email: str):
#     #     """Vérifie que l'email n'existe pas déjà"""
#     #     con = db.get_db_connection()
#     #     try:
#     #         with con.cursor() as cursor:
#     #             cursor.execute("SELECT idUtilisateur FROM Utilisateur WHERE email = %s", (email,))
#     #             if cursor.fetchone():
#     #                 raise ValueError("Cet email est déjà utilisé")
#     #     finally:
#     #         con.close()
