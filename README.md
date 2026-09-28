# Portfolio — Adam

Site multi-pages (HTML/CSS/JS, aucune dépendance à installer, aucun build).
Mise en page et glassmorphism inspirés de [bastienokonski.fr](https://bastienokonski.fr/)
(nav flottante en verre, cartes translucides), habillés avec l'identité de ton
Adobe Portfolio : palette bleu nuit, police manuscrite.

**Tout le contenu (textes, projets, projet favori) se modifie depuis
[`/admin.html`](admin.html), sans toucher au code — voir la section
"Éditer le contenu" plus bas.**

## Structure des pages

- **`index.html`** — l'accueil : titre, bio, deux boutons ("Projets perso" /
  "Projets académiques"), un projet favori mis en avant, la sélection
  "Projets mis en avant" (3 projets), à propos, parcours, contact. **Les
  grilles complètes de projets ne sont plus sur cette page.**
- **`projets-perso.html`** / **`projets-academiques.html`** — la séparation
  principale du site. Chacune affiche d'abord les groupes de sa catégorie
  (voir plus bas), puis les projets qui n'appartiennent à aucun groupe,
  filtrables par tag. La catégorie (`ctx: "perso"`/`"academique"`/`"stage"`)
  d'un projet détermine sa page — `"stage"` compte comme académique.
  `projets.html` (sans distinction) existe toujours en repli, pour la page
  d'un groupe dont la catégorie n'est pas évidente, mais n'est plus lié
  depuis l'accueil.
- **`groupe.html?id=...`** — la page d'un groupe (un club, une agence, un
  stage — plusieurs projets réunis sous une seule carte, ex. "Union Oasis
  Forest" ou "Stage chez En Esprit"). Remplace l'ancien système de
  sous-section figée : un groupe se crée, se renomme et se supprime depuis
  l'admin (sur la fiche d'un projet, ou dans sa propre page en vue visuelle) —
  supprimer un groupe ne supprime jamais ses projets, qui redeviennent
  indépendants.
- **`projet.html`** — la page détail d'un projet (`projet.html?id=...`),
  ouverte en cliquant sur n'importe quelle vignette — voir plus bas.
- **`admin.html`** — le panneau d'édition (voir plus bas).
- **`data.json`** — **tout le contenu du site** : textes (bio, à propos, accroche,
  contact, réseaux sociaux), projet favori, la liste des groupes, et la liste
  des projets. C'est ce fichier que `/admin.html` lit et modifie — tu peux
  aussi l'éditer à la main si tu préfères (c'est du JSON standard).
- **`style.css`** — tout le design, partagé par toutes les pages.
- **`script.js`** — charge `data.json` et se charge de tout le rendu (grilles,
  icônes, projet favori, textes, effet de décryptage), partagé par toutes les
  pages.

Le header (nav flottante) et le footer (contact) sont dupliqués tels quels dans
chaque page — pas de composants partagés, juste du HTML copié-collé volontairement
pour rester sans build tool.

## Éditer le contenu (sans coder)

Va sur **`https://adam.nocturnz.xyz/admin.html`** — c'est le panneau
d'édition. Il te permet de :

- modifier les textes (bio, "à propos", l'accroche du haut, l'email de contact,
  les liens LinkedIn/Instagram) ;
- choisir le **projet favori** (celui mis en avant tout en haut de l'accueil) ;
- ajouter, modifier ou supprimer des **projets** (titre, année, catégorie —
  perso / académique / stage —, médium — graphisme, vidéo, audio, **site web**,
  réseaux sociaux, événementiel, écrit —, tags, description, et s'il est "mis
  en avant" sur l'accueil).

### Deux vues : Formulaire et Vue visuelle

En haut du panneau, un sélecteur bascule entre :

- **Formulaire** — la vue classique, champ par champ. Pratique pour saisir
  beaucoup de choses d'un coup, ou filtrer/chercher parmi les projets.
- **Vue visuelle** — le site réel s'affiche tel quel et s'édite dessus. Les
  contrôles apparaissent **au survol**, en haut à droite de chaque élément :

  | Où | Contrôles |
  |---|---|
  | N'importe quel texte | clic pour éditer (`Échap` annule) |
  | Icônes réseaux sociaux | clic pour changer le lien LinkedIn / Instagram |
  | Étape du parcours | ↑ ↓ réordonner · étape en cours · supprimer — et **+ Étape du parcours** en dessous |
  | Bloc projet favori | choisir un autre projet favori |
  | Vignette de projet | masquer/afficher · mettre en avant · définir favori · changer la miniature · supprimer |
  | Sous une grille | **+ Nouveau projet** |
  | Page projet (bandeau du haut) | tags · médium · catégorie · lien externe · année |
  | Image / vidéo / audio / site / document | ↑ ↓ réordonner · définir comme miniature · masquer · retirer |
  | Bas d'un projet ou d'une section | **+ Image / + Vidéo / + Audio / + Site web / + Document** |
  | Section | ↑ ↓ réordonner · médium · lien · supprimer — et **+ Nouvelle section** en dessous |

  Clique une vignette pour **entrer dans la page détail** du projet, comme sur
  le site public ; ⌂ Accueil et ← Retour servent à circuler. Les éléments
  masqués restent visibles ici, grisés avec un badge « masqué ».

Les deux vues éditent la même chose : ce que tu changes dans l'une apparaît
immédiatement dans l'autre. Dans les deux cas, rien n'est publié tant que tu
n'as pas cliqué **« Enregistrer sur GitHub »**.

Comme le site est hébergé sur GitHub Pages (donc statique, sans serveur), le
panneau enregistre tes modifications directement sur GitHub via un **token
d'accès personnel** — pas ton mot de passe de compte, GitHub ne permet plus
l'accès à son API par mot de passe. La première fois, la page t'explique en
3 étapes comment générer ce token (2 minutes, à faire une seule fois) :

1. [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new)
2. *Repository access* → *Only select repositories* → `portfolio`
3. *Permissions* → *Contents* → *Read and write*, puis *Generate token*

Colle le token dans `/admin.html` : il reste uniquement dans ton navigateur
(stockage local), et n'est envoyé qu'à l'API GitHub pour enregistrer tes
changements. Une fois enregistré, le site public se met à jour tout seul en
30 à 60 secondes (le temps que GitHub Pages republie).

Ne colle pas ce token sur un ordinateur public ; tu peux le révoquer à tout
moment depuis GitHub si besoin. **Ce token fonctionne déjà sur autant
d'appareils que tu veux** — colle le même sur ton téléphone, un autre
ordinateur, etc., pas besoin d'en régénérer un par appareil.

### "Se connecter avec GitHub" (bouton OAuth, en option)

Le bouton **"Se connecter avec GitHub"** en haut de `/admin.html` évite de
copier-coller un token — comme sur oasisforest.be avec Sveltia CMS. GitHub
Pages étant 100% statique, ce flow a besoin d'un petit relais externe qui
garde le "client secret" en sécurité (impossible de le faire en JS pur côté
navigateur). Mise en place, une seule fois (~15-20 min) :

1. **Déployer le relais** — [sveltia-cms-auth](https://github.com/sveltia/sveltia-cms-auth),
   un Cloudflare Worker open-source. Clique son bouton "Deploy to Cloudflare
   Workers" (crée un compte Cloudflare gratuit si besoin), puis récupère
   l'URL du Worker déployé (`https://sveltia-cms-auth.<TON-SOUS-DOMAINE>.workers.dev`).
2. **Créer une OAuth App GitHub** — [github.com/settings/applications/new](https://github.com/settings/applications/new) :
   - *Homepage URL* : `https://adam.nocturnz.xyz/`
   - *Authorization callback URL* : `<URL DU WORKER>/callback`
   - Génère le *Client Secret*.
3. **Configurer le Worker** — dans les *Variables* du Worker sur Cloudflare :
   - `GITHUB_CLIENT_ID` : le Client ID de l'OAuth App
   - `GITHUB_CLIENT_SECRET` : le secret généré (marque-le *encrypted*)
   - `ALLOWED_DOMAINS` : `adam.nocturnz.xyz`
4. **Donne-moi le Client ID et l'URL du Worker** (jamais le Client Secret —
   celui-là reste uniquement dans les variables du Worker) — je les colle
   dans `admin.html` (constantes `OAUTH_CLIENT_ID` / `OAUTH_WORKER_URL`) et
   le bouton "Se connecter avec GitHub" s'active tout seul.

Note sécurité : contrairement au token manuel (limité au seul repo
`portfolio`), un token obtenu via ce flow OAuth a accès en écriture à
**tous tes repos publics** (portée `public_repo`, la plus restrictive que
GitHub propose pour ce type d'app) — un compromis à connaître, propre au
fonctionnement des OAuth Apps GitHub.

## Polices — une substitution à connaître

Tu as demandé les polices **"Bad Dog"** (titres) et **"Homemade Apple Pro"** (texte bio).
- **Homemade Apple** est un Google Font libre — utilisée telle quelle pour le bio et
  le texte "à propos".
- **"Bad Dog"** n'est disponible que sur des sites de fonts gratuites tiers (licence
  "usage personnel uniquement", pas de version Google Fonts) — un CDN externe que je
  ne peux pas charger de façon fiable/légale dans le site. J'ai substitué **Schoolbell**
  (Google Fonts), une manuscrite marker au feeling proche, pour les titres. Si tu as le
  fichier `.ttf`/`.otf` de Bad Dog et que sa licence permet l'usage voulu, donne-le-moi
  et je l'intègre en `@font-face` à la place.

## Fond — en attente de ton fichier

Le fond est actuellement un simple dégradé bleu nuit (`.topo-bg` dans `style.css`).
Quand tu me passes ton image de fond (les traits zébrés), je l'intègre directement en
`background-image` sur `.topo-bg` — une seule ligne à changer, dans un seul fichier,
répercutée sur les 4 pages automatiquement.

## À compléter avant mise en ligne

- [ ] **Email de contact** : remplacer `PLACEHOLDER@email.com` — modifiable depuis
      `/admin.html` (section "Textes du site") — utilise un email perso plutôt que
      ton adresse étudiante ISFSC si possible.
- [ ] **Liens des projets** : les cartes n'ont pas de lien cliquable vers le détail du
      projet (Drive, Behance, YouTube...) — dis-moi si tu veux que j'ajoute ça, projet
      par projet.
- [ ] **Images réelles** : chaque vignette (et le projet favori) est une mire de test
      générée en CSS. Remplace-les par tes vraies images/miniatures (voir plus bas).
- [ ] **CV** : le bouton "CV" pointe vers `cv.pdf` (présent sur les 4 pages) — dépose
      ton CV à jour dans le dossier sous ce nom exact, sinon le bouton mènera à une
      page 404.
- [ ] **Projet favori** et **projets mis en avant** : modifiables directement depuis
      `/admin.html`, plus besoin de toucher au code.
- [ ] Les descriptions de projets sont des reformulations courtes à partir des
      seuls titres — à réécrire avec de vrais détails (contexte, outils, résultat),
      également depuis `/admin.html`.

## Pages détail de projet (clic sur une vignette)

Chaque vignette (grille de projets, projet favori) mène maintenant à une page
détail dédiée (`projet.html?id=...`), dans l'esprit d'Adobe Portfolio. Tout se
configure depuis `/admin.html`, section "Modifier ce projet" — les champs
au-delà de "Description courte" sont optionnels et n'apparaissent que sur la
page détail :

- **Description longue** — remplace la description courte sur la page détail.
- **Contenus du projet** — la liste des médias, alimentée par trois boutons :
  - **+ Image** : choisis un ou plusieurs fichiers ; ils sont convertis en
    **WebP** (1920px max, qualité 85%) et envoyés dans `images/` sur GitHub.
  - **+ Vidéo** : colle un lien YouTube, Vimeo ou un `.mp4`.
  - **+ Audio** : colle un lien **SoundCloud** ou un fichier `.mp3`/`.wav`.
  - **+ Site web** : intègre un site directement dans la page. Certains sites
    refusent d'être intégrés (`X-Frame-Options`) — un lien direct est alors
    proposé juste en dessous.
  - **+ Document** : envoie un **PDF** depuis ton ordinateur (déposé dans
    `docs/` du repo), ou colle un lien. Les PDF et les Google Docs/Slides/Sheets
    s'affichent dans la page ; les fichiers Word/PowerPoint/Excel passent par le
    visualiseur public de Microsoft ; tout autre format devient un simple bouton
    d'ouverture.

  Chaque ligne peut être réordonnée (↑ ↓), **masquée sans être supprimée**
  (l'icône œil) ou retirée (✕). Un contenu masqué reste dans l'admin mais
  n'apparaît pas sur le site.
- **Miniature** — l'image de la vignette avant de cliquer. Par défaut c'est la
  première image visible du projet, mais tu peux en choisir une autre dans la
  liste, ou **envoyer une image dédiée** qui ne figurera pas dans les contenus.
- **Masquer ce projet** — retire le projet des grilles et de l'accueil tout en
  le gardant dans l'admin (utile pour un brouillon).
- **Lien externe** — le bouton "Visiter le site" pointe vers cette URL, et un
  **aperçu du site est intégré directement dans la page** (iframe). Note que
  certains sites refusent d'être intégrés (protection `X-Frame-Options`) : dans
  ce cas l'aperçu reste vide, et une phrase invite à ouvrir le lien directement.

Sur le site, **cliquer une image l'ouvre en plein écran** (flèches ou ← →  pour
naviguer, `Échap` ou clic à côté pour fermer). Le clic droit et le glisser y
sont désactivés — c'est un frein au copier-coller distrait, **pas une vraie
protection** : une capture d'écran ou les outils du navigateur récupèrent
toujours le fichier. Pour des visuels réellement sensibles, mieux vaut un
filigrane ou une version basse définition.

### Rendu « photos collées au mur »

Images et vidéos sont affichées comme des tirages scotchés sur le fond : pas de
cadre, une légère rotation, une ombre portée, et un vrai **ruban de masking
tape** en haut. Le principe vient du traitement polaroid d'oasisforest.be, dont
on ne garde que le scotch (pas le liseré blanc).

Les rubans sont dans `images/tape/` (`tape-1` à `tape-4.webp`, ~17 Ko chacun,
découpés depuis un pack de textures et redimensionnés pour le web). Quatre
variantes tournent automatiquement d'une photo à l'autre, avec des rotations et
des positions différentes, pour qu'aucune ne paraisse dupliquée. Pour en changer
ou en ajouter : dépose un PNG/WebP détouré dans ce dossier et modifie les règles
`.photo::before` / `.photo-1::before`… dans `style.css`.

### Sections

Un projet peut contenir des **sections** — des blocs affichés dans sa page détail, pour découper un gros projet en volets. Par exemple
"Union Oasis Forest" → "Refonte graphique", "Community management",
"Stratégie digitale". Chaque section a son propre titre, médium,
description, images (avec le même upload WebP), vidéo, audio et lien. Ça se
gère depuis le formulaire du projet parent, section « Sections ».

Tous les médiums sont supportés (graphisme, vidéo, audio, **site web**,
réseaux sociaux, événementiel, écrit) — la catégorie ne limite pas les champs
disponibles, tu peux par exemple ajouter une vidéo à un projet "graphisme".

## Déployer le site (gratuit, sans serveur)

Le plus simple, sans rien installer :

1. Va sur [app.netlify.com/drop](https://app.netlify.com/drop)
2. Glisse le dossier `portfolio-adam` entier dans la page (les fichiers doivent
   rester ensemble, dans le même dossier)
3. Netlify te donne une URL en quelques secondes (ex: `adam-karroum.netlify.app`)
4. Tu pourras ensuite brancher ton propre nom de domaine si tu en as un

Alternative : GitHub Pages (si tu as un compte GitHub) ou Vercel — dis-le-moi si tu
veux que je t'accompagne sur l'une de ces options plutôt.

## Prévisualiser en local

Comme le site est maintenant multi-pages avec des fichiers séparés (`style.css`,
`script.js`), l'ouverture directe par double-clic peut ne pas fonctionner selon ton
navigateur (certains bloquent le chargement de fichiers locaux liés). Le plus fiable :
ouvre un terminal dans le dossier `portfolio-adam` et lance :

```bash
python3 -m http.server 8000
```

puis ouvre `http://localhost:8000` dans ton navigateur — tous les liens et pages
fonctionneront normalement.
