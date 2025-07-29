import whisper

# This line tells Whisper to download and load the 'medium' model.
# Subsequent runs will load it instantly from the cache.
model = whisper.load_model("medium")

print("Whisper 'medium' model loaded successfully.")

# You can now use the 'model' object to transcribe audio.
# For example:
# result = model.transcribe("audio.mp3")
# print(result["text"])