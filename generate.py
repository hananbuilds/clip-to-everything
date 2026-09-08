"""
STEP 2 — Rewrite the transcript into content

What this file does, in plain terms:
Takes the transcript text and asks an AI model (Google Gemini, which is
free and has an easy sign-up) to turn it into 4 separate pieces of content:
  1. A blog post
  2. Three tweet ideas
  3. A LinkedIn post
  4. Three catchy title options

We send 4 small, separate requests instead of 1 giant one — this is
more reliable and easier to grade/debug individually.
"""

import os
import google.generativeai as genai

# Reads your API key from an environment variable so it's never hardcoded
# or accidentally uploaded to GitHub. See README for how to set this.
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

MODEL = "gemini-1.5-flash"  # fast + free-tier friendly
_model = genai.GenerativeModel(MODEL)


def _ask(prompt: str, transcript: str) -> str:
    """Sends one prompt + the transcript to the AI model and returns plain text."""
    full_prompt = (
        "You are a skilled content editor for creators.\n\n"
        f"{prompt}\n\nTRANSCRIPT:\n{transcript}"
    )
    response = _model.generate_content(full_prompt)
    return response.text.strip()


def generate_blog_post(transcript: str) -> str:
    prompt = (
        "Turn this video transcript into a well-structured blog post "
        "with a title, intro, a few subheadings, and a short conclusion. "
        "Keep it under 500 words."
    )
    return _ask(prompt, transcript)


def generate_tweets(transcript: str) -> str:
    prompt = (
        "Write 3 short, punchy tweet ideas (each under 280 characters) "
        "summarizing the most interesting points from this video. "
        "Number them 1, 2, 3."
    )
    return _ask(prompt, transcript)


def generate_linkedin_post(transcript: str) -> str:
    prompt = (
        "Write one professional LinkedIn post (150-250 words) sharing the "
        "key insight from this video, in a personal, first-person tone."
    )
    return _ask(prompt, transcript)


def generate_titles(transcript: str) -> str:
    prompt = (
        "Suggest 3 short, catchy video/blog titles (each under 60 characters) "
        "based on this transcript. Number them 1, 2, 3."
    )
    return _ask(prompt, transcript)


def generate_all(transcript: str) -> dict:
    """Runs all 4 generation steps and returns them as a dictionary."""
    print("Generating blog post...")
    blog = generate_blog_post(transcript)

    print("Generating tweets...")
    tweets = generate_tweets(transcript)

    print("Generating LinkedIn post...")
    linkedin = generate_linkedin_post(transcript)

    print("Generating titles...")
    titles = generate_titles(transcript)

    return {
        "blog": blog,
        "tweets": tweets,
        "linkedin": linkedin,
        "titles": titles,
    }


if __name__ == "__main__":
    # Quick manual test: reads outputs/transcript.txt if it already exists
    with open("outputs/transcript.txt", "r", encoding="utf-8") as f:
        sample_transcript = f.read()

    results = generate_all(sample_transcript)
    for name, content in results.items():
        print(f"\n--- {name.upper()} ---\n{content}\n")
