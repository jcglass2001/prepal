-- submission queue table
CREATE TABLE submission_queue (
  id UUID PRIMARY KEY,
  media_type TEXT NOT NULL CHECK ( media_type IN ('video','website') ),
  source_url TEXT NOT NULL,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending','processing','processed','failed')),
  submitted_by TEXT,
  tags TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  processed_at TIMESTAMP
);
-- recipes table 
CREATE TABLE recipes (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  cooking_time_minutes INT,
  nutrition JSONB,
  tags TEXT[],
  source_url TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
-- ingredients table
CREATE TABLE ingredients (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL
);
-- recipe_ingredients table
CREATE TABLE recipe_ingredients (
  id SERIAL PRIMARY KEY,
  recipe_id INT REFERENCES recipes(id) ON DELETE CASCADE,
  ingredient_id INT REFERENCES ingredients(id),
  amount TEXT,
  normalized_unit TEXT,
  normalized_quantity FLOAT
);
