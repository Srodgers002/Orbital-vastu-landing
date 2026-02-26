import Link from 'next/link';

export function Header() {
  return (
    <header className="sticky top-0 z-20 border-b border-white/10 bg-slate-950/80 backdrop-blur">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link href="/" className="font-bold">Global AI Intelligence Portal</Link>
        <nav className="flex gap-5 text-sm text-slate-300">
          <Link href="/">Home</Link>
          <Link href="/search">Semantic Search</Link>
          <Link href="/assistant">Ask AI</Link>
        </nav>
      </div>
    </header>
  );
}
