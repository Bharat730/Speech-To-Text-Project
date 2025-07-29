### **Script Name: `STTAssembly_af.py`

This script automates the process of downloading audio files from URLs listed in an Excel sheet, transcribing the Hindi speech into text, translating that text into English, and saving the results.

-----

### \#\# 1. Libraries and Installation

This script uses several external Python libraries. You can install them all by running the following commands in your terminal:

```powershell
pip install pandas openpyxl
pip install requests
pip install assemblyai
pip install deep-translator
```
#### **What Each Library Does:**

What Each Library Does:

   * os: A built-in Python library for interacting with the operating system. It's used here to ensure the output folders exist.

   * pandas: A powerful library for data analysis. In this script, its main job is to read the data from your .xlsx Excel file.

   * requests: A simple and popular library for making HTTP requests. It is used to download the audio files from the URLs in your Excel sheet.

   * assemblyai: The official Python library for using the AssemblyAI API. It handles the process of uploading your audio files and getting the transcript back.

   * pathlib: A modern, built-in Python library that makes it easier and more reliable to work with file and folder paths across different operating systems (like Windows and Linux).

   * deep_translator: A flexible library that connects to various online translation services. This script uses its GoogleTranslator to translate the Hindi transcript into English.

-----

### \#\# 2. Code Explanation

  * **Lines 1-7: Imports**

      * Imports the necessary libraries: `os` for interacting with the operating system, `pandas` for reading the Excel file, `requests` for downloading audio, `assemblyai` for transcription, `pathlib` for handling file paths, and `GoogleTranslator` for translation.

  * **Lines 9-15: Configuration**

      * `aai.settings.api_key`: **(CRITICAL)** You must replace the placeholder with your actual AssemblyAI API key.
      * `EXCEL_FILE`: Defines the name of your Excel file (`voicesamples.xlsx`).
      * `AUDIO_DIR`: Sets the name of the folder where downloaded audio files will be saved (`audio_files`).
      * `TRANSCRIPTS_DIR`: Sets the name of the folder where the final text transcripts will be saved (`transcripts`).

  * **Lines 17-25: Setup and API Key Check**

      * The script creates the audio and transcript folders if they don't already exist.
      * It checks if you have replaced the placeholder API key and will exit with an error if you haven't.

  * **Lines 27-36: Read Excel File**

      * This block opens and reads the `voicesamples.xlsx` file using `pandas`.
      * It specifically reads the second column (`iloc[:, 1]`) to get the list of audio URLs.
      * It includes error handling in case the Excel file isn't found or can't be read.

  * **Lines 39-40: Initialize Transcriber**

      * Creates a single `Transcriber` object from the AssemblyAI library that will be used for all files.

  * **Lines 42-100: Main Processing Loop**

      * The script loops through each URL found in the Excel file.
      * **Line 50:** A unique local path is created for each audio file (e.g., `audio_1.mp3`, `audio_2.mp3`).
      * **Lines 51-54:** The `requests` library downloads the audio content from the URL.
      * **Lines 58-59:** A configuration is created to tell AssemblyAI to process the audio as Hindi (`language_code="hi"`).
      * **Line 60:** The downloaded local audio file is submitted to AssemblyAI for transcription.
      * **Lines 62-65:** It checks if the transcription was successful. If not, it prints an error and skips to the next file.
      * **Lines 67-70:** It gets the transcribed Hindi text. If no text was detected, it sets a default message.
      * **Lines 73-78:** The `GoogleTranslator` is used to translate the Hindi text into English.
      * **Lines 81-88:** The final content, containing both the Hindi transcription and the English translation, is formatted.
      * **Lines 90-93:** The formatted content is written to a new `.txt` file in the `transcripts` folder.
      * **Lines 95-98:** Catches and reports any errors that occur during the download or transcription process for a specific file.

-----

### \#\# 3. Input Audio Source

  * **Folder:** The script creates and uses a folder named **`audio_files`** to store the MP3s it downloads.
  * **Source:** The audio is sourced from URLs provided in the **second column** of the **`voicesamples.xlsx`** Excel file.

-----

### \#\# 4. Output Transcripts

  * **Folder:** The script creates and saves all transcripts in a folder named **`transcripts`**.
  * **File Format:** Each transcript is saved as a separate `.txt` file, named sequentially (e.g., `transcript_1.txt`, `transcript_2.txt`, etc.).
  * **Content:** Each file contains the Hindi transcription and the corresponding English translation.