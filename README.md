# Visionneuse 1D / 2D — Éditeur technique

Deux éditions de l'application de gestion de schémas, nomenclatures, fonctions et allocations.

## [Version locale](version-locale/)
- Fichier HTML ouvrable sans réseau et sans bibliothèque externe.
- Basée sur le moteur expérimental V4 : extraction de repères du PDF et liste de références, gestion des fonctions/allocations et exports basiques.
- Détection configurée pour deux lettres, cinq chiffres et une lettre suffixe facultative (par exemple AA00200 et AA00200P).
- **Limitations :** pas de zones cliquables géométriquement sur le PDF, pas de lasso PDF ni de moteur complet d'import/export XLSX. Cette édition ne prétend pas avoir la parité avec la version complète.

## [Version complète](version-complete/)
- V5.8.3, application HTML interactive : PDF.js, SheetJS, nomenclature éditable, fonctions, allocations, lasso et panneaux flottants.
- **Dépendance réseau :** PDF.js et SheetJS sont chargés depuis des CDN au démarrage ; les données métier restent dans le navigateur.

## Utilisation
Télécharger le fichier HTML voulu depuis son sous-dossier, puis l'ouvrir dans Edge ou Chrome. Les deux éditions n'envoient pas de données métier à un serveur applicatif.

## Roadmap
- Enrichir la version locale avec le maximum de fonctionnalités compatibles hors ligne.
- Produire ultérieurement une édition complète entièrement hors ligne en incorporant les bibliothèques au fichier HTML.

## Avertissement
La détection des références du PDF dans l'édition locale est expérimentale et dépend de la structure interne des PDF. Tester sur des documents représentatifs avant emploi.
