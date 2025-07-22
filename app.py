import os
import sys
from utils.custom_exception import CustomException
from utils.logger import get_logger
from config.paths_config import UPLOAD_DIR, GENERATED_DIR, PROCESSED_DIR
from flask import Flask, render_template, request, jsonify, send_from_directory
from pipelines.voice_cloner import voice_cloning_pipeline
from utils.audio_uploader import upload_audio

# Create required directories if they don't exist
for directory in [UPLOAD_DIR, PROCESSED_DIR, GENERATED_DIR]:
    os.makedirs(directory, exist_ok=True)

app = Flask(__name__, template_folder='templates/',static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_DIR

logger = get_logger(__name__)

@app.route('/', methods=['GET','POST'])
def home():
    """
    Handles requests to the home page. Get the script and voice file from the form, then use the voice cloning pipeline to generate a cloned voice and then provide a download option.
    """
    if request.method == 'POST':
        script = request.form.get('script')
        language = request.form.get('language', 'en')  # Default to English if not specified
        uploaded_voice = request.files.get('voice_file')

        if not script or not uploaded_voice:
            return jsonify({"error": "Script and voice file are required"}), 400

        try:
            # Save the uploaded voice file
            UPLOADED_AUDIO_PATH = upload_audio(uploaded_voice)

            # Run the voice cloning pipeline with the selected language
            generated_voice_path = voice_cloning_pipeline(
                script=script, 
                uploaded_voice_path=UPLOADED_AUDIO_PATH,
                language=language
            )
            
            # Convert file path to URL path for frontend
            filename = os.path.basename(generated_voice_path)
            voice_url = f"/generated/{filename}"
            
            return jsonify({
                "message": "Voice cloning successful",
                "generated_voice_path": voice_url
            }), 200

        except CustomException as ce:
            logger.error(f"Custom exception occurred: {str(ce)}")
            return jsonify({"error": str(ce)}), 500
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return jsonify({"error": "An unexpected error occurred"}), 500

    return render_template('index.html')

@app.route('/generated/<filename>')
def generated_file(filename):
    """
    Serve generated audio files from the GENERATED_DIR directory
    """
    return send_from_directory(GENERATED_DIR, filename)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=5000)
