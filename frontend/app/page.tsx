import { NewsCard } from '@/components/news-card';
import { fetchArticles, fetchTrending } from '@/lib/api';

export default async function HomePage() {
  const [articles, trending] = await Promise.all([fetchArticles(), fetchTrending()]);

  return (
    <div className="space-y-8">
      <section className="glass p-6">
        <h1 className="text-2xl font-bold">Trending AI News</h1>
        <p className="text-slate-300 mt-2">Live coverage across startups, model launches, regulation, research, and ethics.</p>
      </section>

      <section>
        <h2 className="text-xl mb-4">Breaking AI Alerts</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {trending.map((article: any) => <NewsCard key={article.id} article={article} />)}
        </div>
      </section>

      <section>
        <h2 className="text-xl mb-4">Latest Coverage</h2>
        <div className="grid md:grid-cols-2 gap-4">
          {articles.slice(0, 12).map((article: any) => <NewsCard key={article.id} article={article} />)}
        </div>
      </section>
    </div>
  );
}
