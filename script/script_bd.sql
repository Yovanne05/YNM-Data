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

DELIMITER //

CREATE TRIGGER verif_utilisateur_age
BEFORE INSERT ON Utilisateur
FOR EACH ROW
BEGIN
  IF NEW.age IS NOT NULL AND NEW.age < 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Lâge doit être positif ou nul.';
  END IF;
END;
//

DELIMITER ;


-- Table Abonnement
CREATE TABLE Abonnement (
    idAbonnement INT AUTO_INCREMENT PRIMARY KEY,
    idUtilisateur INT UNIQUE NOT NULL,
    typeAbonnement ENUM('Basic', 'Standard', 'Premium') NOT NULL,
    prix DECIMAL(6,2) NOT NULL CHECK (prix > 0 AND prix <= 20.00),
    FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur) ON DELETE CASCADE
);


DELIMITER //

CREATE TRIGGER verif_abonnement_prix
BEFORE INSERT ON Abonnement
FOR EACH ROW
BEGIN
  IF NEW.prix <= 0 OR NEW.prix > 20.00 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Le prix de labonnement doit être compris entre 0.01 et 20.00 €.';
  END IF;
END;
//

DELIMITER ;

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

DELIMITER //

CREATE TRIGGER verif_titre_annee
BEFORE INSERT ON Titre
FOR EACH ROW
BEGIN
  IF NEW.annee < 1900 OR NEW.annee > YEAR(CURDATE()) + 5 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'L’année doit être comprise entre 1900 et 5 ans après l’année actuelle.';
  END IF;
END;
//

CREATE TRIGGER verif_titre_annee_update
BEFORE UPDATE ON Titre
FOR EACH ROW
BEGIN
  IF NEW.annee < 1900 OR NEW.annee > YEAR(CURDATE()) + 5 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'L’année doit être comprise entre 1900 et 5 ans après l’année actuelle.';
  END IF;
END;
//

DELIMITER ;

DELIMITER //

CREATE TRIGGER verif_titre_insert
BEFORE INSERT ON Titre
FOR EACH ROW
BEGIN
  IF NEW.dateFinLicence <= NEW.dateDebutLicence THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'La date de fin de licence doit être après la date de début.';
  END IF;

  IF NEW.annee > YEAR(NEW.dateDebutLicence) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Lannée doit être inférieure ou égale à lannée de début de licence.';
  END IF;
END;
//

DELIMITER ;


DELIMITER //

CREATE TRIGGER verif_titre_update
BEFORE UPDATE ON Titre
FOR EACH ROW
BEGIN
  IF NEW.dateFinLicence <= NEW.dateDebutLicence THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'La date de fin de licence doit être après la date de début.';
  END IF;

  IF NEW.annee > YEAR(NEW.dateDebutLicence) THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Lannée doit être inférieure ou égale à lannée de début de licence.';
  END IF;
END;
//

DELIMITER ;




-- Table Film
CREATE TABLE Film (
    idFilm INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    duree INT CHECK (duree > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER verif_film_duree
BEFORE INSERT ON Film
FOR EACH ROW
BEGIN
  IF NEW.duree <= 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'La durée du film doit être strictement positive.';
  END IF;
END;
//

DELIMITER ;


-- Table Serie
CREATE TABLE Serie (
    idSerie INT AUTO_INCREMENT PRIMARY KEY,
    idTitre INT UNIQUE NOT NULL,
    saison INT CHECK (saison > 0),
    FOREIGN KEY (idTitre) REFERENCES Titre(idTitre) ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER verif_serie_saison
BEFORE INSERT ON Serie
FOR EACH ROW
BEGIN
  IF NEW.saison <= 0 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'Le nombre de saisons doit être strictement positif.';
  END IF;
END;
//

DELIMITER ;


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


DELIMITER //

CREATE TRIGGER verif_evaluation_note
BEFORE INSERT ON Evaluation
FOR EACH ROW
BEGIN
  IF NEW.note < 1 OR NEW.note > 5 THEN
    SIGNAL SQLSTATE '45000'
    SET MESSAGE_TEXT = 'La note doit être comprise entre 1 et 5.';
  END IF;
END;
//

DELIMITER ;

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
