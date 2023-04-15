from kivymd.app import MDApp, Builder
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.chip import MDChip
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget

from kivy.properties import StringProperty, ObjectProperty, ListProperty

from samudra.startup import on_start
from samudra.interfaces import LemmaQueryBuilder, LemmaData


class DataCard(MDAnchorLayout):
    lemma: LemmaData = ObjectProperty("", allownone=True)
    anchor_x = "center"
    anchor_y = "center"
    padding = 25, 25, 25, 25

    def build(self) -> Widget:
        self.clear_widgets()
        box = MDBoxLayout(padding=30, adaptive_height=True)
        if self.lemma is None:
            box.add_widget(MDLabel(text="Tidak dijumpai"))
            self.add_widget(box)
            return self
        box.add_widget(MDLabel(text=self.lemma.nama, font_style="H2", underline=True, bold=True))
        konsep_box = MDBoxLayout(adaptive_height=True, spacing=5)
        for i, konsep in enumerate(self.lemma.konsep, 1):
            konsep_box.add_widget(
                MDLabel(
                    text="{}. [{:^6}] {}".format(
                        i, konsep.golongan.id, konsep.keterangan
                    ),
                )
            )
            if len(konsep.kata_asing) > 0:
                slot__kataasing = MDBoxLayout(orientation="horizontal", adaptive_height=True)
                for kata_asing_connector in konsep.kata_asing:
                    slot__kataasing.add_widget(
                        MDLabel(
                            text="    {}: {}".format(
                                kata_asing_connector.kata_asing.bahasa,
                                kata_asing_connector.kata_asing.nama,
                            ),
                            italic=True
                        )
                    )
                konsep_box.add_widget(slot__kataasing)
            if len(konsep.cakupan) > 0:
                slot__cakupan = MDBoxLayout(orientation="horizontal", adaptive_size=True)
                for cakupan_connector in konsep.cakupan:
                    slot__cakupan.add_widget(
                        MDChip(text=cakupan_connector.cakupan.nama, padding=0)
                    )
                konsep_box.add_widget(slot__cakupan)

        box.add_widget(konsep_box)
        self.add_widget(box)
        return self

    def on_lemma(self, instance, value: LemmaData) -> None:
        self.build()


class MainApp(MDApp):
    data = ObjectProperty()

    def build(self) -> Widget:
        self.theme_cls.theme_style = "Dark"
        menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            }
            for i in ["edit", "delete"]
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids["menu_button"], items=menu_items, width_mult=4
        )
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
