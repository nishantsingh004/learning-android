from typing import Optional
import base64

class SpeechResult:
    def __init__(self, text: str, confidence: float):
        self.text = text
        self.confidence = confidence

def speech_to_text(audio_bytes: bytes, language: str = "hi-IN") -> SpeechResult:
    return SpeechResult(text="मेरे खेत के लिए अगली फसल क्या हो?", confidence=0.92)

def text_to_speech(text: str, language: str = "hi-IN") -> str:
    dummy = b"FAKE_WAV_BYTES"
    return base64.b64encode(dummy).decode("utf-8")
