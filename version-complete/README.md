# Version complète — V5.8.3

Ouvrir `Editeur_Nomenclature_Fonctions_V5_8_3.html` dans Edge ou Chrome avec accès Internet.

La version complète offre la gestion des schémas PDF interactifs, la nomenclature Excel éditable, les fonctions, la matrice d'allocations, la sélection PDF/nomenclature, le lasso, les vues personnalisées, les exports XLSX/CSV, les projets JSON et les fenêtres flottantes.

**Dépendances réseau** : PDF.js 3.11.174 (moteur et worker) et SheetJS XLSX 0.18.5 sont chargés depuis cdnjs. Sans connexion réseau initiale, le chargement PDF et Excel n'est pas garanti.

Motif de référence par défaut : `\\b[A-Za-z]{2}[0-9]{5}[A-Za-z]?\\b`.

Le moteur PDF recherche le texte extrait du document : les PDF scannés/image et les repères dont le texte est fragmenté ne sont pas garantis.


## Version de test V5.8.6 (16 novembre 2026)

La version [V5.8.6 — Surbrillance par attribut, couleur et export PDF](Editeur_Nomenclature_Fonctions_V5_8_6_TEST_COULEUR_EXPORT_PDF.html) est désormais publiée **en complément** de la V5.8.3, qui reste disponible.

Nouveautés : choix d'une colonne de nomenclature et d'une valeur (y compris des cellules multivaluées telles que `FT1, FT2`), panneau de surbrillance permanent, choix d'une couleur, surbrillance sur le PDF et la nomenclature, export du PDF contenant les surbrillances. L'export PDF ajoute la dépendance `pdf-lib` 1.17.1, chargée via CDN en plus de PDF.js et SheetJS. Version expérimentale : tests fonctionnels navigateur non encore validés.
