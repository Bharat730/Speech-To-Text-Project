### **Script Name: `STTGermanDataset.py`**

This script demonstrates the multilingual transcription and translation capabilities of OpenAI's Whisper model. It downloads a small sample of German audio files from the Hugging Face Hub, transcribes them into German, translates them into English, and saves the results.

-----

### \#\# 1. Libraries and Installation

This script uses several external Python libraries. You can install them all by running the following commands in your terminal:

```powershell
pip install openai-whisper
pip install datasets
pip install torch
pip install numpy
pip install soundfile librosa
```

#### **What Each Library Does:**

  * **`whisper` (`openai-whisper`):** The core library from OpenAI that contains the powerful multilingual speech recognition model. It performs both transcription (speech-to-text in the original language) and translation (speech-to-text in English).
  * **`datasets`:** A library from Hugging Face that makes it easy to download and work with thousands of datasets, including the FLEURS audio dataset used in this script.
  * **`torch` (PyTorch):** A major machine learning framework that Whisper is built on. It handles all the underlying tensor calculations and neural network operations.
  * **`numpy`:** A fundamental library for numerical computing in Python. It's used to represent and manipulate the audio data as a numerical array.
  * **`pathlib`:** A built-in Python library used to handle file and folder paths in a way that works reliably across different operating systems.
  * **`soundfile` & `librosa`:** Helper libraries for audio processing that `datasets` uses in the background to read and decode different audio file formats.

-----

### \#\# 2. Code Explanation

  * **Lines 1-5: Imports**

      * Imports the necessary libraries listed above.

  * **Lines 12-17: Setup**

      * `device = "cpu"`: Configures the script to run on the CPU.
      * `output_directory = Path(...)`: Defines the name of the folder where the final text transcripts will be saved (`multilingual_transcripts`).
      * `output_directory.mkdir(...)`: Creates this folder if it doesn't already exist.

  * **Lines 20-22: Load Whisper Model**

      * `model = whisper.load_model("medium", ...)`: This line downloads (the first time) and loads the multilingual `medium` version of the Whisper model into memory.

  * **Lines 25-30: Load Dataset**

      * This block connects to the Hugging Face Hub to download the Google FLEURS dataset.
      * `load_dataset("google/fleurs", "de_de", ...)`: This specifies that we want the German (`de_de`) portion of the dataset.
      * `split="validation[:5]"`: This efficiently loads only the first 5 audio samples from the validation set for a quick test.

  * **Lines 33-68: Main Processing Loop**

      * The script loops through each of the 5 downloaded audio samples.
      * **Line 37:** Extracts the language name string ("German") from the sample's metadata.
      * **Line 40:** Extracts the audio data and converts it into the `float32` numerical format that Whisper requires.
      * **Line 44:** The first core task. The audio data is passed to `model.transcribe()` with the language specified as "German". This tells the model to convert the speech to German text.
      * **Line 48:** The second core task. The audio data is passed to `model.transcribe()` again, but this time with `task="translate"`. This tells the model to convert the speech into English text, regardless of the source language.
      * **Lines 51-59:** Formats a string containing all the information: the language, the original correct text, the Whisper transcription in German, and the Whisper translation in English.
      * **Lines 61-64:** Saves the formatted string to a new `.txt` file in the `multilingual_transcripts` folder.

-----

### \#\# 3. Input Audio Source

  * **Source:** This script does not use a local folder. It directly downloads and uses a sample dataset from the **Hugging Face Hub**.
  * **Dataset Name:** `google/fleurs`, specifically the German (`de_de`) configuration.

-----

### \#\# 4. Output Transcripts

  * **Folder:** The script creates and saves all transcripts in a folder named **`multilingual_transcripts`**.
  * **File Format:** Each transcript is saved as a separate `.txt` file, named using its index and language ID (e.g., `multilingual_test_0_17.txt`).
  * **Content:** Each file contains the original reference text, the Whisper transcription in German, and the Whisper translation in English.