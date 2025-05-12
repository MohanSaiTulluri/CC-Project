#!/bin/bash

echo "Number Plate Detector Setup Script"
echo "=================================="
echo

# Check if OpenAI API key is provided as an argument
if [ "$1" ]; then
  API_KEY=$1
else
  # Prompt for OpenAI API key
  echo "Please enter your OpenAI API key:"
  read -s API_KEY
  echo
fi

# Validate API key format
if [[ ! $API_KEY =~ ^sk- ]]; then
  echo "Warning: The API key you provided doesn't start with 'sk-'. This might not be a valid OpenAI API key."
  echo "Do you want to continue? (y/n)"
  read CONTINUE
  if [[ ! $CONTINUE =~ ^[Yy] ]]; then
    echo "Setup aborted."
    exit 1
  fi
fi

# Create .env file
echo "Creating .env file for backend..."
echo "OPENAI_API_KEY=$API_KEY" > number-plate-detector-api/.env
echo "Backend .env file created successfully."

# Export for current session
export OPENAI_API_KEY=$API_KEY
echo "OpenAI API key exported to current shell session."

echo
echo "Setup completed successfully!"
echo
echo "Next steps:"
echo "1. Start the application:"
echo "   docker-compose down && docker-compose up -d"
echo
echo "2. Access the application in your browser:"
echo "   http://localhost:3003"
echo
echo "3. To verify everything is working:"
echo "   docker logs cc-project-backend-1"
echo "   docker logs cc-project-frontend-1"
echo
echo "4. If you encounter any issues, please check:"
echo "   - The troubleshooting section in the README.md"
echo "   - The TROUBLESHOOTING.md file in the number-plate-detector-api folder"
echo 