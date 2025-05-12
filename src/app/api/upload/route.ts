import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json({ error: 'No file uploaded' }, { status: 400 });
    }

    // Check MIME type to ensure it's an image
    if (!file.type.startsWith('image/')) {
      return NextResponse.json({ error: 'Uploaded file is not an image' }, { status: 400 });
    }

    // Create a new FormData to forward to the FastAPI backend
    const backendFormData = new FormData();
    backendFormData.append('file', file);

    // Forward the request to FastAPI backend
    const backendResponse = await fetch('http://localhost:8000/detect-plate', {
      method: 'POST',
      body: backendFormData,
    });

    if (!backendResponse.ok) {
      const errorData = await backendResponse.json();
      return NextResponse.json({ error: errorData.detail || 'Backend processing failed' }, { status: backendResponse.status });
    }

    // Return the response from FastAPI
    const data = await backendResponse.json();
    return NextResponse.json(data);
    
  } catch (error) {
    console.error('Error processing image:', error);
    return NextResponse.json({ error: 'Failed to process image' }, { status: 500 });
  }
} 