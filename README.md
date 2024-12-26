# Podcast Insights 🎙️

Une application Streamlit pour analyser les transcriptions de podcasts en utilisant l'IA et la recherche vectorielle.

## 🌟 Fonctionnalités

- Recherche avancée dans les transcriptions de podcasts
- Analyse AI-powered avec OpenAI
- Support multi-podcasts (Lex Fridman, Huberman Lab, DOAC)
- Recherche vectorielle avec ChromaDB
- Interface utilisateur Streamlit

## 🛠️ Installation

1. Cloner le repository :
```bash
git clone https://github.com/EricBlanvillain/podcast-insights.git
cd podcast-insights
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
```bash
# Créer un fichier .env et ajouter :
OPENAI_API_KEY=your_api_key
```

4. Lancer l'application :
```bash
streamlit run app.py
```

## 📁 Structure du Projet

```
podcast-insights/
├── app.py                # Application principale
├── query_processor.py    # Traitement des requêtes
└── ui_components.py      # Interface utilisateur
```