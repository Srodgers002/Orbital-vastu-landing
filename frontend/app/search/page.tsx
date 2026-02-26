'use client';

import { useState } from 'react';

export default function SearchPage() {
  const [q, setQ] = useState('');
  const [results, setResults] = useState<any[]>([]);

  const runSearch = async () => {
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/v1'}/search?q=${encodeURIComponent(q)}`);
    setResults(await res.json());
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Semantic Search</h1>
      <div className="glass p-4 flex gap-3">
        <input value={q} onChange={(e) => setQ(e.target.value)} className="bg-transparent flex-1 outline-none" placeholder="Search by company, topic, model..." />
        <button onClick={runSearch} className="px-4 py-2 bg-cyan-500/80 rounded-lg">Search</button>
      </div>
      <div className="space-y-3">
        {results.map((r) => <div key={r.id} className="glass p-4">{r.title}</div>)}
      </div>
    </div>
  );
}
