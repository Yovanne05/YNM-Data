CREATE SCHEMA IF NOT EXISTS Entrepot_Netflix;
USE Entrepot_Netflix;

CREATE TABLE Utilisateur
(
    idUtilisateur    INT AUTO_INCREMENT PRIMARY KEY,
    nom              VARCHAR(100),
    prenom           VARCHAR(100),
    age              INT CHECK (age >= 0),
    paysResidence    VARCHAR(100),
    email            VARCHAR(255) UNIQUE NOT NULL,
    numero           VARCHAR(15) UNIQUE  NOT NULL,
    statutAbonnement VARCHAR(20) DEFAULT 'Actif' CHECK (statutAbonnement IN ('Actif', 'Résilié'))
)
;

CREATE TABLE Abonnement
(
    idAbonnement   INT AUTO_INCREMENT PRIMARY KEY,
    typeAbonnement VARCHAR(50),
    prix           DECIMAL(6, 2)
)
;

-- Table Temps
CREATE TABLE Temps (
    idDate INT AUTO_INCREMENT PRIMARY KEY,
    jour INT,
    mois INT,
    annee INT,
    trimestre INT,
    jour_semaine INT,
    est_weekend BOOLEAN
);

-- Table Genre
CREATE TABLE Genre (
    idGenre INT AUTO_INCREMENT PRIMARY KEY,
    nomGenre VARCHAR(50)
);

CREATE TABLE Titre (
    idTitre INT AUTO_INCREMENT PRIMARY KEY,
    idGenre INT,
    nom VARCHAR(255),
    annee INT,
    iddateDebutLicence INT,
    iddateFinLicence INT,
    categorieAge VARCHAR(50)  CHECK (categorieAge IN ('Tout public', '12+', '16+', '18+')),
    typeTitre VARCHAR(10) CHECK (typeTitre IN ('film', 'série')),
    description TEXT,
    FOREIGN KEY (iddateDebutLicence) REFERENCES Temps(idDate) ON DELETE SET NULL,
    FOREIGN KEY (iddateFinLicence) REFERENCES Temps(idDate) ON DELETE SET NULL,
    FOREIGN KEY (idGenre) REFERENCES Genre(idGenre) ON DELETE SET NULL

);

-- Table Serie
CREATE TABLE Serie (
    idSerie INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    saison INT CHECK (saison > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre)
);

-- Table Film
CREATE TABLE Film (
    idFilm INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    duree INT CHECK (duree > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre)
);


-- Table Langue
CREATE TABLE Langue (
    idLangue INT AUTO_INCREMENT PRIMARY KEY,
    nomLangue VARCHAR(50)
);

-- Table Langue_Disponible (renamed from Langue_Dispo)
CREATE TABLE Langue_Disponible (
    idLangueDisponible INT AUTO_INCREMENT PRIMARY KEY,
    idLangue INT NOT NULL,
    typeLangue VARCHAR(15) CHECK (typeLangue IN ('audio', 'sous-titre')),
    FOREIGN KEY (idLangue) REFERENCES Langue(idLangue) ON DELETE CASCADE
);

-- Table Visionnage
CREATE TABLE Visionnage (
    idVisionnage INT AUTO_INCREMENT PRIMARY KEY,
    idUtilisateur INT,
    idTitre INT,
    idDate INT,
    idGenre INT,
    idLangueDisponible INT,
    dureeVisionnage INT,
    nombreVues INT DEFAULT 1,
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre),
    FOREIGN KEY (idDate) REFERENCES Temps(idDate),
    FOREIGN KEY (idLangueDisponible) REFERENCES Langue_Disponible(idLangueDisponible),
    FOREIGN KEY (idGenre) REFERENCES Genre(idGenre)
);

-- Table Evaluation
CREATE TABLE Evaluation (
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

-- Table Paiement
CREATE TABLE Paiement (
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