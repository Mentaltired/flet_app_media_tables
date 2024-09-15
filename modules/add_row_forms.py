import flet as ft
import datetime

from modules.DB import get_db_connection, db_disconnect
from modules.add_row import BookAddRow, AnimeBookAddRow, AnimeSeriesAddRow, SeriesAddRow, FilmsAddRow


class AddTagForm(ft.BottomSheet):
    def __init__(self, page, table_name, column_name, new_tag_name, tag_manager, form):
        super().__init__(content=ft.Text(''))
        self.text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE

        self.input_field = ft.TextField(label=new_tag_name, color=self.text_color, border_color=self.text_color)
        self.submit_button = ft.ElevatedButton('Submit', color=self.text_color,
                                               on_click=lambda e: self.on_submit_action(page, table_name, column_name,
                                                                                        tag_manager, form))
        self.cancel_button = ft.ElevatedButton('Cancel', color=self.text_color, on_click=lambda e: page.close(self))

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.input_field,
                    ft.Row(controls=[self.cancel_button, self.submit_button])
                ],
                expand=False,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=30,
            alignment=ft.alignment.top_center,
            height=150,
            width=300
        )

    def on_submit_action(self, page, table_name, column_name, tag_manager, form):
        if self.input_field.value:
            query = f'''INSERT INTO {table_name} ({column_name}) VALUES ('{self.input_field.value}') ON CONFLICT
             ({column_name}) DO NOTHING'''
            connection, cursor = get_db_connection()
            try:
                cursor.execute(query)
                connection.commit()
                tag_manager.selected_tags.append(self.input_field.value)
                tag_manager.selected_tags_chips.append(tag_manager.get_chip(self.input_field.value, page, form))
                tag_manager.get_input_field(page, form)
                form.get_controls()
                page.close(self)
                page.update()
            finally:
                db_disconnect(connection, cursor)


class TagManager:
    def __init__(self, table_name, column_name, add_tag_button_text, new_tag_name, page, form):
        self.text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE
        self.suggested_tags = []
        self.get_suggested_tags_from_db(table_name, column_name)

        self.selected_tags = []
        self.selected_tags_chips = []

        self.input_field = []
        self.get_input_field(page, form)

        self.add_tag_button = ft.CupertinoButton(text=add_tag_button_text, color=self.text_color)
        self.add_tag_button.on_click = lambda e: self.add_tag_button_on_click_action(e, page, table_name, column_name,
                                                                                     new_tag_name, form)

    def get_input_field(self, page, form):
        self.input_field = ft.AutoComplete(
            suggestions=[ft.AutoCompleteSuggestion(key=tag, value=tag) for tag in self.suggested_tags],
            on_select=lambda e: self.input_field_on_select_action(e, page, form)
        )

    def get_suggested_tags_from_db(self, table_name, column_name):
        connection, cursor = get_db_connection()
        query = f'SELECT {column_name} FROM {table_name}'
        cursor.execute(query)
        self.suggested_tags = list(map(lambda x: x[0], cursor.fetchall()))
        db_disconnect(connection, cursor)

    def get_chip(self, tag_name, page, form):
        def remove_chip(e):
            self.selected_tags_chips.remove(tag_chip)
            self.selected_tags.remove(tag_name)
            self.suggested_tags.append(tag_name)

            self.get_input_field(page, form)
            form.get_controls()
            page.update()

        tag_chip = ft.Chip(label=ft.Text(tag_name, color=self.text_color), on_delete=remove_chip)
        return tag_chip

    def input_field_on_select_action(self, e, page, form):
        tag_name = e.selection.value
        self.selected_tags.append(tag_name)
        self.suggested_tags.remove(tag_name)

        self.selected_tags_chips.append(self.get_chip(tag_name, page, form))

        self.get_input_field(page, form)
        form.get_controls()
        page.update()

    def add_tag_button_on_click_action(self, e, page, table_name, column_name, new_tag_name, form):
        page.open(AddTagForm(page, table_name, column_name, new_tag_name, self, form))


class TagRow(ft.Row):
    def __init__(self, tag_chips, add_tag_button):
        super().__init__()
        self.controls = [
            ft.Row(
                controls=tag_chips,
                alignment=ft.MainAxisAlignment.START,
                expand=3,
                wrap=True
            ),
            ft.Row(
                controls=[add_tag_button],
                expand=2,
                alignment=ft.MainAxisAlignment.END
            )
        ]


class AddRowForm(ft.AlertDialog):
    def __init__(self, page):
        super().__init__()
        text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE

        self.content = ft.Column(
            controls=[],
            expand=False,
            scroll=ft.ScrollMode.AUTO,
            width=500
        )

        self.actions = [
            ft.TextButton(content=ft.Text('Cancel', color=text_color), on_click=lambda e: page.close(self)),
            ft.TextButton(content=ft.Text('Confirm', color=text_color))
        ]

    def get_controls(self):
        pass


class BookAddRowForm(AddRowForm):
    def __init__(self, page, table):
        super().__init__(page)
        self.text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE

        self.title = ft.Text('Add book', color=self.text_color)

        self.title_field = ft.TextField(label='Title', color=self.text_color, border_color=self.text_color)

        self.author_tags = TagManager('Authors', 'author_name', 'Add new author',
                                      'Author name', page, self)
        self.series_tags = TagManager('BookSeries', 'book_series_name',
                                      'Add new series', 'Series name', page, self)
        self.genres_tags = TagManager('Genres', 'genre_name', 'Add new genre',
                                      'Genre name', page, self)

        self.rsd_button = ft.CupertinoButton(content=ft.Text('Choose reading start day', color=self.text_color),
                                             on_click=lambda e: self.rsd_button_on_click_action(page))
        self.red_button = ft.CupertinoButton(content=ft.Text('Choose reading end day', color=self.text_color),
                                             on_click=lambda e: self.red_button_on_click_action(page))

        self.symbol_amount = ft.TextField(label='Symbol amount', color=self.text_color, border_color=self.text_color)
        self.read_checkbox = ft.Checkbox(label='Read')

        self.get_controls()

        self.actions[1].on_click = lambda e: self.confirm_action(page, table)


    def get_controls(self):
        self.content.controls = [
            self.title_field,
            self.author_tags.input_field,
            TagRow(self.author_tags.selected_tags_chips, self.author_tags.add_tag_button),
            self.series_tags.input_field,
            TagRow(self.series_tags.selected_tags_chips, self.series_tags.add_tag_button),
            self.genres_tags.input_field,
            TagRow(self.genres_tags.selected_tags_chips, self.genres_tags.add_tag_button),
            ft.Row(controls=[self.rsd_button], alignment=ft.MainAxisAlignment.END),
            ft.Row(controls=[self.red_button], alignment=ft.MainAxisAlignment.END),
            self.symbol_amount,
            ft.Row(controls=[self.read_checkbox], alignment=ft.MainAxisAlignment.END)
        ]

    def rsd_button_on_click_action(self, page):
        def handle_change(e):
            self.rsd_button.content = ft.Text(e.control.value.strftime('%Y-%m-%d'), color=self.text_color)
            self.get_controls()
            page.update()

        date_picker = ft.DatePicker(on_change=handle_change)
        page.open(date_picker)

    def red_button_on_click_action(self, page):
        def handle_change(e):
            self.red_button.content = ft.Text(e.control.value.strftime('%Y-%m-%d'), color=self.text_color)
            self.get_controls()
            page.update()

        date_picker = ft.DatePicker(on_change=handle_change)
        page.open(date_picker)

    def confirm_action(self, page, table):
        BookAddRow(self, page, table)


class AnimeBookAddRowForm(AddRowForm):
    def __init__(self, page, table):
        super().__init__(page)
        self.text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE

        self.title = ft.Text('Add anime book', color=self.text_color)

        self.title_field = ft.TextField(label='Title', color=self.text_color, border_color=self.text_color)
        self.series_tags = TagManager('AnimeBookSeries', 'anime_book_series_name',
                                      'Add new series', 'Series name', page, self)

        self.symbol_amount = ft.TextField(label='Symbol amount', color=self.text_color, border_color=self.text_color)
        self.read_checkbox = ft.Checkbox(label='Read')

        self.get_controls()

        self.actions[1].on_click = lambda e: self.confirm_action(page, table)

    def get_controls(self):
        self.content.controls = [
            self.title_field,
            self.series_tags.input_field,
            TagRow(self.series_tags.selected_tags_chips, self.series_tags.add_tag_button),
            self.symbol_amount,
            ft.Row(controls=[self.read_checkbox], alignment=ft.MainAxisAlignment.END)
        ]

    def confirm_action(self, page, table):
        AnimeBookAddRow(self, page, table)


class AnimeSeriesAddRowForm(AddRowForm):
    def __init__(self, page, table):
        super().__init__(page)
        self.text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE

        self.title = ft.Text('Add anime series', color=self.text_color)

        self.title_field = ft.TextField(label='Title', color=self.text_color, border_color=self.text_color)
        self.series_tags = TagManager('AnimeSeries', 'anime_series_name',
                                      'Add new series', 'Series name', page, self)

        self.number_of_episodes = ft.TextField(label='Number of episodes', color=self.text_color,
                                               border_color=self.text_color)
        self.viewed_checkbox = ft.Checkbox(label='Viewed')

        self.get_controls()
        self.actions[1].on_click = lambda e: self.confirm_action(page, table)

    def confirm_action(self, page, table):
        AnimeSeriesAddRow(self, page, table)

    def get_controls(self):
        self.content.controls = [
            self.title_field,
            self.series_tags.input_field,
            TagRow(self.series_tags.selected_tags_chips, self.series_tags.add_tag_button),
            self.number_of_episodes,
            ft.Row(controls=[self.viewed_checkbox], alignment=ft.MainAxisAlignment.END)
        ]


class SeriesAddRowForm(AddRowForm):
    def __init__(self, page, table):
        super().__init__(page)
        self.text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE

        self.title = ft.Text('Add series', color=self.text_color)

        self.title_field = ft.TextField(label='Title', color=self.text_color, border_color=self.text_color)
        self.season_field = ft.TextField(label='Season', color=self.text_color, border_color=self.text_color)
        self.number_of_episodes = ft.TextField(label='Number of episode', color=self.text_color,
                                               border_color=self.text_color)
        self.episode_duration = ft.TextField(label='Duration of one episode', color=self.text_color,
                                             border_color=self.text_color)
        self.status_checkbox = ft.Checkbox(label='Viewed')

        self.actions[1].on_click = lambda e: self.confirm_action(page, table)

        self.get_controls()

    def get_controls(self):
        self.content.controls = [
            self.title_field,
            self.season_field,
            self.number_of_episodes,
            self.episode_duration,
            ft.Row(controls=[self.status_checkbox], alignment=ft.MainAxisAlignment.END)
        ]

    def confirm_action(self, page, table):
        SeriesAddRow(self, page, table)


class FilmsAddRowForm(AddRowForm):
    def __init__(self, page, table):
        super().__init__(page)
        self.text_color = ft.colors.BLACK if page.theme_mode == 'light' else ft.colors.WHITE

        self.title = ft.Text('Add film', color=self.text_color)

        self.title_field = ft.TextField(label='Title', color=self.text_color, border_color=self.text_color)
        self.series_tags = TagManager('FilmSeries', 'film_series_name',
                                      'Add new series', 'Series name', page, self)

        self.duration = ft.TextField(label='Duration', color=self.text_color, border_color=self.text_color)
        self.viewed_checkbox = ft.Checkbox(label='Viewed')

        self.get_controls()
        self.actions[1].on_click = lambda e: self.confirm_action(page, table)

    def confirm_action(self, page, table):
        FilmsAddRow(self, page, table)

    def get_controls(self):
        self.content.controls = [
            self.title_field,
            self.series_tags.input_field,
            TagRow(self.series_tags.selected_tags_chips, self.series_tags.add_tag_button),
            self.duration,
            ft.Row(controls=[self.viewed_checkbox], alignment=ft.MainAxisAlignment.END)
        ]
