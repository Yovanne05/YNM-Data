-- Création du schéma NetflixDB
CREATE SCHEMA IF NOT EXISTS NetflixDB;
SET search_path TO NetflixDB;

DROP TABLE IF EXISTS Paiement, Evaluation, Top10Titre, Soustitre, Audio, MaListe, Profil, Abonnement, Utilisateur, Realisation, Studio, Acting, Acteur, TitreGenre, Genre, Film, Serie, Langue CASCADE;

-- Table des Utilisateurs
CREATE TABLE Utilisateur (
    idUtilisateur SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),
    paysResidance VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    numero VARCHAR(15) UNIQUE NOT NULL,
    statutAbonnement VARCHAR(20) DEFAULT 'Actif' CHECK (statutAbonnement IN ('Actif', 'Résilié'))
);


CREATE TABLE Abonnement (
    idAbonnement SERIAL PRIMARY KEY,
    idUtilisateur INT UNIQUE NOT NULL,
    typeAbonnement VARCHAR(50) NOT NULL
        CHECK (typeAbonnement IN ('Basic', 'Standard', 'Premium')),
    prix DECIMAL(6,2) NOT NULL
        CHECK (prix > 0 AND prix <= 20.00),
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur) ON DELETE CASCADE
);


-- Table de Paiement
CREATE TABLE Paiement (
    idPaiement SERIAL PRIMARY KEY,
    idAbonnement INT NOT NULL,
    datePaiement DATE NOT NULL,
    montant DECIMAL(6,2) NOT NULL,
    statusPaiement VARCHAR(20) CHECK (statusPaiement IN ('Effectué', 'Échoué')),
    FOREIGN KEY (idAbonnement) REFERENCES Abonnement(idAbonnement) ON DELETE CASCADE
);


-- Table des Profils
CREATE TABLE Profil (
    idProfil SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    typeProfil VARCHAR(10) CHECK (typeProfil IN ('Adulte', 'Enfant')) NOT NULL DEFAULT 'Adulte',
    idUtilisateur INT NOT NULL,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur) ON DELETE CASCADE
);

-- Table MaListe
CREATE TABLE MaListe (
    idMaListe SERIAL PRIMARY KEY,
    idProfil INT NOT NULL,
    idTitre INT NOT NULL,
    FOREIGN KEY (idProfil) REFERENCES Profil(idProfil) ON DELETE CASCADE,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);


-- Table Titre (Film et Série partagent cette table)
CREATE TABLE Titre (
    idTitre SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    annee INT NOT NULL CHECK (annee >= 1900 AND annee <= EXTRACT(YEAR FROM CURRENT_DATE) + 5),  -- Ajout d'une borne supérieure réaliste
    dateDebutLicence DATE NOT NULL,
    dateFinLicence DATE NOT NULL,
    categorieAge VARCHAR(50) NOT NULL CHECK (categorieAge IN ('Tout public', '12+', '16+', '18+')),
    description TEXT,
    CONSTRAINT chk_validite_licence CHECK (dateFinLicence > dateDebutLicence),
    CONSTRAINT chk_annee_coherente CHECK (annee <= EXTRACT(YEAR FROM dateDebutLicence))  -- L'année ne peut pas être postérieure à la date de début de licence
);

-- Table des Films
CREATE TABLE Film (
    idFilm SERIAL PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    duree INT CHECK (duree > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Table des Séries
CREATE TABLE Serie (
    idSerie SERIAL PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    saison INT CHECK (saison > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Table des Genres
CREATE TABLE Genre (
    idGenre SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

-- Table des relations entre Titres et Genres
CREATE TABLE TitreGenre (
    idTitre INT NOT NULL,
    idGenre INT NOT NULL,
    PRIMARY KEY (idTitre, idGenre),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idGenre) REFERENCES Genre(idGenre) ON DELETE CASCADE
);

-- Table des Langues
CREATE TABLE Langue (
    idLangue SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Langue_Disponible (
    idLangueDispo SERIAL PRIMARY KEY,
    idTitre INT NOT NULL,
    idLangue INT NOT NULL,
    typeLangue VARCHAR(15) CHECK (typeLangue IN ('audio', 'sous-titre')),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idLangue) REFERENCES Langue(idLangue) ON DELETE CASCADE
);


-- Table des Acteurs
CREATE TABLE Acteur (
    idActeur SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dateNaissance DATE NOT NULL,
    dateDeces DATE NULL
);

-- Table des relations entre Titres et Acteurs
CREATE TABLE Acting (
    idActing SERIAL PRIMARY KEY,
    idTitre INT NOT NULL,
    idActeur INT NOT NULL,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idActeur) REFERENCES Acteur(idActeur) ON DELETE CASCADE
);

-- Table des Studios
CREATE TABLE Studio (
    idStudio SERIAL PRIMARY KEY,
    nom VARCHAR(255) UNIQUE NOT NULL,
    pays VARCHAR(100) NOT NULL
);

-- Table des Réalisations
CREATE TABLE Realisation (
    idRealisation SERIAL PRIMARY KEY,
    idTitre INT NOT NULL,
    idStudio INT NOT NULL,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idStudio) REFERENCES Studio(idStudio) ON DELETE CASCADE
);



-- Table des Evaluations
CREATE TABLE Evaluation (
    idEvaluation SERIAL PRIMARY KEY,
    idProfil INT NOT NULL,
    idTitre INT NOT NULL,
    note INT CHECK (note BETWEEN 1 AND 5),
    avis TEXT,
    FOREIGN KEY (idProfil) REFERENCES Profil(idProfil) ON DELETE CASCADE,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Ajout des index pour optimiser les performances
CREATE INDEX idx_utilisateur_email ON Utilisateur(email);
CREATE INDEX idx_titre_nom ON Titre(nom);