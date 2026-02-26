import type { Config } from 'tailwindcss';

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        glass: 'rgba(255,255,255,0.08)',
      },
      boxShadow: {
        glass: '0 8px 32px rgba(31, 38, 135, 0.2)',
      },
    },
  },
  plugins: [],
};

export default config;
