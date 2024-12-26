# Guide d'Utilisation

## Installation

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

4. Configurer les API keys
Créer un fichier `.env` avec :
```
OPENAI_API_KEY=your_key_here
BRAVE_API_KEY=your_key_here
YOUTUBE_API_KEY=your_key_here
```

## Utilisation

1. Lancer l'application
```bash
streamlit run app.py
```

2. Interface utilisateur
- Entrer une question dans la barre de recherche
- Ajuster les paramètres de recherche si nécessaire
- Cliquer sur 'Search' pour obtenir les résultats

3. Paramètres avancés
- Max Sources : Nombre maximum de sources à utiliser
- Min Relevance : Score minimum de pertinence
- Podcast Sources : Sélection des podcasts à inclure