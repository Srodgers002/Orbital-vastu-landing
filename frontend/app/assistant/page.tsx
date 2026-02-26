'use client';

import { useState } from 'react';

export default function AssistantPage() {
  const [question, setQuestion] = useState('What happened in AI this week?');
  const [answer, setAnswer] = useState('');

  const ask = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/v1'}/assistant/digest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, days: 7 }),
    });
    const data = await res.json();
    setAnswer(data.answer);
  };

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Ask AI Assistant</h1>
      <textarea value={question} onChange={(e) => setQuestion(e.target.value)} className="w-full h-32 glass p-4" />
      <button onClick={ask} className="px-4 py-2 rounded-lg bg-cyan-500/80">Generate digest</button>
      {answer && <pre className="glass p-4 whitespace-pre-wrap">{answer}</pre>}
    </div>
  );
}
