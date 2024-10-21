#!/bin/bash

# Define the URL for the API
URL="http://localhost:5006/test_ai_insights"

# Define the JSON payload
DATA=$(cat <<EOF
{
  "function": "aivideo",
  "operationtype": "video_summary",
  "url": "http://example.com/video.mp4",
  "text_input": "Some text input",
  "filename": "video_summary.txt"
}
EOF
)

# Make the POST request
curl -X POST $URL \
     -H "Content-Type: application/json" \
     -d "$DATA"

echo -e "\nRequest sent to $URL"
