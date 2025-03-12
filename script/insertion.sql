-- Insertion de donée

INSERT INTO Netflix.Film (idFilm, nom, annee, duree, dateDebutLicence, dateFinLicence, genre, categorieAge, description) VALUES
(1, 'The Irishman', 2019, '3h29', '2023-01-01', '2025-01-01', 'Crime', '16+', 'Un ancien tueur à gages revient sur sa vie.'),
(2, 'Extraction', 2020, '1h57', '2023-05-01', '2025-05-01', 'Action', '18+', 'Un mercenaire tente de sauver un enfant.'),
(3, 'Bird Box', 2018, '2h04', '2023-01-01', '2024-01-01', 'Thriller', '16+', 'Un monde où les gens doivent éviter de voir une entité mystérieuse.'), 
(4, 'Ad Vitam',2025,'1h38',NULL,NULL,'Thriller','13+','Après avoir échappé à une tentative de meurtre, Franck Lazarev doit retrouver sa femme Leo kidnappée par un mystérieux groupe d hommes armés.'),
(5,'Sous la Seine',2024,'1h44',NULL,NULL,'Film d horreur','16+','Sophia, brillante scientifique, est alertée par Mika, une jeune activiste dévouée à l écologie, de la présence d un grand requin dans les profondeurs du fleuve.'),
(6, 'Inception', 2010, '2h28', '2023-01-01', '2025-01-01', 'Science-fiction', '16+', 'Un voleur utilise des rêves pour extraire des informations secrètes.'),
(7, 'Titanic', 1997, '3h14', '2023-01-01', '2025-01-01', 'Drame', '13+', 'Deux amants se rencontrent à bord du célèbre paquebot.'),
(8, 'Avatar', 2009, '2h42', '2023-01-01', '2025-01-01', 'Science-fiction', '12+', 'Un marine sur une planète étrangère se bat pour défendre son peuple.'),
(9, 'The Matrix', 1999, '2h16', '2023-01-01', '2025-01-01', 'Action', '16+', 'Un hacker découvre la vérité sur le monde qu’il habite et les machines qui le contrôlent.'),
(10, 'Gladiator', 2000, '2h35', '2023-01-01', '2025-01-01', 'Historique', '16+', 'Un général romain cherche à se venger de l’empereur corrompu qui l’a trahi.'),
(11, 'The Dark Knight', 2008, '2h32', '2023-01-01', '2025-01-01', 'Action', '12+', 'Batman doit faire face à un criminel de Gotham : le Joker.'),
(12, 'Avengers: Endgame', 2019, '3h01', '2023-01-01', '2025-01-01', 'Action', '13+', 'Les Avengers s’unissent pour inverser les actions de Thanos.'),
(13, 'Interstellar', 2014, '2h49', '2023-01-01', '2025-01-01', 'Science-fiction', '12+', 'Un groupe de scientifiques part dans l’espace pour sauver l’humanité.'),
(14, 'The Godfather', 1972, '2h55', '2023-01-01', '2025-01-01', 'Crime', '18+', 'L’histoire de la famille Corleone dans le milieu de la mafia.'),
(15, 'The Lion King', 1994, '1h58', '2023-01-01', '2025-01-01', 'Animation', 'Tous publics', 'Un lionceau se bat pour prendre sa place en tant que roi des animaux.')

;


INSERT INTO Netflix.Serie (idSerie, nom, genre, saison, annee, dateDebutLicence, dateFinLicence, categorieAge, description) VALUES
(1, 'Stranger Things', 'Fantastique', 4, 2016, '2023-01-01', '2026-01-01', '16+', 'Un groupe d amis lutte contre des créatures d un autre monde.'),
(2, 'The Witcher', 'Fantasy', 2, 2019, '2023-01-01', '2025-01-01', '18+', 'Les aventures de Geralt de Riv dans un monde magique.'),
(3, 'Money Heist', 'Thriller', 5, 2017, '2023-01-01', '2025-12-31', '18+', 'Un groupe de voleurs tente des braquages incroyables.'),
(4,'Squide Game','Coréen',2,2024,null,null,'16+','Tentés par un prix alléchant en cas de victoire, des centaines de joueurs désargentés acceptent de s affronter lors de jeux pour enfants aux enjeux mortels.'),
(5,'A l aube de l Amerique','Series d action et d aventure',1,2024,null,null,'16+','Fuyant leur passé, une mère et son fils se redéfinissent une famille alors qu ils font face à l horizon de liberté et de cruauté de l Ouest américain.'),
(6,'Le Crime à la racine','Séries dramatiques',1,2025,null,null,'13+','Quand un double meurtre bouleverse une ville suédoise paisible, l enquêteur en chef John promet aux familles éplorées de trouver le coupable.'),
(7,'The Rookie : Le flic de Los Angeles','Séries policières',5,2022,'2023-12-01','2027-12-01','13+','Lorsque sa femme le quitte et que son fils part à l université, John Nolan, la quarantaine, est à un tournant de sa vie. Après avoir assisté à un braquage de banque, il fait ses bagages et part pour Los Angeles, où il espère réaliser un vieux rêve : devenir policier'),
(8, 'The Crown', 'Historique', 6, 2016, '2023-01-01', '2026-01-01', '16+', 'La vie de la reine Elizabeth II et de sa famille royale.'),
(9, 'Breaking Bad', 'Drame', 5, 2008, '2023-01-01', '2026-01-01', '18+', 'Un professeur de chimie devenu producteur de méthamphétamines.'),
(10, 'Dark', 'Science-fiction', 3, 2017, '2023-01-01', '2026-01-01', '16+', 'Un groupe de personnes tente de comprendre des événements mystérieux dans leur ville.'),
(11, 'Narcos', 'Crime', 3, 2015, '2023-01-01', '2025-12-31', '18+', 'Lâcher prise dans le monde impitoyable des narcotrafiquants en Colombie.'),
(12, 'Stranger Things', 'Fantastique', 4, 2016, '2023-01-01', '2026-01-01', '16+', 'Des enfants luttent contre des créatures surnaturelles dans une petite ville.'),
(13, 'The Mandalorian', 'Aventure', 2, 2019, '2023-01-01', '2025-12-31', '13+', 'Un chasseur de primes solitaire dans l’univers de Star Wars.'),
(14, 'The Boys', 'Super-héros', 3, 2019, '2023-01-01', '2026-01-01', '16+', 'Une série sur des super-héros dévoyés et un groupe d’hommes qui les affrontent.'),
(15, 'The Walking Dead', 'Horreur', 11, 2010, '2023-01-01', '2025-12-31', '18+', 'Un groupe de survivants luttent pour rester en vie dans un monde post-apocalyptique.'),
(16, 'Money Heist', 'Thriller', 5, 2017, '2023-01-01', '2025-12-31', '18+', 'Un groupe de braqueurs de banque dissimule leur identité tout en commettant un vol audacieux.')

;


INSERT INTO Netflix.Studio (idStudio, nom, pays) VALUES
(1, 'Paramount Pictures', 'USA'),
(2, 'Universal Studios', 'USA'),
(3, 'Warner Bros', 'USA'),
(4, 'Fox Studios', 'USA'),
(5, 'Columbia Pictures', 'USA'),
(6, 'Sony Pictures', 'USA'),
(7, 'Walt Disney Studios', 'USA'),
(8, 'Lionsgate', 'USA'),
(9, 'MGM Studios', 'USA'),
(10, 'Legendary Entertainment', 'USA'),
(11, 'New Line Cinema', 'USA'),
(12, 'Paramount Animation', 'USA'),
(13, 'Warner Animation Group', 'USA'),
(14, 'Pixar', 'USA'),
(15, 'Blue Sky Studios', 'USA')
;


INSERT INTO Netflix.Langue (idLangue, nom) VALUES
(1, 'Anglais'),
(2, 'Français'),
(3, 'espagnol (Espagne)'),
(4, 'Arabe'),
(5,'Coréen'),
(6,'anglais - Audiodescription'),
(7,'turc - Audiodescription'),
(8,'portugais(Portugal)'),
(9, 'Italien'),
(10, 'Allemand'),
(11, 'Néerlandais'),
(12, 'Danois'),
(13, 'Suédois'),
(14, 'Russe'),
(15, 'Japonais')
;


INSERT INTO Netflix.Utilisateur (idUtilisateur, age, nom, prenom, paysResidance, email, numero) VALUES
(1, 25, 'Dupont', 'Alice', 'France', 'alice.dupont@gmail.com', 0612345678),
(2, 32, 'Cariot', 'Mélina', 'France', 'mel.ctr@gmail.com', 0698765432),
(3, 28, 'Emtir', 'Camillia', 'France', 'cam.emt@gmail.com', 0609080704),
(4, 45, 'Lelant', 'Louise', 'France', 'lou.lan@gmail.com', 0611223344),
(5, 22, 'Nguyen', 'Paul', 'France', 'paul.nguyen@gmail.com', 0667788990),
(6, 30, 'Smith', 'John', 'USA', 'john.smith@yahoo.com', 0699887766),
(7, 19, 'Brown', 'Emily', 'USA', 'emily.brown@hotmail.com', 0655667788),
(8, 35, 'Chen', 'Li', 'Chine', 'li.chen@outlook.com', 0615348679),
(9, 27, 'Garcia', 'Maria', 'Espagne', 'maria.garcia@google.com', 0615786425),
(10, 40, 'Kumar', 'Ravi', 'Inde', 'ravi.kumar@rediffmail.com', 0645873203),
(11, 31, 'Yamamoto', 'Aiko', 'Japon', 'aiko.yamamoto@gmail.com', 0644556677),
(12, 29, 'BenYoussef', 'Liam', 'Maroc', 'liam.ibnyouss@icloud.com', 0678549878),
(13, 26, 'Lopez', 'Isabella', 'Mexique', 'isabella.lopez@gmail.com', 0617894568),
(14, 38, 'Fischer', 'Hans', 'Allemagne', 'hans.fischer@yahoo.de', 0657894618),
(15, 23, 'Ayat', 'Sophia', 'Turquie', 'sophia.ayt@gmail.com', 0633445566),
(16, 25, 'Jackson', 'Tom', 'USA', 'tom.jackson@yahoo.com', 0698877665),
(17, 27, 'Carter', 'Emma', 'Canada', 'emma.carter@outlook.com', 0644556678),
(18, 29, 'Martin', 'Leo', 'France', 'leo.martin@orange.fr', 0677888999),
(19, 22, 'Singh', 'Ravi', 'Inde', 'ravi.singh@gmail.com', 0677889001),
(20, 33, 'Kim', 'Jin', 'Corée du Sud', 'jin.kim@naver.com', 0633445555)

;

INSERT INTO Netflix.Acteur (idActeur, nom, prenom, dateNaissance, dateDeces) VALUES
(1, 'DiCaprio', 'Leonardo', '1974-11-11', NULL),
(2, 'Johansson', 'Scarlett', '1984-11-22', NULL),
(3, 'Washington', 'Denzel', '1954-12-28', NULL),
(4,'Lee','Jung-jae','1972-12-15',NULL), 
(5,'Kitsch','Taylor','1981-04-08',NULL),
(6,'Hallin','Annika','1968-02-16',NULL),
(7,'Lyes','Nassim','1988-06-3',NULL),
(8, 'Hanks', 'Tom', '1956-07-09', NULL),
(9, 'Pitt', 'Brad', '1963-12-18', NULL),
(10, 'Clooney', 'George', '1961-05-06', NULL),
(11, 'Streep', 'Meryl', '1949-06-22', NULL),
(12, 'Winslet', 'Kate', '1975-10-05', NULL),
(13, 'Depp', 'Johnny', '1963-06-09', NULL),
(14, 'Theron', 'Charlize', '1975-08-07', NULL),
(15, 'Smith', 'Will', '1968-09-25', NULL),
(16, 'McConaughey', 'Matthew', '1969-11-04', NULL)
; 



INSERT INTO Netflix.Acting (idActing, idFilm, idSerie, idActeur) VALUES
(1,1, NULL, 1),
(2, 2, NULL, 2),
(3, NULL, 1, 3),
(4,NULL,4,4),
(5,NULL,5,5),
(6,4,NULL,7),
(7,5,NULL,7),
(8, NULL, 8, 8),
(9, NULL, 9, 9),
(10, NULL, 10, 10),
(11, NULL, 11, 11),
(12, NULL, 12, 12),
(13, NULL, 13, 13),
(14, NULL, 14, 14),
(15, NULL, 16, 16)

;

INSERT INTO Netflix.Realisation (idRealisation, idFilm, idSerie, idRealisateur, idStudio) VALUES
(1, 1, NULL, 1, 1),
(2, NULL, 1, 2, 2),
(3, 2, NULL, 3, 1),
(4, NULL, 2, 1, 2),
(5, 3, NULL, 2, 3),
(6, NULL, 3, 3, 1),
(7, 4, NULL, 4, 1),
(8, NULL, 4, 5, 2),
(9, 5, NULL, 6, 3),
(10, NULL, 5, 7, 1),
(11, 1, NULL, 2, 3),
(12, NULL, 6, 1, 2),
(13, 2, NULL, 4, 3),
(14, NULL, 7, 5, 2),
(15, 3, NULL, 6, 1)
;

INSERT INTO Netflix.Profil (idProfil, nom, typeDeProfil, idUtilisateur) VALUES
(1, 'Melina', 'Enfant', 2),
(2,'Sergio','Enfant',2),
(3,'Louise','Adulte',2),
(4,'Camillia','Adulte',2),
(5,'John','Adulte',3),
(6, 'Alice', 'Enfant', 1),
(7, 'Loulou', 'Enfant', 1),
(8, 'Bouh', 'Adulte', 4),
(9, 'Paul', 'Adulte', 5),
(10, 'Emily', 'Adulte', 7),
(11, 'Ravi', 'Adulte', 10),
(12, 'Aiko', 'Adulte', 11),
(13, 'Liam', 'Adulte', 12),
(14, 'Sophia', 'Enfant', 15),
(15, 'Hans', 'Adulte', 14)
;



INSERT INTO Netflix.Liste (idListe, idProfil) VALUES
(1, 1),
(2, 2),
(3,3),
(4,4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10),
(11, 11),
(12, 12),
(13, 13),
(14, 14),
(15, 15)

;


INSERT INTO Netflix.MaListe (idMaListe, idFilm, idSerie, idListe) VALUES
(1, 1, NULL, 1),
(2, NULL, 1, 2),
(3, 2, NULL, 1),
(4, NULL, 2, 2),
(5, 3, NULL, 1),
(6, NULL, 3, 2),
(7, 4, NULL, 1),
(8, NULL, 4, 2),
(9, 5, NULL, 1),
(10, NULL, 5, 2),
(11, 1, NULL, 3),
(12, NULL, 1, 3),
(13, 2, NULL, 3),
(14, NULL, 2, 3),
(15, 3, NULL, 3)

;


INSERT INTO Netflix.Audio (idAudio, idFilm, idSerie, idLangue) VALUES
(1, 1, NULL, 1),
(2, 2, NULL, 2),
(3, NULL, 1, 3),
(4, NULL, 4,1),
(5, NULL, 4,2),
(6, NULL, 4,3),
(7, NULL, 4,5),
(8, NULL, 4,6),
(9, NULL, 4,7),
(10,1,NULL,6),
(11, 3, NULL, 4),
(12, 5, NULL, 8),
(13, NULL, 2, 5),
(14, NULL, 6, 7),
(15, NULL, 3, 6)
;

INSERT INTO Netflix.Soustitre (idSoustitre, idFilm, idSerie, idLangue) VALUES
(1, 1, NULL, 1),
(2, 2, NULL, 2),
(3, NULL, 1, 3),
(4, NULL, 4, 1),
(5, NULL, 4, 2),
(6, NULL, 4, 3),
(7, NULL, 4, 4),
(8, NULL, 4, 5),
(9, 3, NULL, 6),
(10, 4, NULL, 7),
(11, 5, NULL, 8),
(12, 1, NULL, 2),
(13, 2, NULL, 3),
(14, NULL, 5, 1),
(15, NULL, 6, 4)
;



INSERT INTO Netflix.Top10Serie (idTop10Serie, pays, idSerie, classement, dateTop10) VALUES

(2, 'France', 5,1, '2025-01-14'),
(3, 'France', 3,8, '2025-01-14'),
(4, 'France', 7,5, '2025-01-16'),
(5, 'France', 5,1, '2025-01-16'),
(6, 'France', 12,8, '2023-01-16'),
(7, 'France', 2,6, '2025-01-16'),
(8, 'France', 3,10, '2025-01-16'),
(9, 'France', 4, 3, '2025-01-16'),
(10, 'France', 4, 3, '2025-01-17'),
(11, 'USA', 2, 1, '2025-01-14'),
(12, 'USA', 1, 2, '2025-01-14'),
(13, 'USA', 3, 3, '2025-01-14'),
(14, 'USA', 4, 4, '2025-01-14'),
(15, 'USA', 5, 5, '2025-01-14')
;

INSERT INTO Netflix.Top10Film (idTop10Film, classement, pays, dateTop10, idFilm) VALUES
(1, 1, 'France', '2023-01-01', 1),
(2, 2, 'USA', '2023-01-01', 2),
(3, 5, 'France', '2024-01-14', 1),
(4,1,'France','2025-01-17',4),
(5,1,'France','2024-06-7',5),
(6, 3, 'USA', '2023-02-01', 3),
(7, 4, 'France', '2023-03-01', 2),
(8, 5, 'USA', '2023-04-01', 6),
(9, 6, 'USA', '2023-05-01', 7),
(10, 7, 'Canada', '2023-06-01', 8),
(11, 8, 'Allemagne', '2023-07-01', 9),
(12, 9, 'Espagne', '2023-08-01', 10),
(13, 10, 'Italie', '2023-09-01', 11),
(14, 11, 'Japon', '2023-10-01', 12),
(15, 12, 'Royaume-Uni', '2023-11-01', 13)