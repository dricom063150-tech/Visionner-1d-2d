# PROMPT MAÎTRE — VERSION COMPLÈTE V5.8.3 (CDN)

## Mode d'emploi
Fournir ce document à l'IA de développement, avec si possible le fichier `Editeur_Nomenclature_Fonctions_V5_8_3.html` présent dans ce dossier. S'il n'est pas transmissible, la spécification ci-dessous permet de **reconstruire de zéro** une version fonctionnellement équivalente. Ne pas demander le code historique comme condition préalable. Ne pas confondre avec la version locale simplifiée.

## 1. Mission et socle technique
Développe/maintiens l'**Éditeur technique — Schémas, nomenclature et fonctions**, version cible V5.8.3. C'est une application d'ingénierie système qui relie des repères présents sur un PDF multipage, les lignes d'une nomenclature Excel et des fonctions système, avec allocations fonction→équipements.

Fournir **un fichier HTML complet** (HTML5, CSS, JS natif), ouvert directement dans Edge/Chrome. Pas de serveur, pas de React, pas de framework, pas d'application à installer. Tous les traitements des fichiers métier s'exécutent dans le navigateur. **Cette édition utilise volontairement des CDN** ; ne pas la présenter comme totalement hors ligne.

Dépendances exactes :
- PDF.js 3.11.174 : `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js`
- Worker associé : `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js`
- SheetJS XLSX 0.18.5 : `https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js`

Afficher une erreur compréhensible lorsque l'une des bibliothèques n'a pas pu charger. Les sources PDF/Excel ne sont pas envoyées à un serveur applicatif.

## 2. Identité visuelle
Interface dense, sombre et professionnelle :
- fond `#101A2B`, texte `#E9EDF0`, accent or `#C7A36A` ;
- panneaux `#19283B`, bordures `#33475E`, champs `#18283C`, boutons secondaires `#26374D` ;
- texte secondaire `#AEBBC9`, fond du visualiseur `#344054`, danger `#5B3039` ;
- sélection nomenclature `#27635B`, contour `#58D5B2` ;
- police `system-ui, Segoe UI, Arial, sans-serif` ;
- en-tête avec « Éditeur technique V5.8.3 » et sous-titre « Schéma PDF · Nomenclature Excel · Allocations fonctionnelles » ;
- boutons en haut « Sauvegarder le projet JSON » et « Charger un projet JSON ».

**Exactement deux onglets** :
1. « Espace de travail » (ouvert par défaut) ;
2. « Chargement des fichiers ».
Ne pas réintroduire une refonte à trois onglets. Changer d'onglet ne détruit pas les éléments ni l'état.

## 3. Onglet Chargement des fichiers
Trois panneaux en grille :
1. « 1 · Schéma PDF » : sélecteur PDF, bouton explicite « Charger / remplacer le schéma », nom de fichier, champ « Format des repères ».
2. « 2 · Nomenclature Excel / CSV » : sélecteur `.xlsx/.xls/.csv`, bouton « Charger / remplacer la nomenclature », sélecteur de feuille, sélecteur « Colonne clé ».
3. « 3 · Analyse fonctionnelle Excel / CSV » : sélecteur Excel/CSV, bouton « Charger l'analyse fonctionnelle », sélecteurs « ID » et « Libellé ». L'import est facultatif : on peut créer des fonctions manuellement.

N'importer qu'au clic des boutons, pas automatiquement à la sélection du fichier.

### Nouvelle règle de reconnaissance V5.8.3
Deux lettres puis cinq chiffres et suffixe **d'une lettre facultative**. Regex **par défaut** :
```regex
\b[A-Za-z]{2}[0-9]{5}[A-Za-z]?\b
```
Valides : `AA00200`, `AA00200P`, `BC12345` ; invalides : `A00200`, `AA0020`, `ABC12345`, `AA00200PQ`. Ne jamais confondre `AA00200` et `AA00200P`. Une regex invalide doit provoquer une erreur contrôlée. Attention : un ancien JSON peut restaurer l'ancien motif ; l'interface doit le signaler ou laisser l'utilisateur le modifier. Les matches ne doivent pas correspondre à des sous-chaînes de repères plus longs.

## 4. Disposition de l'Espace de travail
Sur grand écran, grille `260px minmax(320px,1fr) 370px`, écart de 12 px. Colonne gauche : panneau « Fonctions » puis « Vues de nomenclature ». Centre : « Schéma interactif ». Droite : « Nomenclature — vue active ». Sous la grille, sur toute la largeur : « Matrice Fonction–Équipement » et commandes d'export. Responsive par empilement sous 1100/700 px.

Panneaux compacts, bordure arrondie 9 px, padding 13 px, sans panneau « Fiche équipement » redondant.

## 5. Modèle de données
État JS central équivalent à :
```js
const state = {
  pdfBytes: null, bomWorkbook: null, bomSheet: "",
  bomRows: [], columns: [], key: "",
  functions: [], allocations: [], activeFunction: "",
  linkMode: false, selected: "",
  views: [], activeView: "standard",
  scale: 1.15, pdfItems: [], pdfPageCount: 0
};
```
- `bomRows` : une ligne objet par équipement ; colonnes libres, valeurs modifiables.
- `key` : colonne de référence équipement.
- `functions` : objets `{id,name}`.
- `allocations` : objets `{functionId,equipment}`, séparés de la nomenclature.
- Relation plusieurs-à-plusieurs ; pas de doublons.
- Normaliser les références de comparaison (casse, espaces, tirets) mais conserver la valeur affichée.

**Règle fondamentale : sélectionner une fonction ou un équipement ne crée jamais une allocation.** Seul le mode de création explicitement activé autorise le clic sur un repère PDF à créer un lien.

## 6. PDF interactif
- Importer le PDF avec `pdfjsLib.getDocument` en conservant les octets en mémoire.
- Rendre chaque page dans un `canvas` en utilisant `page.getViewport({scale})`.
- Extraire les objets texte avec `page.getTextContent()`.
- Appliquer la regex à chaque texte ; pour chaque occurrence, créer un élément HTML `.hit` positionné en absolu sur la page, à l'aide des transformations PDF.js (`pdfjsLib.Util.transform(viewport.transform,item.transform)`) et de la position relative de la sous-chaîne.
- Chaque repère trouvé est cliquable ; sa sélection synchronise la nomenclature. Un repère peut apparaître plusieurs fois ; l'identité est sa référence, pas le nœud graphique.
- Zone de consultation scrollable, fond `#344054`, hauteur min 560 px, max 74vh, pages séparées de 15 px, zoom.
- Zoom initial 1.15, incréments ±0.2, bornes 0.45 à 2.5 ; pourcentage `Math.round(scale/1.15*100)`.
- État visuel : repères détectés en orange, liés à la fonction active en vert, équipement sélectionné avec contour cyan ; surbrillance pouvant coexister.
- Sélecteur « Référence détectée » et bouton « Afficher la fiche » : ce bouton sélectionne/navigue sans créer de panneau supplémentaire.
- Éviter les résultats de rendus concurrents : compteur `pdfRenderVersion` et abandon des rendus périmés.
- Limites connues : les PDF scannés et certains repères fragmentés dans le contenu texte ne seront pas reconnus sans OCR/traitement avancé. Les coordonnées des sous-chaînes ne sont qu'une estimation.

## 7. Nomenclature et synchronisation bidirectionnelle
- Import Excel/CSV avec SheetJS ; permettre de choisir la feuille ; lire tableau de cellules `sheet_to_json({header:1,defval:"",raw:false})`, première ligne non vide comme en-tête, colonnes vides/dupliquées renommées, lignes complètement vides ignorées.
- Identifier automatiquement une colonne clé plausible : Référence/Repère/Tag/Identifiant/Equipment ID ; possibilité de changer.
- Tableau avec champs directement éditables, sans écraser le fichier importé.
- Champ « Rechercher un équipement » : chercher dans tous les attributs, insensible à la casse.
- Afficher au maximum les 400 premières lignes filtrées ; **toutes** les données restent en mémoire et à l'export. Garantir la visibilité de la ligne sélectionnée, même au-delà de 400.
- PDF→nomenclature : clic sur un `.hit` sélectionne et fait défiler jusqu'à la ligne correspondante.
- Nomenclature→PDF : clic sur une ligne sélectionne et navigue vers la première occurrence de la référence sur le PDF ; aucune allocation implicite.
- Clé modifiée : refuser vide/doublon, réécrire les allocations concernées et actualiser la sélection.
- Afficher un état clair si une référence PDF est absente de la nomenclature.

## 8. Fonctions et vues
- Panneau « Fonctions » : liste scrollable des fonctions ID+libellé ; fonction active avec contour or ; création manuelle ID+libellé bouton « Ajouter » ; rejeter IDs vides/doublons.
- Import analyse fonctionnelle XLSX/CSV avec choix des colonnes ID/libellé ; fusionner selon ID sans doublons, actualiser le libellé d'une fonction déjà connue.
- Panneau « Vues de nomenclature » : sélecteur, « Nouvelle vue », « Modifier », « Supprimer », éditeur nom+cases à cocher et « Enregistrer/Annuler ».
- « Vue standard » non modifiable/non supprimable : afficher la colonne clé et si présentes les colonnes correspondant à Nom/Désignation, Article/Part number et Masse/Poids.
- Vues personnalisées non destructives : ID, nom, champs ordonnés ; persistance localStorage clé `techViewsV5`, sauvegarde aussi dans le projet JSON.

## 9. Mode « Créer des liens » + lasso
- Par défaut `linkMode=false` et statut « Mode consultation ».
- Bouton « Créer des liens » : exige qu'une fonction soit sélectionnée ; affiche clairement le mode actif.
- En mode de création seulement, un clic sur un `.hit` ajoute `{functionId: activeFunction, equipment: ref}` sans doublon.
- Bouton « Terminer / quitter le mode » : stoppe toute création implicite.
- Lasso rectangulaire PDF : `pointerdown/move/up/cancel` sur une page ; afficher rectangle pointillé jaune translucide ; à la fin, intersecter les rectangles des `.hit` de cette page, dédupliquer les références, ajouter les liens de la fonction active, afficher compte nouveaux liens/références touchées.
- Cliquer sur une ligne de nomenclature ou une fonction ne doit jamais créer d'allocation, même en mode création.

## 10. Matrice et exports
Panneau « Matrice Fonction–Équipement » sous le workspace : table `Fonction | Libellé | Équipement | Action`. Une ligne par association et bouton « Retirer » qui supprime seulement ce lien.

Boutons et formats :
1. **« Exporter nomenclature XLSX »** → `Nomenclature_modifiee.xlsx`, onglet `Nomenclature`, **toutes** les colonnes et lignes avec modifications, indépendamment du filtre/vue ; aucune colonne « Fonction » ajoutée.
2. **« Exporter liens Équipement / Fonction »** → `Liens_Equipement_Fonction.xlsx`, deux onglets :
   - `Fonction vers équipement` : `ID fonction | Libellé fonction | Référence équipement`, une ligne par lien, tri ID fonction puis équipement ;
   - `Équipement vers fonction` : `Référence équipement | Fonctions | Libellés fonctions`, une ligne par équipement lié ; IDs et libellés triés puis joints avec `, `, sans doublons.
3. **« Allocations CSV »** → `Allocations_Fonction_Equipement.csv` ; colonnes ID fonction, Libellé fonction, Référence équipement ; délimiteur `;`, UTF-8 BOM, guillemets échappés.

## 11. Sauvegarde / restauration
- « Sauvegarder le projet JSON » → `Projet_Equipements_Fonctions.json`.
- Objet enregistré : `{version:5,bomRows,columns,key,functions,allocations,views,activeView,pattern,pdfNotEmbedded:true}`.
- Ne pas intégrer le PDF ni les classeurs Excel binaires ; les lignes importées de nomenclature sont **bien** dans le JSON.
- « Charger un projet JSON » : restaurer les données et vues, désactiver le mode création, recalculer les tableaux, inviter à recharger le PDF.
- Gérer les fichiers JSON mal formés et les versions anciennes, sans effacer silencieusement l'état sur échec de validation.
- La disposition des fenêtres flottantes est sauvegardée **séparément** dans localStorage.

## 12. Fenêtres détachables et modulables
Les cinq panneaux « Schéma », « Nomenclature », « Fonctions », « Vues », « Matrice » sont ancrés dans la grille par défaut et chacun possède « Détacher ».
- Détachement : créer un placeholder à l'ancien emplacement, déplacer **le même élément DOM** dans `document.body`, appliquer position `fixed`, largeur/hauteur, ombre/bordure or, z-index en avant-plan ; bouton devient « Ranger ».
- Déplacement par glissement de la barre de fenêtre (Pointer Events), sans démarrer si le clic cible un bouton ; garder l'en-tête accessible.
- Redimensionnement via CSS `resize:both;overflow:auto`, min largeur ~260 px et hauteur ~160 px ; suivre via `ResizeObserver` si disponible.
- « Ranger » ou « Remettre ici » réinsère le même DOM dans la grille.
- Enregistrer/restaurer positions et dimensions via la clé localStorage exacte `editeur-v582-floating-layout`, identifiants de panneaux `schema`, `nomenclature`, `fonctions`, `vues`, `allocations`.
- Après détachement, zoom PDF, lasso, sélection, édition et exports doivent toujours fonctionner.

## 13. Tests de réception
A. Charger PDF multipage, 11 références uniques avec motif AA99999/suffixe ; rejeter les faux positifs et différencier `AA00200` de `AA00200P`.
B. Charger nomenclature XLSX avec colonnes arbitraires, changer la feuille et la clé, retrouver une référence absente.
C. Clic PDF→ligne nomenclature et clic nomenclature→occurrence PDF ; vérifier la bonne surbrillance et la navigation.
D. Modifier masse et référence, vérifier propagation et absence de doublons.
E. Importer/créer fonctions, sélectionner une fonction : **aucun lien automatique**.
F. Activer « Créer des liens », clic PDF puis lasso ; vérifier les liens et l'absence de doublons ; quitter le mode.
G. Retirer un lien ; contrôler les surbrillances et la matrice.
H. Créer/supprimer une vue ; confirmer qu'elle n'altère pas les données.
I. Exporter nomenclature XLSX complète, classeur des liens à deux onglets et CSV ; contrôler lignes/colonnes, tris et regroupements.
J. JSON sauvegardé/restauré sans PDF : vérifier états puis recharger PDF.
K. Détacher/déplacer/redimensionner/ranger les cinq fenêtres ; recharger la page et confirmer la persistance et les interactions.
L. Tests négatifs : regex invalide, Excel vide, JSON incorrect, PDF scanné, plusieurs centaines de lignes, bibliothèque CDN inaccessible.

## 14. Priorités et règles de livraison
- Si le fichier HTML existe : l'inspecter entièrement, auditer les fonctionnalités réellement implémentées et faire des changements incrémentaux. Ne pas le remplacer par une maquette.
- Si le fichier HTML est inaccessible : **reconstruire intégralement à partir de ce prompt**, sans exiger de pièce jointe, et fournir un fichier complet exécuté/testé autant que possible.
- Toujours distinguer **implémenté**, **testé**, **limitation**, **amélioration envisagée**.
- Ne pas créer de fausses commandes, ne pas prétendre qu'une vérification syntaxique équivaut à une recette navigateur.
- Préserver les noms des exports, les clés localStorage, les deux onglets et les règles de métier.
- La future édition complète **100 % locale avec bibliothèques embarquées** est prévue plus tard : **ne pas supprimer aujourd'hui les bibliothèques CDN** et ne pas fusionner silencieusement les éditions.
