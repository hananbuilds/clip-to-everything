"""
MAIN — runs the whole pipeline, start to finish.

Usage:
    python main.py "https://www.youtube.com/watch?v=XXXXXXX"

This ties together all 4 steps:
  1. transcribe.py   -> get the transcript
  2. generate.py     -> turn transcript into blog/tweets/linkedin/titles
  3. score.py        -> grade each piece of content
  4. save_output.py  -> save everything as real files
"""

import sys
from dotenv import load_dotenv
load_dotenv()  # reads your .env file so GROQ_API_KEY is available

from transcribe import get_transcript
from generate import generate_all
from score import score_all
from save_output import save_results


def run_pipeline(video_source: str):
    print(f"\n=== STEP 1: Transcribing '{video_source}' ===")
    transcript = get_transcript(video_source)

    print("\n=== STEP 2: Generating content ===")
    generated = generate_all(transcript)

    print("\n=== STEP 3: Scoring content ===")
    scores = score_all(generated)

    print("\n=== STEP 4: Saving results ===")
    save_results(generated, scores)

    print("\nAll done! Check the outputs/ folder for your content.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python main.py "<youtube_url_or_file_path>"')
        sys.exit(1)

    run_pipeline(sys.argv[1])
