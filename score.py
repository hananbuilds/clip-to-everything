"""
STEP 3 — Check the content automatically (the differentiator)

What this file does, in plain terms:
Looks at each piece of content the AI wrote and grades it using simple,
explainable rules (not another AI call). This is the part that makes
this tool stand out from a plain "generate content" script — it also
checks its own work.

Every score is out of 10, plus a short list of reasons for the score.
"""

import re
import textstat


def score_title(title_block: str) -> dict:
    """Checks the first title in the block: length and whether it's engaging."""
    first_title = title_block.strip().split("\n")[0]
    first_title = re.sub(r"^\d+[\.\)]\s*", "", first_title)  # remove "1. " prefix

    score = 10
    notes = []

    length = len(first_title)
    if length > 60:
        score -= 3
        notes.append(f"Title is {length} chars — over the 60-char sweet spot for SEO.")
    else:
        notes.append(f"Title length ({length} chars) is good for SEO.")

    if not any(char.isdigit() for char in first_title) and "?" not in first_title:
        score -= 1
        notes.append("Consider adding a number or question — these tend to boost clicks.")

    return {"score": max(score, 0), "notes": notes}


def score_blog(blog_text: str) -> dict:
    """Checks word count and readability of the blog post."""
    score = 10
    notes = []

    word_count = len(blog_text.split())
    if word_count < 200:
        score -= 4
        notes.append(f"Only {word_count} words — a bit thin for a blog post.")
    else:
        notes.append(f"Good length: {word_count} words.")

    reading_ease = textstat.flesch_reading_ease(blog_text)
    if reading_ease < 40:
        score -= 2
        notes.append(f"Readability score {reading_ease:.0f} — a bit dense/hard to read.")
    else:
        notes.append(f"Readability score {reading_ease:.0f} — easy to read.")

    return {"score": max(score, 0), "notes": notes}


def score_tweets(tweets_text: str) -> dict:
    """Checks that tweets stay under the character limit and have a hook."""
    score = 10
    notes = []
    lines = [l for l in tweets_text.split("\n") if l.strip()]

    for line in lines:
        if len(line) > 280:
            score -= 3
            notes.append("One tweet is over 280 characters — needs trimming.")
            break
    else:
        notes.append("All tweets fit within the character limit.")

    has_hook = any(("?" in l or any(ch.isdigit() for ch in l)) for l in lines)
    if has_hook:
        notes.append("At least one tweet uses a question or number (good hook).")
    else:
        score -= 1
        notes.append("No question marks or numbers found — hooks could be stronger.")

    return {"score": max(score, 0), "notes": notes}


def score_linkedin(linkedin_text: str) -> dict:
    """Checks LinkedIn post length — too short or too long both hurt engagement."""
    score = 10
    notes = []
    word_count = len(linkedin_text.split())

    if word_count < 100:
        score -= 3
        notes.append(f"Only {word_count} words — LinkedIn posts perform better around 150-250.")
    elif word_count > 300:
        score -= 2
        notes.append(f"{word_count} words is a bit long for LinkedIn's feed format.")
    else:
        notes.append(f"Good length for LinkedIn: {word_count} words.")

    return {"score": max(score, 0), "notes": notes}


def score_all(generated: dict) -> dict:
    """Runs all scoring checks and returns a full report."""
    return {
        "titles": score_title(generated["titles"]),
        "blog": score_blog(generated["blog"]),
        "tweets": score_tweets(generated["tweets"]),
        "linkedin": score_linkedin(generated["linkedin"]),
    }
