import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from dotenv import load_dotenv
import io
from openai import OpenAI
from typing import List, Optional
import base64

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the FastAPI app
app = FastAPI(title="Number Plate Detection API")

# Configure CORS
# Get allowed origins from environment variable or use defaults
cors_origins_env = os.getenv("CORS_ORIGINS", "")
default_origins = [
    "http://localhost:3000",
    "http://localhost:3003",
    "https://cc-project-frontend-107894419251.us-central1.run.app",
]

# Parse the CORS_ORIGINS environment variable
if cors_origins_env:
    origins = cors_origins_env.split(",")
    logger.info(f"Using CORS origins from environment: {origins}")
else:
    origins = default_origins
    logger.info(f"Using default CORS origins: {origins}")

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
async def root():
    """Root endpoint to check if the API is running."""
    return {"message": "Number Plate Detection API"}

@app.post("/detect-plate")
async def detect_plate(file: UploadFile = File(...)):
    """
    Detect a number plate in an uploaded image using OpenAI's vision model.
    """
    try:
        # Read the uploaded file
        contents = await file.read()
        
        # Log the request
        logger.info(f"Processing file: {file.filename}, size: {len(contents)} bytes")
        
        # Process stages for frontend tracking
        stages = [
            {"step": 1, "name": "image_received", "message": "Image received successfully", "completed": True},
            {"step": 2, "name": "processing_image", "message": "Processing image", "completed": False},
            {"step": 3, "name": "detecting_plate", "message": "Detecting number plate with AI", "completed": False},
            {"step": 4, "name": "extracting_text", "message": "Extracting text from plate", "completed": False},
            {"step": 5, "name": "completed", "message": "Process completed", "completed": False}
        ]
        
        # Convert image to base64 for OpenAI API
        base64_image = base64.b64encode(contents).decode('utf-8')
        
        # Update stage
        stages[1]["completed"] = True
        
        # Send to OpenAI Vision API for number plate detection
        try:
            # Update stage
            stages[2]["completed"] = True
            
            response = client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[
                    {"role": "system", "content": "You are a computer vision assistant that specializes in analyzing images of vehicles and extracting number plate information. Your task is to identify and extract the number plate text from the vehicle image provided."},
                    {"role": "user", "content": [
                        {"type": "text", "text": "Please look at this image of a vehicle and extract the number plate text. ONLY return the exact number plate text, nothing else. If you cannot identify a number plate, just respond with 'NO_PLATE_DETECTED'."},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                    ]}
                ],
                max_tokens=100
            )
            
            # Update stage
            stages[3]["completed"] = True
            
            # Extract the number plate text from the response
            plate_text = response.choices[0].message.content.strip()
            
            # Check if a plate was detected
            if plate_text == "NO_PLATE_DETECTED":
                # Update final stage
                stages[4]["completed"] = True
                return JSONResponse(content={
                    "success": False,
                    "plate_number": None,
                    "message": "No number plate detected in the image",
                    "stages": stages
                })
            
            # Update final stage
            stages[4]["completed"] = True
            
            # Return the successful result
            return JSONResponse(content={
                "success": True,
                "plate_number": plate_text,
                "stages": stages
            })
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing image with AI: {str(e)}")

    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing upload: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Start the server
    uvicorn.run("main:app", host="0.0.0.0", port=8002)