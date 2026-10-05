# La mesure du temps dans l'Antiquité

Site statique d'un TPE de première S sur la mesure du temps pendant l'Antiquité (calendriers,
gnomons, cadrans solaires, clepsydres). En ligne sur <https://mesure-du-temps.julsql.fr>.

Uniquement du HTML et du CSS : pas de JavaScript, pas d'étape de build.

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
    │   ├── base.css         variables de thème (clair/sombre), reset, typographie
    │   ├── layout.css       en-tête, navigation, zone de contenu, pied de page
    │   └── components.css   fil d'Ariane, figures, colonnes, cartes, galerie, quiz…
    └── images/
```

L'en-tête, la navigation et le pied de page sont dupliqués dans chaque page : une modification
du menu doit être reportée dans tous les fichiers HTML.

## Développement

```sh
docker compose -f docker-compose-local.yml up --build   # http://localhost:8012
npx prettier --write "public/**/*.{html,css}"           # formatage (100 colonnes)
```

Les liens sont absolus depuis la racine (`/assets/...`) : le site doit être servi par un serveur
HTTP, il ne s'ouvre pas correctement en `file://`.

## Déploiement

Un push sur `main` construit l'image nginx et la pousse sur `ghcr.io/julsql/mesure-du-temps`
(`.github/workflows/docker.yml`), puis notifie Keel qui redéploie le Deployment k3s.
