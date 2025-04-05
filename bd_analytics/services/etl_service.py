from bd_analytics.models.film_model import FilmEntrepot
from bd_analytics.models.serie_model import SerieEntrepot
from databases.database_session import get_main_db_session, get_db_entrepot_session
from databases.db import db
from sqlalchemy import text

GenreDim = db.models.GenreDim
LangueDim = db.models.LangueDim
TempsDim = db.models.TempsDim
LangueDisponibleDim = db.models.LangueDisponibleDim
AbonnementDim = db.models.AbonnementDim
UtilisateurDim = db.models.UtilisateurDim
TitreDim = db.models.TitreDim
PaiementFact = db.models.PaiementFact
EvaluationFact = db.models.EvaluationFact


def extract_transform_load_all():
    print("Début du processus ETL complet")

    extract_transform_dimensions()
    extract_transform_facts()

    print("Processus ETL terminé avec succès")


def extract_transform_dimensions():
    """ETL pour les tables de dimensions"""
    print("Début de l'ETL pour les dimensions")

    process_genre_dim()
    process_langue_dim()
    process_temps_dim()

    process_langue_disponible_dim()
    process_abonnement_dim()
    process_utilisateur_dim()

    process_titre_dim()

    process_film_dim()
    process_serie_dim()

    print("ETL des dimensions terminé")


def extract_transform_facts():
    """ETL pour les tables de faits"""
    print("Début de l'ETL pour les faits")

    process_paiement_fact()
    process_visionnage_fact()
    process_evaluation_fact()

    print("ETL des faits terminé")


def process_genre_dim():
    """Extrait et transforme les données de genre"""
    print("Traitement de la dimension Genre...")

    with get_main_db_session() as session:
        with get_db_entrepot_session() as entrepot_session:
            source_genres = session.execute(text("SELECT idGenre, nom FROM Genre")).fetchall()

            for genre in source_genres:
                genre_dim = GenreDim(
                    idGenre=genre.idGenre,
                    nomGenre=genre.nom
                )
                entrepot_session.merge(genre_dim)

            entrepot_session.commit()
    print(f"{len(source_genres)} genres traités")


def process_langue_dim():
    """Extrait et transforme les données de langue"""
    print("Traitement de la dimension Langue...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        source_langues = session.execute(text("SELECT idLangue, nom FROM Langue")).fetchall()

        for langue in source_langues:
            langue_dim = LangueDim(
                idLangue=langue.idLangue,
                nomLangue=langue.nom
            )
            entrepot_session.merge(langue_dim)

        entrepot_session.commit()
    print(f"{len(source_langues)} langues traitées")


def process_temps_dim():
    """Extrait et transforme les données temporelles"""
    print("Traitement de la dimension Temps...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        # Récupérer toutes les dates uniques
        dates_uniques = set()

        paiement_dates = session.execute(text("SELECT DISTINCT datePaiement FROM Paiement")).fetchall()
        dates_uniques.update([p.datePaiement for p in paiement_dates])

        titre_dates = session.execute(text("SELECT DISTINCT dateDebutLicence, dateFinLicence FROM Titre")).fetchall()
        for t in titre_dates:
            dates_uniques.add(t.dateDebutLicence)
            dates_uniques.add(t.dateFinLicence)

        for date in dates_uniques:
            if not date:
                continue

            temps_dim = TempsDim(
                jour=date.day,
                mois=date.month,
                annee=date.year,
                trimestre=(date.month - 1) // 3 + 1,
                jour_semaine=date.weekday() + 1,
                est_weekend=date.weekday() >= 5
            )
            entrepot_session.merge(temps_dim)

        entrepot_session.commit()
    print(f"{len(dates_uniques)} dates traitées")


def process_langue_disponible_dim():
    """Extrait et transforme les langues disponibles"""
    print("Traitement de la dimension LangueDisponible...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        source_langues_dispo = session.execute(text("""
                SELECT idLangueDisponible, idTitre, idLangue, typeLangue 
                FROM Langue_Disponible
            """)).fetchall()

        for ld in source_langues_dispo:
            langue_dispo_dim = LangueDisponibleDim(
                idLangueDisponible=ld.idLangueDisponible,
                idLangue=ld.idLangue,
                typeLangue=ld.typeLangue
            )
            entrepot_session.merge(langue_dispo_dim)

        entrepot_session.commit()
    print(f"{len(source_langues_dispo)} langues disponibles traitées")


def process_abonnement_dim():
    """Extrait et transforme les abonnements"""
    print("Traitement de la dimension Abonnement...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        source_abonnements = session.execute(text("""
                SELECT idAbonnement, typeAbonnement, prix 
                FROM Abonnement
            """)).fetchall()

        for ab in source_abonnements:
            abonnement_dim = AbonnementDim(
                idAbonnement=ab.idAbonnement,
                typeAbonnement=ab.typeAbonnement,
                prix=ab.prix
            )
            entrepot_session.merge(abonnement_dim)

        entrepot_session.commit()
    print(f"{len(source_abonnements)} abonnements traités")


def process_utilisateur_dim():
    """Extrait et transforme les utilisateurs"""
    print("Traitement de la dimension Utilisateur...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        source_utilisateurs = session.execute(text("""
                SELECT idUtilisateur, nom, prenom, age, paysResidance, email, numero, statutAbonnement
                FROM Utilisateur
            """)).fetchall()

        for user in source_utilisateurs:
            utilisateur_dim = UtilisateurDim(
                idUtilisateur=user.idUtilisateur,
                nom=user.nom,
                prenom=user.prenom,
                age=user.age,
                paysResidence=user.paysResidance,
                email=user.email,
                numero=user.numero,
                statutAbonnement=user.statutAbonnement
            )
            entrepot_session.merge(utilisateur_dim)

        entrepot_session.commit()
    print(f"{len(source_utilisateurs)} utilisateurs traités")


def process_titre_dim():
    """Extrait et transforme les titres"""
    print("Traitement de la dimension Titre...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        source_titres = session.execute(text("""
                SELECT t.idTitre, t.nom, t.annee, t.dateDebutLicence, t.dateFinLicence, 
                       t.categorieAge, t.description, tg.idGenre,
                       CASE WHEN f.idFilm IS NOT NULL THEN 'film' ELSE 'série' END AS typeTitre
                FROM Titre t
                LEFT JOIN Film f ON t.idTitre = f.idTitre
                LEFT JOIN Serie s ON t.idTitre = s.idTitre
                LEFT JOIN TitreGenre tg ON t.idTitre = tg.idTitre
            """)).fetchall()

        for titre in source_titres:
            id_date_debut = None
            if titre.dateDebutLicence:
                date_debut = entrepot_session.query(TempsDim).filter_by(
                    jour=titre.dateDebutLicence.day,
                    mois=titre.dateDebutLicence.month,
                    annee=titre.dateDebutLicence.year
                ).first()
                id_date_debut = date_debut.idDate if date_debut else None

            id_date_fin = None
            if titre.dateFinLicence:
                date_fin = entrepot_session.query(TempsDim).filter_by(
                    jour=titre.dateFinLicence.day,
                    mois=titre.dateFinLicence.month,
                    annee=titre.dateFinLicence.year
                ).first()
                id_date_fin = date_fin.idDate if date_fin else None

            titre_dim = TitreDim(
                idTitre=titre.idTitre,
                nom=titre.nom,
                annee=titre.annee,
                iddateDebutLicence=id_date_debut,
                iddateFinLicence=id_date_fin,
                categorieAge=titre.categorieAge,
                typeTitre=titre.typeTitre,
                description=titre.description,
                idGenre=titre.idGenre
            )
            entrepot_session.merge(titre_dim)

        entrepot_session.commit()
    print(f"{len(source_titres)} titres traités")


def process_paiement_fact():
    """Extrait et transforme les paiements"""
    print("Traitement des faits de Paiement...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        source_paiements = session.execute(text("""
                SELECT p.idPaiement, a.idUtilisateur, p.idAbonnement, p.datePaiement, 
                       p.montant, p.statusPaiement
                FROM Paiement p
                JOIN Abonnement a ON p.idAbonnement = a.idAbonnement
            """)).fetchall()

        for paiement in source_paiements:
            id_date = None
            if paiement.datePaiement:
                date = entrepot_session.query(TempsDim).filter_by(
                    jour=paiement.datePaiement.day,
                    mois=paiement.datePaiement.month,
                    annee=paiement.datePaiement.year
                ).first()
                id_date = date.idDate if date else None

            paiement_fact = PaiementFact(
                idPaiement=paiement.idPaiement,
                idUtilisateur=paiement.idUtilisateur,
                idAbonnement=paiement.idAbonnement,
                idDate=id_date,
                montant=paiement.montant,
                statusPaiement=paiement.statusPaiement
            )
            entrepot_session.merge(paiement_fact)

        entrepot_session.commit()
    print(f"{len(source_paiements)} paiements traités")


def process_visionnage_fact():
    """Extrait et transforme les visionnages"""
    #A implémenter car dans script de base pas de visionnage


def process_evaluation_fact():
    """Extrait et transforme les évaluations"""
    print("Traitement des faits d'Évaluation...")

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        source_evaluations = session.execute(text("""
                SELECT e.idEvaluation, u.idUtilisateur, e.idTitre, tg.idGenre, e.note, e.avis, 
                       CURRENT_DATE() as dateEvaluation
                FROM Evaluation e
                JOIN Profil p ON e.idProfil = p.idProfil
                JOIN Utilisateur u ON p.idUtilisateur = u.idUtilisateur
                LEFT JOIN TitreGenre tg ON e.idTitre = tg.idTitre
            """)).fetchall()

        for eval in source_evaluations:
            id_date = None
            if eval.dateEvaluation:
                date = entrepot_session.query(TempsDim).filter_by(
                    jour=eval.dateEvaluation.day,
                    mois=eval.dateEvaluation.month,
                    annee=eval.dateEvaluation.year
                ).first()
                id_date = date.idDate if date else None

            evaluation_fact = EvaluationFact(
                idEvaluation=eval.idEvaluation,
                idUtilisateur=eval.idUtilisateur,
                idTitre=eval.idTitre,
                idGenre=eval.idGenre,
                idDate=id_date,
                note=eval.note,
                avis=eval.avis
            )
            entrepot_session.merge(evaluation_fact)

        entrepot_session.commit()
    print(f"{len(source_evaluations)} évaluations traitées")


def process_film_dim():
    """Extrait et transforme les films"""
    print("Traitement de la dimension Film...")
    record_count = 0

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        films = session.execute(text("""
                SELECT f.idFilm, f.idTitre, f.duree, t.nom
                FROM Film f
                JOIN Titre t ON f.idTitre = t.idTitre
            """)).fetchall()

        for film in films:
            titre = entrepot_session.query(TitreDim).get(film.idTitre)
            if titre:
                film_dim = FilmEntrepot(
                    idFilm=film.idFilm,
                    idTitre=film.idTitre,
                    duree=film.duree
                )
                entrepot_session.merge(film_dim)
                record_count += 1

        entrepot_session.commit()
    print(f"{record_count} films traités")
    return record_count


def process_serie_dim():
    """Extrait et transforme les séries"""
    print("Traitement de la dimension Série...")
    record_count = 0

    with get_main_db_session() as session, get_db_entrepot_session() as entrepot_session:
        series = session.execute(text("""
                SELECT s.idSerie, s.idTitre, s.saison, t.nom
                FROM Serie s
                JOIN Titre t ON s.idTitre = t.idTitre
            """)).fetchall()

        for serie in series:
            titre = entrepot_session.query(TitreDim).get(serie.idTitre)
            if titre:
                serie_dim = SerieEntrepot(
                    idSerie=serie.idSerie,
                    idTitre=serie.idTitre,
                    saison=serie.saison
                )
                entrepot_session.merge(serie_dim)
                record_count += 1

        entrepot_session.commit()
    print(f"{record_count} séries traitées")
    return record_count
