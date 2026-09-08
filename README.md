# Clip-to-Everything

Turn one video into a week of content — automatically.

## The problem

Creators spend hours after publishing a video, manually rewriting it into
a blog post, tweets, a LinkedIn post, and a catchy title. This tool does
all of that in one run, and even grades its own output so you know what's
actually good before you post it.

## What it does

Give it a YouTube link (or a local video file) and it will:

1. **Transcribe** the video (turn speech into text)
2. **Generate** a blog post, 3 tweet ideas, a LinkedIn post, and 3 title options
3. **Score** each piece of content automatically (length, readability, hook strength — no AI needed for this step, just rules)
4. **Save** everything as real files you can open and use immediately

## How to run it

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your free Gemini API key
cp .env.example .env
# then open .env and paste your key (get one free at https://aistudio.google.com/apikey)

# 3. Run it on any video
python main.py "https://www.youtube.com/watch?v=XXXXXXX"
```

Your results will appear in the `outputs/` folder:
- `blog_post.txt`
- `tweets.txt`
- `linkedin_post.txt`
- `titles.txt`
- `summary.txt` — everything at a glance, with scores
- `scores.json` — the same scores in a machine-readable format

## Example output

*(Replace this section with a real example once you've run it on a video —
judges read this first, so a real before/after example here is worth more
than anything else in the README.)*

## Why this is more than "just an AI wrapper"

Most tools like this stop at "AI writes the post." This one adds a fourth
step: it checks its own work using plain, explainable rules (title length,
word count, readability score, presence of hooks) — so the output isn't
just generated, it's evaluated.

## Tech stack

- `yt-dlp` — downloads audio from a YouTube link
- `openai-whisper` — speech-to-text transcription (runs locally, free)
- `google-generativeai` (Gemini) — free-tier LLM API for content generation
- `textstat` — readability scoring
- Plain Python — for the rule-based scoring and file saving

## Built for

AI Content Engine Hackathon (Devpost) — "Build tools that automate the channel"
