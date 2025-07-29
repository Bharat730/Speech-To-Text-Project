import assemblyai as aai
from pathlib import Path
import requests

# --- PASTE YOUR ASSEMBLYAI API KEY HERE ---
aai.settings.api_key = "23bd7dac28bc40bbb8e1281cd990aa68"

# --- 1. Setup paths and download the audio file ---
output_directory = Path("Diarization transcripts")
output_directory.mkdir(parents=True, exist_ok=True)
output_path = output_directory / "full_transcript.txt"

audio_url = "https://raw.githubusercontent.com/pyannote/pyannote-audio/develop/tutorials/assets/sample.wav"
local_audio_path = Path("two_speaker_test.wav")

if not local_audio_path.exists():
    print(f"⬇️ Downloading a sample conversation from {audio_url}...")
    try:
        response = requests.get(audio_url)
        response.raise_for_status()
        with open(local_audio_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ Audio file saved to: {local_audio_path}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download audio file. Error: {e}")
        exit()
else:
    print(f"✅ Using existing audio file: {local_audio_path}")


if not aai.settings.api_key or "YOUR_ASSEMBLYAI_API_KEY" in aai.settings.api_key:
    print("❌ Error: Please replace 'YOUR_ASSEMBLYAI_API_KEY' with your key from AssemblyAI.")
else:
    try:
        # --- 2. Configure and run transcription ---
        config = aai.TranscriptionConfig(speaker_labels=True)

        print(f"🎤 Uploading '{local_audio_path}' for transcription...")
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(str(local_audio_path), config=config)

        if transcript.status == aai.TranscriptStatus.error:
            print(f"❌ Transcription failed: {transcript.error}")
        else:
            # --- 3. Build the detailed transcript and save it to a file ---
            print(f"📝 Saving detailed transcript to {output_path}...")
            
            speaker_map = {}
            current_speaker_number = 1
            transcript_lines = []

            for utterance in transcript.utterances:
                # Assign a number to each new speaker
                if utterance.speaker not in speaker_map:
                    speaker_map[utterance.speaker] = current_speaker_number
                    current_speaker_number += 1
                
                speaker_number = speaker_map[utterance.speaker]
                text = utterance.text
                
                # Create the line "Speaker 1: text"
                line = f"Speaker {speaker_number}: {text}"
                transcript_lines.append(line)

            # Join all the lines together and save to the file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write("\n".join(transcript_lines))
            
            print(f"✅ Detailed transcript saved successfully.")
            
            # --- 4. Print the same content to the terminal ---
            print("\n--- Diarized Transcript ---")
            for line in transcript_lines:
                print(line)
            
            print("\n🎉 Process complete!")

    except Exception as e:
        print(f"An error occurred: {e}")