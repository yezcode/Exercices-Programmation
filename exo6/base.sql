-- Niveau1
SELECT nom FROM planete

SELECT temperature FROM planete WHERE nom = "Mars"
INSERT INTO planete("id", "nom", "temperature", "distancesol", "diametre") VALUES(9, "Nebula", 1500, 123000, 472000)

-- Niveau2
SELECT nom, diametre FROM planete ORDER BY distancesol DESC LIMIT (1)

SELECT nom FROM planete ORDER BY temperature ASC LIMIT (3)

SELECT SUM(temperature) FROM planete

-- Niveau3
SELECT nom FROM mission ORDER BY nbequipage DESC LIMIT (1)

SELECT planete.nom, planete.diametre 
FROM planete, mission
WHERE planete.id = mission.planete_id
AND mission.id = 2

SELECT AVG(nbequipage) FROM mission