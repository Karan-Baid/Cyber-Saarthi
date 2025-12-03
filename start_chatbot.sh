#!/bin/bash

# Cyber Saarthi - Startup Script
# This script activates the environment and launches the chatbot

echo "🛡️  Starting Cyber Saarthi..."
echo ""

# Activate virtual environment
source saarthi_env/bin/activate

# Check if environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Environment activated: saarthi_env"
echo ""

# Launch Streamlit chatbot
echo "🚀 Launching Cyber Saarthi chatbot..."
echo "📱 Browser will open at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run cyber_saarthi/chatbot_app.py
