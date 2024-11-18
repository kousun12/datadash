import { NextResponse } from 'next/server';


// const MODIFIER_URL = 'http://localhost:8000'
const MODIFIER_URL = 'http://127.0.0.1:8000'

async function makeRequest(args: Record<string, never>) {
  const response = await fetch(`${MODIFIER_URL}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(args),
  });
  return response.json();

}


export async function POST(request: Request) {
  try {
    const body = await request.json();
    console.log('Received message:', body);
    const response = await makeRequest(body);
    console.log('Processed message:', response);

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Error processing message:', error);
    return NextResponse.json(
      { error: 'Failed to process message' },
      { status: 500 }
    );
  }
}
