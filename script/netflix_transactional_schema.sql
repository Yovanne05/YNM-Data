-- Création de la base de données
CREATE DATABASE IF NOT EXISTS NetflixDB;
USE NetflixDB;

DROP TABLE IF EXISTS Paiement, Evaluation, TitreGenre, Langue_Disponible, Acting, Realisation, Studio, Acteur, Langue, Genre, MaListe, Profil, Abonnement, Utilisateur, Film, Serie, Titre;

-- Table Utilisateur
CREATE TABLE Utilisateur (
    idUtilisateur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    age INT ,
    paysResidance VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    numero VARCHAR(15) UNIQUE NOT NULL,
    statutAbonnement ENUM('Actif', 'Résilié') DEFAULT 'Actif'
);

-- Table Abonnement
CREATE TABLE Abonnement (
    idAbonnement INT AUTO_INCREMENT PRIMARY KEY,
    idUtilisateur INT UNIQUE NOT NULL,
    typeAbonnement ENUM('Basic', 'Standard', 'Premium') NOT NULL,
    prix DECIMAL(6,2) NOT NULL CHECK (prix > 0 AND prix <= 20.00),
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur) ON DELETE CASCADE
);

-- Table Paiement
CREATE TABLE Paiement (
    idPaiement INT AUTO_INCREMENT PRIMARY KEY,
    idAbonnement INT NOT NULL,
    datePaiement DATE NOT NULL,
    montant DECIMAL(6,2) NOT NULL,
    statusPaiement ENUM('Effectué', 'Échoué'),
    FOREIGN KEY (idAbonnement) REFERENCES Abonnement(idAbonnement) ON DELETE CASCADE
);

-- Table Profil
CREATE TABLE Profil (
    idProfil INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    typeProfil ENUM('Adulte', 'Enfant') DEFAULT 'Adulte' NOT NULL,
    idUtilisateur INT NOT NULL,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur) ON DELETE CASCADE
);

-- Table Titre
CREATE TABLE Titre (
    idTitre INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    annee INT NOT NULL,
    dateDebutLicence DATE NOT NULL,
    dateFinLicence DATE NOT NULL,
    categorieAge ENUM('Tout public', '12+', '16+', '18+') NOT NULL,
    description TEXT
);

-- Table Film
CREATE TABLE Film (
    idFilm INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    duree INT CHECK (duree > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);
-- Table Serie
CREATE TABLE Serie (
    idSerie INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    saison INT CHECK (saison > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Table Genre
CREATE TABLE Genre (
    idGenre INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

-- Table TitreGenre
CREATE TABLE TitreGenre (
    idTitre INT NOT NULL,
    idGenre INT NOT NULL,
    PRIMARY KEY (idTitre, idGenre),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idGenre) REFERENCES Genre(idGenre) ON DELETE CASCADE
);

-- Table Langue
CREATE TABLE Langue (
    idLangue INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

-- Table Langue_Disponible
CREATE TABLE Langue_Disponible (
    idLangueDisponible INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT NOT NULL,
    idLangue INT NOT NULL,
    typeLangue ENUM('audio', 'sous-titre'),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idLangue) REFERENCES Langue(idLangue) ON DELETE CASCADE
);

-- Table Acteur
CREATE TABLE Acteur (
    idActeur INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    dateNaissance DATE NOT NULL,
    dateDeces DATE NULL
);

-- Table Acting
CREATE TABLE Acting (
    idActing INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT NOT NULL,
    idActeur INT NOT NULL,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idActeur) REFERENCES Acteur(idActeur) ON DELETE CASCADE
);

-- Table Studio
CREATE TABLE Studio (
    idStudio INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) UNIQUE NOT NULL,
    pays VARCHAR(100) NOT NULL
);

-- Table Realisation
CREATE TABLE Realisation (
    idRealisation INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT NOT NULL,
    idStudio INT NOT NULL,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE,
    FOREIGN KEY (idStudio) REFERENCES Studio(idStudio) ON DELETE CASCADE
);

-- Table Evaluation
CREATE TABLE Evaluation (
    idEvaluation INT AUTO_INCREMENT PRIMARY KEY,
    idProfil INT NOT NULL,
    idTitre INT NOT NULL,
    note INT CHECK (note BETWEEN 1 AND 5),
    avis TEXT,
    FOREIGN KEY (idProfil) REFERENCES Profil(idProfil) ON DELETE CASCADE,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Table MaListe
CREATE TABLE MaListe (
    idMaListe INT AUTO_INCREMENT PRIMARY KEY,
    idProfil INT NOT NULL,
    idTitre INT NOT NULL,
    FOREIGN KEY (idProfil) REFERENCES Profil(idProfil) ON DELETE CASCADE,
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

-- Index pour performance
CREATE INDEX idx_utilisateur_email ON Utilisateur(email);
CREATE INDEX idx_titre_nom ON Titre(nom);
