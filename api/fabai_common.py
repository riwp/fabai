from flask import Flask, request, jsonify
import logging
import os, sys
import subprocess
from common.fabai_common_variables import *

from common.Logger import Logger

#allow toggle on/off debugging from IDE
DEBUG_CODE = False
#common.fabai_common_variables.DEBUG_CODE_VALUE

if DEBUG_CODE: 
    DEBUG_PORT = DEBUG_PORT_GETINSIGHTS_VALUE
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

# set up key/value pair to allow short hand for fabric ai patterns
operation_mapping = {
    "claims": "analyze_claims",
    "keynote": "create_keynote",
    "msummary": "create_micro_summary",
    "summary": "create_summary",
    "essay": "write_micro_essay",
    "wisdom": "extract_wisdom"
}


LOG_PATH = os.path.join(API_LOG_PATH, 'api.log') 

#create a logger instance
logger = Logger(app=app, log_path=LOG_PATH, log_level=logging.DEBUG)

logger.log_info("Log initialized - Info Test")
logger.log_exception("Log initialized - exception Test")

