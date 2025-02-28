from gtts import gTTS
import os

def text_to_speech(text, filename="output.wav"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

# Example Usage

text = "Hello, I am your AI avatar. I can speak anything you type."
audio_file = text_to_speech(text)
print(f"Audio saved as {audio_file}")