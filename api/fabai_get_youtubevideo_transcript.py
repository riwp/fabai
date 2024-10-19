import logging
import os
from flask import Flask, request, jsonify
from api.fabai_common import *  # Ensure this module contains the necessary definitions

app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

class GetTranscriptError(Exception):
    pass

#gets youtube video transcript
def get_youtubevideo_transcript(url):
    if not url:
        app.logger.error("No URL provided in request.")
        raise GetTranscriptError("error: URL is required")

    # Temporary subtitle filename
    temp_subtitle = "tempvideo"
    temp_subtitle_path = os.path.join(OUTPUT_DIR_VIDEO, temp_subtitle + ".en.vtt")

    # yt-dlp command to download subtitles
    yt_dlp_command = [
        'yt-dlp',
        '--write-auto-sub',
        '--skip-download',
        '--sub-lang', 'en',  # Ensure this line is correct
        '--output', os.path.join(OUTPUT_DIR_VIDEO, temp_subtitle + '.%(ext)s'),  # Added extension handling
        url
    ]

    app.logger.info(f"Running command: {' '.join(yt_dlp_command)}")

    try:
        # Run the command and capture output
        result = subprocess.run(yt_dlp_command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        app.logger.error(f"yt-dlp command failed: {e}")
        app.logger.error(f"Command output: {e.output}")
        app.logger.error(f"Error message: {e.stderr}")
        raise GetTranscriptError("error: Failed to download subtitles")

    # Check if the subtitle file was created successfully
    if os.path.isfile(temp_subtitle_path):
        with open(temp_subtitle_path, 'r', encoding='utf-8') as subtitle_file:
            subtitle_content = subtitle_file.read()  # Read the content of the VTT file

        # Clean up the temporary subtitle file
        os.remove(temp_subtitle_path)

        # Return the subtitle content
        return subtitle_content

    app.logger.error("Subtitle file not created.")
    raise GetTranscriptError("error: Subtitle file not created")

#add entry point that can be called via CURL to test in isolation
@app.route('/test_get_youtubevideo_transcript', methods=['POST'])
def test_get_youtubevideo_transcript():
    url = request.json.get('url')
    try:
        transcript = get_youtubevideo_transcript(url)
        return jsonify({"output": transcript})
    except GetTranscriptError as e:
        return jsonify({"error": str(e)}), 400

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=PORT_NUMBER)