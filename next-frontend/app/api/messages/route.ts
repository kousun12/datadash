import { NextResponse } from 'next/server';

const MODIFIER_URL = 'http://127.0.0.1:8000';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    console.log('Received message:', body);

    const response = await fetch(MODIFIER_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    // Create a TransformStream to proxy the response
    const { readable, writable } = new TransformStream();
    
    // Pipe the response body to our transform stream
    response.body?.pipeTo(writable);

    // Return a streaming response
    return new Response(readable, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
      },
    });
  } catch (error) {
    console.error('Error processing message:', error);
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    );
  }
}
