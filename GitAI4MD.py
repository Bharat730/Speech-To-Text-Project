import os
from pathlib import Path
import nemo.collections.asr as nemo_asr
import soundfile as sf
from datasets import load_dataset
import shutil

# ========== CONFIG ==========
# Folder to save downloaded audio files
AUDIO_DIR = Path("MahaDhwani_audio")
# Folder for final transcripts
TRANSCRIPTS_DIR = Path("MahaDhwani_transcripts")
# ============================

# --- Setup: Clear previous files and create folders ---
if AUDIO_DIR.exists():
    shutil.rmtree(AUDIO_DIR)
if TRANSCRIPTS_DIR.exists():
    shutil.rmtree(TRANSCRIPTS_DIR)

AUDIO_DIR.mkdir(exist_ok=True)
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

try:
    # --- 1. Load the Pre-trained MahaDhwani Model ---
    print("🧠 Downloading and loading the MahaDhwani Hindi STT model...")
    # This line automatically downloads the model from the NVIDIA NGC repository
    asr_model = nemo_asr.models.EncDecCTCModelBPE.from_pretrained(model_name="stt_hi_conformer_ctc_large")
    print("🤖 Model loaded successfully.")

    # --- 2. Load a Compatible Hindi Dataset ---
    print("\n⬇️ Loading 5 Hindi samples from the IndicSUPERB dataset...")
    # 'as' is the code for the "ASR" task. We take 5 samples from the 'test' split.
    dataset = load_dataset("ai4bharat/IndicSUPERB", "as", split="test[:5]", trust_remote_code=True)
    print(f"✅ Dataset loaded. Found {len(dataset)} audio files.")

    # --- 3. Loop, Save Audio, Transcribe, and Save Transcript ---
    audio_paths_to_transcribe = []
    for i, sample in enumerate(dataset):
        print(f"\n🔊 Preparing File {i + 1}...")
        
        audio_data = sample['audio']['array']
        sampling_rate = sample['audio']['sampling_rate']
        local_audio_path = AUDIO_DIR / f"hindi_sample_{i}.wav"
        
        # Save the audio file locally
        sf.write(local_audio_path, audio_data, sampling_rate)
        audio_paths_to_transcribe.append(str(local_audio_path))
        print(f"✅ Saved audio to: {local_audio_path}")

    # --- 4. Transcribe all files in a batch (more efficient) ---
    print("\n🎤 Transcribing all files...")
    transcriptions = asr_model.transcribe(paths2audio_files=audio_paths_to_transcribe)
    print("✅ Transcription complete.")

    # --- 5. Save the Transcripts ---
    for i, transcription in enumerate(transcriptions[0]):
        output_path = TRANSCRIPTS_DIR / f"hindi_transcript_{i}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcription)
        
        print(f"📝 Saved transcript for file {i+1}: {transcription}")

    print("\n\n🎉 All files processed!")

except Exception as e:
    print(f"\n❌ An error occurred: {e}")
    print("This may be due to a network issue or a problem with the model download.")