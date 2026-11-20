# Version complète — V5.8.3

Ouvrir `Editeur_Nomenclature_Fonctions_V5_8_3.html` dans Edge ou Chrome avec accès Internet.

La version complète offre la gestion des schémas PDF interactifs, la nomenclature Excel éditable, les fonctions, la matrice d'allocations, la sélection PDF/nomenclature, le lasso, les vues personnalisées, les exports XLSX/CSV, les projets JSON et les fenêtres flottantes.

**Dépendances réseau** : PDF.js 3.11.174 (moteur et worker) et SheetJS XLSX 0.18.5 sont chargés depuis cdnjs. Sans connexion réseau initiale, le chargement PDF et Excel n'est pas garanti.

Motif de référence par défaut : `\\b[A-Za-z]{2}[0-9]{5}[A-Za-z]?\\b`.

Le moteur PDF recherche le texte extrait du document : les PDF scannés/image et les repères dont le texte est fragmenté ne sont pas garantis.


## Version de test V5.8.6 (16 novembre 2026)

La version [V5.8.6 — Surbrillance par attribut, couleur et export PDF](Editeur_Nomenclature_Fonctions_V5_8_6_TEST_COULEUR_EXPORT_PDF.html) est désormais publiée **en complément** de la V5.8.3, qui reste disponible.

Nouveautés : choix d'une colonne de nomenclature et d'une valeur (y compris des cellules multivaluées telles que `FT1, FT2`), panneau de surbrillance permanent, choix d'une couleur, surbrillance sur le PDF et la nomenclature, export du PDF contenant les surbrillances. L'export PDF ajoute la dépendance `pdf-lib` 1.17.1, chargée via CDN en plus de PDF.js et SheetJS. Version expérimentale : tests fonctionnels navigateur non encore validés.


## Version V6 (20 novembre 2026)

La version [V6 — Détection des repères sur les schémas CAO](Editeur_Nomenclature_Fonctions_V6.html) reprend la V5.8.6 et corrige la détection des repères sur les pages de schéma.

Les PDF exportés depuis la CAO découpent souvent le texte (caractères isolés, espacement entre lettres lu par PDF.js comme `C D 6 7 8 9 0 A`, polices alternées, texte vertical). La V6 reconstitue les lignes de texte de chaque page avant d'appliquer le motif de repère, puis place la zone cliquable sur l'emprise réelle du repère, y compris pour le texte tourné. La recherche historique par fragment est conservée, et les doublons sont éliminés.

Limites : les PDF dont le texte est vectorisé (polices SHX converties en traits), scanné ou stocké en annotations ne contiennent pas de texte exploitable. Dépendances inchangées par rapport à la V5.8.6 (PDF.js, SheetJS, pdf-lib via CDN). Validée sur un PDF de test reproduisant ces cas ; à confirmer sur des schémas réels.
