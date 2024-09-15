from collections import defaultdict

import flet as ft

from modules.DB import get_db_connection, db_disconnect
from modules.add_row_forms import BookAddRowForm


class TableLabel(ft.Text):
    def __init__(self, text):
        super().__init__(text)
        self.color = ft.colors.BLACK
        self.size = 20
        self.weight = ft.FontWeight.BOLD

    def toggle_theme(self):
        self.color = ft.colors.BLACK if self.color == ft.colors.WHITE else ft.colors.WHITE


class MediaTable(ft.DataTable):
    def __init__(self, column_names, page):
        super().__init__(columns=[ft.DataColumn(ft.Text(column_name)) for column_name in column_names])
        self.columns_amount = len(column_names)
        self.rows = []

        self.page = page

        self.select_statement = ''

    def get_db_rows(self):
        connection, cursor = get_db_connection()
        try:
            cursor.execute(self.select_statement)

            self.rows = [
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(row[i])) for i in range(self.columns_amount)]
                )
                for row in cursor.fetchall()
            ]
        except:
            print('Unknown get rows error')
        finally:
            db_disconnect(connection, cursor)

    def toggle_theme(self):
        pass


class BookTable(MediaTable):
    def __init__(self, column_names, page):
        super().__init__(column_names, page)

        self.select_statement = '''
                SELECT 
                    b.title,
                    string_agg(DISTINCT a.author_name, ', ') AS author_names,
                    string_agg(DISTINCT bs.book_series_name, ', ') AS series_names,
                    string_agg(DISTINCT g.genre_name, ', ') AS genre_names,
                    COALESCE(TO_CHAR(b.reading_start_day, 'YYYY-MM-DD'), 'Не указано') AS reading_start_day,
                    COALESCE(TO_CHAR(b.reading_end_day, 'YYYY-MM-DD'), 'Не указано') AS reading_end_day,
                    b.symbols_amount,
                    CASE 
                        WHEN b.status THEN 'Прочитано'
                        ELSE 'Не прочитано'
                    END AS status
                FROM 
                    Books b
                LEFT JOIN 
                    BookSeriesBooks bsb ON b.book_id = bsb.book_id
                LEFT JOIN 
                    BookSeries bs ON bsb.book_series_id = bs.book_series_id
                LEFT JOIN 
                    BookAuthors ba ON b.book_id = ba.book_id
                LEFT JOIN 
                    Authors a ON ba.author_id = a.author_id
                LEFT JOIN 
                    BookGenres bg ON b.book_id = bg.book_id
                LEFT JOIN 
                    Genres g ON bg.genre_id = g.genre_id
                GROUP BY 
                    b.book_id;
                '''
        self.get_db_rows()


class AnimeBookTable(MediaTable):
    def __init__(self, column_names, page):
        super().__init__(column_names, page)

        self.select_statement = '''
        SELECT
            b.title,
            string_agg(DISTINCT s.anime_book_series_name, ', ') AS series,
            b.symbols_amount,
            CASE 
                WHEN b.status THEN 'Прочитано'
                ELSE 'Не прочитано'
            END AS status
        FROM
            AnimeBooks b
            JOIN AnimeBookSeriesAnimeBooks bs USING(anime_book_id)
            JOIN AnimeBookSeries s USING(anime_book_series_id)
        GROUP BY b.anime_book_id'''
        self.get_db_rows()


class AnimeSeriesTable(MediaTable):
    def __init__(self, column_names, page):
        super().__init__(column_names, page)

        self.select_statement = '''SELECT
            a.title,
            string_agg(DISTINCT s.anime_series_name, ', ') AS series,
            a.number_of_episode,
            a.number_of_episode * 24 AS duration,
            CASE 
                WHEN a.status THEN 'Прочитано'
                ELSE 'Не прочитано'
            END AS status
        FROM
            Animes a
            JOIN AnimeSeriesAnimes USING(anime_id)
            JOIN AnimeSeries s USING(anime_series_id)
        GROUP BY a.anime_id'''
        self.get_db_rows()


class SeriesTable(MediaTable):
    def __init__(self, column_names, page):
        super().__init__(column_names, page)
        self.select_statement = '''SELECT
            title,
            season,
            number_of_episode,
            number_of_episode * duration_of_one_episode as duration,
            CASE 
                WHEN status THEN 'Прочитано'
                ELSE 'Не прочитано'
            END AS status
        FROM Series
        GROUP BY series_id;'''

        self.get_db_rows()


class FilmsTable(MediaTable):
    def __init__(self, column_names, page):
        super().__init__(column_names, page)

        self.select_statement = '''SELECT
            f.title,
            string_agg(DISTINCT s.film_series_name, ', ') AS series,
            f.duration,
            CASE 
                WHEN f.status THEN 'Прочитано'
                ELSE 'Не прочитано'
            END AS status
        FROM
            Films f
            JOIN FilmSeriesFilms USING(film_id)
            JOIN FilmSeries s USING(film_series_id)
        GROUP BY f.film_id'''
        self.get_db_rows()
