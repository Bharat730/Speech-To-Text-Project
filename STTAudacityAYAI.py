import os
import assemblyai as aai
from pathlib import Path
from deep_translator import GoogleTranslator

# ========== CONFIG ==========
# --- PASTE YOUR ASSEMBLYAI API KEY HERE ---
aai.settings.api_key = "23bd7dac28bc40bbb8e1281cd990aa68"

# Folder where you will put your MP3 files
AUDIO_DIR = Path("Audacity_audio")
# Folder where the transcripts will be saved
TRANSCRIPTS_DIR = Path("Audacity_transcripts")
# ============================

# Make sure folders exist
AUDIO_DIR.mkdir(exist_ok=True)
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

# Check for API key
if not aai.settings.api_key or "YOUR_ASSEMBLYAI_API_KEY" in aai.settings.api_key:
    print("❌ Error: Please replace 'YOUR_ASSEMBLYAI_API_KEY' with your key from AssemblyAI.")
    exit()

# Find all MP3 files in the audio directory
audio_files = list(AUDIO_DIR.glob("*.mp3"))


if not audio_files:
    print(f"No .mp3 files found in '{AUDIO_DIR}'. Please add your files to this folder.")
    exit()

# Create a transcriber object
transcriber = aai.Transcriber()

# Loop through each local audio file
for audio_path in audio_files:
    try:
        print(f"\n🔊 Processing File: {audio_path.name}...")

        # Step 1: Transcribe and Diarize using AssemblyAI
        print(f"🎤 Uploading '{audio_path.name}' for transcription...")
        config = aai.TranscriptionConfig(
            speaker_labels=True,  # Enable speaker diarization
            language_code="hi"    # Transcribe to Hindi
        )
        transcript = transcriber.transcribe(str(audio_path), config=config)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"❌ Transcription failed for {audio_path.name}: {transcript.error}")
            continue

        if not transcript.utterances:
            print(f"⚠️ No speech detected in {audio_path.name}. Skipping.")
            continue
            
        # Step 2: Format transcript, translate each part, and save
        output_path = TRANSCRIPTS_DIR / f"{audio_path.stem}_transcript.txt"
        print(f"📝 Translating and saving transcript to {output_path}...")
        
        speaker_map = {}
        current_speaker_number = 1
        final_transcript_lines = []

        for utterance in transcript.utterances:
            # Assign "Speaker 1", "Speaker 2", etc.
            speaker_letter = utterance.speaker
            if speaker_letter not in speaker_map:
                speaker_map[speaker_letter] = f"Speaker {current_speaker_number}"
                current_speaker_number += 1
            
            speaker_label = speaker_map[speaker_letter]
            hindi_text = utterance.text
            
            # Translate each speaker's part to English
            try:
                translated_text = GoogleTranslator(source='hi', target='en').translate(hindi_text)
            except Exception as e:
                translated_text = f"Translation failed: {e}"

            # Add the formatted lines to our list
            final_transcript_lines.append(f"{speaker_label}:")
            final_transcript_lines.append(f"  Hindi: {hindi_text}")
            final_transcript_lines.append(f"  English: {translated_text}\n")
        
        # Join all the lines together and save to the file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(final_transcript_lines))
        
        print(f"✅ File '{audio_path.name}' complete. Transcript saved.")

    except Exception as e:
        print(f"❌ An unexpected error occurred with '{audio_path.name}': {e}")

print("\n\n🎉 All files processed!")