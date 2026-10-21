Pour adtiver le pyenv : source .venv/Scripts/activate

Base de données. Écris les modèles ci-dessus, refais les migrations et teste les contraintes.
Terminé quand : les 6 règles d’unicité sont vérifiées dans le shell Django ou en tests.
Contrat du fichier. Liste les feuilles, les colonnes obligatoires et facultatives, et les colonnes ajoutées par le programme (ID achat, ID Cardmarket, Statut).
Terminé quand : c’est écrit sur une page, avec un Excel d’exemple.
Lecture et validation (Python seul). Une fonction qui renvoie les lignes valides et les erreurs avec leur numéro.
Terminé quand : un test passe pour chaque protection.
Catalogue Cardmarket. Télécharge les fichiers, regarde leur structure, puis écris trouver_produit(ligne).
Terminé quand : sur ~20 produits d’essai, chacun est relié ou marqué « à relier ».
Import en base (ton flowchart). ID déjà présent, produit trouvé ou créé, achat créé, le tout dans une transaction, avec un mode simulation et un bilan chiffré.
Terminé quand : relancer le même fichier deux fois ne change rien.
Fichier de sortie. Copie du fichier avec les IDs écrits et la feuille Bilan.
Terminé quand : l’original est intact et un deuxième import reconnaît les IDs.
Prix et calculs. Importe le guide des prix, puis calcule valeur actuelle et plus-values.
Terminé quand : les calculs retrouvent des chiffres que tu as vérifiés à la main.
Graphiques dans la feuille Bilan : répartition, meilleurs et pires produits.
Extensions, une à la fois : gradées, autres TCG, puis ventes.