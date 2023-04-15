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

    def build(self) -> Widget:
        self.clear_widgets()
        box = MDBoxLayout(padding=40)
        if self.lemma is None:
            box.add_widget(MDLabel(text="Tidak dijumpai"))
            self.add_widget(box)
            return self
        box.add_widget(MDLabel(text=self.lemma.nama, font_style="H2", underline=True))
        konsep_box = MDBoxLayout()
        for i, konsep in enumerate(self.lemma.konsep, 1):
            konsep_box.add_widget(
                MDLabel(
                    text="{}. [{:^6}] {}".format(
                        i, konsep.golongan.id, konsep.keterangan
                    )
                )
            )
            if len(konsep.kata_asing) > 0:
                slot__kataasing = MDBoxLayout(orientation="horizontal")
                for kata_asing_connector in konsep.kata_asing:
                    slot__kataasing.add_widget(
                        MDLabel(
                            text="{}: {}".format(
                                kata_asing_connector.kata_asing.bahasa,
                                kata_asing_connector.kata_asing.nama,
                            )
                        )
                    )
            if len(konsep.cakupan) > 0:
                slot__cakupan = MDBoxLayout(orientation="horizontal")
                for cakupan_connector in konsep.cakupan:
                    slot__cakupan.add_widget(
                        MDChip(text=cakupan_connector.cakupan.nama, padding=0)
                    )
                konsep_box.add_widget(slot__cakupan)
                konsep_box.add_widget(slot__kataasing)

        box.add_widget(konsep_box)
        # box.add_widget(MDLabel(text='\n'.join([f'{i}. {x.keterangan}' for i, x in enumerate(self.lemma.konsep, 1)])))
        self.add_widget(box)
        return self

    def on_lemma(self, instance, value: LemmaData) -> None:
        # self.lemma_nama = value.nama
        # self.lemma_konsep = '\n'.join([f'{i}. {x.keterangan}' for i, x in enumerate(value.konsep, 1)])
        # self.lemma_golongan_kata = value.konsep[0].golongan.id
        # self.lemma_cakupan = value.konsep[0].cakupan.__repr__()
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
