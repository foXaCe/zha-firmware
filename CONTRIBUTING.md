# Contribuer

Merci de votre intérêt pour **ZHA Firmware OTA Manager** !

## Signaler un bug

Utilisez le [modèle de rapport de bug](.github/ISSUE_TEMPLATE/bug_report.yml).

## Proposer une fonctionnalité

Utilisez le [modèle de demande de fonctionnalité](.github/ISSUE_TEMPLATE/feature_request.yml).

## Pull requests

1. Forkez le dépôt.
2. Créez une branche dédiée : `git checkout -b feat/ma-fonctionnalite`.
3. Installez l'environnement : `scripts/setup`.
4. Codez, ajoutez/mettez à jour les tests : `scripts/test`.
5. Vérifiez le lint et le typage : `scripts/lint`.
6. Commits au format [Conventional Commits](https://www.conventionalcommits.org/) : `feat: …`, `fix: …`.
7. Poussez et ouvrez une PR vers `main`.

## Environnement local

```bash
pipx install prek   # ou : brew install j178/prek/prek
scripts/setup       # installe les deps + le hook prek
```

`prek` est un remplaçant Rust de `pre-commit` (10× plus rapide), qui lit le même
`.pre-commit-config.yaml`. Si vous préférez la version Python : `pipx install pre-commit`.

## Gestion des dépendances

Ce dépôt utilise **Renovate** (et non Dependabot). Les PR de mise à jour sont
ouvertes par `@renovate[bot]` ; voir le tableau de bord des dépendances dans les
issues.
