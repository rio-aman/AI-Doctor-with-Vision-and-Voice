# Setup Text to Speech–TTS–model with gTTS and Use Model for Text output to Voice
import os
from gtts import gTTS

try:
    from playsound import playsound
except ImportError:
    raise ImportError("Please install the 'playsound' package: pip install playsound")

def text_to_speech_crossplatform_with_gtts(input_text, output_filepath="output.mp3"):
    """
    Generates MP3 with gTTS and plays it immediately using playsound.
    Works on Windows, macOS, and Linux.
    """
    # Step 1: Generate MP3
    tts = gTTS(text=input_text, lang="hi", slow=False)
    tts.save(output_filepath)

    # Step 2: Play the audio immediately
    abs_path = os.path.abspath(output_filepath)
    playsound(abs_path)


# Example usage
input_text = "Activating AI Doctor system... and now you can access the application by the provided url."
text_to_speech_crossplatform_with_gtts(input_text, "gtts_testing_autoplay.mp3")

