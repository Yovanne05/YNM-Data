-- Création du schéma NetflixDB
CREATE DATABASE IF NOT EXISTS Entrepot_Netflix;
USE Entrepot_Netflix;

-- Suppression des tables dans le bon ordre
DROP TABLE IF EXISTS Paiement, Evaluation, Langue_Disponible, MaListe, Profil, Abonnement, Utilisateur, Realisation, Studio, Acting, Acteur, TitreGenre, Genre, Film, Serie, Titre, Langue CASCADE;

-- Table des Utilisateurs
CREATE TABLE Utilisateur (
    idUtilisateur BIGINT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    age INT CHECK (age >= 0),
    paysResidence VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    numero VARCHAR(15) UNIQUE NOT NULL,
    statutAbonnement VARCHAR(20) DEFAULT 'Actif',
    CHECK (statutAbonnement IN ('Actif', 'Résilié'))
);

-- Création de la table Abonnement
CREATE TABLE IF NOT EXISTS Abonnement (
    idAbonnement INT AUTO_INCREMENT PRIMARY KEY,
    typeAbonnement VARCHAR(50),
    prix DECIMAL(6,2)
);

-- Création de la table Temps
CREATE TABLE IF NOT EXISTS Temps (
    idDate INT AUTO_INCREMENT PRIMARY KEY,
    jour INT,
    mois INT,
    annee INT,
    trimestre INT
);

-- Création de la table Titre
CREATE TABLE IF NOT EXISTS Titre (
    idTitre INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255),
    annee INT,
    iddateDebutLicence INT,
    iddateFinLicence INT,
    categorieAge VARCHAR(50) CHECK (categorieAge IN ('Tout public', '12+', '16+', '18+')),
    description TEXT,
    FOREIGN KEY (iddateDebutLicence) REFERENCES Temps(idDate) ON DELETE SET NULL,
    FOREIGN KEY (iddateFinLicence) REFERENCES Temps(idDate) ON DELETE SET NULL
);

-- Création de la table Serie
CREATE TABLE IF NOT EXISTS Serie (
    idSerie INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    saison INT CHECK (saison > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre)
);

-- Création de la table Film
CREATE TABLE IF NOT EXISTS Film (
    idFilm INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    duree INT CHECK (duree > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre)
);

-- Création de la table Genre
CREATE TABLE IF NOT EXISTS Genre (
    idGenre INT AUTO_INCREMENT PRIMARY KEY,
    nomGenre VARCHAR(50)
);

-- Création de la table Langue
CREATE TABLE IF NOT EXISTS Langue (
    idLangue INT AUTO_INCREMENT PRIMARY KEY,
    nomLangue VARCHAR(50)
);

-- Création de la table Langue_Disponible
CREATE TABLE IF NOT EXISTS Langue_Disponible (
    idLangueDispo INT AUTO_INCREMENT PRIMARY KEY,
    idLangue INT NOT NULL,
    typeLangue VARCHAR(15) CHECK (typeLangue IN ('audio', 'sous-titre')),
    FOREIGN KEY (idLangue) REFERENCES Langue(idLangue) ON DELETE CASCADE
);

-- Création de la table Visionnage
CREATE TABLE IF NOT EXISTS Visionnage (
    idVisionnage INT AUTO_INCREMENT PRIMARY KEY,
    idUtilisateur INT,
    idTitre INT,
    idDate INT,
    idGenre INT,
    idLangueDispo INT,
    dureeVisionnage INT,  -- durée en minutes
    nombreVues INT DEFAULT 1,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre),
    FOREIGN KEY (idDate) REFERENCES Temps(idDate),
    FOREIGN KEY (idLangueDispo) REFERENCES Langue_Disponible(idLangueDispo),
    FOREIGN KEY (idGenre) REFERENCES Genre(idGenre)
);

-- Création de la table Evaluation
CREATE TABLE IF NOT EXISTS Evaluation (
    idEvaluation INT AUTO_INCREMENT PRIMARY KEY,
    idUtilisateur INT,
    idTitre INT,
    idGenre INT,
    idDate INT,
    note INT,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre),
    FOREIGN KEY (idDate) REFERENCES Temps(idDate),
    FOREIGN KEY (idGenre) REFERENCES Genre(idGenre)
);

-- Création de la table Paiement
CREATE TABLE IF NOT EXISTS Paiement (
    idPaiement INT AUTO_INCREMENT PRIMARY KEY,
    idUtilisateur INT NOT NULL,
    idAbonnement INT NOT NULL,
    idDate INT NOT NULL,
    montant DECIMAL(6,2),
    statusPaiement VARCHAR(20),
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY (idAbonnement) REFERENCES Abonnement(idAbonnement),
    FOREIGN KEY (idDate) REFERENCES Temps(idDate)
);
