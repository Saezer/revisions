# Cahier de révisions

Application web pour faire réviser un enfant : il lit les questions, tape ses réponses, et suit sa progression.

## Utilisation

Ouvrir `index.html` dans un navigateur (double-clic suffit, aucune installation).

1. Créer un cahier avec le prénom de l'enfant (plusieurs enfants possibles).
2. Choisir les tables, la façon de jouer et le nombre de questions, puis « C'est parti ! ».
3. Taper la réponse et appuyer sur Entrée.

## Ce qui est suivi

- Pourcentage de réussite, bonnes réponses, record de bonnes réponses d'affilée.
- **Table de Pythagore** colorée : chaque calcul passe du rouge (difficile) au vert (maîtrisé = réussi 3 fois de suite).
- **À retravailler** : les calculs qui posent le plus de problèmes.
- **Progression** : réussite des 15 dernières séances.
- **40 succès** à débloquer (séries, sans-faute, réponses éclair, contre-la-montre, régularité, revanches, maîtrise de chaque table…).

## Façons de jouer

- **Entraînement** : des multiplications au hasard dans les tables choisies ; les calculs fragiles reviennent plus souvent.
- **Points faibles** : uniquement les calculs les moins réussis.
- **Contre la montre** : un maximum de bonnes réponses en 1 minute.
- Après une séance : **Retravailler mes erreurs**.

## Sauvegarde

La progression est enregistrée dans le navigateur (`localStorage`), sur l'appareil utilisé.
Ouverte comme artefact claude.ai, la page enregistre aussi en ligne.

## Ajouter un sujet

Le premier sujet est les tables de multiplication (`SUJET = "multiplications"` dans `index.html`).
Les données de chaque élève sont rangées par sujet (`eleve.sujets[<sujet>]`) pour en ajouter d'autres plus tard.
