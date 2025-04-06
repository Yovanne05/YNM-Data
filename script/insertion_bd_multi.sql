-- Insertion des dates (Temps)
INSERT INTO Entrepot_Netflix.Temps (jour, mois, annee, trimestre) VALUES
-- Dates de paiement
(15, 1, 2023, 1), (10, 1, 2023, 1), (5, 1, 2023, 1), (20, 1, 2023, 1),
(12, 1, 2023, 1), (7, 1, 2023, 1), (18, 1, 2023, 1), (14, 1, 2023, 1),
(9, 1, 2023, 1), (22, 1, 2023, 1), (11, 1, 2023, 1), (6, 1, 2023, 1),
(19, 1, 2023, 1), (13, 1, 2023, 1), (8, 1, 2023, 1), (21, 1, 2023, 1),
(16, 1, 2023, 1), (4, 1, 2023, 1), (17, 1, 2023, 1), (23, 1, 2023, 1),
-- Dates de licence
(27, 11, 2019, 4), (6, 12, 2019, 4), (14, 12, 2018, 4), (1, 12, 2021, 4),
(24, 12, 2021, 4), (24, 4, 2020, 2), (22, 7, 2022, 3), (23, 9, 2020, 3),
(11, 3, 2022, 1), (12, 11, 2021, 4), (21, 12, 2018, 4), (10, 7, 2020, 3),
(21, 5, 2021, 2), (30, 4, 2021, 2), (8, 7, 2022, 3), (15, 11, 2019, 4),
(16, 11, 2018, 4), (25, 10, 2019, 4), (16, 10, 2020, 4), (12, 6, 2020, 2),
-- Dates séries
(15, 7, 2016, 3), (4, 11, 2016, 4), (2, 5, 2017, 2), (20, 12, 2019, 4),
(25, 12, 2020, 4), (21, 7, 2017, 3), (23, 10, 2020, 4), (28, 8, 2015, 3),
(1, 12, 2017, 4), (17, 9, 2021, 3), (12, 9, 2013, 3), (4, 12, 2011, 4),
(10, 10, 2015, 4), (13, 10, 2017, 4), (15, 2, 2019, 1), (11, 1, 2019, 1),
(9, 9, 2018, 3), (12, 10, 2018, 4), (6, 11, 2021, 4), (23, 4, 2021, 2),
(5, 8, 2022, 3), (7, 2, 2020, 1), (25, 12, 2022, 4), (23, 11, 2022, 4),
(17, 11, 2022, 4), (10, 12, 2020, 4), (2, 5, 2018, 2), (19, 9, 2016, 3),
(1, 2, 2019, 1);

-- Insertion des utilisateurs
INSERT INTO Entrepot_Netflix.Utilisateur (nom, prenom, age, paysResidence, email, numero, statutAbonnement) VALUES
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

-- Insertion des abonnements
INSERT INTO Entrepot_Netflix.Abonnement (typeAbonnement, prix) VALUES
('Premium', 15.99),
('Standard', 11.99),
('Basic', 7.99);

-- Insertion des genres
INSERT INTO Entrepot_Netflix.Genre (nomGenre) VALUES
('Action'), ('Comédie'), ('Drame'), ('Science-Fiction'), ('Horreur'),
('Romance'), ('Documentaire'), ('Animation'), ('Thriller'), ('Fantastique');

-- Insertion des langues
INSERT INTO Entrepot_Netflix.Langue (nomLangue) VALUES
('Français'), ('Anglais'), ('Espagnol'), ('Allemand'), ('Italien'),
('Japonais'), ('Coréen'), ('Chinois'), ('Russe'), ('Portugais');

-- Insertion des langues disponibles
INSERT INTO Entrepot_Netflix.Langue_Disponible (idLangue, typeLangue) VALUES
(1, 'audio'), (2, 'audio'), (3, 'audio'),
(1, 'sous-titre'), (2, 'sous-titre'), (3, 'sous-titre'),
(4, 'sous-titre'), (5, 'sous-titre');

-- Insertion des titres (films et séries)
INSERT INTO Entrepot_Netflix.Titre (nom, annee, iddateDebutLicence, iddateFinLicence, categorieAge, typeTitre, description) VALUES
-- Films
('The Irishman', 2019, 1, 2, '18+', 'film', 'Un tueur à gages se remémore son implication dans le crime organisé'),
('Marriage Story', 2019, 3, 4, '16+', 'film', 'Un couple traverse un divorce difficile'),
('Roma', 2018, 5, 6, '16+', 'film', 'La vie d une domestique dans le Mexique des années 70'),
('The Power of the Dog', 2021, 7, 8, '18+', 'film', 'Un rancher cruel fait souffrir son nouveau beau-frère'),
('Don t Look Up', 2021, 9, 10, '16+', 'film', 'Deux astronomes tentent d avertir l humanité d une comète mortelle'),
('Extraction', 2020, 11, 12, '18+', 'film', 'Un mercenaire est chargé de sauver le fils d un baron de la drogue'),
('The Gray Man', 2022, 13, 14, '18+', 'film', 'Un agent de la CIA devient la cible d un ancien collègue psychopathe'),
('Enola Holmes', 2020, 15, 16, '12+', 'film', 'La jeune soeur de Sherlock Holmes résout son premier mystère'),
('The Adam Project', 2022, 17, 18, '12+', 'film', 'Un pilote voyage dans le temps et rencontre son jeune soi'),
('Red Notice', 2021, 19, 20, '16+', 'film', 'Un agent du FBI traque le voleur d art le plus recherché au monde'),
('Bird Box', 2018, '2018-12-21', '2026-12-21', '18+', 'film', 'Des créatures invisibles poussent les gens au suicide'),
('The Old Guard', 2020, '2020-07-10', '2028-07-10', '18+', 'film', 'Un groupe de mercenaires immortels protège l humanité'),
('Army of the Dead', 2021, '2021-05-21', '2029-05-21', '18+', 'film',  'Un groupe de mercenaires tente un casse à Las Vegas pendant une épidémie zombie'),
('The Mitchells vs. The Machines', 2021, '2021-04-30', '2029-04-30', 'Tout public', 'film',  'Une famille dysfonctionnelle sauve le monde des robots'),
('The Sea Beast', 2022, '2022-07-08', '2030-07-08', 'Tout public', 'film',  'Un chasseur de monstres marins découvre une vérité surprenante'),
('Klaus', 2019, '2019-11-15', '2027-11-15', 'Tout public', 'film',  'Un postier paresseux crée accidentellement la légende du Père Noël'),
('The Ballad of Buster Scruggs', 2018, '2018-11-16', '2026-11-16', '18+', 'film',  'Six histoires de l Ouest américain'),
('Dolemite Is My Name', 2019, '2019-10-25', '2027-10-25', '18+', 'film',  'L histoire vraie de Rudy Ray Moore, créateur du personnage Dolemite'),
('The Trial of the Chicago 7', 2020, '2020-10-16', '2028-10-16', '16+', 'film',  'L histoire des manifestants accusés d incitation aux émeutes en 1968'),
('Da 5 Bloods', 2020, '2020-06-12', '2028-06-12', '18+', 'film',  'Quatre vétérans du Vietnam retournent chercher un trésor'),

-- Séries
('Stranger Things', 2016, 41, 42, '16+', 'série', 'Une petite ville découvre un mystère terrifiant'),
('The Crown', 2016, 43, 44, '16+', 'série', 'La vie de la reine Elizabeth II'),
('La Casa de Papel', 2017, 45, 46, '18+', 'série', 'Un braquage audacieux de la Monnaie espagnole'),
('The Witcher', 2019, 47, 48, '18+', 'série', 'Un chasseur de monstres mutant parcourt un monde corrompu'),
('Bridgerton', 2020, 49, 50, '000018+', 'série', 'Les drames romantiques de la haute société londonienne'),
('Ozark', 2017, 51, 52, '18+', 'série', 'Un conseiller financier blanchit de l argent pour un cartel de drogue'),
('The Queen s Gambit', 2020, 53, 54, '16+', 'série', 'Une prodige des échecs lutte contre la dépendance'),
('Narcos', 2015, 55, 56, '18+', 'série', 'L ascension et la chute du cartel de Medellín'),
('Dark', 2017, 57, 58, '16+', 'série', 'La disparition d un enfant révèle les secrets de quatre familles'),
('Money Heist', 2017, 59, 60, '18+', 'série', 'Un groupe de braqueurs prend des otages à la Monnaie espagnole'),
('Squid Game', 2021, 61, 62, '18+', 'série', 'Des joueurs endettés participent à des jeux mortels pour de l argent'),
('Peaky Blinders', 2013, 63, 64, '18+', 'série', 'Un gang familial règne sur Birmingham après la Première Guerre mondiale'),
('Black Mirror', 2011, 65, 66, '18+', 'série', 'Une anthologie explorant les côtés sombres de la technologie'),
('The Last Kingdom', 2015, 67, 68, '18+', 'série', 'Un guerrier saxon élevé par les Vikings cherche à reconquérir son royaume'),
('Mindhunter', 2017, 69, 70, '18+', 'série', 'Des agents du FBI développent des profils de tueurs en série'),
('The Umbrella Academy', 2019, 71, 72, '16+', 'série', 'Une famille dysfonctionnelle de super-héros se réunit pour résoudre un mystère'),
('Sex Education', 2019, 73, 74, '18+', 'série', 'Un adolescent maladroit ouvre une clinique de thérapie sexuelle à son école'),
('You', 2018, 75, 76, '18+', 'série', 'Un gérant de librairie devient obsédé par une cliente'),
('The Haunting of Hill House', 2018, 77, 78, '18+', 'série', 'Une famille confrontée à des événements paranormaux dans un manoir hanté'),
('Arcane', 2021, 79, 80, '16+', 'série', 'L origine des champions légendaires de League of Legends'),
('Shadow and Bone', 2021, 81, 82, '16+', 'série', 'Une jeune femme découvre un pouvoir qui pourrait unifier son pays divisé'),
('The Sandman', 2022, 83, 84, '18+', 'série', 'Le seigneur des rêves est capturé et emprisonné pendant un siècle'),
('Locke & Key', 2020, 85, 86, '16+', 'série', 'Trois enfants découvrent des clés magiques dans leur nouvelle maison'),
('The Witcher: Blood Origin', 2022, 87, 88, '18+', 'série', 'Préquelle de The Witcher se déroulant 1200 ans avant les événements principaux'),
('Wednesday', 2022, 89, 90, '16+', 'série', 'Wednesday Addams enquête sur une série de meurtres dans son école'),
('1899', 2022, 91, 92, '18+', 'série', 'Des migrants rencontrent un navire abandonné en mer'),
('Alice in Borderland', 2020, 93, 94, '18+', 'série', 'Un gamer se retrouve piégé dans une version dystopique de Tokyo'),
('Cobra Kai', 2018, 95, 96, '16+', 'série', 'Suite de la saga Karate Kid, 34 ans après les événements du premier film'),
('The Good Place', 2016, 97, 98, '12+', 'série', 'Une femme se réveille dans l au-delà et découvre qu elle est au paradis par erreur'),
('Russian Doll', 2019, 99, 100, '18+', 'série', 'Une femme meurt et revit sans cesse la même soirée');
-- Insertion des films (suite des attributs);

-- Insertion des films (tous les films avec leurs durées)
INSERT INTO Entrepot_Netflix.Film (idTitre, duree) VALUES
(1, 209),   -- The Irishman
(2, 137),   -- Marriage Story
(3, 135),   -- Roma
(4, 126),   -- The Power of the Dog
(5, 138),   -- Don t Look Up
(6, 117),   -- Extraction
(7, 129),   -- The Gray Man
(8, 123),   -- Enola Holmes
(9, 106),   -- The Adam Project
(10, 118),  -- Red Notice
(11, 124),  -- Bird Box
(12, 125),  -- The Old Guard
(13, 148),  -- Army of the Dead
(14, 113),  -- The Mitchells vs. The Machines
(15, 115),  -- The Sea Beast
(16, 96),   -- Klaus
(17, 132),  -- The Ballad of Buster Scruggs
(18, 118),  -- Dolemite Is My Name
(19, 130),  -- The Trial of the Chicago 7
(20, 154);  -- Da 5 Bloods

-- Insertion des séries (toutes les séries avec leurs saisons)
INSERT INTO Entrepot_Netflix.Serie (idTitre, saison) VALUES
(21, 4),   -- Stranger Things
(22, 5),   -- The Crown
(23, 5),   -- La Casa de Papel
(24, 3),   -- The Witcher
(25, 2),   -- Bridgerton
(26, 4),   -- Ozark
(27, 1),   -- The Queen s Gambit
(28, 3),   -- Narcos
(29, 3),   -- Dark
(30, 5),   -- Money Heist
(31, 1),   -- Squid Game
(32, 6),   -- Peaky Blinders
(33, 5),   -- Black Mirror
(34, 5),   -- The Last Kingdom
(35, 2),   -- Mindhunter
(36, 3),   -- The Umbrella Academy
(37, 3),   -- Sex Education
(38, 4),   -- You
(39, 1),   -- The Haunting of Hill House
(40, 1),   -- Arcane
(41, 1),   -- Shadow and Bone
(42, 1),   -- The Sandman
(43, 3),   -- Locke & Key
(44, 1),   -- The Witcher: Blood Origin
(45, 1),   -- Wednesday
(46, 1),   -- 1899
(47, 2),   -- Alice in Borderland
(48, 5),   -- Cobra Kai
(49, 4),   -- The Good Place
(50, 2);   -- Russian Doll

-- Insertions pour Visionnage (données conçues pour l'analyse)
INSERT INTO Visionnage (idUtilisateur, idTitre, idDate, idGenre, idLangueDisponible, dureeVisionnage, nombreVues) VALUES
-- Utilisateur 1 (Très actif - 15 visionnages)
(1, 1, 1, 1, 1, 120, 1),   -- The Irishman (partiel)
(1, 6, 1, 1, 2, 117, 1),    -- Extraction (complet)
(1, 10, 1, 1, 1, 80, 1),    -- Red Notice (partiel)
(1, 24, 2, 1, 1, 45, 3),    -- The Witcher (3 épisodes)
(1, 7, 3, 1, 3, 129, 1),    -- The Gray Man
(1, 12, 4, 1, 2, 125, 1),   -- The Old Guard
(1, 21, 5, 4, 1, 50, 2),    -- Stranger Things (2 épisodes)
(1, 31, 6, 1, 3, 60, 4),    -- Squid Game (4 épisodes)
(1, 24, 7, 1, 1, 45, 2),    -- The Witcher (weekend)
(1, 6, 8, 1, 2, 117, 1),    -- Extraction (revisionnage)
(1, 10, 13, 1, 1, 118, 1),  -- Red Notice (complet)
(1, 38, 14, 3, 2, 45, 3),   -- You (3 épisodes weekend)
(1, 7, 15, 1, 3, 129, 1),   -- The Gray Man (revisionnage)
(1, 31, 20, 1, 3, 60, 4),   -- Squid Game (fin de saison)
(1, 1, 21, 1, 1, 209, 1),   -- The Irishman (complet weekend)

-- Utilisateur 2 (Actif moyen - 10 visionnages)
(2, 5, 1, 2, 3, 138, 1),    -- Don't Look Up
(2, 17, 2, 2, 1, 90, 1),     -- Buster Scruggs (partiel)
(2, 37, 3, 2, 2, 30, 3),    -- Sex Education (3 épisodes)
(2, 22, 6, 3, 1, 45, 2),    -- The Crown (weekend)
(2, 45, 7, 5, 2, 45, 1),    -- Wednesday (weekend)
(2, 5, 8, 2, 3, 138, 1),    -- Don't Look Up (revisionnage)
(2, 25, 13, 6, 1, 45, 2),   -- Bridgerton (weekend)
(2, 37, 14, 2, 2, 30, 2),   -- Sex Education (weekend)
(2, 16, 15, 8, 2, 96, 1),   -- Klaus
(2, 45, 21, 5, 2, 45, 1),   -- Wednesday (weekend)

-- Utilisateur 3 (Peu actif - 5 visionnages)
(3, 21, 1, 4, 1, 50, 1),    -- Stranger Things
(3, 31, 5, 1, 3, 60, 2),    -- Squid Game (2 épisodes)
(3, 45, 7, 5, 2, 45, 1),    -- Wednesday (weekend)
(3, 21, 14, 4, 1, 50, 1),   -- Stranger Things (weekend)
(3, 16, 21, 8, 2, 96, 1),   -- Klaus (weekend)

-- Utilisateur 4 (Irregulier - 8 visionnages)
(4, 3, 2, 3, 4, 135, 1),    -- Roma
(4, 15, 4, 8, 1, 115, 1),   -- The Sea Beast
(4, 30, 6, 1, 2, 50, 2),    -- Money Heist (weekend)
(4, 8, 7, 2, 1, 123, 1),    -- Enola Holmes (weekend)
(4, 14, 13, 8, 1, 113, 1),  -- Mitchells vs Machines
(4, 30, 14, 1, 2, 50, 2),   -- Money Heist (weekend)
(4, 3, 20, 3, 4, 135, 1),   -- Roma (revisionnage)
(4, 40, 21, 4, 1, 45, 1),   -- Arcane (weekend)

-- Utilisateur 5 (Fan d'horreur - 7 visionnages)
(5, 11, 3, 5, 5, 124, 1),   -- Bird Box
(5, 39, 5, 5, 1, 45, 3),    -- Haunting of Hill House
(5, 7, 6, 1, 3, 129, 1),    -- The Gray Man (weekend)
(5, 13, 7, 5, 1, 148, 1),   -- Army of the Dead (weekend)
(5, 39, 13, 5, 1, 45, 2),   -- Haunting of Hill House (weekend)
(5, 46, 14, 9, 1, 45, 1),  -- 1899 (weekend)
(5, 11, 20, 5, 5, 124, 1), -- Bird Box (revisionnage)

-- Utilisateur 6 (Famille - 6 visionnages)
(6, 14, 1, 8, 1, 113, 1),   -- Mitchells vs Machines
(6, 16, 2, 8, 2, 96, 1),    -- Klaus
(6, 8, 6, 2, 1, 123, 1),    -- Enola Holmes (weekend)
(6, 14, 7, 8, 1, 113, 1),   -- Mitchells vs Machines (weekend)
(6, 15, 14, 8, 1, 115, 1),  -- The Sea Beast (weekend)
(6, 16, 21, 8, 2, 96, 1),   -- Klaus (weekend)

-- Utilisateur 7 (Résilié - 3 visionnages)
(7, 2, 1, 3, 2, 60, 1),     -- Marriage Story (partiel)
(7, 25, 2, 6, 1, 45, 1),    -- Bridgerton
(7, 37, 3, 2, 2, 30, 1),    -- Sex Education

-- Utilisateur 8 (Nocturne - 12 visionnages)
(8, 18, 1, 2, 1, 118, 1),   -- Dolemite Is My Name
(8, 29, 1, 4, 2, 50, 2),    -- Dark (nuit)
(8, 33, 2, 9, 1, 30, 1),    -- Black Mirror (nuit)
(8, 18, 3, 2, 1, 118, 1),   -- Dolemite Is My Name
(8, 29, 5, 4, 2, 50, 2),    -- Dark (nuit)
(8, 33, 6, 9, 1, 30, 1),    -- Black Mirror (weekend nuit)
(8, 38, 7, 3, 2, 45, 1),    -- You (weekend nuit)
(8, 29, 13, 4, 2, 50, 2),   -- Dark (weekend nuit)
(8, 33, 14, 9, 1, 30, 1),   -- Black Mirror (weekend nuit)
(8, 46, 15, 9, 1, 45, 1),   -- 1899 (nuit)
(8, 29, 20, 4, 2, 50, 2),   -- Dark (nuit)
(8, 33, 21, 9, 1, 30, 1),   -- Black Mirror (weekend nuit)

-- Utilisateur 9 (Documentaires - 5 visionnages)
(9, 27, 4, 3, 1, 45, 1),    -- The Queen's Gambit
(9, 28, 5, 3, 2, 50, 1),    -- Narcos
(9, 19, 6, 3, 1, 130, 1),   -- Chicago 7 (weekend)
(9, 27, 13, 3, 1, 45, 1),   -- The Queen's Gambit (weekend)
(9, 20, 14, 3, 1, 154, 1),  -- Da 5 Bloods (weekend)

-- Utilisateur 10 (Animation - 6 visionnages)
(10, 14, 1, 8, 1, 113, 1),  -- Mitchells vs Machines
(10, 15, 2, 8, 1, 115, 1),  -- The Sea Beast
(10, 16, 6, 8, 2, 96, 1),   -- Klaus (weekend)
(10, 14, 7, 8, 1, 113, 1),  -- Mitchells vs Machines (weekend)
(10, 40, 14, 10, 1, 45, 1), -- Arcane (weekend)
(10, 16, 21, 8, 2, 96, 1);  -- Klaus (weekend)

-- Insertions pour Evaluation (données cohérentes avec les visionnages)
INSERT INTO Entrepot_Netflix.Evaluation (idUtilisateur, idTitre, idDate, idGenre, note) VALUES
-- Evaluations cohérentes avec les habitudes de visionnage
(1, 1, 1, 1, 4),   -- The Irishman
(1, 6, 2, 1, 5),    -- Extraction
(2, 5, 3, 2, 3),    -- Don't Look Up
(2, 37, 4, 2, 4),   -- Sex Education
(3, 21, 5, 3, 5),   -- Stranger Things
(3, 31, 6, 1, 5),   -- Squid Game
(4, 3, 7, 3, 4),    -- Roma
(4, 15, 8, 8, 5),   -- The Sea Beast
(5, 11, 9, 5, 2),   -- Bird Box (n'a pas aimé)
(5, 7, 10, 1, 4),   -- The Gray Man
(6, 14, 11, 8, 5),  -- Mitchells vs Machines
(6, 16, 12, 8, 5),  -- Klaus
(7, 2, 13, 3, 3);   -- Marriage Story

-- Insertions pour Paiement (données réalistes pour analyse financière)
INSERT INTO Entrepot_Netflix.Paiement (idUtilisateur, idAbonnement, idDate, montant, statusPaiement) VALUES
-- Historique complet sur 6 mois
-- Utilisateur Premium (1)
(1, 1, 1, 15.99, 'Effectué'),  -- Janvier
(1, 1, 32, 15.99, 'Effectué'), -- Février (idDate 32 = 15/2/2023)
(1, 1, 60, 15.99, 'Effectué'), -- Mars
(1, 1, 91, 15.99, 'Effectué'), -- Avril

-- Utilisateur Standard (2)
(2, 2, 2, 11.99, 'Effectué'),
(2, 2, 33, 11.99, 'Effectué'),
(2, 2, 61, 11.99, 'Effectué'),
(2, 2, 92, 11.99, 'Retard'),   -- Paiement en retard

-- Utilisateur Basic (3)
(3, 3, 3, 7.99, 'Effectué'),
(3, 3, 34, 7.99, 'Effectué'),
(3, 3, 62, 7.99, 'Échoué'),     -- Paiement échoué
(3, 3, 93, 7.99, 'Effectué'),

-- Utilisateur Premium (4)
(4, 1, 4, 15.99, 'Effectué'),
(4, 1, 35, 15.99, 'Effectué'),
(4, 1, 63, 15.99, 'Effectué'),

-- Utilisateur qui a résilié (7)
(7, 2, 7, 11.99, 'Effectué'),
(7, 2, 38, 11.99, 'Effectué'); -- Dernier paiement avant résiliation