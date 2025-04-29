import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

export async function POST(request: Request) {
  const { question, chatHistory } = await request.json();
  const scriptPath = path.join(process.cwd(), 'algorithms.py');

  return new Promise<NextResponse>((resolve) => {
    const py = spawn('python', [scriptPath]);

    let out = '';
    let err = '';

    py.stdout.on('data', (d) => (out += d.toString()));
    py.stderr.on('data', (d) => (err += d.toString()));

    py.on('close', (code) => {
      if (code !== 0) {
        resolve(NextResponse.json({ error: err.trim() }, { status: 500 }));
      } else {
        try {
          const parsed = JSON.parse(out.trim());
          resolve(NextResponse.json({ answer: parsed }));
        } catch (e) {
          resolve(NextResponse.json({ answer: out.trim() }));
        }
      }
    });

    const inputData = JSON.stringify({
      question,
      chatHistory: chatHistory || [],
    });

    py.stdin.write(inputData + '\n');
    py.stdin.end();
  });
}
