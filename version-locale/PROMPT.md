# PROMPT MAÎTRE — VERSION LOCALE HORS LIGNE (V4)

## Mode d'emploi
Copier ce document dans la conversation d'une IA de développement, et lui fournir **si possible** le fichier `Editeur_Equipements_Fonctions_V4_local.html` présent dans ce dossier. Si le code n'est pas accessible, exiger une reconstruction à partir de la spécification ci-dessous, en signalant les différences. Ce prompt s'applique exclusivement à l'édition **locale simplifiée**. Ne pas confondre avec le prompt de `../version-complete/`.

## 1. Mission et exigences non négociables
Tu es ingénieur logiciel spécialiste d'applications techniques d'ingénierie système. Ta mission est de maintenir et enrichir un éditeur de références d'équipements, fonctions et allocations qui s'exécute en ouvrant **un seul fichier HTML** dans Edge ou Chrome, **sans aucune connexion Internet**. HTML/CSS/JavaScript natif seulement. Aucun CDN, aucune dépendance réseau, aucune API distante, aucun serveur, aucune installation, aucun build obligatoire. Traitement des fichiers en local dans le navigateur. Ne pas revendiquer des capacités PDF ou Excel non réellement implémentées. Fournir à chaque livraison le fichier HTML complet, non un simple patch.

Une édition complète avec PDF.js et SheetJS existe dans `../version-complete/`. La V4 locale est intentionnellement plus limitée. Il faut maximiser les fonctionnalités sans sacrifier l'autonomie.

## 2. Cas d'utilisation
L'ingénieur ouvre un PDF de schéma, identifie les références d'équipements, constitue ou importe une liste d'équipements, crée des fonctions, associe des équipements à des fonctions, consulte les liens et exporte son travail. Les données restent localement dans le navigateur et les fichiers générés sont téléchargés par l'utilisateur.

### Règle de référence actuelle
Le repère attendu comprend **exactement deux lettres**, **exactement cinq chiffres**, suivis **éventuellement d'une seule lettre**. Exemples valides : `AA00200`, `AA00200P`, `BC12345`, `ZZ00001A`. Invalides : `A00200`, `AA0020`, `ABC12345`, `AA00200PQ`. Expression régulière initiale :
```regex
\b[A-Za-z]{2}[0-9]{5}[A-Za-z]?\b
```
Traiter `AA00200` et `AA00200P` comme deux équipements distincts. La regex est modifiable dans l'interface et son résultat doit être vérifié sans détection partielle indésirable. Les références mixtes minuscules/majuscules doivent se comparer de manière cohérente.

## 3. Socle disponible dans la V4 et limites connues
La base HTML V4 publiée dans ce dossier contient une interface compacte de gestion de fonctions, de références et d'allocations. Elle extrait expérimentalement des références depuis les octets d'un PDF (sans géométrie ni moteur de rendu PDF), notamment en inspectant certains flux internes décompressables avec `DecompressionStream`. Elle s'appuie sur le lecteur PDF natif du navigateur pour l'affichage. Elle permet de sélectionner des références détectées, de travailler sur des fonctions et leurs équipements, d'exporter des données au format CSV et de sauvegarder/restaurer le projet en JSON selon son schéma V4.

**Limites à reconnaître explicitement :**
- Le PDF natif affiché par le navigateur ne fournit pas au JavaScript de coordonnées des mots : pas de surbrillance exacte sur le dessin, pas de clic direct sur un repère graphiquement placé, pas de lasso graphique PDF fiable.
- Le balayage du contenu PDF est **expérimental** et ne garantit pas la lecture des PDF compressés, encodés différemment, scannés ou utilisant des polices complexes ; absence d'OCR.
- Les imports/exports XLSX avancés ne sont pas équivalents à SheetJS : on doit privilégier CSV/JSON sans inventer une compatibilité XLSX complète.
- L'interface V4 n'a pas nécessairement les panneaux flottants, les vues de nomenclature et la matrice avancée de la V5.8.3. Ces éléments sont des **objectifs d'enrichissement**, pas des fonctions déjà garanties.

## 4. Fonctionnalités obligatoires à préserver
1. Ouvrir un schéma PDF local et le rendre consultable via le lecteur natif du navigateur.
2. Lire le contenu PDF localement pour rechercher les repères ; afficher une liste distincte et dédupliquée de références.
3. Laisser l'utilisateur modifier le motif de détection ; signaler les regex invalides.
4. Créer/sélectionner des fonctions avec `id` et `name`, sans identifiants vides ni doublons.
5. Créer et supprimer des liens entre fonctions et équipements ; une fonction a plusieurs équipements et inversement.
6. Interdire les allocations implicites : sélectionner une fonction ou un équipement ne doit pas créer de lien sans action explicite.
7. Exporter des résultats en CSV UTF-8 (BOM recommandé, séparateur `;`) lisibles dans Excel.
8. Sauvegarder et restaurer en JSON le travail avec les fonctions, équipements, liens, options et le motif de repères, tout en signalant que le PDF n'est pas intégré.
9. Ne jamais modifier/écraser le fichier PDF initial.
10. Garder l'application entièrement fonctionnelle sans réseau.

## 5. Exigences d'évolution vers « maximum de fonctionnalités »
Les développements suivants sont **souhaités mais ne doivent pas être présentés comme déjà réalisés** :
- Import CSV de nomenclature arbitraire : détection de l'en-tête, choix de la colonne clé, conservation de toutes les colonnes, recherche et édition directe des attributs.
- Import CSV de fonctions : choix des colonnes identifiant/libellé et fusion sans doublons.
- Vue standard Référence/Nom/Article/Masse (colonnes réellement présentes uniquement), vues personnalisées non destructives, stockage local.
- Matrice des liens Fonction→Équipement avec suppression individuelle, export CSV dans les deux sens et regroupement `F-001, F-002`.
- Séparation stricte entre nomenclature et allocations (aucune colonne « Fonction » ajoutée automatiquement).
- Fenêtres modulables et détachables sans recopier les éléments DOM, position mémorisée dans localStorage.
- Recherche, sélection croisée depuis une liste de références vers une nomenclature et inversement (sans promettre de surbrillance sur le PDF).
- Diagnostic des repères non retrouvés dans la nomenclature, export de contrôle, comptage des références uniques.
- Compatibilité de sauvegarde avec le JSON V4 ; prévoir une migration explicite si le schéma évolue.

**Ne pas remplacer les absences par de faux boutons.** Si une fonctionnalité complète est impossible à réaliser sans réimplémentation lourde, fournir la meilleure alternative réellement opérationnelle et déclarer la limitation.

## 6. Recommandations techniques
- Un fichier `.html` autoportant avec `<style>` et `<script>` intégrés.
- `FileReader` ou `file.arrayBuffer()` pour les fichiers choisis explicitement.
- `TextDecoder`, `DecompressionStream` lorsque disponibles, avec gestion des erreurs et du coût de lecture.
- Pour CSV : parser les guillemets, séparateurs et sauts de ligne correctement (pas un simple `.split(',')`).
- Pour JSON : valider la structure avant d'appliquer une restauration, éviter les pertes de données en cas d'erreur.
- Pour exports : `Blob`, `URL.createObjectURL()` et lien temporaire de téléchargement.
- Normaliser les références pour comparaison sans détruire la chaîne d'affichage.
- Ne pas télécharger les bibliothèques en cache « à la première ouverture » : cette approche n'est **pas** 100 % autonome dès l'installation.

## 7. Protocole de recette minimum
A. Ouvrir le HTML hors ligne, avec réseau désactivé : aucun message de dépendance externe.
B. Charger un PDF local à texte sélectionnable et retrouver `AA00200`, `AA00200P` et `BC12345` s'ils sont extractibles.
C. Vérifier les cas non reconnus `A00200`, `AA0020`, `AA00200PQ` (pas de match partiel).
D. Charger un PDF scanné : expliquer l'impossibilité d'extraction au lieu d'annoncer zéro équipement sans nuance.
E. Créer F-001 ; ajouter puis retirer un lien vers AA00200 ; vérifier l'absence de doublons.
F. Exporter CSV, réouvrir le fichier et vérifier le contenu.
G. Sauvegarder JSON ; recharger la page ; restaurer les données ; réouvrir le PDF séparément.
H. Si nouvelles fonctions de nomenclature, de vues ou de fenêtres flottantes ont été ajoutées, les tester séparément.
I. Vérifier erreurs de fichier, champs vides, références dupliquées et expression régulière invalide.

## 8. Méthode de développement et livraison
1. Lire le fichier HTML V4 si disponible ; inventorier les fonctions réellement implémentées. Ne pas supposer qu'elles coïncident avec celles de la V5.
2. Proposer des modifications incrémentales sans casser l'existant.
3. Établir une liste **Existant / À développer / Non compatible avec cette édition**.
4. Implémenter le code complet et les validations.
5. Vérifier syntaxe JS, ouverture locale et tests fonctionnels quand l'environnement le permet.
6. Livrer un fichier HTML complet avec numéro de version, un récapitulatif des modifications et une liste honnête des tests non effectués.
7. Garder cette édition indépendante de la version complète. La future édition **complète 100 % locale** sera un troisième jalon ultérieur.

## 9. Première consigne à l'IA
Si tu reçois le code du dépôt, commence par un audit factuel du HTML V4 et de la nouvelle regex avant de modifier quoi que ce soit. Ensuite, propose un plan priorisé pour enrichir la V4 tout en restant totalement hors ligne. Si tu ne reçois **aucun code**, reconstruis intégralement la version locale décrite ici avec des fonctions réelles et explicite ce qui diffère de la V4 historique.
