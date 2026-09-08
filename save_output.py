"""
STEP 4 — Save everything as real files

What this file does, in plain terms:
Takes the generated content and its scores, and writes them out as
plain text files inside the outputs/ folder, plus one summary file
that shows everything at a glance. This is the proof, for judges,
that the tool "actually runs and produces a real result."
"""

import os
import json


def save_results(generated: dict, scores: dict, output_dir: str = "outputs") -> None:
    os.makedirs(output_dir, exist_ok=True)

    # Save each piece of content as its own file
    with open(os.path.join(output_dir, "blog_post.txt"), "w", encoding="utf-8") as f:
        f.write(generated["blog"])

    with open(os.path.join(output_dir, "tweets.txt"), "w", encoding="utf-8") as f:
        f.write(generated["tweets"])

    with open(os.path.join(output_dir, "linkedin_post.txt"), "w", encoding="utf-8") as f:
        f.write(generated["linkedin"])

    with open(os.path.join(output_dir, "titles.txt"), "w", encoding="utf-8") as f:
        f.write(generated["titles"])

    # Save a single human-readable summary with everything + scores
    summary_lines = ["CLIP-TO-EVERYTHING — RESULTS SUMMARY", "=" * 40, ""]

    for section in ["titles", "blog", "tweets", "linkedin"]:
        summary_lines.append(f"\n## {section.upper()}  —  Score: {scores[section]['score']}/10")
        for note in scores[section]["notes"]:
            summary_lines.append(f"  - {note}")

    with open(os.path.join(output_dir, "summary.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    # Also save a machine-readable version (nice to show technical depth)
    with open(os.path.join(output_dir, "scores.json"), "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)

    print(f"\nAll files saved in the '{output_dir}/' folder:")
    for fname in ["blog_post.txt", "tweets.txt", "linkedin_post.txt", "titles.txt", "summary.txt", "scores.json"]:
        print(f"  - {output_dir}/{fname}")
