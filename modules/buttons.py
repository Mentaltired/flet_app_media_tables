import flet as ft

from modules.add_row_forms import BookAddRowForm, AnimeBookAddRowForm, AnimeSeriesAddRowForm, SeriesAddRowForm, \
    FilmsAddRowForm


class ToggleThemeButton(ft.IconButton):
    def __init__(self, ui):
        super().__init__(
            icon="dark_mode",
            selected_icon="light_mode",
            style=ft.ButtonStyle(
                color={"": ft.colors.BLACK, "selected": ft.colors.WHITE}
            )
        )
        self.on_click = lambda e: self.on_click_action(ui)

    def toggle_theme(self):
        self.selected = not self.selected

    @staticmethod
    def on_click_action(ui):
        for control in ui.toggle_theme:
            control.toggle_theme()

        ui.page.theme_mode = 'dark' if ui.page.theme_mode == 'light' else 'light'
        ui.page.update()


class MediaTypeButton(ft.CupertinoButton):
    button_amount = 0

    def __init__(self, text, ui, expand=1):
        super().__init__()
        self.content = ft.Text(
            text,
            color=ft.colors.BLACK,
            size=20
        )

        self.button_number = self.button_amount
        type(self).button_amount += 1

        self.expand = expand
        self.on_click = lambda e: self.on_click_action(ui)

    def on_click_action(self, ui):
        ui.cur_page_index = self.button_number

        ui.page.remove(ui.content)
        ui.set_ui_content()
        ui.page.add(ui.content)
        ui.page.update()

    def toggle_theme(self):
        self.content.color = ft.colors.BLACK if self.content.color == ft.colors.WHITE else ft.colors.WHITE


class AddRowButton(ft.FloatingActionButton):
    button_amount = 0
    add_row_forms = [
        BookAddRowForm,
        AnimeBookAddRowForm,
        AnimeSeriesAddRowForm,
        SeriesAddRowForm,
        FilmsAddRowForm
    ]

    def __init__(self, ui):
        super().__init__()

        self.on_click = None
        self.bgcolor = ft.colors.WHITE
        self.icon_color = ft.colors.BLACK
        self.icon = ft.icons.ADD

        self.button_number = self.button_amount
        type(self).button_amount += 1

        self.on_click = lambda e: self.on_click_action(ui)

    def on_click_action(self, ui):
        new_form = type(self).add_row_forms[self.button_number](ui.page, ui.controls.tables[self.button_number])
        ui.page.open(new_form)

    def toggle_theme(self):
        self.bgcolor = ft.colors.GREY_800 if self.bgcolor == ft.colors.WHITE else ft.colors.WHITE
        self.icon_color = ft.colors.BLACK if self.icon_color == ft.colors.WHITE else ft.colors.WHITE
