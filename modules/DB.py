import psycopg2


def get_db_connection():
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="",
            host="localhost",
            port="5432",
            database="MyMedia"
        )

        connection = connection
        cursor = connection.cursor()
        return connection, cursor

    except (Exception, psycopg2.Error) as error:
        print("Ошибка при работе с PostgreSQL", error)


def db_disconnect(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()