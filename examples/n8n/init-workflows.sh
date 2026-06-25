#!/bin/sh

if [ -n "$GOOGLE_API_KEY" ]; then
  cat > /tmp/cred.json <<CRED_EOF
[
  {
    "id": "1",
    "name": "Google Gemini API Key",
    "type": "googlePalmApi",
    "data": {
      "host": "https://generativelanguage.googleapis.com",
      "apiKey": "$GOOGLE_API_KEY"
    }
  }
]
CRED_EOF
  n8n import:credentials --input=/tmp/cred.json 2>/dev/null && \
    echo "Gemini credential imported." || \
    echo "WARNING: Could not import credential."
  rm -f /tmp/cred.json
else
  echo "WARNING: GOOGLE_API_KEY not set. Credential not created."
fi

n8n import:workflow --input=/home/node/workflows/workflow_triaje.json
n8n publish:workflow --id=triaje-siniestros
echo "Batch workflow imported and published."

n8n import:workflow --input=/home/node/workflows/workflow_triaje_chat.json
n8n publish:workflow --id=triaje-siniestros-chat
echo "Chat workflow imported and published."

exec n8n start
