CREATE TABLE Serie (
    idSerie INT PRIMARY KEY,
    nom VARCHAR(255),
    genre VARCHAR(100),
    saison INT,
    annee INT,
    dateDebutLicence DATE,
    dateFinLicence DATE,
    categorieAge VARCHAR(50),
    description TEXT
);

CREATE TABLE Film (
    idFilm INT PRIMARY KEY,
    nom VARCHAR(255),
    annee INT,
    duree VARCHAR(50),
    dateDebutLicence DATE,
    dateFinLicence DATE,
    genre VARCHAR(100),
    categorieAge VARCHAR(50),
    description TEXT
);

CREATE TABLE Studio (
    idStudio INT PRIMARY KEY,
    nom VARCHAR(255),
    pays VARCHAR(100)
);

CREATE TABLE Langue (
    idLangue INT PRIMARY KEY,
    nom VARCHAR(100)
);

CREATE TABLE Utilisateur (
    idUtilisateur INT PRIMARY KEY,
    age INT,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    paysResidance VARCHAR(100),
    email VARCHAR(255),
    numero INT
);

CREATE TABLE Acteur (
    idActeur INT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    dateNaissance DATE,
    dateDeces DATE
);

CREATE TABLE Acting (
    idActing INT PRIMARY KEY,
    idFilm INT,
    idSerie INT,
    idActeur INT,
    CONSTRAINT fk_Acting_Film FOREIGN KEY (idFilm) REFERENCES Film(idFilm),
    CONSTRAINT fk_Acting_Serie FOREIGN KEY (idSerie) REFERENCES Serie(idSerie),
    CONSTRAINT fk_Acting_Acteur FOREIGN KEY (idActeur) REFERENCES Acteur(idActeur)
);

CREATE TABLE Realisation (
    idRealisation INT PRIMARY KEY,
    idFilm INT,
    idSerie INT,
    idRealisateur INT,
    idStudio INT,
    CONSTRAINT fk_Realisation_Film FOREIGN KEY (idFilm) REFERENCES Film(idFilm),
    CONSTRAINT fk_Realisation_Serie FOREIGN KEY (idSerie) REFERENCES Serie(idSerie),
    CONSTRAINT fk_Realisation_Studio FOREIGN KEY (idStudio) REFERENCES Studio(idStudio)
);

CREATE TABLE Profil (
    idProfil INT PRIMARY KEY,
    nom VARCHAR(100),
    typeDeProfil VARCHAR(50),
    idUtilisateur INT,
    CONSTRAINT fk_Profil_Utilisateur FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur)
);

CREATE TABLE Liste (
    idListe INT PRIMARY KEY,
    idProfil INT,
    CONSTRAINT fk_Liste_Profil FOREIGN KEY (idProfil) REFERENCES Profil(idProfil)
);

CREATE TABLE MaListe (
    idMaListe INT PRIMARY KEY,
    idFilm INT,
    idSerie INT,
    idListe INT,
    CONSTRAINT fk_MaListe_Film FOREIGN KEY (idFilm) REFERENCES Film(idFilm),
    CONSTRAINT fk_MaListe_Serie FOREIGN KEY (idSerie) REFERENCES Serie(idSerie),
    CONSTRAINT fk_MaListe_Liste FOREIGN KEY (idListe) REFERENCES Liste(idListe)
);

CREATE TABLE Audio (
    idAudio INT PRIMARY KEY,
    idFilm INT,
    idSerie INT,
    idLangue INT,
    CONSTRAINT fk_Audio_Film FOREIGN KEY (idFilm) REFERENCES Film(idFilm),
    CONSTRAINT fk_Audio_Serie FOREIGN KEY (idSerie) REFERENCES Serie(idSerie),
    CONSTRAINT fk_Audio_Langue FOREIGN KEY (idLangue) REFERENCES Langue(idLangue)
);

CREATE TABLE Soustitre (
    idSoustitre INT PRIMARY KEY,
    idFilm INT,
    idSerie INT,
    idLangue INT,
    CONSTRAINT fk_Soustitre_Film FOREIGN KEY (idFilm) REFERENCES Film(idFilm),
    CONSTRAINT fk_Soustitre_Serie FOREIGN KEY (idSerie) REFERENCES Serie(idSerie),
    CONSTRAINT fk_Soustitre_Langue FOREIGN KEY (idLangue) REFERENCES Langue(idLangue)
);

CREATE TABLE Top10Serie (
    idTop10Serie INT PRIMARY KEY,
    pays VARCHAR(100),
    idSerie INT,
    classement INT,
    dateTop10 DATE,
    CONSTRAINT fk_Top10Serie_Serie FOREIGN KEY (idSerie) REFERENCES Serie(idSerie)
);

CREATE TABLE Top10Film (
    idTop10Film INT PRIMARY KEY,
    classement INT,
    pays VARCHAR(100),
    dateTop10 DATE,
    idFilm INT,
    CONSTRAINT fk_Top10Film_Film FOREIGN KEY (idFilm) REFERENCES Film(idFilm)
);

CREATE TABLE Evaluation (
    idEvaluation INT PRIMARY KEY,
    idProfil INT,
    idSerie INT,
    idFilm INT,
    avis VARCHAR(255),
    CONSTRAINT fk_Evaluation_Profil FOREIGN KEY (idProfil) REFERENCES Profil(idProfil),
    CONSTRAINT fk_Evaluation_Serie FOREIGN KEY (idSerie) REFERENCES Serie(idSerie),
    CONSTRAINT fk_Evaluation_Film FOREIGN KEY (idFilm) REFERENCES Film(idFilm)
);

CREATE TABLE Abonnement (
    idAbonnement INT PRIMARY KEY,
    prix INT,
    idUtilisateur INT,
    typeAbonnement VARCHAR(50),
    CONSTRAINT fk_Abonnement_Utilisateur FOREIGN KEY (idUtilisateur) REFERENCES Utilisateur(idUtilisateur)
);

;
