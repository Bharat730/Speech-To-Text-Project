# Speech-to-Text Transcription Project

This repository contains a collection of Python scripts demonstrating various methods for Speech-to-Text (STT) transcription, translation, and speaker diarization. The project explores different models and services, including OpenAI's Whisper, AssemblyAI's API, and Google's Gemini API.

---

## Features

-   **Multi-Engine Transcription:** Scripts for both local processing (Whisper) and cloud-based APIs (AssemblyAI, Gemini).
-   **Speaker Diarization:** Identify and label different speakers in an audio file.
-   **Multilingual Transcription:** Transcribe audio in different languages (e.g., Hindi, German).
-   **Translation:** Translate transcribed text into English.
-   **Multiple Audio Sources:** Process audio from local files, URLs from an Excel sheet, or sample datasets from the Hugging Face Hub.

---

## Project Structure

The project is organized into the following folders. **Note:** The `.gitignore` file is configured to exclude all audio and transcript folders, so you will only see the script and documentation files on GitHub.

---

## Scripts Overview

This project contains several scripts, each designed for a specific transcription task. Detailed documentation for each script can be found in the corresponding `*_Documentation.txt` or `*Readme.txt` files.

-   **`STTAssembly_af.py`**: Downloads audio from URLs in `voicesamples.xlsx` and uses the AssemblyAI API for Hindi transcription and translation.
-   **`STTAudacityAYAI.py`**: Processes local audio files from the `Audacity_audio` folder using the AssemblyAI API for diarization and translation.
-   **`GeminiCLI.py`**: Uses the powerful Google Gemini 1.5 Pro API for advanced transcription, diarization, and translation of local audio files.
-   **`STTHindiDataset.py`**: Uses OpenAI's Whisper model to transcribe and translate Hindi audio samples from a Hugging Face dataset.
-   **`STTGermanDataset.py`**: A demonstration script for Whisper's multilingual transcription and translation capabilities using German audio samples.
-   **`STTdummydataset.py`**: A simple test script to verify a local Whisper installation using a small, clean dummy dataset.

---

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/Speech-To-Text-Project.git](https://github.com/your-username/Speech-To-Text-Project.git)
    cd Speech-To-Text-Project
    ```

2.  **Install Python:** This project was developed using Python 3.10. It is recommended to use this version to avoid dependency issues.

3.  **Install Libraries:** Install all necessary Python packages by running:
    ```powershell
    pip install -r requirements.txt
    ```
    *(Note: You will need to create the `requirements.txt` file. See below.)*

---

## Usage

1.  **Add API Keys:** Open the relevant scripts (`STTAssembly_af.py`, `GeminiCLI.py`, etc.) and paste your secret API keys in the designated placeholder variables. **Do not commit your API keys to GitHub.**
2.  **Place Audio Files:** For scripts that use local audio, place your `.wav` or `.mp3` files in the correct input folder (e.g., `Audacity_audio` for the `STTAudacityAYAI.py` script).
3.  **Run the Scripts:** Execute the desired Python script from your terminal. For example:
    ```powershell
    python GeminiCLI.py
    ```
    The script will create the necessary output folders and save the transcripts as `.txt` files.