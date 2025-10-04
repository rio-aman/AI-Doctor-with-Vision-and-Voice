from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr

from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_crossplatform_with_gtts

system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
                What's in this image?. Do you find anything wrong with it medically? 
                If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
                your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
                Donot say 'In the image I see' but say 'With what I see, I think you have ....'
                Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
                Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# Ensure 'final' folder exists
OUTPUT_FOLDER = os.path.join(os.getcwd(), "final")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_next_filename(base_name="final", extension=".mp3", folder=OUTPUT_FOLDER):
    """
    Returns a filename like final1.mp3, final2.mp3, ... in the specified folder.
    """
    i = 1
    while True:
        filename = os.path.join(folder, f"{base_name}{i}{extension}")
        if not os.path.exists(filename):
            return filename
        i += 1

def process_inputs(audio_filepath, image_filepath):
    # Step 1: Transcribe audio
    speech_to_text_output = transcribe_with_groq(
        GROQ_API_KEY=os.getenv("GROQ_API_KEY"), 
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    # Step 2: Analyze image if provided
    if image_filepath:
        encoded_img = encode_image(image_filepath)
        doctor_response = analyze_image_with_query(
            query=system_prompt + speech_to_text_output,
            encoded_image=encoded_img,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "No image provided for me to analyze"

    # Step 3: Generate TTS audio in 'final' folder
    voice_of_doctor = get_next_filename(base_name="final", extension=".mp3")
    text_to_speech_crossplatform_with_gtts(input_text=doctor_response, output_filepath=voice_of_doctor)

    # Return results
    return speech_to_text_output, doctor_response, voice_of_doctor

# Create Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath"),
        gr.Image(type="filepath")
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response", lines=5),
        gr.Audio(label="Doctor's Voice")
    ],
    title="AI Doctor with Vision and Voice"
)

iface.launch(debug=True)
