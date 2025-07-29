### **Script Name: `GeminiCLI.py`**

This is an advanced script that leverages the powerful multimodal capabilities of Google's Gemini 1.5 Pro model. It processes a folder of local audio files, uploading each one to the Gemini API. It then sends a detailed prompt instructing the model to perform transcription, speaker diarization (labeling Speaker 1, Speaker 2, etc.), and translation to English, all in a single step.
Note: This code uses actual money every time it is compiled.
-----

### \#\# 1. Libraries and Installation

This script uses the official Google AI Python library.

```powershell
pip install google-generativeai
```

#### **What Each Library Does:**

  * **`os`, `time`, `shutil`:** These are built-in Python libraries used for system interaction, such as managing folders (`shutil`), adding delays (`time`), and working with the operating system (`os`).
  * **`google.generativeai`:** This is the official Python library (SDK) from Google for interacting with the Gemini API. It handles API key configuration, file uploads, and sending prompts to the generative model.
  * **`pathlib`:** A modern, built-in Python library for handling file and folder paths in a way that works reliably across different operating systems.

-----

### \#\# 2. Code Explanation

  * **Lines 1-5: Imports**

      * Imports the necessary libraries listed above.

  * **Lines 7-13: Configuration**

      * `GOOGLE_API_KEY`: **(CRITICAL)** You must replace the placeholder with your actual API key from Google AI Studio.
      * `AUDIO_DIR`: Defines the name of the folder where the script will look for your source audio files (`GemCLI_audio`).
      * `TRANSCRIPTS_DIR`: Sets the name of the folder where the final text transcripts will be saved (`GemCLI_transcripts`).

  * **Lines 15-26: Setup**

      * `genai.configure(...)`: Configures the library with your API key.
      * The script then clears any previous transcripts by deleting and recreating the `TRANSCRIPTS_DIR` folder to ensure a clean run.
      * It checks that you have replaced the placeholder API key.

  * **Lines 28-34: Find Audio Files**

      * This block scans the `GemCLI_audio` folder and creates a list of all files with common audio extensions (`.wav`, `.mp3`, `.m4a`, `.flac`).

  * **Lines 39-40: Initialize Gemini Model**

      * `model = genai.GenerativeModel(...)`: This line initializes the powerful `gemini-1.5-pro-latest` model, making it ready to receive prompts.

  * **Lines 43-100: Main Processing Loop**

      * The script loops through each audio file it found.
      * **Lines 49-59:** This is the file upload process. The local audio file is uploaded to Google's temporary storage using `genai.upload_file()`. The `while` loop waits until the file is fully processed and ready for analysis by the model.
      * **Lines 62-75:** This is the **prompt engineering** step. A detailed, multi-line prompt is created to give the Gemini model very specific instructions: transcribe, identify speakers, translate, and format the output in a structured way.
      * **Line 77:** `model.generate_content(...)`: This is the core API call. It sends both the detailed prompt and a reference to the uploaded audio file to the Gemini model.
      * **Lines 80-82:** The raw text response from the model is saved directly into a `.txt` file in the `GemCLI_transcripts` folder.
      * **Lines 87-89:** `genai.delete_file(...)`: After processing, this line cleans up by deleting the temporary file from Google's servers.

-----

### \#\# 3. Input Audio Source

  * **Folder:** This script reads local audio files from a folder named **`GemCLI_audio`**.
  * **Format:** It is configured to look for `.wav`, `.mp3`, `.m4a`, and `.flac` files.

-----

### \#\# 4. Output Transcripts

  * **Folder:** The script creates and saves all transcripts in a folder named **`GemCLI_transcripts`**.
  * **File Format:** Each transcript is saved as a separate `.txt` file, using the original audio's name (e.g., `my-audio-file_transcript.txt`).
  * **Content:** Each file contains the full, formatted response from the Gemini model, which includes the speaker-separated dialogue with both the original language transcription and the English translation for each segment, as requested by the prompt.