"""text2speech package exports

Expose the most commonly used symbols at package level so callers can
do `from text2speech import tts, Voice` if desired.
"""
from .src.tts import tts
from .src.voice import Voice

__all__ = ["tts", "Voice"]
