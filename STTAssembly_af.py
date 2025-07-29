import os
import pandas as pd
import requests
import assemblyai as aai
from pathlib import Path
from deep_translator import GoogleTranslator # Import the translator

# ========== CONFIG ==========
# --- PASTE YOUR ASSEMBLYAI API KEY HERE ---
aai.settings.api_key = "23bd7dac28bc40bbb8e1281cd990aa68"

EXCEL_FILE = "voicesamples.xlsx"
AUDIO_DIR = Path("audio_files")
TRANSCRIPTS_DIR = Path("transcripts")
# ============================

# Make sure output folders exist
AUDIO_DIR.mkdir(exist_ok=True)
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

if not aai.settings.api_key or "YOUR_ASSEMBLYAI_API_KEY" in aai.settings.api_key:
    print("❌ Error: Please replace 'YOUR_ASSEMBLYAI_API_KEY' with your key from AssemblyAI.")
    exit()

# Read Excel and get all URLs
try:
    df = pd.read_excel(EXCEL_FILE)
    urls = df.iloc[:, 1].dropna().tolist()
except FileNotFoundError:
    print(f"❌ Error: The file '{EXCEL_FILE}' was not found.")
    exit()
except Exception as e:
    print(f"❌ Error reading Excel file: {e}")
    exit()

# Create a transcriber object
transcriber = aai.Transcriber()

# Loop through each URL
for idx, url in enumerate(urls, 1):
    try:
        print(f"\n🔊 Processing File {idx} from URL: {url[:50]}...")

        # Step 1: Download audio
        local_audio_path = AUDIO_DIR / f"audio_{idx}.mp3"
        r = requests.get(url, timeout=60)
        r.raise_for_status()
        with open(local_audio_path, "wb") as f:
            f.write(r.content)
        print(f"✅ Downloaded and saved to: {local_audio_path}")

        # Step 2: Transcribe using AssemblyAI
        print(f"🎤 Uploading '{local_audio_path.name}' for transcription...")
        config = aai.TranscriptionConfig(language_code="hi") # Transcribe to Hindi
        transcript = transcriber.transcribe(str(local_audio_path), config=config)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"❌ Transcription failed for File {idx}: {transcript.error}")
            continue

        hindi_text = transcript.text
        if not hindi_text:
            hindi_text = "NO SPEECH DETECTED"
        
        # --- NEW: Step 3: Translate the Hindi text to English ---
        print(f"🌐 Translating transcript to English...")
        try:
            translated_text = GoogleTranslator(source='hi', target='en').translate(hindi_text)
        except Exception as e:
            print(f"⚠️ Translation failed: {e}")
            translated_text = "Translation failed."

        # Step 4: Save both transcripts to the file
        output_path = TRANSCRIPTS_DIR / f"transcript_{idx}.txt"
        print(f"📝 Saving Hindi and English transcripts to {output_path}...")

        file_content = (
            f"Hindi Transcription:\n{hindi_text}\n"
            f"\n----------------------------------------\n\n"
            f"English Translation:\n{translated_text}"
        )

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        
        print(f"✅ File {idx} complete. Transcript saved.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Download error for File {idx}: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred with File {idx}: {e}")

print("\n\n🎉 All files processed!")