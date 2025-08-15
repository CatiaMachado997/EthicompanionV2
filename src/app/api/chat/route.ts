import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    console.log('Frontend received request:', body);
    
    // Forward the request to the FastAPI backend
    const backendUrl = process.env.BACKEND_URL || 'http://127.0.0.1:8000';
    const response = await fetch(`${backendUrl}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      console.error(`Backend responded with status: ${response.status}`);
      const errorText = await response.text();
      console.error('Backend error response:', errorText);
      throw new Error(`Backend responded with status: ${response.status}, body: ${errorText}`);
    }

    const data = await response.json();
    console.log('Backend response:', data);
    
    return NextResponse.json({
      response: data.reply,
    });
  } catch (error) {
    console.error('Error in chat API route:', error);
    
    // Return a more specific error message
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
