from flask import Flask, request, jsonify
import logging
import os, sys
import subprocess
import common.fabai_common_variables

#allow toggle on/off debugging from IDE
DEBUG_CODE = False
#common.fabai_common_variables.DEBUG_CODE_VALUE

if DEBUG_CODE: 
    DEBUG_PORT = common.fabai_common_variables.DEBUG_PORT_GETINSIGHTS_VALUE
    import debugpy
    # Listen for the VS Code debugger to attach on port 5678
    debugpy.listen(("0.0.0.0", DEBUG_PORT))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()  # Pause execution until the debugger is attached

#port number for API to run on
API_PORT_NUMBER = 5006

app = Flask(__name__)

# Declare static variables

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

#location to write logs to
LOG_PATH = os.path.join(current_directory, 'fabai_api.log')

#location for output of web content
OUTPUT_DIR_WEB = os.path.join(current_directory, '..', 'out', 'web')
os.makedirs(OUTPUT_DIR_WEB, exist_ok=True)

#location for output of video content
OUTPUT_DIR_VIDEO = os.path.join(current_directory, '..', 'out', 'video')
os.makedirs(OUTPUT_DIR_VIDEO, exist_ok=True)

#location for output of video content
OUTPUT_DIR_TEXT = os.path.join(current_directory, '..', 'out', 'text')
os.makedirs(OUTPUT_DIR_TEXT, exist_ok=True)


#location for static content when in debug mode to avoid hitting AI server
DEBUG_STATIC_VIDEO_FILE = os.path.join(current_directory, '..', 'static', 'fabai_video_static_response.txt')

# Setup logging to log to a file
logging.basicConfig(
    filename=os.path.expanduser(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# set up key/value pair to allow short hand for fabric ai patterns
operation_mapping = {
    "claims": "analyze_claims",
    "keynote": "create_keynote",
    "msummary": "create_micro_summary",
    "summary": "create_summary",
    "essay": "write_micro_essay",
    "wisdom": "extract_wisdom"
}
