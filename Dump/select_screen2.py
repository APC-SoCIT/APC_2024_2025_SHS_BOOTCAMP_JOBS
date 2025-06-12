from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder


class SelectScreen(MDScreen):
    def on_worker_press(self):
        print("👷‍♂️ Worker option selected")

    def on_employer_press(self):
        print("💼 Employer option selected")

class SelectApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        Builder.load_file("select_screen.kv")
        return SelectScreen()

if __name__ == '__main__':
    SelectApp().run()
