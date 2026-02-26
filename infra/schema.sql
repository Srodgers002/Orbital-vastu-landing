CREATE TABLE sources (
  id SERIAL PRIMARY KEY,
  name VARCHAR(120) UNIQUE NOT NULL,
  source_type VARCHAR(30) NOT NULL,
  url VARCHAR(500) NOT NULL,
  country VARCHAR(80),
  is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE categories (
  id SERIAL PRIMARY KEY,
  name VARCHAR(80) UNIQUE NOT NULL
);

CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  title VARCHAR(400) NOT NULL,
  canonical_url VARCHAR(600) UNIQUE NOT NULL,
  raw_content TEXT,
  summary TEXT,
  key_insights JSONB,
  category_id INT REFERENCES categories(id),
  source_id INT REFERENCES sources(id) NOT NULL,
  published_at TIMESTAMPTZ,
  country VARCHAR(80),
  company_tags JSONB,
  model_tags JSONB,
  topic_tags JSONB,
  is_breaking BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE embeddings (
  id SERIAL PRIMARY KEY,
  article_id INT UNIQUE REFERENCES articles(id),
  vector_id VARCHAR(120) UNIQUE NOT NULL,
  model_name VARCHAR(120) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  display_name VARCHAR(120),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE bookmarks (
  id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(id) NOT NULL,
  article_id INT REFERENCES articles(id) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, article_id)
);
