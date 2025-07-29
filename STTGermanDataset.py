import whisper
from datasets import load_dataset
import torch
import numpy as np
from pathlib import Path

def test_multilingual_tasks_efficiently():
    """
    Loads a small sample from a specific language (German) to efficiently
    test Whisper's transcription and translation capabilities.
    """
    device = "cpu"
    output_directory = Path("multilingual_transcripts")
    output_directory.mkdir(parents=True, exist_ok=True)

    print(f"Using device: {device}")
    print(f"Transcripts will be saved to: {output_directory.resolve()}")

    print("🧠 Loading Whisper model 'medium'...")
    model = whisper.load_model("medium", device=device)
    print("🤖 Model loaded.")

    print("\n⬇️ Loading 5 German samples from the FLEURS dataset...")
    try:
        dataset = load_dataset("google/fleurs", "de_de", split="validation[:5]", trust_remote_code=True)
    except Exception as e:
        print(f"❌ Failed to load dataset. Error: {e}")
        return

    total_files = len(dataset)
    print(f"✅ Dataset loaded. Found {total_files} audio files to process.")

    for i, sample in enumerate(dataset):
        # --- THE FIX IS HERE ---
        # Use 'language' to get the string name (e.g., "German") instead of 'lang_id' which is a number.
        language_code = sample['language']
        
        print(f"\nProcessing file {i + 1}: Language '{language_code}'")

        audio_input = sample['audio']['array'].astype(np.float32)
        reference_transcript = sample['transcription']

        # Task 1: Transcribe in the original language
        # We pass the full language name string (e.g., "German") to Whisper
        transcribe_result = model.transcribe(audio_input, language=language_code)
        transcription_text = transcribe_result['text']

        # Task 2: Translate to English
        translate_result = model.transcribe(audio_input, task="translate")
        translation_text = translate_result['text']

        # --- Save Results ---
        file_content = (
            f"Language: {sample['language']}\n"
            f"Reference Text: {reference_transcript}\n"
            "----------------------------------------\n"
            f"Whisper Transcription (in original language):\n{transcription_text}\n"
            "----------------------------------------\n"
            f"Whisper Translation (to English):\n{translation_text}"
        )

        output_path = output_directory / f"multilingual_test_{i}_{sample['lang_id']}.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        print(f"Saved results to {output_path}")

    print("\n\n🎉 Multilingual test complete!")

if __name__ == "__main__":
    test_multilingual_tasks_efficiently()