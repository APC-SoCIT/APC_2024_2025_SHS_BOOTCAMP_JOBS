from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout


Builder.load_file('jobscreen1.kv')


class JobScreen1(BoxLayout):  
    def spinner_clicked(self, value):
        self.ids.spinner_id.text = f'{value}'


class SampleApp(MDApp):  
    def build(self):
        self.theme_cls.theme_style = "Dark"  
        self.theme_cls.primary_palette = "Blue"  
        return JobScreen1()


if __name__ == '__main__':
    SampleApp().run()