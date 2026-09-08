"""
STEP 1 — Get the video's words (transcript)

What this file does, in plain terms:
1. Takes a YouTube link (or a local video/audio file).
2. Downloads just the audio (fast, small file).
3. Runs Whisper (speech-to-text) on that audio to get a full transcript.

You do not need to understand every line to use this — just run it
and it will hand you back a text file with everything said in the video.
"""

import os
import sys
import whisper
import yt_dlp


def download_audio(youtube_url: str, output_dir: str = "downloads") -> str:
    """Downloads only the audio track from a YouTube video and saves it as an mp3."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "audio.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return os.path.join(output_dir, "audio.mp3")


def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    Turns an audio file into text using OpenAI's Whisper model.
    model_size options (bigger = more accurate but slower):
      "tiny"   -> fastest, least accurate
      "base"   -> good balance for a hackathon (recommended)
      "small"  -> more accurate, a bit slower
    """
    print(f"Loading Whisper model ({model_size})... this only happens once.")
    model = whisper.load_model(model_size)

    print("Transcribing audio... this can take a minute or two.")
    result = model.transcribe(audio_path)

    return result["text"]


def get_transcript(source: str) -> str:
    """
    Main entry point for Step 1.
    'source' can be a YouTube URL or a path to a local audio/video file.
    Returns the full transcript as a single string.
    """
    if source.startswith("http"):
        print("Downloading audio from YouTube...")
        audio_path = download_audio(source)
    else:
        audio_path = source  # assume it's already a local file

    transcript = transcribe_audio(audio_path)
    return transcript


if __name__ == "__main__":
    # Example: python transcribe.py "https://www.youtube.com/watch?v=XXXXXXX"
    if len(sys.argv) < 2:
        print('Usage: python transcribe.py "<youtube_url_or_file_path>"')
        sys.exit(1)

    video_source = sys.argv[1]
    text = get_transcript(video_source)

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/transcript.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("\nDone! Transcript saved to outputs/transcript.txt")
    print("\n--- Preview ---")
    print(text[:300] + "...")
