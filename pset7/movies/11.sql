SELECT title
FROM movies JOIN ratings ON movies.id = ratings.movie_id JOIN stars ON stars.movie_id = movies.id WHERE stars.person_id = (SELECT id FROM people WHERE name = 'Chadwick Boseman') LIMIT 5;
