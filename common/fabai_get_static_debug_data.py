import logging, sys, os
from flask import Flask, request, jsonify

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#from api.fabai_common import *

app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

# Example static debug function
def get_static_debug_data(DEBUG_FILE_PATH):
    app.logger.info(f"get_static_debug_data - DEBUG_FILE_PATH: {DEBUG_FILE_PATH}")
    try:
        # Load the response from a plain text file
        with open(DEBUG_FILE_PATH, 'r') as file:
            response = file.read()  # Read file as plain text
        return response
        
    except FileNotFoundError:
        raise GetStaticContentError("error: Stub file not found")
    except Exception as e:
        app.logger.error(f"Error reading the stub file: {e}")
        raise GetStaticContentError("error: Error reading the stub file")

#add entry point that can be called via CURL to test in isolation
@app.route('/test_get_static_debug_data', methods=['POST'])
def test_get_static_debug_data():
    return get_static_debug_data()

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=PORT_NUMBER)
