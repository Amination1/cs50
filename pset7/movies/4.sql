SELECT COUNT(title) + 1 FROM movies WHERE id = (SELECT movie_id FROM ratings WHERE rating = 10.0);
