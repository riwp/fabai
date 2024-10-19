from flask import Flask, render_template, request, jsonify
import requests
import logging
import os
import sys
import json

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import common.fabai_common_variables

# Code to get static text file and returns as stub for testing purposes
from common.fabai_get_static_debug_data import *

# For UI troubleshooting. Return static response as if you called fabric AI
DEBUG_STATIC_FABRIC_RESPONSE = common.fabai_common_variables.DEBUG_STATIC_FABRIC_RESPONSE_VALUE

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Location for static content when in debug mode to avoid hitting AI server
DEBUG_STATIC_FABRIC_FILE = os.path.join(current_directory, '..', 'static', 'fabai_fabric_static_response_to_webui_for_test.txt')



# Allow toggle on/off debugging from IDE
DEBUG_CODE = common.fabai_common_variables.DEBUG_CODE_VALUE
if DEBUG_CODE:
    DEBUG_PORT = common.fabai_common_variables.DEBUG_PORT_AIWEBUI_VALUE
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

# URL for the new api_fabricAI service
FABRIC_AI_API_URL = "http://localhost:5006/get_ai_insights"

# Path to store metadata (you can choose where to store the descriptions)
METADATA_FILE = common.fabai_common_variables.OUT_FILES_METADATA

@app.route('/')
def index():
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
        if DEBUG_STATIC_FABRIC_RESPONSE:
            output_data = get_static_debug_data(DEBUG_STATIC_FABRIC_FILE)
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


@app.route('/files/<string:filename>/description', methods=['GET'])
def get_description(filename):
    """Fetch the description for a given file."""
    description_file_path = common.fabai_common_variables.OUT_FILES_METADATA

    try:
        # Attempt to open the description file and load the descriptions as a dictionary
        with open(description_file_path, 'r') as f:
            descriptions = json.load(f)
        
        # Find the description that matches the filename
        matched_description = descriptions.get(filename, {}).get('description', 'No description available.')
        
        # Return the description to the client
        return jsonify({"description": matched_description}), 200

    except FileNotFoundError:
        # Handle the case where the metadata file does not exist
        app.logger.warning(f"Metadata file not found: {description_file_path}.")
        return jsonify({"description": "No description available. The metadata file does not exist."}), 200

    except Exception as e:
        # If any other error occurs, log it and return the error message to the client
        app.logger.error(f"Error fetching description for {filename}: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/rename', methods=['POST'])
def rename_file():
    # Get all form values
    operationtype = request.form.get('operationtype')
    function = request.form.get('function')
    textInput = request.form.get('textInput')
    url = request.form.get('url')
    result = request.form.get('result')  # This may not be necessary here, remove if unused.
    new_file_name = request.form.get('newfilename')  # Updated to capture the new filename
    current_file_name = request.form.get('currentfilename')
    current_file_directory = request.form.get('currentfiledirectory')

    app.logger.debug(f"Current file directory: {current_file_directory}")
    
    old_filepath = os.path.join(current_file_directory, current_file_name)
    new_filepath = os.path.join(current_file_directory, new_file_name)

    app.logger.debug(f"Renaming file: {old_filepath} to {new_filepath}")

    app.logger.debug(f"""operationtype: {operationtype}, 
        function: {function},
        textInput: {textInput},
        url: {url},
        new_file_name: {new_file_name},
        old_filepath: {old_filepath},
        new_filepath: {new_filepath}""")

    if os.path.exists(old_filepath):
        try:
            os.rename(old_filepath, new_filepath)
            message = f'File renamed successfully to {new_file_name}'
        except Exception as e:
            message = f'Error renaming file: {str(e)}'
            app.logger.error(message)
    else:
        message = 'Selected file does not exist.'

    # Redirect back to the index with the values preserved
    return render_template('index.html', 
                           operationtype=operationtype, 
                           function=function,
                           textInput=textInput,
                           url=url,
                           result=message,  # Change to show success/error message
                           filename=new_file_name)  # Show the new filename


@app.route('/files/<string:filename>/description', methods=['POST'])
def update_description(filename):
    """Update file description."""
    # Extract the JSON payload from the request
    category = request.json.get('category')
    description = request.json.get('description')

    # Validate inputs
    if not category or not description:
        return jsonify({"error": "Invalid input."}), 400

    try:
        # Path to the metadata file
        metadata_file_path = common.fabai_common_variables.OUT_FILES_METADATA

        # Load existing metadata if the file exists
        if os.path.exists(metadata_file_path):
            with open(metadata_file_path, 'r') as f:
                metadata = json.load(f)
        else:
            metadata = {}  # Initialize an empty dictionary if file doesn't exist

        # Update the metadata for the current file
        metadata[filename] = {"description": description}

        # Write the updated metadata back to the file
        with open(metadata_file_path, 'w') as f:
            json.dump(metadata, f, indent=4)

        # Return success message
        return jsonify({"message": "Description updated successfully."}), 200

    except Exception as e:
        app.logger.error(f"Error updating description: {str(e)}")
        return jsonify({"error": str(e)}), 500

OUT_DIRECTORIES = {
    'video': '/home/cmollo/fabai/out/video/',
    'web': '/home/cmollo/fabai/out/web/',
    'text': '/home/cmollo/fabai/out/text/'
}

@app.route('/files/<string:category>/<string:filename>/content', methods=['GET'])
def get_file_content(category, filename):
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=AIWEBUI_PORT_NUMBER, debug=True)
