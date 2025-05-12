# Number Plate Detector API

A FastAPI backend that provides an API for detecting number plates in car images using OpenAI's GPT-4o Mini.

## Prerequisites

- Python 3.9+
- OpenAI API key

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the API

Start the FastAPI server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### `GET /`

Returns a simple message confirming the API is running.

### `POST /detect-plate`

Detects number plates in car images.

**Request:**
- Content-Type: multipart/form-data
- Body: form field "file" containing an image file

**Response:**
```json
{
  "success": true,
  "imageUrl": "data:image/jpeg;base64,...",
  "message": "Number plate detected successfully.",
  "numberPlate": "ABC123"
}
```

## Integration with Next.js

This API is designed to work with the Number Plate Detector Next.js frontend. The frontend sends images to this API, which processes them and returns the detection results.

## Troubleshooting

If you encounter any issues, please check the [Troubleshooting Guide](./TROUBLESHOOTING.md) for common problems and their solutions. 