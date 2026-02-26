import './globals.css';
import { Header } from '@/components/header';

export const metadata = {
  title: 'Global AI Intelligence Portal',
  description: 'Real-time AI news intelligence platform',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Header />
        <main className="max-w-7xl mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
