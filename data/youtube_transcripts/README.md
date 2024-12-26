# Transcriptions de Podcasts

## Structure
Chaque transcription est stockée au format JSON avec la structure suivante :

```json
{
    "title": "Titre de l'épisode",
    "channel": "Nom du podcast",
    "published_at": "YYYY-MM-DD",
    "text": "Transcription...",
    "metadata": {
        "duration": "HH:MM:SS",
        "language": "en",
        "url": "URL de l'épisode"
    }
}
```

## Gestion des données

1. Générer des données de test :
```bash
python data/tools/generate_test_data.py
```

2. Backup de ChromaDB :
```bash
python data/tools/backup_chromadb.py
```