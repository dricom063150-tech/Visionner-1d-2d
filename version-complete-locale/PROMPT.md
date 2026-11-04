# PROMPT MAÎTRE — VERSION COMPLÈTE 100 % LOCALE V5.8.4

Tu es un développeur senior HTML/CSS/JavaScript, PDF.js et SheetJS spécialisé en ingénierie système.

## Mission
Maintenir et améliorer **l'application existante dans ce dossier**, `Editeur_Nomenclature_Fonctions_V5_8_4_local.html`, en préservant le comportement métier de la V5.8.3 tout en garantissant qu'aucune dépendance réseau n'est nécessaire. Les bibliothèques sont **déjà enregistrées localement** dans `libs/`.

Ne pas repasser aux CDN ni supprimer le moteur PDF.js, l'édition XLSX ou le lasso. Ne pas remplacer l'application par une version simplifiée.

Si le code du dossier est disponible, l'inspecter intégralement avant toute évolution. Sinon, reprendre le cahier des charges fonctionnel détaillé de `../version-complete/PROMPT.md`, en substituant les bibliothèques locales aux URLs CDN.

## Fichiers obligatoires
```text
Editeur_Nomenclature_Fonctions_V5_8_4_local.html
libs/pdf.min.js
libs/pdf.worker.min.js
libs/xlsx.full.min.js
```
Les chemins relatifs doivent fonctionner lorsque le dossier complet est copié d'un ordinateur à un autre. Le PDF n'est pas intégré au JSON projet.

## Fonctionnalités à conserver
- Interface sombre et compacte ; exactement deux onglets « Espace de travail » et « Chargement des fichiers ».
- Chargement du schéma PDF multipage, zoom et extraction du texte PDF.
- Motif par défaut des repères : `\b[A-Za-z]{2}[0-9]{5}[A-Za-z]?\b` ; références telles que `AA00200` et `AA00200P` distinctes ; pas de faux positifs partiels.
- Zones interactives localisées sur le schéma PDF ; surbrillance et synchronisation vers la nomenclature.
- Nomenclature Excel/CSV à colonnes arbitraires, sélection de feuille et colonne clé, cellules éditables, recherche, vues personnalisées.
- Analyse fonctionnelle Excel/CSV ; fonctions `{id,name}` saisissables manuellement.
- Mode consultation par défaut sans allocation implicite ; mode « Créer des liens » explicite ; sélection multiple par lasso ; associations séparées de la nomenclature et sans doublons.
- Matrice fonction-équipement et retrait individuel des liens.
- Export nomenclature `Nomenclature_modifiee.xlsx`, export deux feuilles `Liens_Equipement_Fonction.xlsx`, export CSV.
- Sauvegarde/restauration `Projet_Equipements_Fonctions.json` (sans PDF binaire).
- Cinq fenêtres détachables, déplaçables, redimensionnables et réancrables ; persistance via `editeur-v582-floating-layout`.

## Dépendances hors ligne
**Aucun script ne doit être référencé par HTTP(S).** Les balises de chargement doivent pointer sur :
```html
<script src="libs/pdf.min.js"></script>
<script src="libs/xlsx.full.min.js"></script>
```
Le worker PDF doit être configuré via `pdfjsLib.GlobalWorkerOptions.workerSrc = "libs/pdf.worker.min.js"`, sauf mise en œuvre d'une solution encore plus robuste, toujours hors ligne.

## Point de vigilance prioritaire : file:// et PDF worker
Tester **en désactivant le réseau** l'ouverture directe du HTML dans Edge ou Chrome. Les restrictions de Worker et d'accès aux fichiers `file://` peuvent varier. Si le worker relatif ne démarre pas :
1. Identifier précisément l'erreur navigateur.
2. Rechercher une solution complètement locale compatible avec le navigateur, par exemple l'amorçage explicite d'un worker/fake-worker ou un empaquetage inline.
3. Ne pas imposer de serveur réseau externe ni masquer l'échec.
4. Retester la lecture PDF, la détection des repères et le lasso.

## Recette obligatoire
- Débrancher réseau, ouvrir HTML.
- Charger PDF et Excel : aucune erreur liée aux bibliothèques.
- Détecter `AA00200`, `AA00200P` ; rejeter `AA0020` et `AA00200PQ`.
- Clic PDF ↔ nomenclature, modification attribut et export.
- Créer F-001 ; cliquer en consultation : zéro nouveau lien. Activer « Créer des liens » : clic et lasso fonctionnent et évitent les doublons.
- Vérifier exports XLSX (y compris les deux onglets) et CSV, JSON sauvegardé/restauré.
- Détacher/déplacer/redimensionner/ranger toutes les fenêtres et restaurer la disposition.
- Tester avec des fichiers représentatifs, plusieurs pages et centaines d'équipements.
- Tester la différence entre ouvrir localement et lancer une prévisualisation de GitHub.

## Consignes de livraison
Toujours livrer **tous les fichiers nécessaires**, sans omission de `libs/`. Signaler les tests réellement réalisés et les limites. Ne pas appeler « fichier HTML autonome unique » une livraison qui contient encore des scripts séparés. Conserver les mentions de licence PDF.js et SheetJS.
