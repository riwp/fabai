import logging
import subprocess
from flask import Flask, request, jsonify
from api.fabai_common import *  # Importing custom modules or configurations

app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

#download html, clean it up, and return
def get_webpage_as_text(url):

    # Validate that the URL is provided
    if not url:
        raise GetWebError("error: URL is required")

    try:
        # Execute the command to get the HTML content, pipe it to html2text
        result = subprocess.run(
            f"chromium-browser --headless --disable-gpu --dump-dom '{url}' | html2text",
            shell=True,  # Need shell=True to allow piping between commands
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            app.logger.error(f"Command failed: {result.stderr.strip()}")
            raise GetWebError({"error": f"Command failed: {result.stderr.strip()}"})

        return result.stdout.strip()

    except Exception as e:
        app.logger.error(f"Error occurred: {e}")
        raise GetWebError({"error": f"An error occurred: {str(e)}"})

#add entry point that can be called via CURL to test in isolation
@app.route('/test_get_webpage_as_text', methods=['POST'])
def test_get_webpage_as_text():
    url = request.json.get('url')  # Extract URL from the request body
    return get_webpage_as_text(url)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=PORT_NUMBER)
