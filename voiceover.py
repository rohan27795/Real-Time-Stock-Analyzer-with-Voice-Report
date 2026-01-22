from gtts import gTTS
import os
from datetime import datetime

def generate_voice_report(swot_text):
    """
    Generate a voice report from SWOT text using Google Text-to-Speech.
    
    Args:
        swot_text (str): The SWOT analysis text to convert to speech
        
    Returns:
        str: Path to the generated audio file
    """
    # Create audio directory if it doesn't exist
    audio_dir = "audio_reports"
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    
    # Generate unique filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file = os.path.join(audio_dir, f"swot_report_{timestamp}.mp3")
    
    try:
        # Convert text to speech
        tts = gTTS(text=swot_text, lang='en', slow=False)
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        print(f"Error generating voice report: {e}")
        # Return a placeholder or handle error appropriately
        raise

