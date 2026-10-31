# Portfolio d'Adam — contexte pour reprendre le travail

Site statique (HTML/CSS/JS, aucun build, aucune dépendance) servi par GitHub Pages sur
**https://adam.nocturnz.xyz/** — dépôt `tristede/adam`, branche `main`. Un push = en ligne en
30 à 60 s. `README.md` documente le moteur et l'admin ; il décrit la page Projets unique et
les anciennes pages perso/académique qui redirigent vers `projets.html`.

Ce fichier dit quoi respecter et où on en est. À mettre à jour en fin de session.

## Règles (priorité absolue)

1. **Publier uniquement sur demande d'Adam.** Avant tout push : `git fetch`, vérifier que rien de
   plus récent n'est en ligne (Adam avance aussi avec d'autres agents, et `/admin.html` commit
   `data.json` directement), puis scanner le diff : **dépôt public, jamais de nom de famille ni
   d'adresse e-mail perso**. Après le push, vérifier le site en ligne (`script.js?v=N` servi).
2. **Ne pas toucher à la direction artistique** : fond bleu nuit étoilé, texte manuscrit qui se
   « décrypte » au survol sur ordinateur et automatiquement au scroll sur téléphone (effet
   `scramble`). C'est voulu, ne pas le « corriger ». Demander avant tout changement de DA.
3. **Positionnement : « créatif volatile », « enfant d'internet ».** Ne pas le présenter d'abord
   comme « créateur de contenu ». Ne citer aucun autre créateur, chaîne ou marque comme référence.
4. **TristeJeu** : on ne fait qu'une fiche dans ce portfolio. Ne jamais modifier le dossier du
   projet lui-même.
5. **NGC Hub** : parler des outils (dock OBS, régie IRL), jamais de l'histoire du collectif.
6. **Aucun son pendant les tests** : vidéos muettes, onglets fermés après usage.
7. Adam écrit en français familier et décide sur retour visuel : proposer, montrer, itérer. Il corrige
   précisément ; ne pas généraliser une correction à autre chose que ce qu'il désigne.

## Architecture

| Fichier | Rôle |
|---|---|
| `data.json` | **Tout le contenu** (textes, compétences, parcours, groupes, projets). JSON indenté 2 espaces, UTF-8 non échappé, retour ligne final (c'est le format qu'écrit l'admin : ne pas le reformater autrement, sinon gros diffs) |
| `script.js` | Tout le rendu (grilles, filtres, infobulles, pages détail, effet scramble). Partagé par toutes les pages et par la vue visuelle de l'admin |
| `style.css` / `ciel.css` | Design commun / ciel étoilé animé |
| `index.html` | Accueil : hero, 2 cartes (perso / académique), favori, sélection, à propos + compétences, parcours, bannière stage, contact |
| `projets.html` | **Page Projets unique** (filtres, grille). `projets-perso.html` et `projets-academiques.html` ne sont que des redirections vers `projets.html?cat=…` (elles restent chargeables dans l'admin) |
| `groupe.html?id=` / `projet.html?id=` | Pages détail, rendues par JS |
| `admin.html` | Panneau d'édition (formulaire + vue visuelle sur le vrai site), enregistre sur GitHub avec un token |
| `404.html`, `robots.txt`, `sitemap.xml`, `og.png` | SEO / partage |
| `images/`, `images/thumbs/`, `docs/` | Médias. `thumbs/` = miniatures de cartes en 1200 px de large |

Particularités à connaître :

- **Les pages HTML sont des fragments sans `<!DOCTYPE>`** (mode quirks, sauf `<html lang="fr">`
  ajouté en tête). Ne pas ajouter de DOCTYPE sans tout retester : ça peut décaler la mise en page.
- **Cache-busting manuel** : `style.css?v=N` et `script.js?v=N` dans *toutes* les pages (y compris
  `404.html`). Incrémenter N à chaque modification de ces fichiers, dans tous les HTML
  (`sed -i '' 's/style.css?v=22/style.css?v=23/' *.html`). Version actuelle : voir `index.html`.
- Le header et le footer sont dupliqués dans chaque page (volontaire, pas de composants).
- `admin.html` lit le même `script.js` avec `window.__EDIT_MODE__` : en édition, les éléments
  masqués restent visibles (grisés) et les descriptions se modifient sur les cartes (pas d'infobulle).
- Toute nouvelle clé de projet doit être gérée à trois endroits : le rendu (`script.js`), le
  formulaire de l'admin (champ + chargement + enregistrement), et le gabarit « nouveau projet ».

## Modèle de données

Projet : `id`, `title`, `year`, `current`, `ctx` (`perso` | `academique` | `stage`), `medium`
(`web` | `video` | `graphisme` | `audio` | `social` | `event` | `ecrit`), `tags[]`, `desc` (courte),
`longDesc`, `featured`, `hidden`, `secondary`, `preview`, `link`, `embed`, `assets[]`
(`image` | `video` | `audio` | `doc` | `web` | `text` | `carousel`), `thumb`, `subProjects[]`, `group`.

Groupe (`site.groups[]`) : `id`, `kicker`, `title`, `desc`, `thumb`, `featured`, `hidden`,
`socialLinks`. Un projet appartient à au plus un groupe (`project.group`).
Autres clés de `site` : `skills[{group,name,detail}]`, `timeline[]`, `stageCta`, `socialLinks`,
`favoriProjectId`, `theme`, textes d'accueil.

Statuts d'un projet :
- **`hidden`** : invisible partout sur le site public (conservé dans l'admin).
- **`secondary`** : absent de l'accueil et des groupes, visible uniquement quand un filtre
  (médium/tag) est actif sur la page Projets.
- **`featured`** : affiché dans « Projets mis en avant » sur l'accueil (un groupe peut l'être aussi ;
  ne pas marquer à la fois un groupe et ses projets).
- L'admin a un filtre « Statut » (Visibles / Secondaires / Masqués) pour retrouver les masqués.

## Comportements décidés (ne pas refaire autrement sans demander)

- **Page Projets** : à gauche `Perso | Académique`, à droite trois pastilles de médium (les
  mieux fournies : aujourd'hui Web, Vidéo, Graphisme) puis `+` qui ouvre une liste dans la page
  (pousse les cartes, ne flotte pas dessus). **Pas de bouton « Tout »** : rien de choisi = tout,
  recliquer retire le filtre. Catégorie et tag sont exclusifs ; **un tag cherche dans tout le
  portfolio**, projets de groupes et secondaires compris, à plat. État dans l'URL : `?tag=web`,
  `?cat=perso`. Les médiums sont les presets ; les `tags` libres alimentent la liste du `+`.
- **Cartes** : pas de description dans la grille sur appareil à survol. Après **0,35 s** de survol,
  infobulle avec la description seule (pas le titre, déjà sur la carte), 2 lignes max. Après
  **1 s**, si le projet a un `preview` (`.gif`, `.webp` animé, `.mp4`/`.webm`), il remplace la
  miniature (muet, en boucle). Sur tactile, la description reste affichée.
- **Groupes** : le badge « N projets » ouvre au survol un aperçu des projets (6 max).
- **Page projet** : phrase courte (`desc`) sous le titre ; **`longDesc` dans le corps, après les
  visuels** ; `embed: true` affiche le lien en iframe (voulu pour le site du club : on visite le
  site sans quitter le portfolio, garder).
- **Accueil** : compétences en pastilles (noms seuls, détail au survol), sans titre « Compétences », en
  deux groupes `Hard skills` / `Soft skills`, centrés, une pastille par ligne avec un
  espacement de 18 px ; parcours centré sur l'axe
  vertical en bureau (colonne à gauche en mobile) ; bannière stage et boutons centrés.
- Ligne de métier sous le prénom (`roleMain` + `roleAccent`).

## Règles de contenu

- **`desc` courte : mots-clés, 62 caractères max, séparés par « · », sans répéter le titre**
  (un contrôle de mots communs titre/description existait ; le refaire après chaque ajout). Le
  détail va dans `longDesc`.
- Pas de phrases creuses ; ton direct. Ne rien inventer : si un fait manque, le demander.
- Miniatures de cartes : WebP, ≤ 1200 px de large, dans `images/thumbs/`. Aperçus animés prévus dans
  `images/previews/` (dossier à créer) : 4 à 6 s, 480p, sans son, de préférence < 600 Ko. Un GIF
  brut est lourd (3 à 8 Mo) : le convertir en WebP animé.
- Pas d'embed TikTok (Adam n'en veut pas) : héberger/importer les vidéos autrement. Vidéos
  complètes sur YouTube (non répertorié accepté) ; Google Drive ne convient pas comme lecteur.

## État au moment de ce fichier

43 projets (20 visibles, 23 masqués), 6 groupes : Union Oasis Forest, Stage chez En Esprit,
Chloé Ly, Nocturnz, NGC Hub, Daybreak.

**Masqués par choix d'Adam** (laisser masqués) : `ilonka-club`, `montage-video-style-youtube`,
`miniatures-youtube`, `episode-podcast`, `melo-de-la-semaine`, `post-actualite`,
`thumbnails-youtube`, `reel-tiktok`, `community-management-easypermis`.

**Créés masqués, en attente de matière** (descriptions courtes déjà écrites, à compléter puis
démasquer) : `ngc-dock-obs`, `ngc-regie-irl-srt`, `daybreak-smp`, `lg-le-village`,
`oasis-outil-admin`, `oasis-strategie-sponsoring`, `oasis-rapport-social-media`, `esprit-soolking`,
`esprit-la-haine`, `esprit-workshops`, `pourquoi-tu-votes`, `feminitea`, `alertesinfos`,
`manif-video`.

**Matière qu'Adam doit fournir** (ne pas l'inventer) :
- vidéos d'autres projets pour Chloé Ly ; vidéo de la manifestation du 9 octobre ; vidéos Oasis en
  fichier (pas d'embed TikTok) ;
- noms des coéquipiers sur le reportage de BAC 2 ;
- clips d'aperçu (champ `preview`) pour les projets vidéo ;
- contexte pour étoffer les `longDesc` vides : rap, reportage, Echo Nexus, articles de presse, logo
  vectoriel, montage long format, Artwork ; et DEI-Belgique / #AvantTout à compléter ;
- à terme : séparer « Montage vidéo : long format » par tournage, rattacher les miniatures et reels
  aux projets de tournage correspondants ; ranger les projets Ilonka (vidéo à part, graphisme à masquer).

**Visibles sans miniature** : `union-oasis-forest-tiktok`, `nocturnz-review`, `nocturnz-todo`,
`nocturnz-edit`, `tristejeu` (fond avec icône par défaut).

## Pistes non faites (audit du 31 oct. 2026)

- Tester l'admin de bout en bout (enregistrement GitHub) : les champs « secondaire », « Statut »,
  « Aperçu animé » et la description longue séparée n'ont pas été éprouvés avec une vraie connexion.
- Contrastes, navigation clavier, Lighthouse, aperçus de partage réels ; `<!DOCTYPE>` ; pages
  `projet.html?id=` rendues en JS (peu indexables).
- Mettre le rôle chez Oasis dans le parcours est une décision d'Adam (il a retiré l'étape).

## Tester en local

```bash
python3 -m http.server 8124   # dans ce dossier, puis http://localhost:8124/
```

Pièges rencontrés :
- Naviguer vers `/#ancre` depuis `/` ne recharge pas la page : ajouter `?r=2` pour forcer un rechargement.
- Les règles bureau (`min-width: 800px`) ne s'appliquent pas dans un volet étroit : tester à
  1280 px de large, et en mobile à 375 px.
- Les cartes apparaissent au scroll (IntersectionObserver) : attendre après un scroll avant de mesurer.
- `html{scroll-behavior:smooth}` : un `scrollTo` programmatique est animé, utiliser `behavior:'instant'`.
- `404.html` ne s'affiche qu'en production (le serveur Python ne la sert pas).
- Un site externe en iframe (club) montre sa propre bannière de cookies : normal.

## Dernière vérification locale — 31 octobre 2026

- Les données et le rendu local contiennent déjà les groupes Hard skills / Soft skills.
  Leur présence dans le code ne vaut pas validation visuelle ni publication.
- README actualisé : page Projets unique, redirections, descriptions longues, statuts,
  aperçus et procédure de publication.
- Modifications locales préexistantes conservées et incluses dans le lot de publication
  autorisé par Adam : compétences Hard skills / Soft skills, titre Compétences et
  version de script `v=18`. Fetch effectué sans divergence ; JSON, syntaxe JavaScript,
  diff et confidentialité des ajouts vérifiés avant publication.
- Validation visuelle des compétences et tests réels de l’admin toujours à faire.

- Ajustements locaux demandés après publication : retrait du titre Compétences,
  libellés Graphisme et Vibecoding, groupes et pastilles centrés, espacement augmenté.
  Versions : CSS `v=26`, script `v=19`. Publication demandée par Adam.
- Pastilles de compétences de taille identique : 240 × 52 px, largeur limitée
  au conteneur sur petit écran, texte centré horizontalement et verticalement.
- Titres Hard skills / Soft skills en police manuscrite du site (`--font-script`),
  sans capitales forcées. Ces ajustements sont inclus dans la publication demandée.
