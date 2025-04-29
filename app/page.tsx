'use client';

import { useEffect, useRef, useState } from 'react';
import FibonacciTree from '@/components/FibonacciTree';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [treeData, setTreeData] = useState<any>(null);
  const [chatHistory, setChatHistory] = useState<string[]>([]);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    const updatedHistory = [...chatHistory, `> ${question}`];

    try {
      const res = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, chatHistory: updatedHistory }),
      });

      const data = await res.json();

      if (data.answer?.error) {
        setChatHistory([...updatedHistory, `! ${data.answer.error}`]);
      } else {
        setChatHistory(updatedHistory);
        setTreeData(data.answer);
      }
    } catch (err) {
      setChatHistory([...updatedHistory, '! An unexpected error occurred.']);
    }

    setQuestion('');
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory]);

  return (
    <div className="flex h-screen font-mono text-sm bg-gray-100">
      {/* Left: Graph */}
      <div className="w-1/2 p-4 overflow-auto border-r border-gray-300">
        <FibonacciTree data={treeData} />
      </div>

      {/* Right: Chat panel */}
      <div className="w-1/2 flex flex-col p-4 bg-white shadow-inner">
        <div className="flex-grow overflow-y-auto space-y-1 mb-4 p-2 bg-gray-50 border rounded">
          {chatHistory.map((msg, idx) => (
            <div key={idx} className={msg.startsWith('!') ? 'text-red-600' : ''}>
              {msg}
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            className="border px-2 py-1 flex-grow rounded"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Type a command (e.g. insert 6)"
          />
          <button
            type="submit"
            className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
          >
            Submit
          </button>
        </form>
      </div>
    </div>
  );
}
