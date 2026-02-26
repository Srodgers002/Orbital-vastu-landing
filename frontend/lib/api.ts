const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/v1';

export async function fetchArticles(params?: Record<string, string>) {
  const query = params ? `?${new URLSearchParams(params).toString()}` : '';
  const res = await fetch(`${API_BASE}/articles${query}`, { next: { revalidate: 60 } });
  if (!res.ok) throw new Error('Failed to fetch articles');
  return res.json();
}

export async function fetchTrending() {
  const res = await fetch(`${API_BASE}/trending`, { next: { revalidate: 60 } });
  if (!res.ok) throw new Error('Failed to fetch trending');
  return res.json();
}
