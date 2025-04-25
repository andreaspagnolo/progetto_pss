CREATE TABLE IF NOT EXISTS watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    movie_name TEXT NOT NULL,
    movie_id INTEGER NOT NULL,
    UNIQUE(user_id, movie_name)
);