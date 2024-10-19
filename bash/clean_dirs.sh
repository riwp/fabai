#!/bin/bash

# Define the directories and files to be deleted
LOG_FILE="../api/fabai_api.log"
TEXT_DIR="../out/text/*"
VIDEO_DIR="../out/video/*"
WEB_DIR="../out/web/*"

# Delete the log file if it exists
if [ -f "$LOG_FILE" ]; then
    rm "$LOG_FILE"
    echo "Deleted: $LOG_FILE"
else
    echo "Log file not found: $LOG_FILE"
fi

# Delete all files in the text, video, and web directories
rm -rf $TEXT_DIR
echo "Deleted all files in: ../out/text/"

rm -rf $VIDEO_DIR
echo "Deleted all files in: ../out/video/"

rm -rf $WEB_DIR
echo "Deleted all files in: ../out/web/"
