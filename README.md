# Podcast Insights 🎙️

Une application Streamlit pour analyser les transcriptions de podcasts en utilisant l'IA et la recherche vectorielle.

## 🌟 Fonctionnalités

- Recherche avancée dans les transcriptions de podcasts
- Analyse alimentée par l'IA avec OpenAI
- Support pour plusieurs sources de podcasts (Lex Fridman, Huberman Lab, DOAC)
- Recherche par similarité vectorielle utilisant ChromaDB
- Interface utilisateur intuitive avec Streamlit

## 🛠 Technologies

- **Frontend**: Streamlit
- **Base de données**: ChromaDB
- **IA**: OpenAI API
- **Language**: Python
- **Dépendances**: streamlit, chromadb, openai, python-dotenv, pandas

## 🚀 Installation

1. Cloner le repository
```bash
git clone https://github.com/EricBlanvillain/podcast-insights.git
cd podcast-insights
```

2. Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: .\venv\Scripts\activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

4. Configurer les variables d'environnement
```bash
# Créer un fichier .env à la racine du projet et ajouter :
OPENAI_API_KEY=votre_clé_api_ici
```

5. Lancer l'application
```bash
streamlit run src/app.py
```

## 📁 Structure du Projet

```
podcast-insights/
├── src/
│   ├── __init__.py
│   ├── app.py              # Application principale
│   ├── query_processor.py  # Traitement des requêtes
│   └── ui_components.py    # Interface utilisateur
├── tests/
│   └── __init__.py
├── data/
│   └── youtube_transcripts/
├── docs/
│   ├── API.md
│   └── INSTALLATION.md
└── requirements.txt
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forker le projet
2. Créer une nouvelle branche (`git checkout -b feature/amazing-feature`)
3. Commiter vos changements (`git commit -m 'Add amazing feature'`)
4. Pusher sur la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📧 Contact

Eric Blanvillain - [@EricBlanvillain](https://github.com/EricBlanvillain)

Lien du projet: [https://github.com/EricBlanvillain/podcast-insights](https://github.com/EricBlanvillain/podcast-insights)