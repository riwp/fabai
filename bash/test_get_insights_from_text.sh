#!/bin/bash

# Define the URL
URL="http://127.0.0.1:5000/test_get_webpage_as_text"

# Define the JSON payload
JSON_PAYLOAD=$(cat <<EOF
{
  "function": "textInput",
  "operation_type": "summary",
  "base_filename": "test_get_webpage_as_text",
  "text_content": "This is a test content."
}
EOF
)

# Make the POST request using curl
curl -X POST $URL \
     -H "Content-Type: application/json" \
     -d "$JSON_PAYLOAD"

# Print a message to indicate the test is done
echo "Test completed."
