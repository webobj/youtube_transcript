import os
import re
import json
from pathlib import Path
from typing import Optional, List
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class YouTubeSummarizer:
    def __init__(self, api_key: Optional[str] = None):
        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your environment or .env file.")
        
        genai.configure(api_key=key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Cache setup
        self.cache_file = Path(__file__).parent / ".summary_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> dict:
        """Loads the cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        """Saves the cache to disk."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.cache, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")

    def get_cached_summary(self, video_id: str) -> Optional[str]:
        """Retrieves a summary from the cache if available."""
        return self.cache.get(video_id)

    def save_summary(self, video_id: str, summary: str):
        """Saves a summary to the cache."""
        self.cache[video_id] = summary
        self._save_cache()

    def extract_video_id(self, url: str) -> str:
        """Extracts the video ID from a YouTube URL."""
        video_id = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if video_id:
            return video_id.group(1)
        raise ValueError(f"Could not extract video ID from URL: {url}")

    def get_transcript(self, video_id: str) -> str:
        """Fetches the transcript for a given video ID.

        Tries English first, then falls back to any available language.
        """
        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)

            # Try English first
            try:
                transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB'])
            except Exception:
                # Fall back to any available transcript
                transcript = next(iter(transcript_list))

            fetched = transcript.fetch()
            return " ".join([item.text for item in fetched])
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")

    def summarize(self, transcript: str) -> str:
        """Summarizes the transcript using Gemini."""
        prompt = (
            "You are an expert at summarizing YouTube videos. "
            "Given the following transcript, provide a short, concise summary that extracts the key points. "
            "Use bullet points for the key takeaways.\n\n"
            f"Transcript: {transcript}"
        )
        
        response = self.model.generate_content(prompt)
        return response.text

if __name__ == "__main__":
    # For testing purposes
    pass
