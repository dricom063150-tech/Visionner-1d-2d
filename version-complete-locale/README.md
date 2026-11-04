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
