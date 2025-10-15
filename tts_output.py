import os
from dotenv import load_dotenv
from murf import Murf
import os 
import time
from playsound import playsound

# Load .env file
load_dotenv()

# Get API key from environment
MURF_API_KEY = os.getenv("MURF_API_KEY")

client=Murf(api_key=MURF_API_KEY)

def stream_text_to_speech_calm(text, output_path):
    try:
        print(f"Streaming text: {text}")
        audio_stream = client.text_to_speech.stream(
            text=text,
            voice_id="en-US-wayne",
            format="MP3",
            sample_rate=48000.0,
            channel_type="STEREO",
            style="Calm",
            rate=-30,
            pitch=0
        )

        with open(output_path, "wb") as file:
            for chunk in audio_stream:
                file.write(chunk)
        playsound(f'{output_path}')
        os.remove(output_path)
        print(f'Audio created at {output_path}')

    except Exception as e:
        print(f'ERROR in Text to Speech: {e}')
        raise

def stream_text_to_speech_stern(text, output_path):
    try:
        print(f"Streaming text: {text}")
        audio_stream = client.text_to_speech.stream(
            text=text,
            voice_id="en-US-wayne",
            format="MP3",
            sample_rate=48000.0,
            channel_type="STEREO",
            style="Angry",
            rate=-15,
            pitch=50
        )

        with open(output_path, "wb") as file:
            for chunk in audio_stream:
                file.write(chunk)
        
        
        print(f'Audio created at {output_path}')
        playsound(f'{output_path}')
        os.remove(output_path)
        print('Audio deleted after playback')

    except Exception as e:
        print(f'ERROR in Text to Speech: {e}')
        raise


