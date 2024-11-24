import logging
import os  # Ensure os is imported
import subprocess
from flask import Flask, request, jsonify
from api.fabai_common import *  # Importing custom modules or configurations

app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

#calls fabric for insights
def get_fabric_insights_from_text(function, operation_type, base_filename, text_content):

    logger.log_info(f"Received request: operation_type={operation_type}, text_content={text_content}")

    if not operation_type or not text_content:
        raise ValueError("error: operation_type and text_content are required")
    
    # Validate operation type and get corresponding fabric pattern
    if operation_type not in operation_mapping:
        raise ValueError({"error": f"Invalid operationtype. Supported types: {', '.join(operation_mapping.keys())}"})

    #map the short pattern name to the actual parameter
    fabric_pattern = operation_mapping[operation_type]
    logger.log_info(f"Using fabric pattern: {fabric_pattern}")

    #make sure there is content and log for debugging purposes
    transcript_length = len(text_content)
    logger.log_info(f"Transcript length: {transcript_length} characters")

    #handle error when no content recieved
    if transcript_length == 0:
        logger.log_exception("No subtitles received.")
        raise ValueError("error: No subtitles received")

    #logger.log_info(f"Subtitles content: {text_content[:500]}...")  # Log first 500 characters of the subtitle

    # Prepare output filename
    filename_without_extension = os.path.splitext(base_filename)[0]

    #store the file name    
    output_file_name = ""
    
    #add video to the name if video
    if function == 'aivideo':
        output_file_name = os.path.join(OUTPUT_DIR_VIDEO, f"video_{operation_type}_{filename_without_extension}.txt")

    #add web to the name if video
    elif function == 'aiweb':  # Change `function` to `function`
        output_file_name = os.path.join(OUTPUT_DIR_WEB, f"video_{operation_type}_{filename_without_extension}.txt")
    
    #add web to the name if video
    elif function == 'textInput':  
        output_file_name = os.path.join(OUTPUT_DIR_TEXT, f"text_{operation_type}_{filename_without_extension}.txt")

    else:
        return jsonify({"error": f"invalid function {function}"}), 500
   
    # Prepare fabric command
    fabric_command = [
        "fabric", "--pattern", fabric_pattern
    ]

    # Log the command being executed
    logger.log_info(f"Executing command: {' '.join(fabric_command)}")

    try:
        # Run fabric command and capture stdout and stderr
        result = subprocess.run(fabric_command, input=text_content, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            logger.log_exception(f"Fabric command failed: {error_message}")
            raise ValueError({"error": f"Fabric command failed: {error_message}"})

        # Write the output to the file
        with open(output_file_name, 'w') as output_file:
            output_file.write(result.stdout)
    except Exception as e:
        logger.log_exception(f"Error running fabric command: {e}")
        raise ValueError({"error": "Error executing fabric command"})  # Fix the syntax error here

    # Check if the output file contains data
    if os.path.getsize(output_file_name) == 0:
        logger.log_exception("Fabric command completed but the output file is empty.")
        raise ValueError("error: Output file is empty")

    # Read and return the contents of the output file
    try:
        with open(output_file_name, 'r') as output_file:
            output_content = output_file.read()
    except Exception as e:
        logger.log_exception(f"Error reading output file: {e}")
        raise ValueError("error: Error reading output file")

    logger.log_info(f"Output content: {output_content[:500]}...")  # Log first 500 characters of the output


    payload = {
    'filename': output_file_name,
    'output': output_content
    }

    return jsonify(payload)

#add entry point that can be called via CURL to test in isolation
@app.route('/test_get_webpage_as_text', methods=['POST'])
def test_get_fabric_insights_from_text():
    
    
    
    function = request.json.get('function')
    operation_type = request.json.get('operation_type')
    operation_type = request.json.get('operation_type')
    base_filename = request.json.get('base_filename')
    text_content = request.json.get('text_content')
    return get_fabric_insights_from_text(function, operation_type, base_filename, text_content)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=PORT_NUMBER)
