# Podcast Insights 🎙️

Une application Streamlit pour analyser les transcriptions de podcasts en utilisant l'IA et la recherche vectorielle.

## 🌟 Fonctionnalités

- Recherche avancée dans les transcriptions de podcasts
- Analyse IA-powered avec OpenAI GPT-4
- Support pour plusieurs sources de podcasts (Lex Fridman, Huberman Lab, DOAC)
- Recherche par similarité vectorielle utilisant ChromaDB
- Interface utilisateur intuitive avec Streamlit

## 🛠️ Technologies

- **Frontend**: Streamlit
- **Base de données vectorielle**: ChromaDB
- **IA**: OpenAI API (GPT-4 & Ada)
- **Recherche**: Brave API
- **Média**: YouTube API
- **Language**: Python 3.9+

## 🚀 Installation

### Méthode 1: Installation locale

1. Cloner le repository :
```bash
git clone https://github.com/EricBlanvillain/podcast-insights.git
cd podcast-insights
```

2. Installer les dépendances :
```bash
# Installation standard
make install
# OU pour le développement
make install-dev
```

3. Configurer les variables d'environnement :
```bash
cp .env.example .env
# Éditer .env et ajouter vos clés API :
# - OPENAI_API_KEY
# - BRAVE_API_KEY
# - YOUTUBE_API_KEY
```

4. Lancer l'application :
```bash
make run
```

### Méthode 2: Utilisation avec Docker

```bash
# Construction de l'image
make docker-build

# Lancement de l'application
make docker-run
```

## 📁 Structure du Projet

```
podcast-insights/
├── src/                    # Code source
│   ├── app.py             # Application principale
│   ├── query_processor.py # Traitement des requêtes
│   └── ui_components.py   # Interface utilisateur
├── tests/                 # Tests
│   ├── integration/      # Tests d'intégration
│   ├── performance/      # Tests de performance
│   └── fixtures/         # Fixtures de test
├── data/                 # Données
│   ├── youtube_transcripts/  # Transcriptions
│   └── tools/              # Outils de gestion des données
├── docs/                 # Documentation
└── docker/               # Configuration Docker
```

## 🧪 Tests

```bash
# Lancer tous les tests
make test

# Tests d'intégration uniquement
pytest tests/integration

# Tests de performance
pytest tests/performance

# Vérification du style
make lint
```

## 📊 Gestion des Données

### Génération de données de test
```bash
python data/tools/generate_test_data.py
```

### Backup de ChromaDB
```bash
python data/tools/backup_chromadb.py
```

## 🔧 Développement

1. Installation de l'environnement de développement :
```bash
make install-dev
pre-commit install
```

2. Linting et formatage :
```bash
make lint
```

3. Mise à jour des dépendances :
```bash
pip-compile requirements.in
pip-compile requirements-dev.in
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forker le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/amazing-feature`)
3. Commiter vos changements (`git commit -m 'Add amazing feature'`)
4. Pousser vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📧 Contact

Eric Blanvillain - [@EricBlanvillain](https://github.com/EricBlanvillain)