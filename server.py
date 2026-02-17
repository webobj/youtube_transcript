from mcp.server.fastmcp import FastMCP
import subprocess
import os

# Initialize FastMCP server
mcp = FastMCP("YouTube Summarizer")

@mcp.tool()
def summarize_video(url: str) -> str:
    """
    Summarize a YouTube video given its URL. 
    This tool runs a separate process to fetch the transcript and generate the summary, 
    ensuring resources are released immediately after use.
    """
    try:
        # Use uv to run the main.py script
        # We assume main.py is in the same directory and uv is available in path
        result = subprocess.run(
            ["uv", "run", "main.py", url],
            capture_output=True,
            text=True,
            check=False, # We'll handle the return code manually
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        if result.returncode != 0:
            return f"Error summarizing video:\n{result.stderr}"
        
        return result.stdout
        
    except Exception as e:
        return f"Failed to execute summarizer: {str(e)}"

if __name__ == "__main__":
    mcp.run()
