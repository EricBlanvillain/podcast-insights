# Guide de Développement

## Structure du Projet

```
podcast-insights/
├── src/
│   ├── __init__.py
│   ├── app.py              # Application principale
│   ├── query_processor.py  # Traitement des requêtes
│   └── ui_components.py    # Interface utilisateur
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_query_processor.py
│   └── test_ui_components.py
└── docs/
    ├── API.md
    ├── USAGE.md
    └── DEVELOPMENT.md
```

## Tests

Exécuter les tests :
```bash
python -m pytest
```

## Configuration du Développement

1. Pre-commit hooks
```bash
pre-commit install
```

2. Linting
```bash
flake8 src tests
black src tests
```

## Guidelines

1. Code Style
- Suivre PEP 8
- Utiliser Black pour le formatage
- Documentation en français

2. Tests
- Écrire des tests pour chaque nouvelle fonctionnalité
- Maintenir une couverture > 80%

3. Documentation
- Documenter toutes les fonctions publiques
- Maintenir la documentation à jour
- Exemples pour les fonctionnalités principales