from kivymd.app import MDApp
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget
from kivy.properties import StringProperty

from samudra.startup import on_start
from samudra.interfaces import LemmaQueryBuilder


class MainApp(MDApp):
    lemma_data_heading = StringProperty()
    lemma_data_konsep = StringProperty("test")
    lemma_data_golongan_kata = StringProperty()
    lemma_data_cakupan = StringProperty()

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
        # TODO Error handling for cakupan and kata_asing if not exist
        data = (
            LemmaQueryBuilder(lemma=self.root.ids["lemma_field"].text)
            .get_cakupan()
            .get_kata_asing()
        )
        if (konsep := data.collect()) is not None:
            self.lemma_data_heading = konsep.lemma.nama
            self.lemma_data_golongan_kata = konsep.golongan.nama
            self.lemma_data_konsep = konsep.keterangan
            self.lemma_data_cakupan = str(konsep.cakupan.get().cakupan.nama)
        else:
            self.lemma_data_konsep = konsep


if __name__ == "__main__":
    on_start()
    MainApp().run()
