import sys
import argparse
from summarizer import YouTubeSummarizer

def process_video(url: str, summarizer: YouTubeSummarizer):
    """
    Processes a single video URL: extracts ID, gets transcript, and prints summary.
    """
    try:
        print(f"[*] Extracting video ID from {url}...")
        video_id = summarizer.extract_video_id(url)
        
        # Check cache first
        cached_summary = summarizer.get_cached_summary(video_id)
        if cached_summary:
            print(f"(*) Summary retrieved from cache.")
            summary = cached_summary
        else:
            print(f"[*] Fetching transcript for video ID: {video_id}...")
            transcript = summarizer.get_transcript(video_id)
            
            print(f"[*] Summarizing transcript using Gemini...")
            summary = summarizer.summarize(transcript)
            
            # Save to cache
            summarizer.save_summary(video_id, summary)
        
        print("\n" + "="*50)
        print("VIDEO SUMMARY")
        print("="*50)
        print(summary)
        print("="*50)
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Summarize a YouTube video using Gemini.")
    # nargs='?' makes valid if 0 or 1 arguments are provided
    parser.add_argument("url", nargs='?', help="The YouTube video URL (optional)")
    args = parser.parse_args()

    try:
        summarizer = YouTubeSummarizer()
        
        if args.url:
            # CLI mode (one-shot) - used by MCP server
            process_video(args.url, summarizer)
        else:
            # Interactive mode
            print("=== YouTube Summarizer Interactive Mode ===")
            print("Enter a YouTube URL to summarize it.")
            print("Press ENTER (empty input) to exit.")
            print("="*41)
            
            while True:
                try:
                    url = input("\nEnter YouTube URL: ").strip()
                    if not url:
                        print("Exiting...")
                        break
                    
                    process_video(url, summarizer)
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
        
    except Exception as e:
        print(f"Fatal Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
