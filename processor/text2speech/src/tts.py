# Text-to-Speech module for ContentDroid 
# This code is largely credit to @mark-rez on GitHub, who created the original version of this module.
# https://github.com/mark-rez/TikTok-Voice-TTS

# Python standard modules
import asyncio
import subprocess
import os
import base64
import re
from json import load
import tempfile
import whisper
from typing import Dict, List, Optional
from pathlib import Path

# Downloaded modules
import aiohttp

# Local files
from .voice import Voice

def tts(
    text: str,
    voice: Voice,
    output_file_path: str = "output.mp3",
):
    """Main function to convert text to speech and save to a file."""
    
    # Validate input arguments
    _validate_args(text, voice)

    # Load endpoint data from the endpoints.json file
    endpoint_data: List[Dict[str, str]] = _load_endpoints()
    success: bool = False    

    # Iterate over endpoints to find a working one
    for endpoint in endpoint_data:
        # Generate audio bytes from the current endpoint
        audio_bytes: bytes = asyncio.run(_fetch_audio_bytes_async(endpoint, text, voice))

        if audio_bytes:
            # Create video with audio using ffmpeg
            script_dir = os.path.dirname(__file__)
            # join without a leading slash so the path is relative to the package directory
            video_path = os.path.join(script_dir, '../../videos', 'background.mp4')
            add_audio_and_captions_to_video(video_path=video_path, audio_bytes=audio_bytes, text=text, output_path=output_file_path)
            
            success = True
            # Stop after processing a valid endpoint
            break

    if not success:
        raise Exception("failed to generate audio, all endpoints failed")

def _save_audio_file(output_file_path: str, audio_bytes: bytes):
    """Write the audio bytes to a file."""
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
        
    with open(output_file_path, "wb") as file:
        file.write(audio_bytes)

async def _fetch_audio_bytes_async(
    endpoint: Dict[str, str],
    text: str,
    voice: Voice
) -> Optional[bytes]:
    text_chunks: List[str] = _split_text(text)
    audio_chunks: List[str] = [""] * len(text_chunks)

    async def fetch_chunk(
        session: aiohttp.ClientSession,
        index: int,
        text_chunk: str
    ):
        async with session.post(
            endpoint["url"],
            json={"text": text_chunk, "voice": voice.value},
        ) as response:
            response.raise_for_status()
            data = await response.json()
            audio_chunks[index] = data[endpoint["response"]]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_chunk(session, i, chunk) for i, chunk in enumerate(text_chunks)]
        
        try:
            await asyncio.gather(*tasks)
        except:
            return None

    return base64.b64decode("".join(audio_chunks))

def _load_endpoints() -> List[Dict[str, str]]:
    """Load endpoint configurations from a JSON file."""
    script_dir = os.path.dirname(__file__)
    # join without a leading slash so the path is relative to the package directory
    json_file_path = os.path.join(script_dir, '../config', 'config.json')
    with open(json_file_path, 'r') as file:
        return load(file)

def _validate_args(text: str, voice: Voice):
    """Validate the input arguments."""
    
    # Check if the voice is of the correct type
    if not isinstance(voice, Voice):
        raise TypeError("'voice' must be of type Voice")
    
    # Check if the text is not empty
    if not text:
        raise ValueError("text must not be empty")

def _split_text(text: str) -> List[str]:
    """Split text into chunks of 300 characters or less."""
    
    # Split text into chunks based on punctuation marks
    merged_chunks: List[str] = []
    separated_chunks: List[str] = re.findall(r'.*?[.,!?:;-]|.+', text)
    character_limit: int = 300
    # Further split any chunks longer than 300 characters
    for i, chunk in enumerate(separated_chunks):
        if len(chunk.encode("utf-8")) > character_limit:
            separated_chunks[i:i+1] = re.findall(r'.*?[ ]|.+', chunk) 

    # Combine chunks into segments of 300 characters or less
    current_chunk: str = ""
    for separated_chunk in separated_chunks:
        if len(current_chunk.encode("utf-8")) + len(separated_chunk.encode("utf-8")) <= character_limit:
            current_chunk += separated_chunk
        else:
            merged_chunks.append(current_chunk)
            current_chunk = separated_chunk

    # Append the last chunk
    merged_chunks.append(current_chunk)
    return merged_chunks


def add_audio_and_captions_to_video(video_path: str, audio_bytes: bytes, text: str, output_path: str, audio_format: str = "mp3"):
    # Write audio to temp file
    with tempfile.NamedTemporaryFile(suffix=f".{audio_format}", delete=False) as tmp_audio:
        tmp_audio.write(audio_bytes)
        tmp_audio_path = tmp_audio.name

    # Generate SRT from audio using Whisper
    model = whisper.load_model("base")
    result = model.transcribe(tmp_audio_path, word_timestamps=True)
    
    # Write SRT temp file
    srt_path = tmp_audio_path.replace(f".{audio_format}", ".srt")
    with open(srt_path, "w") as f:
        i = 1
        for segment in result["segments"]:
            for word in segment["words"]:
                start = format_srt_time(word["start"])
                end = format_srt_time(word["end"])
                f.write(f"{i}\n{start} --> {end}\n{word['word'].strip()}\n\n")
                i += 1

    try:
        subprocess.run([
            "ffmpeg",
            "-i", video_path,
            "-i", tmp_audio_path,
            "-c:v", "libx264",         # must re-encode to burn in subtitles
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-vf", f"subtitles={srt_path}:force_style='Fontname=Komika Axis,Alignment=10,PrimaryColour=&H03fcff,Fontsize=35'",
            "-shortest",
            "-y",
            output_path
        ], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("FFmpeg failed:", e.stderr)
        raise
    finally:
        os.unlink(tmp_audio_path)
        os.unlink(srt_path)

def format_srt_time(seconds: float) -> str:
    ms = int((seconds % 1) * 1000)
    s = int(seconds) % 60
    m = int(seconds // 60) % 60
    h = int(seconds // 3600)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"