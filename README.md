
# Car Number Plate Detector

A Next.js application that detects and extracts number plates from car images. The application allows users to upload images of cars and uses GPT-4o Mini computer vision to identify and extract the number plates via a FastAPI backend.

## Features

- Image upload via drag-and-drop or file selection
- Number plate detection using OpenAI's GPT-4o Mini
- FastAPI backend for image processing and AI integration
- Responsive UI with Tailwind CSS

## Prerequisites

- Node.js 18+ and npm
- Python 3.9+ (for the FastAPI backend)
- An OpenAI API key with access to GPT-4o Mini

## Project Structure

This project consists of two parts:
1. **Frontend**: A Next.js application for the user interface
2. **Backend**: A FastAPI application for processing images and communicating with OpenAI

## Frontend Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd ../number-plate-detector-api
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the backend directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## How it Works

1. The user uploads an image through the Next.js frontend
2. The image is sent to the FastAPI backend via the Next.js API route
3. The backend processes the image and sends it to OpenAI's GPT-4o Mini for number plate detection
4. The detection results are returned to the frontend and displayed to the user

## Production Deployment

### Frontend
Build the Next.js application:
```bash
npm run build
npm start
```

### Backend
Run the FastAPI application with a production ASGI server like Uvicorn or Gunicorn:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Notes

- For a production deployment, consider implementing proper authentication and authorization to secure your API endpoints.
- Ensure that your OpenAI API key is kept secure and not exposed to the client.

## Docker Setup

The application can be run using Docker and Docker Compose for easier deployment.

1. Make sure you have Docker and Docker Compose installed on your system.

2. Run the setup script to configure your OpenAI API key:
   ```bash
   ./setup.sh
   ```
   
   Alternatively, you can set your API key directly:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

4. Access the application at [http://localhost:3003](http://localhost:3003)

## Troubleshooting

If you encounter any issues, please check the following:

1. Make sure your OpenAI API key is correctly set in the `.env` file or as an environment variable.
2. Check the logs of the backend and frontend containers:
   ```bash
   docker logs cc-project-backend-1
   docker logs cc-project-frontend-1
   ```
3. Refer to the [Backend Troubleshooting Guide](./number-plate-detector-api/TROUBLESHOOTING.md) for common issues and solutions.

## License

MIT 
>>>>>>> 0069fcc (Initial commit)
