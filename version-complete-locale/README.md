# Version complète locale — V5.8.4

Cette édition conserve l'interface et les fonctions de la V5.8.3, **mais charge les bibliothèques PDF.js et SheetJS depuis les fichiers inclus dans ce dossier**, sans CDN et sans dépendance à Internet.

## Arborescence

```text
version-complete-locale/
├── Editeur_Nomenclature_Fonctions_V5_8_4_local.html
├── README.md
├── PROMPT.md
└── libs/
    ├── pdf.min.js
    ├── pdf.worker.min.js
    ├── xlsx.full.min.js
    ├── LICENSE-PDFJS.txt
    └── LICENSE-SHEETJS.txt
```

## Utilisation

1. Sur GitHub, télécharger le **dépôt complet en ZIP** via `Code > Download ZIP` (ou cloner le dépôt). Conserver la structure `version-complete-locale/libs/`.
2. Extraire le ZIP sur le disque dur.
3. Ouvrir `version-complete-locale/Editeur_Nomenclature_Fonctions_V5_8_4_local.html` dans Edge ou Chrome.
4. Utiliser les trois panneaux d'import pour charger les fichiers PDF, nomenclature Excel et analyse fonctionnelle.

Aucune bibliothèque n'est téléchargée depuis Internet. Les PDF et fichiers Excel sont traités localement dans le navigateur.

**Attention :** une navigation directe depuis la page GitHub de prévisualisation ne lance pas l'application HTML ; il faut télécharger les fichiers. Les restrictions de sécurité liées à l'origine `file://` et au chargement du worker PDF peuvent varier selon les navigateurs : le comportement doit être **validé hors ligne sur le poste cible**. En cas de restriction, ne pas présenter l'application comme fonctionnellement validée ; étudier un worker intégré via Blob ou un lancement local adapté, sans appel Internet.

## Bibliothèques embarquées et licences

- PDF.js `3.11.174` : `libs/pdf.min.js`
- PDF.js worker `3.11.174` : `libs/pdf.worker.min.js`
- SheetJS `0.18.5` : `libs/xlsx.full.min.js`

Les fichiers sont distribués avec leurs avis et les textes de licence Apache 2.0 associés dans `libs/`. Conserver les mentions de licence en cas de redistribution.

## Ce qui change par rapport à V5.8.3

- Remplacement des deux balises `script src` CDN par des chemins relatifs `libs/pdf.min.js` et `libs/xlsx.full.min.js`.
- Remplacement de l'adresse CDN du worker par `libs/pdf.worker.min.js`.
- Messages de chargement adaptés au fonctionnement local.
- **Aucune réécriture volontaire de la logique métier.** La validation navigateur complète reste à faire.

## Limite de packaging

Ce dossier est **hors ligne mais multifichier**. La future livraison « un seul HTML embarquant les trois scripts » est distincte et n'est pas revendiquée ici.

## Sources du code des bibliothèques

Fichiers issus de la distribution officielle recopiée depuis `cdnjs/cdnjs` sur GitHub :
- `ajax/libs/pdf.js/3.11.174/pdf.min.js`
- `ajax/libs/pdf.js/3.11.174/pdf.worker.min.js`
- `ajax/libs/xlsx/0.18.5/xlsx.full.min.js`


---

# Version V6 locale — 100 % hors ligne (20 novembre 2026)

Fichier : [`Editeur_Nomenclature_Fonctions_V6_local.html`](Editeur_Nomenclature_Fonctions_V6_local.html) — **un seul fichier HTML autonome** (≈ 2,9 Mo).

Fonctions identiques à la [V6 complète](../version-complete/Editeur_Nomenclature_Fonctions_V6.html) : détection des repères sur les schémas issus de CAO, surbrillance par attribut, export du PDF surligné, nomenclature, fonctions, allocations, lasso, vues, exports XLSX/CSV/JSON, fenêtres flottantes.

## Garantie « aucune donnée ne sort du PC »

1. **Bibliothèques intégrées dans le HTML** : PDF.js 3.11.174 (moteur et worker), SheetJS 0.18.5 et pdf-lib 1.17.1, copiées sans modification (seul le commentaire `sourceMappingURL` de pdf-lib est retiré). Aucun CDN.
2. **Worker PDF.js créé en mémoire** (`blob:`) : il fonctionne lorsque la page est ouverte directement depuis le disque (`file://`), ce qui lève la limite signalée pour la V5.8.4.
3. **Politique de sécurité (CSP) intégrée** : `connect-src 'none'`, images, polices et scripts limités à `data:` / `blob:` / code intégré, `form-action 'none'`. Le navigateur **refuse toute connexion réseau** émise par la page, y compris par une bibliothèque.

Tests réalisés dans Chromium, réseau coupé : chargement PDF, nomenclature XLSX, fonctions CSV, liens, surbrillance, et les cinq exports (PDF surligné, nomenclature XLSX, liens XLSX, CSV, projet JSON) → **0 requête réseau, 0 erreur, 0 violation CSP**. Avec réseau actif, des tentatives volontaires d'envoi (`fetch`, `sendBeacon`, image distante) sont **bloquées par la CSP**.

Vérification personnelle : ouvrir le fichier, appuyer sur F12 → onglet *Réseau*, charger les fichiers et travailler ; aucune requête ne doit apparaître. On peut aussi couper le réseau : l'application fonctionne à l'identique.

## Ce qui reste local, sur le poste

- Le stockage du navigateur (`localStorage`) mémorise uniquement les vues de nomenclature et la position des fenêtres flottantes.
- Les exports sont générés dans le navigateur puis enregistrés dans le dossier de téléchargement.

## Reconstruction et contrôle

`construire_V6_local.py` régénère le fichier depuis la V6 complète et les bibliothèques de `libs/` :

```text
python3 construire_V6_local.py ../version-complete/Editeur_Nomenclature_Fonctions_V6.html libs libs/pdf-lib.min.js Editeur_Nomenclature_Fonctions_V6_local.html
```

Empreintes SHA-256 des bibliothèques (identiques aux paquets officiels npm `pdfjs-dist@3.11.174`, `xlsx@0.18.5`, `pdf-lib@1.17.1`) :

```text
0f9a5cad07941f0826586c94e089d89b918c46e5c17cf2d5a3c6f666e3bc694f  libs/pdf-lib.min.js
5b5799e6f8c680663207ac5b42ee14eed2a406fa7af48f50c154f0c0b1566946  libs/pdf.min.js
feabdf309770ed24bba31a5467836cdc8cf639c705af27d52b585b041bb8527b  libs/pdf.worker.min.js
c9506197caf809a075b6dee1da0d36fb19da7158ffe8a88e7b0c96c5d8623c99  libs/xlsx.full.min.js
```

Licences : Apache 2.0 (PDF.js, SheetJS) et MIT (pdf-lib), textes dans `libs/`.
