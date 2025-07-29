import os
import whisper
from pathlib import Path
import shutil
from datasets import load_dataset
import soundfile as sf
import numpy as np

# ========== CONFIG ==========
AUDIO_DIR = Path("Audio_Hindi")
TRANSCRIPTS_DIR = Path("transcripts_Hindi")
# ============================

# --- Setup: Clear previous transcripts and create folders ---
if TRANSCRIPTS_DIR.exists():
    print(f"🧹 Clearing previous transcripts from '{TRANSCRIPTS_DIR}'...")
    shutil.rmtree(TRANSCRIPTS_DIR)

AUDIO_DIR.mkdir(exist_ok=True)
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

# --- 1. Load Whisper Model ---
print("🧠 Loading Whisper model 'medium'...")
model = whisper.load_model("medium")
print("🤖 Model loaded.")

# --- 2. Load 5 Hindi Samples from the FLEURS Dataset ---
print("\n⬇️ Loading 5 Hindi samples from the Hugging Face FLEURS dataset...")
try:
    dataset = load_dataset("google/fleurs", "hi_in", split="test[:5]", trust_remote_code=True)
    print(f"✅ Dataset loaded. Found {len(dataset)} audio files.")
except Exception as e:
    print(f"❌ Failed to load dataset. Error: {e}")
    exit()

# --- 3. Loop, Transcribe, Translate, and Save ---
for i, sample in enumerate(dataset):
    print(f"\n🔊 Processing File {i + 1}...")
    
    audio_data = sample['audio']['array']
    sampling_rate = sample['audio']['sampling_rate']
    local_audio_path = AUDIO_DIR / f"hindi_sample_{i}.wav"
    
    try:
        # Save audio file if it doesn't exist
        if not local_audio_path.exists():
            sf.write(local_audio_path, audio_data, sampling_rate)
            print(f"✅ Saved audio to: {local_audio_path}")
        else:
            print(f"✅ Using existing audio file: {local_audio_path}")
        
        # Prepare audio data for Whisper
        audio_for_whisper = audio_data.astype(np.float32)

        # Task 1: Transcribe in Hindi
        print(f"🎤 Transcribing '{local_audio_path.name}' to Hindi...")
        result_hindi = model.transcribe(audio_for_whisper, language="hi")
        transcription_text = result_hindi['text']

        # Task 2: Translate to English
        print(f"🌐 Translating '{local_audio_path.name}' to English...")
        result_english = model.transcribe(audio_for_whisper, task="translate")
        translation_text = result_english['text']

        # Prepare the content for the text file
        file_content = (
            f"Hindi Transcription:\n{transcription_text}\n"
            f"\n----------------------------------------\n\n"
            f"English Translation:\n{translation_text}"
        )

        # Save the combined transcript to a text file
        output_path = TRANSCRIPTS_DIR / f"hindi_transcript_{i}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        print(f"📝 Hindi: {transcription_text}")
        print(f"📝 English: {translation_text}")
        print(f"✅ Saved transcript to {output_path}")

    except Exception as e:
        print(f"❌ An unexpected error occurred with File {i + 1}: {e}")

print("\n\n🎉 Transcription and translation of all 5 Hindi files complete!")
