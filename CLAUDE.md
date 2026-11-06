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
4. **TristeJeu** : groupe dans ce portfolio, avec un projet par jeu. Ne jamais modifier le dossier du
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
(`image` | `video` | `audio` | `doc` | `web` | `text` | `carousel` | `beforeafter`), `thumb`, `subProjects[]`, `group`, `newUntil` (date d'expiration du badge NEW, facultatif).

Groupe (`site.groups[]`) : `id`, `kicker`, `title`, `desc`, `thumb`, `featured`, `hidden`,
`socialLinks`, `parent` (id du groupe parent, facultatif), `newUntil` (date d'expiration du badge NEW, facultatif). Un projet appartient à au plus un groupe (`project.group`).
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
  deux groupes `Hard skills` / `Soft skills` sous le texte À propos, côte à côte ;
  pastilles de largeur naturelle avec retour à la ligne et espacement de 10 px ; parcours centré sur l'axe
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

69 projets (42 visibles, 27 masqués), 11 groupes :
Union Oasis Forest, En Esprit et Vidéos, Chloé Ly, Nocturnz, NGC Hub, Daybreak,
Projet 360° : DEI-Belgique, TristeJeu, Identité visuelle d’Echo Nexus, AdamXBC.

**Masqués par choix d'Adam** (laisser masqués) : `ilonka-club`, `montage-video-style-youtube`,
`miniatures-youtube`, `episode-podcast`, `melo-de-la-semaine`, `post-actualite`,
`thumbnails-youtube`, `reel-tiktok`, `community-management-easypermis`, `nocturnz-edit`, `montage-video-long-format`.

**Créés masqués, en attente de matière** (descriptions courtes déjà écrites, à compléter puis
démasquer) : `ngc-dock-obs`, `ngc-regie-irl-srt`, `daybreak-smp`,
`oasis-outil-admin`, `oasis-strategie-sponsoring`, `oasis-rapport-social-media`, `esprit-la-haine`, `esprit-workshops`, `pourquoi-tu-votes`, `feminitea`, `alertesinfos`.

**Matière qu'Adam doit fournir** (ne pas l'inventer) :
- vidéos d'autres projets pour Chloé Ly ; vidéos Oasis en
  fichier (pas d'embed TikTok) ;
- noms des coéquipiers sur le reportage de BAC 2 ;
- clips d'aperçu (champ `preview`) pour les projets vidéo ;
- contexte pour étoffer les `longDesc` vides : rap, reportage, Echo Nexus, articles de presse, logo
  vectoriel, montage long format, Artwork ; et DEI-Belgique / #AvantTout à compléter ;
- à terme : rattacher les miniatures et reels
  aux projets de tournage correspondants ; ranger les projets Ilonka (vidéo à part, graphisme à masquer).

**Visibles sans miniature** : `union-oasis-forest-tiktok`, `dei-agence-site`, `lg-le-village`, `daybreak-discord`, `daybreak-aeterna`.

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
  Versions : CSS `v=29`, script `v=19`. Publication demandée par Adam.
- Pastilles de compétences de taille identique : 240 × 52 px, largeur limitée
  au conteneur sur petit écran, texte centré horizontalement et verticalement.
- Titres Hard skills / Soft skills en Schoolbell (`--font-title`), comme « Curieux de nature »,
  sans capitales forcées. Ces ajustements sont inclus dans la publication demandée.
- Nocturnz Edit masqué à la demande d’Adam ; médium changé de `web` à `video`
  (extension Premiere Pro), tags Outil et Montage vidéo conservés.

- Dernière décision : retour à la disposition initiale des skills (alignement gauche,
  largeur naturelle, écart de 10 px), en conservant les nouveaux libellés et les titres
  manuscrits. Remplace les consignes de centrage et de taille uniforme ci-dessus.
- En Esprit : cinq fiches vidéo séparées (MEESYZ, Sins/SDM, Soolking, Mallaury, Udeyfa),
  chacune avec sa vidéo et une miniature WebP issue de YouTube. Ancienne fiche long
  format masquée, médias conservés pour référence. La Haine et Workshops restent masqués.
- Correction précisée par Adam : la police des titres de skills est celle du titre
  « Curieux de nature, touche-à-tout par passion » (Schoolbell), pas Homemade Apple.

- Relecture locale des descriptions : Nocturnz décrit désormais l’usage des outils
  (sites de présentation, annotation vidéo, listes partagées, extension Premiere Pro).
  Descriptions vagues précisées à partir des informations existantes ; VEO développé,
  Cinematek recentré sur les visuels, tournages En Esprit différenciés.
  Tous les projets et groupes restent sous 62 caractères. Mise à jour non publiée.
- Ajustement local suivant : Hard skills à gauche et Soft skills à droite, en deux
  colonnes ; pastilles de largeur naturelle conservées. Community management retiré
  des compétences uniquement, à la demande d’Adam. Non publié.

- Groupes imbriqués en local : `parent` relie un groupe à son parent. En Esprit
  contient le sous-groupe Vidéos, qui contient les cinq tournages visibles.
  Les cartes du niveau principal restent au niveau racine ; compteurs et aperçus
  incluent les descendants. Filtres par tag toujours à plat. Retour du sous-groupe
  vers son parent ; masquage hérité des ancêtres.
- Admin visuel : création de sous-groupes depuis une page groupe, choix du parent
  sur les cartes et les pages groupe, cycles interdits. Supprimer un groupe
  conserve ses sous-groupes et les remonte au niveau supérieur.
  Script local `v=20`, CSS `v=29`. Non publié.
- Miniatures : zoom systématique de 15 % dans le cadre, avec débordement masqué,
  pour remplir les cartes et couper les bandes intégrées aux images YouTube.
  Même recadrage pour les aperçus animés et les cartes favorites. CSS local `v=30`.

- Miniatures web : format de référence Nocturnz, capture du site dans un cadre
  arrondi gris, marges et fond noir (1200 × 675 px). Oasis Forest, Review, Todo et
  TristeJeu disposent de nouvelles captures WebP. Les cartes web et groupes web
  conservent ces marges (sans zoom ni dégradé par-dessus la capture).
  Les outils masqués sans URL ni interface fournie restent à illustrer.
- TristeJeu reste une seule fiche, lien https://tristejeu.web.app/ fourni par Adam,
  avec cinq sections : TristeParty, Qui De Nous ?, Loup-Garou, Qui suis-je ?, WA7AD.
  Liste et règles vérifiées dans le catalogue public de la version en ligne ;
  aucune modification du dépôt TristeJeu. Captures de jeux à fournir ensuite.
  Versions locales CSS `v=31`, script `v=21`. Non publié.
- Vérification locale : les cinq projets web visibles ont une miniature ; la fiche
  TristeJeu affiche les cinq jeux et leur description. Aucun salon créé et aucun
  son déclenché pendant les captures.

## Lot de publication autorisé — 31 octobre 2026

Descriptions clarifiées, skills en deux colonnes sans Community management,
En Esprit → Vidéos, zoom des miniatures hors Web, captures web encadrées,
fiche TristeJeu avec cinq jeux. Versions finales : CSS `v=32`, script `v=21`.
Fetch sans divergence ; syntaxe, données, versions HTML et scénarios de groupes
vérifiés. Rendu public vérifié en local ; enregistrement GitHub de l’admin non testé.
Ce lot remplace le statut « non publié » des étapes locales ci-dessus.

## Ajustements locaux après publication

- Miniatures Review et Todo remplacées par les interfaces : capture de la review
  fournie par Adam (lecture en pause) et capture Todo fournie. Cadre web conservé.
  Aucun lien privé de review enregistré dans les fichiers du portfolio.
- Skills sous le texte À propos : deux groupes côte à côte, pastilles compactes
  qui se répartissent sur plusieurs lignes. Texte manuscrit conservé.
- Tags des groupes déduits des projets descendants : quatre tags les plus présents
  sur les cartes, tous les tags en liens vers le filtre global dans la page groupe.
  Aucun champ supplémentaire à maintenir dans l’admin.
- Versions locales : CSS `v=33`, script `v=22`. Non publié.

## Ajustements en cours de publication

- Projet 360° DEI converti en groupe : Présentation de la campagne (six visuels
  conservés), Multipage stratégique (trois médias dont le PDF), Site de l’agence
  fictive (lien existant). Favori transféré au groupe. Le site lié présente une
  erreur de certificat : aucune capture ni contenu supplémentaire inventé.
- TristeJeu converti en véritable groupe avec cinq projets de jeux, remplaçant les
  anciennes sections. Les anciens liens de projet devenus groupes redirigent vers
  le groupe correspondant. Pas de modification des dépôts de ces autres projets.
- Daybreak visible en perso avec LeVillage, Site web, Discord et Aeterna ; les trois
  dernières fiches attendent leurs liens et/ou leur contexte. Nouveau médium Jeu
  pour LeVillage, disponible aussi dans les formulaires de l’admin.
- Nocturnz mis en avant. La sélection défile horizontalement avec flèches et scroll
  fluide, trois cartes en bureau, deux sur tablette, une sur téléphone.
- Badges favoris en vert. Versions finales de ce lot : CSS `v=34`, script `v=23`.

- Précisions Daybreak fournies par Adam : site https://daybreak.fr/ (capture encadrée
  ajoutée), Discord sans lien, Aeterna = serveurs SMP survie. Les fiches correspondantes
  sont renseignées avec ces seules informations.
- Vérifications locales : navigation groupes et tags, cinq projets TristeJeu,
  conservation des six visuels et du multipage DEI, skills compactés, défilement
  vers Nocturnz et badge favori vert. Publication explicitement demandée pour ce lot.

- Derniers contrôles avant push : affichage à 1280 px et à 375 px sans débordement
  horizontal global ; défilement vers la quatrième carte testé ; migrations et
  médias conservés vérifiés. Fetch et scan de confidentialité effectués avant push.

- Dernière demande : texte À propos à gauche, compétences à droite sur deux colonnes
  dont les cases occupent la hauteur disponible. Sur mobile, empilement conservé.
- Sélection mise en avant : flèches retirées ; glissement souris, tactile et trackpad,
  avec navigation clavier possible. CSS `v=35`, script `v=24`. Non publié.
- Indicateur de défilement masqué ; le focus clavier reste visible.
- Sélection : léger défilement automatique aller-retour, suspendu au survol,
  au focus, pendant l’interaction et si les animations réduites sont activées.
  CSS `v=36`, script `v=25` ; non publié.

- Cinq miniatures TristeJeu créées depuis les jeux ouverts : WA7AD et Qui suis-je ?
  en salon de test, TristeParty, Qui De Nous ? et Loup-Garou en bêta locale admin.
  Format capture encadrée web. Le groupe Daybreak utilise la capture du site ;
  miniatures des projets Minecraft et Discord en attente d’Adam. Non publié.

- TristeParty masqué à la demande d’Adam. Les fiches des jeux contiennent leur
  fonctionnement et les technologies de la plateforme, React et Firebase ; le
  contexte personnel et les outils IA restent à préciser par Adam, ne pas inventer.
- Groupe favori : couleur de texte d’origine. Les sites web ayant une URL sont
  intégrés en iframe sauf les jeux TristeJeu ; garder les liens directs.
- Miniatures WA7AD et Qui suis-je ? présentes et vérifiées. Script local `v=26`.

- Fiches TristeJeu enrichies : contexte, déroulement, technologies et IA indiquées
  par Adam. Sources vérifiées : documents du dépôt TristeJeu pour Open Mercy,
  Cacabox et l’audit de références Loup-Garou. Les projets consultés ne sont pas
  présentés comme du code réutilisé. TristeParty reste masqué. Non publié.

- Dernière correction d’Adam : cases des skills compactes et de largeur naturelle,
  réparties sur la hauteur à droite du texte ; pas de grandes cases étirées.
  CSS `v=37`, script `v=26` ; publication demandée.

- Lot validé pour publication : skills compacts à droite du texte, carrousel
  glissable avec défilement lent, nouvelles miniatures TristeJeu et Daybreak,
  TristeParty masqué, descriptions des jeux et iframes web. NGC Hub et la vidéo
  de manifestation restent en attente des éléments d’Adam. CSS `v=37`, JS `v=26`.

- Sélection : boucle continue dans le même sens, recadrage invisible aux extrémités,
  glissement manuel et pause à l’interaction. Copies visuelles hors navigation clavier.
  Skills resserrés à droite du texte, cases compactes. CSS `v=38`, JS `v=27`. Publication demandée.

- Proposition locale demandée par Adam : Hard skills et Soft skills présentés
  sous forme de deux constellations, étoiles reliées et noms lisibles. La vue
  d’édition conserve les cartes avec leurs détails. CSS `v=39`, JS `v=28`.
  À valider visuellement ; non publié.

- Proposition locale demandée : parcours en branches parallèles, avec NGC Hub
  (2021), Union Oasis Forest (2024) et AdamXBC (2026), dates fournies par Adam.
  Ces branches indiquent une contemporanéité, pas une causalité affirmée avec
  les études. `site.timelineBranches` éditable en formulaire et vue visuelle.
- Constellations retravaillées : formes distinctes avec plusieurs liaisons et
  étoiles secondaires. CSS `v=41`, JS `v=30` ; non publié.

- Constellations : Grande Casserole (partie de la Grande Ourse) et Cassiopée,
  avec étoiles supplémentaires et décalage vertical demandé. Textes publics non
  sélectionnables ; saisie et vue d’édition restent sélectionnables. CSS `v=42`,
  JS `v=31`. Proposition locale non publiée.

- Parcours corrigé selon Adam : seul l’axe principal reste vertical ; branches
  alternées, celle d’Oasis part de 2024 et son texte descend près de 2026. Côté et
  année d’arrivée sont éditables pour chaque branche. Non publié.

- Essai local EasyUI : les feuilles des cartes de groupes s’écartent doucement au
  survol ou au focus clavier, sans modifier les cartes de projets. CSS `v=44`.
  Constellations Grande Casserole et Orion ; branches du parcours mauves ; BAC 3
  retiré du parcours, la bannière de recherche de stage est conservée. Non publié.

- Constellation Soft skills remplacée par la Lyre, à la demande d’Adam (Orion évoquait un sablier). CSS `v=45`, JS `v=33`. Non publié.

- Frise MCU abandonnée à la demande d’Adam : ligne simple alternée, projets personnels conservés comme étapes. JS `v=34`. Non publié.

- Soft skills : Cassiopée remplace la Lyre afin de distinguer les deux formes. CSS `v=46`, JS `v=35`. Non publié.

- Frise revenue à sa présentation initiale ; projets personnels issus de la version MCU et contrôles associés supprimés. BAC 3 reste retiré selon la demande précédente. CSS `v=47`, JS `v=36`. Non publié.

- Soft skills : Scorpion stylisé remplace Cassiopée. CSS `v=48`, JS `v=37`. Non publié.

- Constellations agrandies en hauteur ; Soft skills décalés davantage vers le bas. CSS `v=49`, non publié.

- Curieux de nature placé à droite de son étoile pour l’éloigner de Vibecoding. CSS `v=50`, non publié.

- Sur ordinateur, Hard skills commence à hauteur du titre À propos et Soft skills finit près du bas du texte ; libellé Curieux de nature replacé à gauche de son étoile. CSS `v=51`, non publié.

- Aperçu des projets déclenché sur toute la miniature des groupes ; description affichée au survol de toute la zone de texte de la carte. JS `v=38`, non publié.

- Pop-up des projets du groupe suit la souris, avec adaptation aux bords de l’écran. JS `v=39`, non publié.

- Effets inspirés d’EasyUI en local : halo glissant dans la navigation au survol et au clavier, étoiles des compétences éclairées à proximité du pointeur. Animations réduites respectées. CSS `v=52`, JS `v=40`, non publié.

- Points des étoiles de compétences réduits de 9 à 6 px. CSS `v=53`, non publié.

- Étoiles des deux constellations uniformisées en points ronds de 5 px, y compris les étoiles secondaires. CSS `v=54`, JS `v=42`, non publié.

- Placement des libellés des constellations corrigé après l’ajout des points secondaires. JS `v=43`, non publié.

- Points des constellations réduits à 3 px, halos atténués ; JS `v=44`, CSS `v=55`, non publié.

- Étoiles des compétences animées d’un scintillement léger et décalé, désactivé en mouvement réduit. CSS `v=56`, non publié.

- Mixage audio placé sur l’étoile droite pour dégager la constellation. CSS `v=57`, JS `v=45`, non publié.

- Pastille glissante de la navigation en contour, assortie au bouton CV. CSS `v=58`, non publié.

- Affichage agrandi des images : ouverture et fermeture fluides, accès clavier aux photos ; les carrousels conservent leur propre navigation. CSS `v=59`, JS `v=46`, non publié.

- Pastille de navigation : remplissage et animation conservés, forme arrondie assortie au bouton CV. CSS `v=60`, non publié.

- Pastille de navigation dimensionnée sur le contour du bouton CV (hauteur et marges). CSS `v=61`, JS `v=47`, non publié.

- Tags revus : thèmes généraux et hard skills pertinents seulement ; Vibecoding réservé aux projets dont l’usage est documenté. Les tags des groupes restent déduits de leurs projets. Non publié.

- Pastille de navigation au moins aussi large que CV, centrée sur le libellé et incluant la bordure extérieure. JS `v=48`, non publié.

- Tag Vibecoding retiré des projets à la demande d’Adam ; compétence conservée. Non publié.

- Tag Réseaux sociaux retiré, y compris du repli automatique des groupes et des fiches. JS `v=49`.

- Boutons de téléchargement du CV désactivés temporairement, sur toutes les pages. CSS `v=62`.

- Aperçu des groupes : grille compacte de miniatures en trois colonnes au-delà de trois projets, nombre conservé ; liste avec titres conservée jusqu’à trois. CSS `v=63`, JS `v=50`, non publié.

- Aperçu des groupes : miniature temporaire « ? » pour les projets sans image. CSS `v=64`, JS `v=51`.

- Point d’interrogation des miniatures temporaires en police normale. CSS `v=65`, non publié.

- Toutes les vidéos des fiches, y compris les lecteurs Adobe importés, sont réglées en taille L. Non publié.

- Image de partage actualisée : titre manuscrit inspiré de celui du site ; URL de partage versionnée pour rafraîchir les aperçus. Non publié.

- Libellés des constellations centrés sur leur étoile même lorsqu’ils passent sur deux lignes ; hauteur des paragraphes À propos réservée selon les trois polices de l’effet scramble. CSS `v=67`, JS `v=53`, local.

- Udeyfa : les deux parties réunies dans la même fiche. La Haine : fiche de tournage visible dans En Esprit → Vidéos, vidéo et miniature ajoutées ; rôle précisé (tournage et reels, pas le montage de la vidéo longue). Non publié.

- En Esprit → Vidéos : titres harmonisés ITW / IMMERSION ; NK Divine et DJ Kawest ajoutés avec leurs vidéos de montage et miniatures. Année et rattachement confirmés par Adam. Mallaury était déjà présente. Non publié.

- Miniatures En Esprit auparavant en 480 × 360 remplacées par les versions YouTube en 1 200 × 675, compression plus légère ; noms de fichiers distincts pour éviter le cache. Non publié.

- Tag « Montage vidéo » renommé « Montage » ; tag « Tournage » ajouté à La Haine, Soolking et Workshops selon les rôles documentés. Autres tournages à confirmer. Non publié.

- Tournage confirmé et tag ajouté pour Mallaury et Udeyfa. Feminitea / Spill the Tea (Mallaury) ajouté : carte blanche sur format, montage et DA. Fiches reels Tiakola, Youssef Swatt’s, Slice et Feminitea masquées en attendant les fichiers ; vidéo Feminitea écartée à la demande d’Adam. Non publié.

- Libellé « Groupe favori » des cartes passé en rose, sans modifier « Projet favori ». CSS `v=68`, non publié.

- Fiche Nocturnz Portfolio : lien vers la vitrine dédiée et retrait du positionnement forcé du bloc descriptif. Non publié.

- Accueil : lien « Voir tous les projets » à droite du titre de la sélection, vers la page Projets sans filtre. CSS `v=69`, non publié.

- Fiche Nocturnz Portfolio : précise que le moteur fait tourner ce site et décrit son panneau d’édition visuel. Non publié.

- Lien « Voir tous les projets » rapproché du sous-titre de la sélection. CSS `v=70`, non publié.

- Fiche Nocturnz Portfolio : textes regroupés dans la description longue afin de les aligner. Non publié.

- Captures des jeux TristeJeu affichées aussi dans les fiches ; TristeParty reste masqué.

- Groupes : description longue facultative, éditable en vue visuelle après les projets. TristeJeu décrit l’architecture, les rôles, les salons, Firebase et les tests selon le code vérifié. Fiches enrichies à partir des informations disponibles ; précisions complémentaires demandées à Adam. CSS `v=71`, JS `v=54`, non publié.

- Descriptions techniques enrichies après lecture des projets associés : moteur et OAuth du portfolio, React/Firebase/stockage de Review, PWA/Firebase de Todo, site et outil Oasis, architecture modulaire Paper de LeVillage et état en développement de Nocturnz Edit. Les projets masqués le restent. Non publié.

- Descriptions de page de groupe (`pageDesc`) séparées des descriptions courtes des cartes ; présentations concises pour chaque groupe, éditables dans la vue visuelle. JS `v=55`, non publié.

- Daybreak : plateforme sociale d’événements multijoueurs temporaires, lancée sur Minecraft avec l’ambition d’autres jeux et de serveurs permanents ; LeVillage est un mode propriétaire en développement. Non publié.

- Campagne 360° : fiche Stratégie digitale avec posts, story, maquettes et proposition graphique ; fiche identité Echo Nexus avec logo ; justification des supports ajoutée à la présentation. Documents contenant des coordonnées ou noms complets exclus du dépôt public. Non publié.

- Campagne 360° : posts du dossier fourni, carrousel des doudous et recto de la carte Echo Nexus ajoutés ; verso et mockup exclus car contiennent des noms et coordonnées. Non publié.

- Fiche masquée du site de campagne : zoning en deux visuels, site non disponible en attente d’une sauvegarde. Deux vidéos de stratégie digitale attendent des liens YouTube non répertoriés. Non publié.

- Projet 360° → Identité visuelle d’Echo Nexus : sous-groupe rassemblant le logo et la carte de visite. Non publié.

- Stratégie digitale : tailles des visuels variées pour utiliser le mur d’affiches existant plutôt qu’une colonne de grandes images. Non publié.

- Stratégie digitale : posts rose/orange et campagne répartis dans deux carrousels ; planche de recherche graphique conservée à part. Non publié.

- Stratégie digitale : seuls les posts au format carré restent dans les deux carrousels ; stories et autres formats sont placés séparément sur le mur. Non publié.

- Correction d’Adam : un seul site dans le projet 360°, celui de la campagne ; fiche existante renommée et masquée avec le zoning, doublon supprimé. Non publié.

- Format avant / après : deux images comparées par un curseur ; ajout et inversion dans l’éditeur. Fiche logo En Esprit mise à jour. CSS `v=72`, JS `v=56`, non publié.

- Modules texte centrés par défaut, alignement gauche / centre / droite éditable ; comparaison du logo centrée et recadrée en 16:9. CSS `v=73`, JS `v=57`, non publié.

- 4 novembre 2026 : boucle et défilement automatique du carrousel conservés sur mobile ; pause pendant tout le geste tactile, inertie native et clones sans animation d'apparition. Double-tape zoom désactivé, pincement conservé. Badge NEW auto-expirant après 30 jours (`newUntil`), posé par l'admin sur les nouveaux projets et groupes. Groupe AdamXBC ajouté avec Linktree, Twitch affilié et TikTok Quick (30 000 vues). `manif-video`, déjà créé mais masqué, rendu visible avec la vidéo YouTube du 9 octobre à Bruxelles. ITW : LOSSA ajouté au groupe Chloé Ly avec le lien YouTube fourni. Modifications locales, non publiées.

- 5 novembre 2026 — CV publié (`cv.pdf` + `cv-clair.pdf`), tous deux générés par
  `tools/generate_cv.py` (`CV_THEME=clair` pour la version imprimable, liée en bas
  à droite de la version couleur). Nom en Schoolbell, phrase de recherche de stage
  dictée par Adam, bio courte sous les projets, Instagram `adamkarr_` (voulu).
  Photo essayée puis abandonnée à la demande d'Adam. Chloé Levy reste nommée.
  Pas de langue autre que français/anglais. Stage En Esprit : « Avril — Juin 2025 » (22 avril → 13 juin).
  Boutons CV du site réactivés (liens `cv.pdf` avec `download`).

- 5 novembre 2026 (suite) — **Visionneuse du CV** : les boutons CV (`a[data-cv-viewer]`,
  « Voir mon CV » sur l'accueil) ouvrent le CV en plein écran au lieu de le télécharger.
  Image `images/cv/cv.webp` + zones cliquables lues dans `images/cv/cv.json` (liens +
  empreintes anti-cache), Télécharger (nom « CV Etudiant COM - Adam Karroum - ISFSC.pdf »),
  Imprimer (la visionneuse passe d'abord à la version blanche, puis impression de
  `images/cv/cv-clair.webp` seule, 1 page A4), Fermer / Échap. `#cv` ouvre la visionneuse.
  Tout est régénéré par `tools/generate_cv.py` (macOS : qlmanage pour les images).
  Version papier : adresses écrites (adam.karroum.be, redirige vers adam.nocturnz.xyz
  en gardant le chemin), QR codes bleus à la place des « Voir » + Portfolio / LinkedIn /
  Instagram en bas. CSS `v=81`, JS `v=61`.

- 6 novembre 2026 — **Recadrage des miniatures** : bouton « Recadrer » (vue visuelle,
  cartes projet et groupe) → glisser / molette / double-clic, enregistre `thumbPos`
  `{x, y, z}` (projet ou groupe ; rendu par `thumbStyle` dans script.js), remis à zéro
  quand la miniature change, conservé par le formulaire. **Miniature générée** quand il
  n'y en a pas : fond bleu nuit + titre en Schoolbell (`.thumb-title`). Flyers = dépliant
  ouvert ; le groupe Oasis a désormais sa propre miniature (photo d'équipe) au lieu de
  reprendre celle des Flyers. Manif : miniature BXL + stats (X, Instagram, TikTok, données
  fournies par Adam). NGC Hub masqué (aucun projet visible). Vidéos (iframe/video) non
  inclinées : bords crénelés sinon. Visionneuse CV : retour à la version web dès que la
  fenêtre d'impression se ferme. CSS `v=83`, JS `v=63`.
