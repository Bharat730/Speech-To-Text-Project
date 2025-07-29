### **Script Name: `STTAudacityAYAI.py`**

This script is designed to process a folder of local audio files. For each file, it performs Hindi transcription with speaker diarization using the AssemblyAI API, translates each segment of dialogue to English, and saves a detailed, formatted transcript.

-----

### \#\# 1. Libraries and Installation

This script uses several external Python libraries. You can install them by running the following commands in your terminal:

```powershell
pip install assemblyai
pip install deep-translator
```

#### **What Each Library Does:**

  * **`os`:** A built-in Python library for interacting with the operating system.
  * **`assemblyai`:** The official Python library for the AssemblyAI API. It handles uploading the audio files and retrieving the transcription with speaker labels.
  * **`pathlib`:** A modern, built-in Python library used to handle file and folder paths, making the code cleaner and more reliable across different operating systems.
  * **`deep_translator`:** A flexible library that connects to various online translation services. This script uses its `GoogleTranslator` to translate the Hindi transcript into English.

-----

### \#\# 2. Code Explanation

  * **Lines 1-6: Imports**

      * Imports the necessary libraries listed above.

  * **Lines 8-14: Configuration**

      * `aai.settings.api_key`: **(CRITICAL)** You must replace the placeholder with your actual AssemblyAI API key.
      * `AUDIO_DIR`: Defines the name of the folder where the script will look for your source MP3 files (`Audacity_audio`).
      * `TRANSCRIPTS_DIR`: Sets the name of the folder where the final text transcripts will be saved (`Audacity_transcripts`).

  * **Lines 16-24: Setup and API Key Check**

      * The script creates the audio and transcript folders if they don't already exist.
      * It checks if you have replaced the placeholder API key and will exit with an error if you haven't.

  * **Lines 26-32: Find Audio Files**

      * This block scans the `Audacity_audio` folder and creates a list of all files that end with the `.mp3` extension.
      * If no files are found, it prints a message and exits.

  * **Lines 35-36: Initialize Transcriber**

      * Creates a single `Transcriber` object from the AssemblyAI library that will be used to process all the audio files.

  * **Lines 39-86: Main Processing Loop**

      * The script loops through each MP3 file found in the `AUDIO_DIR`.
      * **Lines 46-50:** A configuration is created to tell AssemblyAI to enable speaker diarization (`speaker_labels=True`) and to process the audio as Hindi (`language_code="hi"`).
      * **Line 51:** The local audio file is submitted to AssemblyAI for transcription. The script waits here until the process is complete.
      * **Lines 53-60:** It checks if the transcription was successful or if no speech was detected. If either is true, it skips to the next file.
      * **Lines 63-82:** This is the core formatting and translation loop. It processes the results one speaker segment ("utterance") at a time.
          * It assigns a number ("Speaker 1", "Speaker 2") to each unique speaker.
          * It takes the Hindi text for that speaker's segment.
          * It calls `GoogleTranslator` to translate that specific segment into English.
          * It formats the output with clear labels for "Hindi" and "English".
      * **Lines 85-86:** The fully formatted, bilingual, and diarized transcript is saved to a new `.txt` file in the `Audacity_transcripts` folder.

-----

### \#\# 3. Input Audio Source

  * **Folder:** This script reads local audio files from a folder named **`Audacity_audio`**.
  * **Format:** It is specifically configured to look for `.mp3` files.

-----

### \#\# 4. Output Transcripts

  * **Folder:** The script creates and saves all transcripts in a folder named **`Audacity_transcripts`**.
  * **File Format:** Each transcript is saved as a separate `.txt` file, using the original audio's name (e.g., `my-audio-file_transcript.txt`).
  * **Content:** Each file contains the full conversation, separated by speaker. For each speaker's turn, both the original Hindi transcription and the English translation are provided.