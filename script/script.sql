-- Création du schéma NetflixDB
CREATE SCHEMA IF NOT EXISTS NetflixDB;
USE NetflixDB;

-- Suppression des tables dans le bon ordre
DROP TABLE IF EXISTS Paiement, Evaluation, Langue_Disponible, MaListe, Profil, Abonnement, Utilisateur, Realisation, Studio, Acting, Acteur, TitreGenre, Genre, Film, Serie, Titre, Langue;

-- Table des Utilisateurs
CREATE TABLE Utilisateur (
    idUtilisateur BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),
    paysResidance VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    numero VARCHAR(15) UNIQUE NOT NULL,
    statutAbonnement VARCHAR(20) DEFAULT 'Actif' CHECK (statutAbonnement IN ('Actif', 'Résilié'))
);

-- Table des Abonnements
CREATE TABLE Abonnement (
    idAbonnement BIGINT AUTO_INCREMENT PRIMARY KEY,
    idUtilisateur BIGINT UNIQUE NOT NULL,
    typeAbonnement VARCHAR(50) NOT NULL,
    prix DECIMAL(6,2) NOT NULL,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur) ON DELETE CASCADE
);

-- Table des Profils
CREATE TABLE Profil (
    idProfil BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    typeProfil VARCHAR(10) CHECK (typeProfil IN ('Adulte', 'Enfant')) NOT NULL DEFAULT 'Adulte',
    idUtilisateur BIGINT NOT NULL,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur) ON DELETE CASCADE
);

-- Table des Titres (Film et Série partagent cette table)
CREATE TABLE Titre (
    idTitre BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    annee INT CHECK (annee >= 1900),
    dateDebutLicence DATE NOT NULL,
    dateFinLicence DATE NOT NULL,
    categorieAge VARCHAR(50),
    description TEXT
);

-- Table des Films
CREATE TABLE Film (
    idFilm BIGINT AUTO_INCREMENT PRIMARY KEY,
    idTitre BIGINT UNIQUE NOT NULL,
    duree INT CHECK (duree > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Table des Séries
CREATE TABLE Serie (
    idSerie BIGINT AUTO_INCREMENT PRIMARY KEY,
    idTitre BIGINT UNIQUE NOT NULL,
    saison INT CHECK (saison > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Table des Genres
CREATE TABLE Genre (
    idGenre BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

-- Table des relations entre Titres et Genres
CREATE TABLE TitreGenre (
    idTitre BIGINT NOT NULL,
    idGenre BIGINT NOT NULL,
    PRIMARY KEY (idTitre, idGenre),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idGenre) REFERENCES Genre(idGenre) ON DELETE CASCADE
);

-- Table des Langues
CREATE TABLE Langue (
    idLangue BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

-- Table des Langues Disponibles pour les Titres
CREATE TABLE Langue_Disponible (
    idLangueDispo BIGINT AUTO_INCREMENT PRIMARY KEY,
    idTitre BIGINT NOT NULL,
    idLangue BIGINT NOT NULL,
    typeLangue VARCHAR(15) CHECK (typeLangue IN ('audio', 'sous-titre')),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idLangue) REFERENCES Langue(idLangue) ON DELETE CASCADE
);

-- Table des Acteurs
CREATE TABLE Acteur (
    idActeur BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dateNaissance DATE NOT NULL,
    dateDeces DATE NULL
);

-- Table des relations entre Titres et Acteurs
CREATE TABLE Acting (
    idActing BIGINT AUTO_INCREMENT PRIMARY KEY,
    idTitre BIGINT NOT NULL,
    idActeur BIGINT NOT NULL,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idActeur) REFERENCES Acteur(idActeur) ON DELETE CASCADE
);

-- Table des Studios
CREATE TABLE Studio (
    idStudio BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) UNIQUE NOT NULL,
    pays VARCHAR(100) NOT NULL
);

-- Table des Réalisations
CREATE TABLE Realisation (
    idRealisation BIGINT AUTO_INCREMENT PRIMARY KEY,
    idTitre BIGINT NOT NULL,
    idStudio BIGINT NOT NULL,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idStudio) REFERENCES Studio(idStudio) ON DELETE CASCADE
);

-- Table MaListe
CREATE TABLE MaListe (
    idMaListe BIGINT AUTO_INCREMENT PRIMARY KEY,
    idProfil BIGINT NOT NULL,
    idTitre BIGINT NOT NULL,
    FOREIGN KEY (idProfil) REFERENCES Profil(idProfil) ON DELETE CASCADE,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Table de Paiement
CREATE TABLE Paiement (
    idPaiement BIGINT AUTO_INCREMENT PRIMARY KEY,
    idAbonnement BIGINT NOT NULL,
    datePaiement DATE NOT NULL,
    montant DECIMAL(6,2) NOT NULL,
    statusPaiement VARCHAR(20) CHECK (statusPaiement IN ('Effectué', 'Échoué')),
    FOREIGN KEY (idAbonnement) REFERENCES Abonnement(idAbonnement) ON DELETE CASCADE
);

-- Table des Evaluations
CREATE TABLE Evaluation (
    idEvaluation BIGINT AUTO_INCREMENT PRIMARY KEY,
    idProfil BIGINT NOT NULL,
    idTitre BIGINT NOT NULL,
    note INT CHECK (note BETWEEN 1 AND 5),
    avis VARCHAR(255),
    FOREIGN KEY (idProfil) REFERENCES Profil(idProfil) ON DELETE CASCADE,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Ajout des index pour optimiser les performances
CREATE INDEX idx_utilisateur_email ON Utilisateur(email);
CREATE INDEX idx_titre_nom ON Titre(nom);
