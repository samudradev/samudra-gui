from kivymd.app import MDApp, Builder
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget

from kivy.properties import StringProperty, ObjectProperty, ListProperty

from samudra.startup import on_start
from samudra.interfaces import (
    LemmaQueryBuilder,
    LemmaData,
)

from components import build_top_right_button, build_konsep_list, build_title


class DataCard(MDAnchorLayout):
    lemma: LemmaData = ObjectProperty("", allownone=True)
    anchor_x = "center"
    anchor_y = "center"
    padding = 25, 25, 25, 25

    def goto_edit_mode(self, caller: Widget):
        self.build(mode="edit")

    def goto_display_mode(self, caller: Widget):
        self.build(mode=None)

    def build(self, mode: str = None) -> Widget:
        self.clear_widgets()
        if mode == "edit":
            btn__menu = build_top_right_button(
                icon="exit-to-app", on_release=self.goto_display_mode
            )
        else:
            btn__menu = build_top_right_button(
                icon="pen", on_release=self.goto_edit_mode
            )
        self.add_widget(btn__menu)

        box__display = MDBoxLayout(padding=30, adaptive_height=True)
        if self.lemma is None:
            box__display.add_widget(MDLabel(text="Tidak dijumpai"))
            self.add_widget(box__display)
            return self
        build_title(self.lemma.nama, container=box__display, mode=mode)
        build_konsep_list(self.lemma.konsep, container=box__display, mode=mode)
        self.add_widget(box__display)
        return self

    def on_lemma(self, instance, value: LemmaData) -> None:
        self.build()


class MainApp(MDApp):
    data = ObjectProperty()

    def build(self) -> Widget:
        self.theme_cls.theme_style = "Dark"
        return self.root

    def menu_callback(self, text):
        print(text)

    def search(self, *args):
        data: LemmaData = (
            LemmaQueryBuilder(lemma=self.root.ids["lemma_field"].text)
            .get_cakupan()
            .get_kata_asing()
            .collect()
        )
        self.root.ids["datacard"].lemma = data


if __name__ == "__main__":
    on_start()
    MainApp().run()
