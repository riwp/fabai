from flask import Flask, render_template, request, jsonify
import requests
import logging
import os
import sys
import json

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.fabai_common_variables import *

# Code to get static text file and returns as stub for testing purposes
from common.fabai_get_static_debug_data import *

# For UI troubleshooting. Return static response as if you called fabric AI
DEBUG_STATIC_FABRIC_RESPONSE = DEBUG_STATIC_FABRIC_RESPONSE_VALUE

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Location for static content when in debug mode to avoid hitting AI server
DEBUG_STATIC_FABRIC_FILE = os.path.join(current_directory, '..', 'static', 'fabai_fabric_static_response_to_webui_for_test.txt')



# Allow toggle on/off debugging from IDE
DEBUG_CODE = DEBUG_CODE_VALUE
if DEBUG_CODE:
    DEBUG_PORT = DEBUG_PORT_AIWEBUI_VALUE
    import debugpy
    # Listen for the VS Code debugger to attach on port 5678
    debugpy.listen(("0.0.0.0", DEBUG_PORT))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()  # Pause execution until the debugger is attached

# Port number to run UI on
AIWEBUI_PORT_NUMBER = 5005

app = Flask(__name__)

# Set the log path to go up one directory and then to the log folder
LOG_PATH = os.path.join(current_directory, 'fabai_webui.log')

# Setup logging to log to a file
logging.basicConfig(
    filename=os.path.expanduser(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@app.route('/')
def index():
    #app.logger.info(f'current_directory: {current_directory}')
    app.logger.info("Rendering index.html")
   
    return render_template('index.html')


def validate_request(function, operationtype, url, text_input, filename):
    errors = []

    # Validate text input if function is "textInput"
    if function == 'textInput':
        if not text_input.strip():
            errors.append("Text input is required when 'Text Input' is selected.")

    # Validate URL input if function is "aiweb" or "aivideo"
    elif function in ['aiweb', 'aivideo']:
        if not url or not url.strip():
            errors.append("URL is required when 'AIWeb' or 'AIVideo' is selected.")

    # Validate filename if 'textInput' is selected
    if function == 'textInput' and filename:
        if not filename.strip():
            errors.append("File name is required when 'Text Input' is selected.")

    # Return the list of errors if validation fails, or None if validation passes
    if errors:
        return errors

    return None


@app.route('/submit', methods=['POST'])
def submit():
    app.logger.info("Starting submit")
    # Get form data
    data = request.json
    function = data.get('function')
    operationtype = data.get('operationtype', 'wisdom')
    url = data.get('url')
    text_input = data.get('textInput', "")
    filename = data.get('filename', "")  # Get filename from the request

    app.logger.info(f"Received data: function={function}, operationtype={operationtype}, url={url}, text_input={text_input}, filename={filename}")

    try:
        if ((DEBUG_STATIC_FABRIC_RESPONSE) or (function=='static')):
            static_data = get_static_debug_data(DEBUG_STATIC_FABRIC_FILE)
            
            payload = {
                'filename': 'static',
                'output': static_data
            }

            output_data = jsonify(payload)
            
            app.logger.info(f"Using Fabric Static data {DEBUG_STATIC_FABRIC_FILE}")
        else:
            # Validate the request
            validation_errors = validate_request(function, operationtype, url, text_input, filename)

            # If validation fails, return the error response
            if validation_errors:
                app.logger.info("Stopping user. Failed validation.")
                return jsonify({'error': 'Validation failed', 'messages': validation_errors}), 400
            
            payload = {
                'function': function,
                'operationtype': operationtype,
                'url': url,
                'text_input': text_input,
                'filename': filename  # Include filename in the payload
            }

            app.logger.info(f"Sending payload to API: {payload}")    
            
            response = requests.post(FABRIC_AI_API_URL, json=payload)
            response.raise_for_status()
            
            output_data = response.json()
            # Not required, but if you need to get specific elements
            #filename = data.get('filename', 'No filename received.')
            #output = data.get('output', 'No output received.')
            
            app.logger.info(f"API response: {output_data}")

        return output_data  # Return output as JSON

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error connecting to API: {e}")
        return jsonify({"error": f"Error connecting to API: {e}"}), 500  # Return JSON error response






@app.route('/browse', methods=['GET'])
def browse():
    """Serve the browse page with a list of files in the selected category."""
    category = request.args.get('category', 'video')  # Default to 'video' category if not provided
    file_path = common.fabai_common_variables.OUT_DIRECTORIES.get(category, common.fabai_common_variables.OUT_DIRECTORIES['video'])

    try:
        # Fetch all files in the selected category directory
        files = os.listdir(file_path)
        files_sorted = sorted(files, key=lambda x: os.path.getmtime(os.path.join(file_path, x)), reverse=True)

        message = None
    except Exception as e:
        # Log any errors while trying to read the directory
        files = []
        message = f"Error accessing files: {str(e)}"
        app.logger.error(message)
    
    # Render the browse page, passing the list of files and the selected category
    return render_template('browse.html', files=files_sorted, selected_category=category, message=message, currentfiledirectory=file_path)


@app.route('/files/<string:category>/<string:filename>/content', methods=['GET'])
def get_file_content(category, filename):
    
    OUT_DIRECTORIES = {'video','web', 'text'}
    # Check if the category is valid
    if category not in OUT_DIRECTORIES:
        return jsonify({'error': 'Invalid category'}), 400

    # Construct the file path based on the category
    file_path = OUT_DIRECTORIES[category] + filename

    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content, 200
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/submit_note', methods=['POST'])
def submit_note():
    # Get form data from the request
    file_name = request.form.get('file_name')
    note_header = request.form.get('note_header')
    note_content = request.form.get('note_content')
    tags = request.form.get('tags')  # Assuming tags are comma-separated
    related_notes = request.form.get('related_notes')  # Assuming related notes are comma-separated


    # Validate the required form fields
    if not file_name or not note_content:
        return jsonify({"status": "error", "message": "Please enter required fields."}), 400

    # Prepare the payload to be sent to the Obsidian API
    payload = {
        'file_name': file_name,
        'note_header': note_header,
        'note_content': note_content,
        'tags': tags.split(','),  # Convert tags string into a list
        'related_notes': related_notes.split(',')  # Convert related_notes string into a list
    }

    try:
        # Call the Obsidian API at /save_to_obsidian
        response = requests.post(OBSIDIAN_API_PATH, json=payload)

        # If the response from Obsidian is successful, return the success message
        if response.status_code == 201:
            return jsonify({"status": "success", "message": "Note saved successfully."}), 201

        # Handle error responses from the Obsidian API
        else:
            return jsonify({"status": "error", "message": response.json().get('message', 'Failed to save note.')}), 500

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error calling Obsidian API: {e}")
        return jsonify({"status": "error", "message": "Failed to save note due to server error."}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=AIWEBUI_PORT_NUMBER, debug=True)
