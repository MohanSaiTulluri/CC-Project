# Backend Deployment Instructions

This document provides instructions for deploying the backend API with proper CORS configuration to allow requests from your frontend application.

## CORS Configuration

The main issue you're experiencing is a CORS (Cross-Origin Resource Sharing) error. This happens because your backend server is not configured to accept requests from your frontend domain.

### How to Fix CORS Issues

1. Make sure your backend has the FastAPI CORS middleware configured with your frontend domain:

```python
from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:3003",
    "https://cc-project-frontend-107894419251.us-central1.run.app",
    # Add any other domains that need to access this API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Ensure this middleware is added to your FastAPI application before any routes are defined.

## Environment Variables

Create a `.env` file in the root of your backend project with the following variables:

```
OPENAI_API_KEY=your_openai_api_key_here
PORT=8002
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Deployment Steps

1. Clone the repository:
   ```bash
   git clone your-repo-url
   cd number-plate-detector-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create your `.env` file with your OpenAI API key.

5. Run the application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8002
   ```

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t number-plate-detector-api .
   ```

2. Run the container:
   ```bash
   docker run -p 8002:8002 --env-file .env number-plate-detector-api
   ```

## Google Cloud Run Deployment

For Google Cloud Run, make sure to:

1. Use the Dockerfile in this repository
2. Set the OpenAI API key as an environment variable in the Cloud Run configuration
3. Allow unauthenticated invocations if you want the API to be publicly accessible
4. Set the container port to 8002 or use the PORT environment variable

## Troubleshooting

If you're still experiencing CORS issues:

1. Check the network tab in your browser's developer tools to see the exact CORS error
2. Verify that your frontend is making requests to the correct backend URL
3. Make sure your backend is correctly deployed and the CORS middleware is working
4. Try testing with a tool like cURL or Postman to isolate browser-specific issues

Remember that CORS is enforced by the browser, so server-to-server requests won't have CORS restrictions. 