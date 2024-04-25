from os import getenv

MOVIES_DBCONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '24329611Aa',
    'database': 'movies'
}

TG_BOT_TOKEN = getenv('TG_BOT_TOKEN')

TG_CHAT_ID = '1002012956420'

ALL_GENRES = 'SELECT genres FROM movies '

ALL_YEARS = 'SELECT `year` FROM movies '

GENRES_QUERY = ('SELECT poster, title, `imdb.rating`, `year`, genres, runtime, plot '
                'FROM movies '
                'WHERE "{}" IN (genres)'
                'ORDER BY `imdb.rating` DESC '
                'LIMIT 10')

YEAR_QUERY = ('SELECT poster, title, `imdb.rating`, `year`, genres, runtime, plot '
              'FROM movies '
              'WHERE {} = `year` '
              'ORDER BY `imdb.rating` DESC '
              'LIMIT 10')

RATING_QUERY = ('SELECT poster, title, `imdb.rating`, `year`, genres, runtime, plot '
                'FROM movies '
                'ORDER BY `imdb.rating` DESC '
                'LIMIT 10')

ACTOR_QUERY = ('SELECT poster, title, `imdb.rating`, `year`, genres, runtime, plot '
               'FROM movies '
               'WHERE JSON_CONTAINS(cast, \'"{}"\') '
               'ORDER BY `imdb.rating` DESC '
               'LIMIT 10')

KEYWORD_QUERY = ('SELECT poster, title, `imdb.rating`, `year`, genres, runtime, plot '
                 'FROM movies '
                 'WHERE title LIKE "% {word} %" OR title LIKE "{word} %" OR title LIKE "% {word}"'
                 'ORDER BY `imdb.rating` DESC '
                 'LIMIT 10')

MOST_COMMON_QUERIES = """
SELECT query, COUNT(query) AS query_count
FROM search_history
GROUP BY query
ORDER BY query_count DESC
LIMIT 10"""

WRITE_HISTORY = 'INSERT INTO search_history (query, user_id) VALUES ("{}", {})'
