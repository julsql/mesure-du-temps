# La mesure du temps dans l'Antiquité

Site statique d'un TPE de première S sur la mesure du temps pendant l'Antiquité (calendriers,
gnomons, cadrans solaires, clepsydres). En ligne sur <https://mesure-du-temps.julsql.fr>.

HTML et CSS uniquement, sans étape de build, sans backend ni base de données. Le thème reprend
celui du site d'origine (e-monsite). Seule exception au « zéro JavaScript » : `assets/js/album.js`
(15 lignes) pour naviguer au clavier (← → Échap) dans la visionneuse de l'album.

## Aperçu

<p align="center">
  <img src="docs/screenshots/home.jpg" alt="Page d'accueil" width="80%">
</p>

## Structure

```
public/                      racine servie par nginx
├── index.html               accueil
├── notions-de-physique.html
├── mesure-de-l-annee/       partie I : calendriers lunaires, luni-solaires, solaires
├── mesure-de-la-journee/    partie II : horloges solaires, horloges à eau
├── album.html               galerie photo (visionneuse en CSS, `:target`)
├── video.html
├── quiz.html                quiz corrigé en CSS (`:has` + `:checked`)
├── bibliographie.html
├── contact.html
├── 404.html
└── assets/
    ├── css/
    │   ├── base.css         polices, variables du thème, reset, typographie
    │   ├── layout.css       barre du haut, bannière, contenu, menu latéral, pied de page
    │   └── components.css   fil d'Ariane, figures, colonnes, cartes, galerie, quiz…
    ├── fonts/               Roboto, Droid Serif, Courgette (auto-hébergées)
    ├── js/album.js          navigation clavier de la visionneuse
    └── images/
```

La barre du haut, le menu latéral et le pied de page sont dupliqués dans chaque page : une modification
du menu doit être reportée dans tous les fichiers HTML.

## Développement

```sh
docker compose -f docker-compose-local.yml up --build   # http://localhost:8012
npx prettier --write "public/**/*.{html,css,js}"          # formatage (100 colonnes)
python3 -m unittest discover -s tests                     # contrôles SEO (titres, meta, OG, JSON-LD, sitemap)
```

Les liens sont absolus depuis la racine (`/assets/...`) : le site doit être servi par un serveur
HTTP, il ne s'ouvre pas correctement en `file://`.

## Déploiement

Un push sur `main` construit l'image nginx et la pousse sur `ghcr.io/julsql/mesure-du-temps`
(`.github/workflows/docker.yml`), puis notifie Keel qui redéploie le Deployment k3s.
