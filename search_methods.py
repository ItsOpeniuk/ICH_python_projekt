from urllib import response

from DBclass import ProcessDB, execute_query, execute_write_query
import config_file


def all_genres():
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    response = execute_query(connector, config_file.ALL_GENRES)
    result = []
    for row in response:
        for genres in row:
            for genre in genres:
                if genre not in result:
                    result.append(genre)
    return result


def all_years():
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    response = execute_query(connector, config_file.ALL_YEARS)
    year_list = []
    for i in response:
        for year in i:
            if year not in year_list:
                year_list.append(year)
    return year_list


def search_mv_by_genres(genre):
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    query = config_file.GENRES_QUERY.format(genre)
    response = execute_query(connector, query)
    return response


def search_mv_by_year(year):
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    query = config_file.YEAR_QUERY.format(year)
    response = execute_query(connector, query)
    return response


def search_mv_by_rating():
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    query = config_file.RATING_QUERY
    response = execute_query(connector, query)
    return response


def search_mv_by_actor(actor):
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    query = config_file.ACTOR_QUERY.format(actor)
    response = execute_query(connector, query)
    return response


def search_mv_by_keyword(keyword):
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    query = config_file.KEYWORD_QUERY.format(word=keyword)
    response = execute_query(connector, query)
    return response


def search_history():
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    response = execute_query(connector, config_file.MOST_COMMON_QUERIES)
    return response


def write_history(query, user_id):
    db = ProcessDB(config_file.MOVIES_DBCONFIG)
    connector = db.connect()
    execute_write_query(connector, config_file.WRITE_HISTORY.format(query, user_id))


if __name__ == '__main__':
    print(search_mv_by_rating())
