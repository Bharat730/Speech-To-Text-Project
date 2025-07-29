import os
import google.generativeai as genai
from pathlib import Path
import time
import shutil

# ========== CONFIG ==========
# --- PASTE YOUR GOOGLE AI API KEY HERE ---
GOOGLE_API_KEY = "AIzaSyDcOyEAcgoGOClGl2r_jSUstfQGoo8EoWY"

# Folder where you will put your audio files
AUDIO_DIR = Path("GemCLI_audio")
# Folder where the transcripts will be saved
TRANSCRIPTS_DIR = Path("GemCLI_transcripts")
# ============================

# --- Setup: Configure API and create folders ---
try:
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"❌ API Key Configuration Error: {e}")
    exit()

AUDIO_DIR.mkdir(exist_ok=True)
if TRANSCRIPTS_DIR.exists():
    shutil.rmtree(TRANSCRIPTS_DIR)
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

if "YOUR_GOOGLE_API_KEY" in GOOGLE_API_KEY:
    print("❌ Error: Please replace 'YOUR_GOOGLE_API_KEY' with your key from Google AI Studio.")
    exit()

# Find all audio files in the directory
audio_files = list(AUDIO_DIR.glob("*.[wW][aA][vV]")) + \
              list(AUDIO_DIR.glob("*.[mM][pP][3]")) + \
              list(AUDIO_DIR.glob("*.[mM][4][aA]")) + \
              list(AUDIO_DIR.glob("*.[fF][lL][aA][cC]"))

if not audio_files:
    print(f"No audio files found in '{AUDIO_DIR}'. Please add your files to this folder.")
    exit()

# --- Initialize the Gemini Model ---
print("🧠 Initializing Gemini 1.5 Pro model...")
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

# Loop through each audio file
for audio_path in audio_files:
    audio_file_for_api = None # Define variable outside try block
    try:
        print(f"\n- - - - - Processing File: {audio_path.name} - - - - -")
        output_path = TRANSCRIPTS_DIR / f"{audio_path.stem}_transcript.txt"

        # --- Step 1: Upload the audio file to Google ---
        print(f"⬆️  Uploading '{audio_path.name}'...")
        audio_file_for_api = genai.upload_file(path=str(audio_path))
        
        while audio_file_for_api.state.name == "PROCESSING":
            print("    - Waiting for file processing...")
            time.sleep(5) # Shorter wait time is fine
            audio_file_for_api = genai.get_file(audio_file_for_api.name)

        if audio_file_for_api.state.name == "FAILED":
            print(f"❌ File processing failed for {audio_path.name}")
            continue
        
        print("✅ File uploaded and ready.")

        # --- Step 2: Send the prompt to Gemini ---
        print("🎤 Sending request for transcription...")
        
        prompt = (
            "You are an expert transcriber and translator.\n"
            "Please process the attached audio file and provide the following:\n"
            "1. A complete transcription of the dialogue.\n"
            "2. Identify each speaker and label them as 'Speaker 1', 'Speaker 2', etc.\n"
            "3. For each speaker's turn, provide an English translation of what they said.\n"
            "Format the output clearly for each turn. For example:\n"
            "Speaker 1:\n"
            "  Original: [The original transcribed text]\n"
            "  English: [The English translation]\n"
        )

        response = model.generate_content([prompt, audio_file_for_api])

        # --- Step 3: Save the result ---
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        
        print(f"✅ Transcript saved to {output_path}")

    except Exception as e:
        print(f"❌ An unexpected error occurred with '{audio_path.name}': {e}")
    
    finally:
        # --- Step 4: Clean up the uploaded file ---
        if audio_file_for_api:
            print(f"🗑️  Deleting uploaded file from Google's server...")
            genai.delete_file(audio_file_for_api.name)

print("\n\n🎉 All files processed!")