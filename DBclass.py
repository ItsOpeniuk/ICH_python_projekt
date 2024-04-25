import mysql.connector


def execute_query(connect, query):
    try:
        with connect.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f'Ошибка {err}, Пожалуйста повторите попытку!')
        results = None
    return results


def execute_write_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()


class ProcessDB:
    def __init__(self, config):
        self.config = config

    def connect(self):
        connection = None
        try:
            connection = mysql.connector.connect(**self.config)
        except mysql.connector.Error as err:
            print(f"Ошибка {err} при подключении к MySQL")
        return connection
