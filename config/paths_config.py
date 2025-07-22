import os
from utils.resource_utils import resource_path

# Specific file paths for modularity and simplicity

BASE_DIR = resource_path("artifacts")

AUDIO_DIR = os.path.join(BASE_DIR, "audio")
MODEL_DIR = os.path.join(BASE_DIR, "model")

# Audio Directory paths
UPLOAD_DIR = os.path.join(AUDIO_DIR, "uploaded")
PROCESSED_DIR = os.path.join(AUDIO_DIR, "processed")
GENERATED_DIR = os.path.join(AUDIO_DIR, "generated")


PROCESSED_VOICE_PATH = os.path.join(PROCESSED_DIR, "processed_voice.wav")
GENERATED_VOICE_PATH = os.path.join(GENERATED_DIR,"generated_voice.wav")

# Model paths
#MODEL_PATH = "artifacts/model/tts/tts_models--multilingual--multi-dataset--xtts_v2/"
MODEL_PATH = os.path.join(MODEL_DIR,"tts","tts_models--multilingual--multi-dataset--xtts_v2")
#MODEL_CONFIG_PATH = "artifacts/model/tts/tts_models--multilingual--multi-dataset--xtts_v2/config.json"
MODEL_CONFIG_PATH = os.path.join(MODEL_DIR,"tts","tts_models--multilingual--multi-dataset--xtts_v2","config.json")
# Settings
LANGUAGE = "en"