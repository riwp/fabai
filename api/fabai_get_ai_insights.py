import logging, sys, os
from flask import Flask, request, jsonify
import random

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#import common variables, classes
from api.fabai_common import *

#code to get static text file and returns as stub for testing purposes
from common.fabai_get_static_debug_data import *

#code to download and clean up html and return clean text
from fabai_get_webpage_as_text import *

#code to get youtube transcripts
from fabai_get_youtubevideo_transcript import *

#code to call fabric and get insights
from fabai_get_fabric_insights_from_text import *


app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

def generate_random_unique_number(start, end):
    return random.randint(start, end)

#primary entry point into application called by web ui
@app.route('/get_ai_insights', methods=['POST'])
def get_AI_Insights():

    app.logger.info(f"DEBUG_CODE_VALUE={common.fabai_common_variables.DEBUG_CODE_VALUE}, DEBUG_STATIC_FABRIC_RESPONSE_VALUE={common.fabai_common_variables.DEBUG_STATIC_FABRIC_RESPONSE_VALUE}, DEBUG_STATIC_YOUTUBE_RESPONSE_VALUE={common.fabai_common_variables.DEBUG_STATIC_YOUTUBE_RESPONSE_VALUE}")

    data = request.json
    
    #used to determine whether to get web or video or other source content
    function = data.get('function', 'aivideo')
    
    #contains the different fabric patterns to be mapped from web ui to parameters
    operation_type = data.get('operationtype')
    
    #the target url to get the content
    url = data.get('url')
    
    text_input = data.get('text_input')
    
    filename = data.get('filename')
       
    app.logger.info(f"Received request: function={function}, operation_type={operation_type}, url={url}, text_input={text_input}")

    payload = {
        'filename': None,
        'output': None
    }

    #If Debugging is on, return static content   
    if common.fabai_common_variables.DEBUG_STATIC_YOUTUBE_RESPONSE_VALUE:
        app.logger.info(f"Returning static data")
        
        payload['filename'] = None
        payload['output'] = get_static_debug_data(DEBUG_STATIC_VIDEO_FILE)

        return jsonify(payload)
        
    #if content type is video, get the youtube transcript and then pass it to fabric
    if function == 'aivideo':
        app.logger.info(f"calling get_youtubevideo_transcript with URL: {url}")
        youtube_transcript = get_youtubevideo_transcript(url)
        fabric_response = get_fabric_insights_from_text(function, operation_type, os.path.basename(url), youtube_transcript)

        #return jsonify(payload)
        return fabric_response

    #if content type is web, get the web html, clean it up, and then pass it to fabric
    elif function == 'aiweb':
        app.logger.info(f"calling get_webpage_as_text with URL: {url}")
        web_text = get_webpage_as_text(url)
        fabric_response = get_fabric_insights_from_text(function, operation_type, os.path.basename(url), web_text)
        
        return fabric_response
    
        #if content type is web, get the web html, clean it up, and then pass it to fabric
    elif function == 'textInput':
        app.logger.info(f"calling fabric with text {text_input}")
        
        unique_number = generate_random_unique_number(1000, 9999)  # Generates a random number between 1000 and 9999
        file_name = filename + str(unique_number)
        fabric_response = get_fabric_insights_from_text(function, operation_type, file_name, text_input)
        
        return fabric_response
    
    #otherwise, not a valid type
    else:
        return jsonify({"error": "Invalid function. Supported values: 'aiweb', 'aivideo'."}), 400















#primary entry point into application called by web ui
@app.route('/test_ai_insights', methods=['POST'])
def test_AI_Insights():

    app.logger.info(f"DEBUG_CODE_VALUE={common.fabai_common_variables.DEBUG_CODE_VALUE}, DEBUG_STATIC_FABRIC_RESPONSE_VALUE={common.fabai_common_variables.DEBUG_STATIC_FABRIC_RESPONSE_VALUE}, DEBUG_STATIC_YOUTUBE_RESPONSE_VALUE={common.fabai_common_variables.DEBUG_STATIC_YOUTUBE_RESPONSE_VALUE}")

    data = request.json
    
    #used to determine whether to get web or video or other source content
    function = data.get('function', 'aivideo')
    
    #contains the different fabric patterns to be mapped from web ui to parameters
    operation_type = data.get('operationtype')
    
    #the target url to get the content
    url = data.get('url')
    
    text_input = data.get('text_input')
    
    filename = data.get('filename')
       
    app.logger.info(f"Received request (test_ai_insights): function={function}, operation_type={operation_type}, url={url}, text_input={text_input}")

    return jsonify({"output": get_static_debug_data(DEBUG_STATIC_VIDEO_FILE)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT_NUMBER, debug=True)
