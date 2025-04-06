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


-- Autre insertion via ETL