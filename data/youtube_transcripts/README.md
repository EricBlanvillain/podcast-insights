# Transcriptions de Podcasts

Ce dossier contient les transcriptions de podcasts au format JSON.

## Structure

```
youtube_transcripts/
├── lex_fridman/
│   ├── 2024_01_episode1.json
│   └── 2024_01_episode2.json
├── huberman_lab/
│   ├── 2024_01_episode1.json
│   └── 2024_01_episode2.json
└── doac/
    ├── 2024_01_episode1.json
    └── 2024_01_episode2.json
```

## Format JSON

```json
{
    "title": "Titre de l'épisode",
    "channel": "Nom du podcast",
    "published_at": "2024-01-01",
    "text": "Transcription complète...",
    "metadata": {
        "duration": "HH:MM:SS",
        "language": "en",
        "url": "https://youtube.com/..."
    }
}
```