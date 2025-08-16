import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const audioFile = formData.get('audio_file') as File;
    
    if (!audioFile) {
      return NextResponse.json(
        { error: 'No audio file provided' },
        { status: 400 }
      );
    }

    console.log('Frontend received audio file:', {
      name: audioFile.name,
      size: audioFile.size,
      type: audioFile.type
    });
    
    // Forward the audio file to the FastAPI backend
    const backendUrl = 'http://127.0.0.1:8000';
    const backendFormData = new FormData();
    backendFormData.append('audio_file', audioFile);
    
    console.log('Forwarding to backend URL:', `${backendUrl}/speech-to-text`);
    const response = await fetch(`${backendUrl}/speech-to-text`, {
      method: 'POST',
      body: backendFormData,
    });

    if (!response.ok) {
      console.error(`Backend responded with status: ${response.status}`);
      const errorText = await response.text();
      console.error('Backend error response:', errorText);
      throw new Error(`Backend responded with status: ${response.status}, body: ${errorText}`);
    }

    const data = await response.json();
    console.log('Backend speech-to-text response:', data);
    
    return NextResponse.json({
      text: data.text,
      filename: data.filename,
      content_type: data.content_type,
      size_bytes: data.size_bytes
    });
  } catch (error) {
    console.error('Error in speech-to-text API route:', error);
    
    if (error instanceof Error) {
      return NextResponse.json(
        { error: `Frontend API error: ${error.message}` },
        { status: 500 }
      );
    }
    
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
