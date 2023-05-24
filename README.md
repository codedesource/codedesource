# Procédure de la récupération des données Météo France SWI 1969—2022, mailles et métadonnées

## Télécharger les données

1. Se rendre à la [page dédiée][1]:
   * télécharger l'archive zip avec toutes les mailles depuis la rubrique `Téléchargement` ;
   * télécharger le fichier `Coordonnées des mailles` depuis la rubrique `Documentation`.

## Souder les fichiers

3. Décompresser l'archive téléchargée.
4. Extraire la ligne d'en-tête de l'un des fichiers CSV et la sauvegarder dans un fichier à part (`swi_mailles_header`).
5. Souder le contenu de tous les fichiers CSV à l'exception de la première ligne de chacun en l'enregistrant dans un fichier (`swi_mailles_headless`).
6. Souder ensemble `swi_mailles_header` et `swi_mailles_headless` (`swi_mailles`).
7. Effectuer la jointure entre le fichier mailles et celui des métadonnées.

[1]: https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=301&id_rubrique=40