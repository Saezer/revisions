# Cahier de révisions

Application web pour faire réviser un enfant : il lit les questions, tape ses réponses et suit sa
progression. Des GIF, des mèmes et des sons de chats et de blocs façon Minecraft l'encouragent.
Premier sujet : les tables de multiplication.

## Lancer

Ouvrir `index.html` dans **Edge ou Chrome** (double-clic). Rien à installer.

1. **Profils** : choisir son prénom ou créer un profil. Le profil administrateur (Seb) ouvre l'espace parent.
2. **Bienvenue {prénom}** : rappel de la dernière séance, puis « Ouvrir mon cahier ».
3. Choisir les tables et la façon de jouer, puis « C'est parti ! ». Taper la réponse et appuyer sur Entrée.

## Sauvegarde dans le repo

Chaque profil est enregistré dans `profils/<prénom>.json` et les réglages parent dans `reglages.json`,
**directement dans ce repo GitHub**, pour reprendre depuis n'importe quel appareil. Chaque fin de
séance crée un commit (« Luke : 9/10 en entraînement (tables 2, 3, 4, 5) »).

À faire **une fois par appareil** : sur l'écran des profils, cliquer sur « Connecter GitHub » et coller
un jeton d'accès. Pour créer le jeton :

1. GitHub → *Settings* → *Developer settings* → *Personal access tokens* → *Fine-grained tokens* → *Generate new token*.
2. *Repository access* : *Only select repositories* → `Saezer/revisions`.
3. *Permissions* → *Repository permissions* → *Contents* : **Read and write**.
4. Copier le jeton (`github_pat_…`) dans le cahier.

Le jeton reste dans le navigateur de l'appareil. Sans connexion, la progression est gardée dans le
navigateur et envoyée au lancement suivant. Comme l'application fait des commits sur `main`, faire un
`git pull` avant de pousser ses propres modifications.

## Espace parent

Profil administrateur et mot de passe (en clair) dans `config.js`. Réglages :

- tables proposées (par défaut **1 à 9**), multiplicateurs (1 à 10), durée du contre la montre ;
- images et sons activés ou non, thèmes (chats, blocs) ;
- **âge maximum des médias** (par défaut 16 ans : rien de réservé aux 18 ans et plus) ;
- **contenus interdits** (par défaut : caractère sexuel, NSFW) ; un média sans âge est traité comme 18 ans et plus ;
- fréquence des mèmes (par défaut toutes les 3 bonnes réponses d'affilée et toutes les 3 erreurs).

La **galerie** montre chaque GIF et son avec ses déclencheurs, et indique s'il est autorisé ou bloqué.

## Quand apparaissent les médias

| Moment | Image / mème | Son |
| --- | --- | --- |
| Bonne réponse | toutes les 3 d'affilée (série à partir de 6) | à chaque fois |
| Erreur | toutes les 3 erreurs, pour encourager | à chaque fois |
| Succès débloqué | dans l'annonce du succès | fanfare |
| Fin de séance | « bravo » (80 % et plus) ou « courage » | oui |

Un bouton dans l'en-tête permet à l'enfant de couper le son.

## Ajouter un GIF, un mème ou un son

1. Déposer le fichier dans `medias/images/` ou `medias/sons/`.
2. L'ajouter dans `medias/medias.js` avec ses `moments`, son `theme`, son `age` (3, 7, 12, 16, 18) et
   ses `etiquettes` éventuelles (`sexuel`, `nsfw`, `violence`, `grossier`, `peur`).

Les médias fournis sont dessinés par `outils/generer_medias.py` (pixel art et sons de synthèse, sans
fichier externe) : `python3 outils/generer_medias.py` les régénère.

## Suivi et succès

- Réussite globale, bonnes réponses, record d'affilée.
- **Table de Pythagore** colorée : un calcul devient vert quand il est réussi 3 fois de suite.
- **À retravailler** : les calculs qui posent le plus de problèmes ; **Progression** des 15 dernières séances.
- Modes : Entraînement, Points faibles, Contre la montre, Retravailler mes erreurs.
- Une trentaine de **succès** (séries, sans-faute, éclairs, régularité, revanches, maître de chaque table…).

## Ajouter un sujet

Les données de chaque élève sont rangées par sujet (`eleve.sujets[<sujet>]`, ici `multiplications`)
pour en ajouter d'autres plus tard.
