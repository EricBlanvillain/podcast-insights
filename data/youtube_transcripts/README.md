# Transcriptions de Podcasts

Ce dossier contient les transcriptions de podcasts au format JSON.

## Structure

```
youtube_transcripts/
├── Lex_Fridman/
│   ├── 2024_01_episode1.json
│   └── 2024_01_episode2.json
├── Andrew_Huberman/
│   ├── 2024_01_episode1.json
│   └── 2024_01_episode2.json
└── The_Diary_Of_A_CEO/
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
