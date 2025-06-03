from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

class JobScreen2(MDScreen):
    def add_card(self, text):
        card = MDCard(
            style="filled",
            orientation="vertical",
            padding=dp(10),
            size_hint=(None, None), 
            size=(self.ids.job_grid.width / 2 - dp(20), dp(100)), 
            ripple_behavior=True,
        )
        card.add_widget(MDLabel(
            text=text,
            halign="center",
            valign="middle",
            text_size=(card.width - dp(20), None)
        ))
        self.ids.job_grid.add_widget(card)


class AddJobScreen(MDScreen):
    def submit_text(self):
        location = self.ids.input_location.text.strip()
        time = self.ids.input_time.text.strip()
        salary = self.ids.input_salary.text.strip()

        if location or time or salary:
            text = f"Location: {location}\nTime: {time}\nSalary: {salary}"
            job_screen = self.manager.get_screen('job_screen')
            job_screen.add_card(text)

            # Clear inputs
            self.ids.input_location.text = ""
            self.ids.input_time.text = ""
            self.ids.input_salary.text = ""

            # Go back to job screen
            self.manager.current = 'job_screen'


class SampleApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("jobs2.kv")


if __name__ == '__main__':
    SampleApp().run()
