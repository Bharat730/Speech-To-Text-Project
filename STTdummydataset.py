import whisper
from datasets import load_dataset
import torch
import numpy as np
from pathlib import Path

def transcribe_dummy_dataset():
    """
    Loads a tiny dummy dataset, transcribes all its files,
    and saves each transcript to a separate .txt file.
    This is a fast and space-efficient way to test the code.
    """
    # --- 1. Setup ---
    device = "cpu"
    output_directory = Path("transcripts_dummy_test")
    output_directory.mkdir(parents=True, exist_ok=True)

    print(f"Using device: {device}")
    print(f"Transcripts will be saved to: {output_directory.resolve()}")

    # --- 2. Load Model ---
    print("🧠 Loading Whisper model 'medium'...")
    model = whisper.load_model("medium", device=device)
    print("🤖 Model loaded.")

    # --- 3. Load the Tiny Dummy Dataset ---
    # This dataset is very small (a few MB) and will download instantly.
    print("\n⬇️ Loading the dummy test dataset...")
    try:
        dataset = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
    except Exception as e:
        print(f"❌ Failed to load dataset. Error: {e}")
        return

    # --- 4. Loop, Transcribe, and Save ---
    total_files = len(dataset)
    print(f"✅ Dataset loaded. Found {total_files} audio files to transcribe.")

    for i, sample in enumerate(dataset):
        print(f"\nProcessing file {i + 1} of {total_files}...")

        audio_input = sample['audio']['array']
        reference_transcript = sample['text']

        # Convert audio to the correct format for Whisper
        audio_input = audio_input.astype(np.float32)

        # Transcribe the audio
        result = model.transcribe(audio_input)
        model_transcript = result['text']

        # Prepare the content for the text file
        file_content = (
            f"Reference: {reference_transcript}\n"
            f"----------------------------------------\n"
            f"Whisper Output: {model_transcript}"
        )

        # Save the transcript to a text file
        output_path = output_directory / f"dummy_transcript_{i}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        print(f"Saved transcript to {output_path}")

    print("\n\n🎉 Transcription of dummy dataset complete!")

if __name__ == "__main__":
    transcribe_dummy_dataset()