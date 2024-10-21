#!/bin/bash

# Define the API endpoint
API_URL="http://localhost:5006/save_to_obsidian"

# Prepare the JSON payload
JSON_PAYLOAD='{
    "file_name": "test_note_2",
    "note_header": "Header 2",
    "note_content": "This is the content of the new note.",
    "tags": ["tag1", "tag2"],
    "tags": ["tag1", "tag2"],
    "related_notes": ["related note 1", "related note 2"]
}'

# Send the POST request using curl
curl -X POST "$API_URL" \
-H "Content-Type: application/json" \
-d "$JSON_PAYLOAD"

# Check if the curl command was successful
if [ $? -eq 0 ]; then
    echo -e "\nRequest sent successfully."
else
    echo -e "\nFailed to send the request."
fi
