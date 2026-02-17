# YouTube Transcript Summarizer

A simple Python tool to summarize YouTube videos using their transcripts and Google's Gemini LLM. 

If you spending too much time watching YouTube videos, even the useful ones, you might be wasting time before you get the core ideas or having to skip the ads. Here is a solution to get some time back.

## Setup

1.  **Clone the project** (or create the directory).
2.  **Install dependencies**:
    ```bash
    uv add youtube-transcript-api google-generativeai python-dotenv mcp
    ```
3.  **Configure API Key**:
    - Copy `.env.example` to `.env`: `cp .env.example .env`
    - Add your [Gemini API Key](https://aistudio.google.com/app/apikey) to the `.env` file:
      ```
      GEMINI_API_KEY=your_actual_api_key_here
      ```

## Usage

Run the script with a YouTube video URL:

```bash
uv run main.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

The tool will extract the transcript, send it to Gemini, and output a concise summary with key takeaways.

### Interactive Mode

You can also run the tool without arguments to enter interactive mode. This is useful if you want to paste multiple URLs or avoid quoting issues in the shell.

```bash
uv run main.py
```

It will prompt you:
```
Enter YouTube URL: https://www.youtube.com/watch?v=...
```
Press **Enter** on an empty line to exit.

## Global Usage

To run this tool from anywhere in your terminal, add the following alias to your `~/.zshrc` (or `~/.bashrc`):

```bash
alias summarize-video='uv run --directory "/path/to/youtube_transcript" main.py'
```

After adding the alias, reload your shell (`source ~/.zshrc`). Now you can use it like this:

```bash
summarize-video "https://www.youtube.com/watch?v=VIDEO_ID"
```

## MCP Server (Claude Desktop)

To use this tool from Claude Desktop as an MCP server, add the following configuration to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "youtube-summarizer": {
      "command": "uv",
      "args": [
        "run",
        "server.py"
      ],
      "cwd": "/path/to/youtube_transcript"
    }
  }
}
```

This server is **ephemeral**: it stays running but consumes minimal resources. When you ask it to summarize a video, it spins up a separate process to do the heavy lifting, which then exits, freeing resources immediately.
