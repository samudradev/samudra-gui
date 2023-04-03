from kivymd.app import MDApp
from kivymd.uix.textfield.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.widget import Widget

from samudra.startup import on_start
from samudra.interfaces import LemmaQueryBuilder

class MainApp(MDApp):
    def build(self) -> Widget:
        self.theme_cls.theme_style = "Dark"
        menu_items = [
            {
                "text": i,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=f"Item {i}": self.menu_callback(x),
            } for i in ['edit', 'delete']
        ]
        self.menu = MDDropdownMenu(
            caller=self.root.ids.menu_button,
            items=menu_items,
            width_mult=4
        )
        return self.root

    def menu_callback(self, text):
        print(text)

    def search(self, *args):
        data = LemmaQueryBuilder(konsep='',lemma=self.root.ids['lemma_field'].text).get_cakupan().get_kata_asing()
        print(data.collect())

if __name__ == '__main__':
    on_start()
    MainApp().run()