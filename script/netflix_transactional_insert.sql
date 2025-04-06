-- Insertion des utilisateurs (20)
INSERT INTO Utilisateur (nom, prenom, age, paysResidance, email, numero, statutAbonnement) VALUES
('Martin', 'Emma', 28, 'France', 'emma.martin@email.com', '0612345678', 'Actif'),
('Bernard', 'Lucas', 35, 'Belgique', 'lucas.bernard@email.com', '0623456789', 'Actif'),
('Dubois', 'Chloé', 22, 'Suisse', 'chloe.dubois@email.com', '0634567890', 'Résilié'),
('Thomas', 'Hugo', 41, 'France', 'hugo.thomas@email.com', '0645678901', 'Actif'),
('Robert', 'Léa', 29, 'Canada', 'lea.robert@email.com', '0656789012', 'Actif'),
('Richard', 'Nathan', 33, 'France', 'nathan.richard@email.com', '0667890123', 'Actif'),
('Petit', 'Camille', 27, 'Belgique', 'camille.petit@email.com', '0678901234', 'Résilié'),
('Durand', 'Louis', 45, 'Suisse', 'louis.durand@email.com', '0689012345', 'Actif'),
('Leroy', 'Manon', 31, 'Espagne', 'manon.leroy@email.com', '0690123456', 'Actif'),
('Moreau', 'Ethan', 24, 'France', 'ethan.moreau@email.com', '0601234567', 'Actif'),
('Simon', 'Zoé', 38, 'France', 'zoe.simon@email.com', '0613456789', 'Actif'),
('Laurent', 'Mathis', 26, 'Belgique', 'mathis.laurent@email.com', '0624567890', 'Actif'),
('Michel', 'Inès', 43, 'Suisse', 'ines.michel@email.com', '0635678901', 'Résilié'),
('Garcia', 'Théo', 30, 'France', 'theo.garcia@email.com', '0646789012', 'Actif'),
('David', 'Sarah', 25, 'Canada', 'sarah.david@email.com', '0657890123', 'Actif'),
('Bertrand', 'Adam', 36, 'France', 'adam.bertrand@email.com', '0668901234', 'Actif'),
('Roux', 'Juliette', 23, 'Belgique', 'juliette.roux@email.com', '0679012345', 'Actif'),
('Vincent', 'Paul', 44, 'Suisse', 'paul.vincent@email.com', '0680123456', 'Actif'),
('Fournier', 'Lina', 32, 'Espagne', 'lina.fournier@email.com', '0691234567', 'Actif'),
('Mercier', 'Noah', 21, 'France', 'noah.mercier@email.com', '0602345678', 'Actif');

-- Insertion des abonnements (3 types)
INSERT INTO Abonnement (idUtilisateur, typeAbonnement, prix) VALUES
(1, 'Premium', 15.99),
(2, 'Standard', 11.99),
(3, 'Basic', 7.99),
(4, 'Premium', 15.99),
(5, 'Standard', 11.99),
(6, 'Basic', 7.99),
(7, 'Premium', 15.99),
(8, 'Standard', 11.99),
(9, 'Basic', 7.99),
(10, 'Premium', 15.99),
(11, 'Standard', 11.99),
(12, 'Basic', 7.99),
(13, 'Premium', 15.99),
(14, 'Standard', 11.99),
(15, 'Basic', 7.99),
(16, 'Premium', 15.99),
(17, 'Standard', 11.99),
(18, 'Basic', 7.99),
(19, 'Premium', 15.99),
(20, 'Standard', 11.99);

-- Insertion des paiements
INSERT INTO Paiement (idAbonnement, datePaiement, montant, statusPaiement) VALUES
(1, '2023-01-15', 15.99, 'Effectué'),
(1, '2023-02-15', 15.99, 'Effectué'),
(2, '2023-01-10', 11.99, 'Effectué'),
(2, '2023-02-10', 11.99, 'Effectué'),
(3, '2023-01-05', 7.99, 'Effectué'),
(4, '2023-01-20', 15.99, 'Effectué'),
(5, '2023-01-12', 11.99, 'Effectué'),
(6, '2023-01-07', 7.99, 'Effectué'),
(7, '2023-01-18', 15.99, 'Échoué'),
(8, '2023-01-14', 11.99, 'Effectué'),
(9, '2023-01-09', 7.99, 'Effectué'),
(10, '2023-01-22', 15.99, 'Effectué'),
(11, '2023-01-11', 11.99, 'Effectué'),
(12, '2023-01-06', 7.99, 'Effectué'),
(13, '2023-01-19', 15.99, 'Effectué'),
(14, '2023-01-13', 11.99, 'Effectué'),
(15, '2023-01-08', 7.99, 'Effectué'),
(16, '2023-01-21', 15.99, 'Effectué'),
(17, '2023-01-16', 11.99, 'Effectué'),
(18, '2023-01-04', 7.99, 'Effectué'),
(19, '2023-01-17', 15.99, 'Effectué'),
(20, '2023-01-23', 11.99, 'Effectué');

-- Insertion des profils (2-3 par utilisateur)
INSERT INTO Profil (nom, typeProfil, idUtilisateur) VALUES
('Principal', 'Adulte', 1),
('Enfants', 'Enfant', 1),
('Principal', 'Adulte', 2),
('Principal', 'Adulte', 3),
('Principal', 'Adulte', 4),
('Enfants', 'Enfant', 4),
('Principal', 'Adulte', 5),
('Principal', 'Adulte', 6),
('Principal', 'Adulte', 7),
('Principal', 'Adulte', 8),
('Enfants', 'Enfant', 8),
('Principal', 'Adulte', 9),
('Principal', 'Adulte', 10),
('Enfants', 'Enfant', 10),
('Principal', 'Adulte', 11),
('Principal', 'Adulte', 12),
('Principal', 'Adulte', 13),
('Principal', 'Adulte', 14),
('Enfants', 'Enfant', 14),
('Principal', 'Adulte', 15),
('Principal', 'Adulte', 16),
('Principal', 'Adulte', 17),
('Enfants', 'Enfant', 17),
('Principal', 'Adulte', 18),
('Principal', 'Adulte', 19),
('Principal', 'Adulte', 20),
('Enfants', 'Enfant', 20);

-- Insertion des genres (10)
INSERT INTO Genre (nom) VALUES
('Action'),
('Comédie'),
('Drame'),
('Science-Fiction'),
('Horreur'),
('Romance'),
('Documentaire'),
('Animation'),
('Thriller'),
('Fantastique');

-- Insertion des langues (10)
INSERT INTO Langue (nom) VALUES
('Français'),
('Anglais'),
('Espagnol'),
('Allemand'),
('Italien'),
('Japonais'),
('Coréen'),
('Chinois'),
('Russe'),
('Portugais');

-- Insertion des studios (10)
INSERT INTO Studio (nom, pays) VALUES
('Netflix Originals', 'USA'),
('Warner Bros', 'USA'),
('Universal Pictures', 'USA'),
('Disney', 'USA'),
('Studio Ghibli', 'Japon'),
('BBC Films', 'Royaume-Uni'),
('Gaumont', 'France'),
('Pathé', 'France'),
('Canal+', 'France'),
('Amazon Studios', 'USA');

-- Insertion des acteurs (20)
INSERT INTO Acteur (nom, prenom, dateNaissance, dateDeces) VALUES
('Depp', 'Johnny', '1963-06-09', NULL),
('Jolie', 'Angelina', '1975-06-04', NULL),
('DiCaprio', 'Leonardo', '1974-11-11', NULL),
('Portman', 'Natalie', '1981-06-09', NULL),
('Smith', 'Will', '1968-09-25', NULL),
('Lawrence', 'Jennifer', '1990-08-15', NULL),
('Pitt', 'Brad', '1963-12-18', NULL),
('Johansson', 'Scarlett', '1984-11-22', NULL),
('Washington', 'Denzel', '1954-12-28', NULL),
('Blanchett', 'Cate', '1969-05-14', NULL),
('Dujardin', 'Jean', '1972-06-19', NULL),
('Cotillard', 'Marion', '1975-09-30', NULL),
('Omar Sy', '', '1978-01-20', NULL),
('Gainsbourg', 'Charlotte', '1971-07-21', NULL),
('Auteuil', 'Daniel', '1950-01-24', NULL),
('Hanks', 'Tom', '1956-07-09', NULL),
('Bullock', 'Sandra', '1964-07-26', NULL),
('Gadot', 'Gal', '1985-04-30', NULL),
('Hemsworth', 'Chris', '1983-08-11', NULL),
('Reynolds', 'Ryan', '1976-10-23', NULL);

-- Insertion des titres (50)
INSERT INTO Titre (nom, annee, dateDebutLicence, dateFinLicence, categorieAge, description) VALUES
-- Films (20)
('The Irishman', 2019, '2019-11-27', '2027-11-27', '18+', 'Un tueur à gages se remémore son implication dans le crime organisé'),
('Marriage Story', 2019, '2019-12-06', '2027-12-06', '16+', 'Un couple traverse un divorce difficile'),
('Roma', 2018, '2018-12-14', '2026-12-14', '16+', 'La vie d une domestique dans le Mexique des années 70'),
('The Power of the Dog', 2021, '2021-12-01', '2029-12-01', '18+', 'Un rancher cruel fait souffrir son nouveau beau-frère'),
('Don t Look Up', 2021, '2021-12-24', '2029-12-24', '16+', 'Deux astronomes tentent d avertir l humanité d une comète mortelle'),
('Extraction', 2020, '2020-04-24', '2028-04-24', '18+', 'Un mercenaire est chargé de sauver le fils d un baron de la drogue'),
('The Gray Man', 2022, '2022-07-22', '2030-07-22', '18+', 'Un agent de la CIA devient la cible d un ancien collègue psychopathe'),
('Enola Holmes', 2020, '2020-09-23', '2028-09-23', '12+', 'La jeune soeur de Sherlock Holmes résout son premier mystère'),
('The Adam Project', 2022, '2022-03-11', '2030-03-11', '12+', 'Un pilote voyage dans le temps et rencontre son jeune soi'),
('Red Notice', 2021, '2021-11-12', '2029-11-12', '16+', 'Un agent du FBI traque le voleur d art le plus recherché au monde'),
('Bird Box', 2018, '2018-12-21', '2026-12-21', '18+', 'Des créatures invisibles poussent les gens au suicide'),
('The Old Guard', 2020, '2020-07-10', '2028-07-10', '18+', 'Un groupe de mercenaires immortels protège l humanité'),
('Army of the Dead', 2021, '2021-05-21', '2029-05-21', '18+', 'Un groupe de mercenaires tente un casse à Las Vegas pendant une épidémie zombie'),
('The Mitchells vs. The Machines', 2021, '2021-04-30', '2029-04-30', 'Tout public', 'Une famille dysfonctionnelle sauve le monde des robots'),
('The Sea Beast', 2022, '2022-07-08', '2030-07-08', 'Tout public', 'Un chasseur de monstres marins découvre une vérité surprenante'),
('Klaus', 2019, '2019-11-15', '2027-11-15', 'Tout public', 'Un postier paresseux crée accidentellement la légende du Père Noël'),
('The Ballad of Buster Scruggs', 2018, '2018-11-16', '2026-11-16', '18+', 'Six histoires de l Ouest américain'),
('Dolemite Is My Name', 2019, '2019-10-25', '2027-10-25', '18+', 'L histoire vraie de Rudy Ray Moore, créateur du personnage Dolemite'),
('The Trial of the Chicago 7', 2020, '2020-10-16', '2028-10-16', '16+', 'L histoire des manifestants accusés d incitation aux émeutes en 1968'),
('Da 5 Bloods', 2020, '2020-06-12', '2028-06-12', '18+', 'Quatre vétérans du Vietnam retournent chercher un trésor'),

-- Séries (30)
('Stranger Things', 2016, '2016-07-15', '2025-07-15', '16+', 'Une petite ville découvre un mystère terrifiant'),
('The Crown', 2016, '2016-11-04', '2024-11-04', '16+', 'La vie de la reine Elizabeth II'),
('La Casa de Papel', 2017, '2017-05-02', '2025-05-02', '18+', 'Un braquage audacieux de la Monnaie espagnole'),
('The Witcher', 2019, '2019-12-20', '2027-12-20', '18+', 'Un chasseur de monstres mutant parcourt un monde corrompu'),
('Bridgerton', 2020, '2020-12-25', '2028-12-25', '18+', 'Les drames romantiques de la haute société londonienne'),
('Ozark', 2017, '2017-07-21', '2025-07-21', '18+', 'Un conseiller financier blanchit de l argent pour un cartel de drogue'),
('The Queen s Gambit', 2020, '2020-10-23', '2028-10-23', '16+', 'Une prodige des échecs lutte contre la dépendance'),
('Narcos', 2015, '2015-08-28', '2025-08-28', '18+', 'L ascension et la chute du cartel de Medellín'),
('Dark', 2017, '2017-12-01', '2025-12-01', '16+', 'La disparition d un enfant révèle les secrets de quatre familles'),
('Money Heist', 2017, '2017-05-02', '2025-05-02', '18+', 'Un groupe de braqueurs prend des otages à la Monnaie espagnole'),
('Squid Game', 2021, '2021-09-17', '2029-09-17', '18+', 'Des joueurs endettés participent à des jeux mortels pour de l argent'),
('Peaky Blinders', 2013, '2013-09-12', '2026-09-12', '18+', 'Un gang familial règne sur Birmingham après la Première Guerre mondiale'),
('Black Mirror', 2011, '2011-12-04', '2025-12-04', '18+', 'Une anthologie explorant les côtés sombres de la technologie'),
('The Last Kingdom', 2015, '2015-10-10', '2025-10-10', '18+', 'Un guerrier saxon élevé par les Vikings cherche à reconquérir son royaume'),
('Mindhunter', 2017, '2017-10-13', '2025-10-13', '18+', 'Des agents du FBI développent des profils de tueurs en série'),
('The Umbrella Academy', 2019, '2019-02-15', '2027-02-15', '16+', 'Une famille dysfonctionnelle de super-héros se réunit pour résoudre un mystère'),
('Sex Education', 2019, '2019-01-11', '2027-01-11', '18+', 'Un adolescent maladroit ouvre une clinique de thérapie sexuelle à son école'),
('You', 2018, '2018-09-09', '2026-09-09', '18+', 'Un gérant de librairie devient obsédé par une cliente'),
('The Haunting of Hill House', 2018, '2018-10-12', '2026-10-12', '18+', 'Une famille confrontée à des événements paranormaux dans un manoir hanté'),
('Arcane', 2021, '2021-11-06', '2029-11-06', '16+', 'L origine des champions légendaires de League of Legends'),
('Shadow and Bone', 2021, '2021-04-23', '2029-04-23', '16+', 'Une jeune femme découvre un pouvoir qui pourrait unifier son pays divisé'),
('The Sandman', 2022, '2022-08-05', '2030-08-05', '18+', 'Le seigneur des rêves est capturé et emprisonné pendant un siècle'),
('Locke & Key', 2020, '2020-02-07', '2028-02-07', '16+', 'Trois enfants découvrent des clés magiques dans leur nouvelle maison'),
('The Witcher: Blood Origin', 2022, '2022-12-25', '2030-12-25', '18+', 'Préquelle de The Witcher se déroulant 1200 ans avant les événements principaux'),
('Wednesday', 2022, '2022-11-23', '2030-11-23', '16+', 'Wednesday Addams enquête sur une série de meurtres dans son école'),
('1899', 2022, '2022-11-17', '2030-11-17', '18+', 'Des migrants rencontrent un navire abandonné en mer'),
('Alice in Borderland', 2020, '2020-12-10', '2028-12-10', '18+', 'Un gamer se retrouve piégé dans une version dystopique de Tokyo'),
('Cobra Kai', 2018, '2018-05-02', '2026-05-02', '16+', 'Suite de la saga Karate Kid, 34 ans après les événements du premier film'),
('The Good Place', 2016, '2016-09-19', '2024-09-19', '12+', 'Une femme se réveille dans l au-delà et découvre qu elle est au paradis par erreur'),
('Russian Doll', 2019, '2019-02-01', '2027-02-01', '18+', 'Une femme meurt et revit sans cesse la même soirée');

-- Insertion des films (20)
INSERT INTO Film (idTitre, duree) VALUES
(1, 209),
(2, 137),
(3, 135),
(4, 126),
(5, 138),
(6, 117),
(7, 129),
(8, 123),
(9, 106),
(10, 118),
(11, 124),
(12, 125),
(13, 148),
(14, 113),
(15, 115),
(16, 96),
(17, 132),
(18, 118),
(19, 130),
(20, 154);

-- Insertion des séries (30)
INSERT INTO Serie (idTitre, saison) VALUES
(21, 4),
(22, 5),
(23, 5),
(24, 3),
(25, 2),
(26, 4),
(27, 1),
(28, 3),
(29, 3),
(30, 5),
(31, 1),
(32, 6),
(33, 5),
(34, 5),
(35, 2),
(36, 3),
(37, 3),
(38, 4),
(39, 1),
(40, 1),
(41, 1),
(42, 1),
(43, 3),
(44, 1),
(45, 1),
(46, 1),
(47, 2),
(48, 5),
(49, 4),
(50, 2);

-- Insertion des titres et genres
INSERT INTO TitreGenre (idTitre, idGenre) VALUES
-- Films
(1, 1), (1, 3),
(2, 3),
(3, 3),
(4, 3), (4, 9),
(5, 2), (5, 4),
(6, 1), (6, 9),
(7, 1), (7, 9),
(8, 1), (8, 10),
(9, 1), (9, 4),
(10, 1), (10, 2),
(11, 4), (11, 5), (11, 9),
(12, 1), (12, 4),
(13, 1), (13, 5),
(14, 2), (14, 8),
(15, 8), (15, 10),
(16, 2), (16, 8),
(17, 1), (17, 2),
(18, 2), (18, 3),
(19, 3),
(20, 1), (20, 3),

-- Séries
(21, 4), (21, 9),
(22, 3),
(23, 1), (23, 9),
(24, 1), (24, 4), (24, 10),
(25, 3), (25, 6),
(26, 1), (26, 3), (26, 9),
(27, 3),
(28, 1), (28, 3),
(29, 4), (29, 9),
(30, 1), (30, 9),
(31, 1), (31, 9),
(32, 1), (32, 3), (32, 9),
(33, 4), (33, 9),
(34, 1), (34, 3),
(35, 3), (35, 9),
(36, 1), (36, 4), (36, 10),
(37, 2), (37, 6),
(38, 3), (38, 9),
(39, 5), (39, 9),
(40, 4), (40, 10),
(41, 1), (41, 4), (41, 10),
(42, 4), (42, 10),
(43, 1), (43, 4), (43, 10),
(44, 1), (44, 4),
(45, 2), (45, 5),
(46, 4), (46, 9),
(47, 1), (47, 2),
(48, 2), (48, 4),
(49, 2), (49, 4),
(50, 2), (50, 4);

-- Insertion des langues disponibles
-- Pour chaque titre, nous ajoutons plusieurs langues audio et sous-titres
INSERT INTO Langue_Disponible (idTitre, idLangue, typeLangue)
SELECT t.idTitre, l.idLangue, 'audio'
FROM Titre t
CROSS JOIN Langue l
WHERE l.idLangue IN (1, 2, 3)  -- Français, Anglais, Espagnol pour audio
ORDER BY t.idTitre, l.idLangue;

INSERT INTO Langue_Disponible (idTitre, idLangue, typeLangue)
SELECT t.idTitre, l.idLangue, 'sous-titre'
FROM Titre t
CROSS JOIN Langue l
WHERE l.idLangue IN (1, 2, 3, 4, 5)  -- Plus de langues pour sous-titres
ORDER BY t.idTitre, l.idLangue;

-- Insertion des acteurs dans les titres
-- Insertion supplémentaire dans la table Acting pour couvrir tous les titres
INSERT INTO Acting (idTitre, idActeur) VALUES
-- Films supplémentaires
(1, 3),   -- The Irishman avec DiCaprio
(2, 12),  -- Marriage Story avec Cotillard
(3, 14),  -- Roma avec Gainsbourg
(4, 16),  -- The Power of the Dog avec Hanks
(5, 17),  -- Don't Look Up avec Bullock
(6, 18),  -- Extraction avec Gadot
(7, 19),  -- The Gray Man avec Hemsworth
(8, 20),  -- Enola Holmes avec Reynolds
(9, 1),   -- The Adam Project avec Depp
(10, 2),  -- Red Notice avec Jolie

-- Séries supplémentaires
(21, 4),  -- Stranger Things avec Portman
(22, 5),  -- The Crown avec Smith
(23, 6),  -- La Casa de Papel avec Lawrence
(24, 7),  -- The Witcher avec Pitt
(25, 8),  -- Bridgerton avec Johansson
(26, 9),  -- Ozark avec Washington
(27, 10), -- The Queen's Gambit avec Blanchett
(28, 11), -- Narcos avec Dujardin
(29, 12), -- Dark avec Cotillard
(30, 13), -- Money Heist avec Omar Sy
(31, 14), -- Squid Game avec Gainsbourg
(32, 15), -- Peaky Blinders avec Auteuil
(33, 16), -- Black Mirror avec Hanks
(34, 17), -- The Last Kingdom avec Bullock
(35, 18), -- Mindhunter avec Gadot
(36, 19), -- The Umbrella Academy avec Hemsworth
(37, 20), -- Sex Education avec Reynolds
(38, 1),  -- You avec Depp
(39, 2),  -- The Haunting of Hill House avec Jolie
(40, 3),  -- Arcane avec DiCaprio
(41, 4),  -- Shadow and Bone avec Portman
(42, 5),  -- The Sandman avec Smith
(43, 6),  -- Locke & Key avec Lawrence
(44, 7),  -- The Witcher: Blood Origin avec Pitt
(45, 8),  -- Wednesday avec Johansson
(46, 9),  -- 1899 avec Washington
(47, 10), -- Alice in Borderland avec Blanchett
(48, 11), -- Cobra Kai avec Dujardin
(49, 12), -- The Good Place avec Cotillard
(50, 13); -- Russian Doll avec Omar Sy


-- Insertions supplémentaires pour MaListe (chaque profil a 3-5 titres)
INSERT INTO MaListe (idProfil, idTitre) VALUES
-- Profils 1-10
(1, 5), (1, 17), (1, 38),  -- Utilisateur 1 (Profil Principal)
(2, 8), (2, 22), (2, 45),  -- Profil Enfant
(3, 12), (3, 29), (3, 41),
(4, 3), (4, 19), (4, 33),
(5, 7), (5, 24), (5, 47),
(6, 9), (6, 27), (6, 36),
(7, 14), (7, 31), (7, 44),
(8, 2), (8, 18), (8, 39),
(9, 6), (9, 25), (9, 42),
(10, 11), (10, 28), (10, 50),

-- Profils 11-20
(11, 4), (11, 20), (11, 35),
(12, 10), (12, 23), (12, 46),
(13, 1), (13, 16), (13, 37),
(14, 13), (14, 30), (14, 48),
(15, 15), (15, 26), (15, 43),
(16, 21), (16, 34), (16, 49),
(17, 5), (17, 18), (17, 40),
(18, 9), (18, 22), (18, 45),
(19, 14), (19, 29), (19, 38),
(20, 7), (20, 24), (20, 47),

-- Profils 21-30
(21, 3), (21, 19), (21, 33),
(22, 6), (22, 25), (22, 42),
(23, 12), (23, 28), (23, 50),
(24, 2), (24, 17), (24, 39),
(25, 8), (25, 22), (25, 45);

-- Insertions supplémentaires pour Evaluation (2-3 évaluations par profil)
INSERT INTO Evaluation (idProfil, idTitre, note, avis) VALUES
-- Évaluations supplémentaires
(1, 5, 4, 'Drôle et pertinent sur notre société'),
(1, 38, 3, 'Un peu trop dramatique à mon goût'),
(2, 22, 5, 'Les décors sont somptueux'),
(3, 12, 2, 'Effets spéciaux médiocres'),
(4, 19, 4, 'Scénario intelligent'),
(5, 24, 5, 'Henry Cavill est parfait en Geralt de Riv'),
(6, 9, 3, 'Sympa pour un film familial'),
(7, 14, 5, 'Animation révolutionnaire'),
(8, 2, 4, 'Performances émouvantes'),
(9, 25, 2, 'Trop cliché'),

(10, 11, 1, 'Trop angoissant pour moi'),
(11, 4, 5, 'Un chef-dœuvre contemplatif'),
(12, 10, 3, 'Divertissant mais prévisible'),
(13, 1, 5, 'Scorsese au sommet de son art'),
(14, 13, 4, 'Zombies et action - parfait combo'),
(15, 15, 5, 'Ma fille adore ce film'),
(16, 21, 4, 'Nostalgie des années 80 bien rendue'),
(17, 5, 4, 'Satire sociale réussie'),
(18, 9, 3, 'Correct sans plus'),
(19, 14, 5, 'Notre film danimation préféré'),

(20, 7, 2, 'Trop violent pour moi'),
(21, 3, 5, 'Photographie magnifique'),
(22, 6, 4, 'Chris Hemsworth est convaincant'),
(23, 12, 3, 'Scènes daction répétitives'),
(24, 17, 5, 'Western moderne réussi'),
(25, 8, 4, 'Parfait pour les adolescents');