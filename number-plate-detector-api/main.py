from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import base64
from PIL import Image
import io
import openai
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Number Plate Detection API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002", "http://localhost:3003"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def read_root():
    return {"message": "Number Plate Detection API"}

@app.post("/detect-plate")
async def detect_plate(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = await file.read()
        
        # Process image (resize if needed)
        try:
            image = Image.open(io.BytesIO(contents))
            
            # Resize if too large (optional)
            max_size = 800
            if max(image.size) > max_size:
                ratio = max_size / max(image.size)
                new_size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
                image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Convert back to bytes
            buffer = io.BytesIO()
            image.save(buffer, format=image.format or "JPEG")
            processed_image = buffer.getvalue()
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image: {str(e)}")
        
        # Convert to base64
        base64_image = base64.b64encode(processed_image).decode("utf-8")
        mime_type = file.content_type
        data_uri = f"data:{mime_type};base64,{base64_image}"
        
        # Send to OpenAI
        try:
            if not os.getenv("OPENAI_API_KEY"):
                raise HTTPException(
                    status_code=500, 
                    detail="OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable."
                )
                
            client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a computer vision expert specialized in detecting license plates from car images. Respond with ONLY the license plate number if you can see one. If no license plate is visible, respond with 'No license plate detected'. If the image is not a car, respond with 'Not a car image'."
                    },
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What's the license plate number in this image?"},
                            {"type": "image_url", "image_url": {"url": data_uri}}
                        ],
                    },
                ],
                max_tokens=100
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Prepare result
            if "not a car" in ai_response.lower():
                result = {
                    "success": True,
                    "imageUrl": data_uri,
                    "message": "The uploaded image does not appear to be a car.",
                    "numberPlate": None
                }
            elif "no license plate" in ai_response.lower() or "no licence plate" in ai_response.lower():
                result = {
                    "success": True,
                    "imageUrl": data_uri,
                    "message": "No number plate detected in the image.",
                    "numberPlate": None
                }
            else:
                result = {
                    "success": True,
                    "imageUrl": data_uri,
                    "message": "Number plate detected successfully.",
                    "numberPlate": ai_response
                }
                
            return JSONResponse(content=result)
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 