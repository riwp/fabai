#!/bin/bash

# Define the URL
URL="http://localhost:5006/get_ai_insights"

JSON_PAYLOAD=$(cat <<EOF
{
  "function": "aivideo", 
  "operationtype": "summary",
  "url": "https://youtu.be/7vVWFTzOt24?si=7TcZWf125rO2UY7_",
  "text_input": "",
  "filename": "test_video"
}
EOF
)

# Make the POST request using curl
curl -X POST $URL \
     -H "Content-Type: application/json" \
     -d "$JSON_PAYLOAD"

# Print a message to indicate the test is done
echo "Test completed."
