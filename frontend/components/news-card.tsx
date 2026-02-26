export function NewsCard({ article }: { article: any }) {
  return (
    <article className="glass p-5 space-y-3">
      <p className="text-xs uppercase text-cyan-300">{article.category ?? 'Uncategorized'}</p>
      <h3 className="font-semibold text-lg leading-tight">{article.title}</h3>
      <p className="text-sm text-slate-300">{article.summary ?? 'Summary pending.'}</p>
      <ul className="list-disc pl-5 text-sm text-slate-400 space-y-1">
        {(article.key_insights || []).slice(0, 3).map((insight: string) => (
          <li key={insight}>{insight}</li>
        ))}
      </ul>
      <a className="text-cyan-300 text-sm" href={article.canonical_url} target="_blank">Read source ↗</a>
    </article>
  );
}
