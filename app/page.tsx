'use client';

import { useState } from 'react';
import FibonacciTree from '@/components/FibonacciTree';

export default function Home() {
  const [question, setQuestion] = useState('');
  const [treeData, setTreeData] = useState<any>(null);

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    const res = await fetch('/api/query', {
      method: 'POST',
      body: JSON.stringify({ question, chatHistory: [] }),
    });
    const data = await res.json();
    setTreeData(data.answer);
    setQuestion('');
  };

  return (
    <div className="p-6">
      <form onSubmit={handleSubmit} className="mb-4 flex gap-2">
        <input
          type="text"
          className="border px-2 py-1 w-72"
          value={question}
          placeholder="Type a command (e.g. insert 6)"
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">
          Submit
        </button>
      </form>
      <FibonacciTree data={treeData} />
    </div>
  );
}
