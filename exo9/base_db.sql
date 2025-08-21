exercice1.sql
SELECT nom FROM cheval

SELECT nom, prenom FROM jockey

INSERT INTO cheval("nom", "sexe", "poid") VALUES("Digital Phoenix", "M", 532)

exercice2.sql
SELECT nom from cheval WHERE sexe = "M"

SELECT id FROM jockey WHERE nom = "Midas" AND prenom = "Laurent"

SELECT SUM(distance) FROM course

UPDATE jockey
SET cheval_id = (SELECT id FROM cheval WHERE nom = "Digital Phoenix")
WHERE datenaissance = "5/04/1998"

exercice3.sql
Select cheval.nom
FROM cheval, jockey, courseparticipant, course
WHERE courseparticipant.casaque = "bleu cassis"
AND courseparticipant.course_id = course.id
AND courseparticipant.jockey_id = jockey.id
AND jockey.cheval_id = cheval.id


SELECT AVG(cheval.poid)
FROM cheval, jockey, courseparticipant, course
WHERE course.nomprix = "Z Fury"
AND course.id = courseparticipant.course_id
AND courseparticipant.jockey_id = jockey.id
AND jockey.cheval_id = cheval.id

DELETE FROM courseparticipant
WHERE courseparticipant.id = (SELECT id FROM course WHERE nomprix = "Final Strike")
AND courseparticipant.jockey_id = 1

SELECT cheval.nom, cheval.poid
FROM cheval, jockey, courseparticipant, course
WHERE course.nomprix = "Final Strike"
AND course.id = courseparticipant.course_id
AND courseparticipant.jockey_id = jockey.id
AND jockey.cheval_id = cheval.id
ORDER BY cheval.poid ASC