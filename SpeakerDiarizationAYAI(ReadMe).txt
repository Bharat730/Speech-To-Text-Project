### **Script Name: `SpeakerDiarizationAYAI.py`**

This script uses the AssemblyAI API to perform speaker diarization on a sample audio file. It downloads the audio, transcribes the speech, identifies the different speakers, and saves the formatted, speaker-separated transcript to a text file.

-----

### \#\# 1. Libraries and Installation

This script uses several external Python libraries. You can install them by running the following commands in your terminal:

```powershell
pip install assemblyai
pip install requests
```

#### **What Each Library Does:**

  * **`assemblyai`:** This is the official Python library (SDK) provided by AssemblyAI. It simplifies the process of interacting with their API, handling file uploads, transcription requests, and retrieving results.
  * **`pathlib`:** A modern, built-in Python library for handling file and folder paths in an object-oriented way. It makes code cleaner and more reliable across different operating systems (like Windows and Linux).
  * **`requests`:** A popular and simple library for making HTTP requests. This script uses it to download the sample audio file from a URL on the internet.

-----

### \#\# 2. Code Explanation

  * **Lines 1-3: Imports**

      * Imports the necessary libraries listed above.

  * **Lines 6-13: Configuration & Setup**

      * `aai.settings.api_key`: **(CRITICAL)** This is where you must paste your secret API key from your AssemblyAI dashboard.
      * `output_directory` / `output_path`: Defines the folder (`Diarization transcripts`) and filename (`full_transcript.txt`) for the final output.
      * `audio_url` / `local_audio_path`: Specifies the web address of the sample audio and the name it will be saved as locally (`two_speaker_test.wav`).

  * **Lines 15-26: Audio File Handling**

      * This block first checks if `two_speaker_test.wav` already exists in the project folder.
      * If the file is not found, it uses the `requests` library to download it from the `audio_url`.

  * **Lines 29-41: Transcription Request**

      * It first checks that you have replaced the placeholder API key.
      * `config = aai.TranscriptionConfig(speaker_labels=True)`: This is the key line that tells the AssemblyAI API to enable speaker diarization.
      * `transcriber = aai.Transcriber()`: Creates the main object used to interact with the API.
      * `transcript = transcriber.transcribe(...)`: This line uploads your local audio file and starts the transcription job. The script will wait here until the job is complete.

  * **Lines 43-73: Processing and Saving the Transcript**

      * The script first checks if the transcription was successful.
      * It then loops through the `transcript.utterances`. An "utterance" is a segment of speech from a single speaker.
      * **Lines 52-55:** This logic assigns a number (Speaker 1, Speaker 2, etc.) to each unique speaker letter (A, B, etc.) that the API returns.
      * **Lines 57-60:** It formats each line of dialogue with the correct speaker number.
      * **Lines 63-65:** It joins all the formatted lines together and writes them to the `full_transcript.txt` file.
      * **Lines 68-71:** For convenience, it also prints the final result to the terminal.

-----

### \#\# 3. Input Audio Source

  * **Source:** The script uses a local audio file named **`two_speaker_test.wav`**.
  * **Automatic Download:** If this file is not found in your project folder, the script will automatically download it from a sample URL on GitHub.

-----

### \#\# 4. Output Transcripts

  * **Folder:** The script creates and saves the transcript in a folder named **`Diarization transcripts`**.
  * **File Format:** The transcript is saved as a single `.txt` file named **`full_transcript.txt`**.
  * **Content:** The file contains the full conversation, with each line of dialogue labeled by "Speaker 1," "Speaker 2," etc.