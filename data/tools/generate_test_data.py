import json
import os
from datetime import datetime, timedelta

def generate_sample_transcript(channel: str, episode_number: int, date: datetime):
    return {
        "title": f"{channel} Episode {episode_number}",
        "channel": channel,
        "published_at": date.strftime("%Y-%m-%d"),
        "text": f"This is a sample transcript for {channel} episode {episode_number}...",
        "metadata": {
            "duration": "01:30:00",
            "language": "en",
            "url": f"https://youtube.com/{channel.lower()}/episode{episode_number}"
        }
    }

def main():
    channels = ["Lex Fridman", "Huberman Lab", "DOAC"]
    base_path = os.path.join(os.path.dirname(__file__), "..", "youtube_transcripts")
    
    for channel in channels:
        channel_path = os.path.join(base_path, channel.lower().replace(" ", "_"))
        os.makedirs(channel_path, exist_ok=True)
        
        date = datetime.now()
        for i in range(5):  # Generate 5 episodes per channel
            transcript = generate_sample_transcript(channel, i+1, date)
            filename = f"{date.strftime('%Y%m%d')}_episode{i+1}.json"
            
            with open(os.path.join(channel_path, filename), 'w') as f:
                json.dump(transcript, f, indent=2)
            
            date -= timedelta(days=7)  # One episode per week

if __name__ == "__main__":
    main()