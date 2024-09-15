import flet as ft

from modules.buttons import MediaTypeButton, ToggleThemeButton, AddRowButton
from modules.tables import TableLabel, BookTable, AnimeBookTable, AnimeSeriesTable, SeriesTable, FilmsTable


class UI:
    def __init__(self, page):
        self.page = page

        self.controls = PageContent(self)
        self.page_amount = len(self.controls.media_type_buttons)
        self.cur_page_index = 0

        self.toggle_theme = self.get_toggle_theme()

        self.content = None
        self.set_ui_content()

    def set_ui_content(self):
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Row(
                            controls=[
                                self.controls.table_labels[self.cur_page_index],
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.START
                        ),
                        ft.Row(
                            controls=[
                                self.controls.toggle_theme_button
                            ],
                            expand=True,
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    expand=1
                ),
                ft.Stack(
                    controls=[
                        ft.Column(
                            controls=[self.controls.tables[self.cur_page_index]],
                            expand=True,
                            scroll=ft.ScrollMode.AUTO,
                            horizontal_alignment=ft.CrossAxisAlignment.STRETCH
                        ),
                        ft.Container(
                            content=self.controls.add_row_buttons[self.cur_page_index],
                            width=56,
                            height=56,
                            bottom=0,
                            right=10
                        )
                    ],
                    expand=15
                ),
                ft.Row(
                    controls=[
                        self.controls.media_type_buttons[i] for i in range(self.page_amount)
                    ],
                    expand=2
                )
            ],
            expand=True
        )

    def get_toggle_theme(self):
        res = []
        res += self.controls.media_type_buttons
        res += [self.controls.toggle_theme_button]
        res += self.controls.tables
        res += self.controls.table_labels
        res += self.controls.add_row_buttons

        return res


class PageContent:
    def __init__(self, ui):
        self.media_type_buttons = [
            MediaTypeButton('Books', ui),
            MediaTypeButton('Anime books', ui),
            MediaTypeButton('Anime series', ui),
            MediaTypeButton('Series', ui),
            MediaTypeButton('Films', ui)
        ]

        self.toggle_theme_button = ToggleThemeButton(ui)

        self.tables = [
            BookTable(['Title', 'Authors', 'Series', 'Genres', 'Reading start day', 'Reading end day',
                       'Symbols amount', 'Status'], ui.page),
            AnimeBookTable(['Title', 'Series', 'Symbol amount', 'Status'], ui.page),
            AnimeSeriesTable(['Title', 'Season', 'Number of episode', 'Duration', 'Status'], ui.page),
            SeriesTable(['Title', 'Season', 'Number of episode', 'Duration', 'Status'], ui.page),
            FilmsTable(['Title', 'Series', 'Duration', 'Status'], ui.page)
        ]

        self.add_row_buttons = [
            AddRowButton(ui),
            AddRowButton(ui),
            AddRowButton(ui),
            AddRowButton(ui),
            AddRowButton(ui)
        ]

        self.table_labels = [
            TableLabel('Books'),
            TableLabel('Anime books'),
            TableLabel('Anime series'),
            TableLabel('Series'),
            TableLabel('Films')
        ]


class App:
    def __init__(self, page):
        self.page = page
        self.page.title = 'Media saver'
        self.page.theme_mode = 'light'
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.window.width = 1500
        self.page.window.height = 800

        self.ui = UI(self.page)

        self.open_ui()

    def open_ui(self):
        self.page.add(self.ui.content)


def main(page: ft.Page):
    App(page)


if __name__ == '__main__':
    ft.app(target=main)
