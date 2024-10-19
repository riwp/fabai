#!/bin/bash

# Send a POST request to the Flask API endpoint
curl -X POST http://127.0.0.1:5006/get_ai_insights \
-H "Content-Type: application/json" \
-d '{
    "function": "aivideo",
    "operationtype": "summary",
    "url": "https://youtu.be/VC6QCEXERpU?si=T9C-B2nomRZ2yvCS"
}'