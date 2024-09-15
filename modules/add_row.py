import flet as ft

from modules.DB import get_db_connection, db_disconnect


class AddRow:
    def __init__(self):
        self.queries = []

    @staticmethod
    def print_error_message(error_name, page):
        text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE
        error_message = ft.BottomSheet(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(controls=[ft.Text(error_name, color=text_color, size=17)]),
                        ft.Row(controls=[ft.TextButton(content=ft.Text('Ok', color=text_color),
                                                       on_click=lambda e: page.close(error_message))])
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=30,
                alignment=ft.alignment.top_center,
                width=300,
                height=110
            )
        )
        page.open(error_message)

    def insert_values(self, page, form, table):
        connection, cursor = get_db_connection()
        try:
            for query, values in self.queries:
                print(values)
                cursor.execute(query, values)
                connection.commit()
        finally:
            db_disconnect(connection, cursor)

        table.get_db_rows()
        page.close(form)
        page.update()


class BookAddRow(AddRow):
    def __init__(self, form, page, table):
        super().__init__()

        if not ((form.title_field.value.strip() and len(form.author_tags.selected_tags) > 0
                 and form.symbol_amount.value.strip())):
            self.print_error_message('Invalid data format', page)
        elif form.title_field.value.strip() in self.get_titles():
            self.print_error_message('Book with this title already exists', page)
        else:
            rsd = form.rsd_button.content.value if form.rsd_button.content.value != 'Choose reading start day' else None
            red = form.red_button.content.value if form.red_button.content.value != 'Choose reading end day' else None

            self.queries.append([
                '''INSERT INTO Books(title, reading_start_day, reading_end_day, symbols_amount, status) 
                VALUES (%s, %s, %s, %s, %s)''',
                [form.title_field.value, rsd, red, form.symbol_amount.value, form.read_checkbox.value]
            ])

            for author in form.author_tags.selected_tags:
                self.queries.append([
                    '''INSERT INTO BookAuthors(book_id, author_id)
                        SELECT
                            b.book_id,
                            a.author_id
                        FROM Books b
                        JOIN Authors a ON a.author_name = %s AND b.title = %s;''',
                    [author, form.title_field.value]])

            for genre in form.genres_tags.selected_tags:
                self.queries.append([
                    '''INSERT INTO BookGenres(book_id, genre_id)
                        SELECT
                            b.book_id,
                            g.genre_id
                        FROM Books b
                        JOIN Genres g ON g.genre_name = %s AND b.title = %s;''',
                    [genre, form.title_field.value]])
            if len(form.series_tags.selected_tags) > 0:
                for series in form.series_tags.selected_tags:
                    self.queries.append([
                        '''INSERT INTO BookSeriesBooks(book_id, book_series_id)
                            SELECT
                                b.book_id,
                                bs.book_series_id
                            FROM Books b
                            JOIN BookSeries bs ON bs.book_series_name = %s AND b.title = %s;''',
                        [series, form.title_field.value]])
            else:
                self.queries.append([
                    '''INSERT INTO BookSeriesBooks(book_id, book_series_id)
                        SELECT
                            b.book_id,
                            bs.book_series_id
                        FROM Books b
                        JOIN BookSeries bs ON bs.book_series_name = %s AND b.title = %s;''',
                    ['Без серии', form.title_field.value]])

            self.insert_values(page, form, table)

    @staticmethod
    def get_titles():
        connection, cursor = get_db_connection()
        try:
            cursor.execute('SELECT title FROM Books')
            res = list(map(lambda e: e[0], cursor.fetchall()))
            return res
        finally:
            db_disconnect(connection, cursor)


class AnimeBookAddRow(AddRow):
    def __init__(self, form, page, table):
        super().__init__()

        if not (form.title_field.value.strip() and form.symbol_amount.value.strip()):
            self.print_error_message('Invalid data format', page)
        elif form.title_field.value.strip() in self.get_titles():
            self.print_error_message('Book with this title already exists', page)
        else:
            self.queries.append([
                'INSERT INTO AnimeBooks(title, symbols_amount, status) VALUES (%s, %s, %s);',
                [form.title_field.value, form.symbol_amount.value, form.read_checkbox.value]
            ])
            if len(form.series_tags.selected_tags) == 0:
                form.series_tags.selected_tags.append('Без серии')
            for series in form.series_tags.selected_tags:
                self.queries.append([
                    '''INSERT INTO AnimeBookSeriesAnimeBooks(anime_book_id, anime_book_series_id)
                    SELECT b.anime_book_id, s.anime_book_series_id
                    FROM AnimeBooks b JOIN AnimeBookSeries s ON b.title = %s AND s.anime_book_series_name = %s''',
                    [form.title_field.value, series]
                ])

            self.insert_values(page, form, table)

    @staticmethod
    def get_titles():
        connection, cursor = get_db_connection()
        try:
            cursor.execute('SELECT title FROM AnimeBooks')
            res = list(map(lambda e: e[0], cursor.fetchall()))
            return res
        finally:
            db_disconnect(connection, cursor)


class AnimeSeriesAddRow(AddRow):
    def __init__(self, form, page, table):
        super().__init__()
        if not (form.title_field.value.strip() and form.number_of_episodes.value.strip()):
            self.print_error_message('Invalid data format', page)
        elif form.title_field.value.strip() in self.get_titles():
            self.print_error_message('Anime with this title already exists', page)
        else:
            self.queries.append([
                '''INSERT INTO Animes(title, number_of_episode, status) VALUES (%s, %s, %s);''',
                [form.title_field.value, form.number_of_episodes.value, form.viewed_checkbox.value]
            ])
            if len(form.series_tags.selected_tags) == 0:
                form.series_tags.selected_tags.append('Без серии')
            for series in form.series_tags.selected_tags:
                self.queries.append([
                    '''INSERT INTO AnimeSeriesAnimes(anime_id, anime_series_id)
                    SELECT
                        a.anime_id,
                        s.anime_series_id
                    FROM Animes a JOIN AnimeSeries s ON a.title = %s AND s.anime_series_name = %s;''',
                    [form.title_field.value, series]
                ])

            self.insert_values(page, form, table)

    @staticmethod
    def get_titles():
        connection, cursor = get_db_connection()
        try:
            cursor.execute('SELECT title FROM Animes')
            res = list(map(lambda e: e[0], cursor.fetchall()))
            return res
        finally:
            db_disconnect(connection, cursor)


class SeriesAddRow(AddRow):
    def __init__(self, form, page, table):
        super().__init__()
        if not (form.title_field.value.strip() and form.number_of_episodes.value.strip() and
                form.number_of_episodes.value.strip()):
            self.print_error_message('Invalid data format', page)
        elif [form.title_field.value.strip(), int(form.season_field.value.strip())] in self.get_titles():
            self.print_error_message('Series with this title already exists', page)
        else:
            self.queries.append([
                '''INSERT INTO Series(title, season, number_of_episode, duration_of_one_episode, status) 
                VALUES (%s, %s, %s, %s, %s)''',
                [form.title_field.value, form.season_field.value, form.number_of_episodes.value,
                 form.episode_duration.value, form.status_checkbox.value]
            ])

            self.insert_values(page, form, table)

    @staticmethod
    def get_titles():
        connection, cursor = get_db_connection()
        try:
            cursor.execute('SELECT title, season FROM Series')
            res = list(map(lambda e: [e[0], e[1]], cursor.fetchall()))
            return res
        finally:
            db_disconnect(connection, cursor)


class FilmsAddRow(AddRow):
    def __init__(self, form, page, table):
        super().__init__()
        if not (form.title_field.value.strip() and form.duration.value.strip()):
            self.print_error_message('Invalid data format', page)
        elif form.title_field.value.strip() in self.get_titles():
            self.print_error_message('Film with this title already exists', page)
        else:
            self.queries.append([
                'INSERT INTO Films(title, duration, status) VALUES (%s, %s, %s)',
                [form.title_field.value, form.duration.value, form.viewed_checkbox.value]
            ])
            if len(form.series_tags.selected_tags) == 0:
                form.series_tags.selected_tags.append('Без серии')
            for series in form.series_tags.selected_tags:
                self.queries.append([
                    '''INSERT INTO FilmSeriesFilms(film_id, film_series_id)
                    SELECT f.film_id, s.film_series_id
                    FROM Films f JOIN FilmSeries s ON f.title = %s AND s.film_series_name = %s;''',
                    [form.title_field.value, series]
                ])

            self.insert_values(page, form, table)

    @staticmethod
    def get_titles():
        connection, cursor = get_db_connection()
        try:
            cursor.execute('SELECT title FROM Films')
            res = list(map(lambda e: e[0], cursor.fetchall()))
            return res
        finally:
            db_disconnect(connection, cursor)
