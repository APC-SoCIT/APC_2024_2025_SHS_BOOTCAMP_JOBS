from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

Window.size = (360, 640)

# Custom Image Button for stars
class StarButton(ButtonBehavior, Image):
    def __init__(self, index, callback, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.callback = callback
        self.source = 'star_outline.png'

    def on_press(self):
        self.callback(self.index)

# Main screen layout
class RatingScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=20, padding=20, **kwargs)
        self.rating = 0

        with self.canvas.before:
            Color(0.93, 0.92, 0.89, 1)  # Light beige background
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # Top red header
        self.add_widget(self._header())

        self.add_widget(Label(text="Rate Your Experience", font_size=30, color=(0, 0, 0, 1), size_hint=(1, 0.1)))


        # Star row
        self.star_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, 0.2))
        self.stars = []
        for i in range(5):
            star = StarButton(index=i + 1, callback=self.set_rating)
            self.stars.append(star)
            self.star_layout.add_widget(star)
        self.add_widget(self.star_layout)

        # Feedback input
        self.feedback_input = TextInput(hint_text="Leave feedback...", size_hint=(1, 0.3), background_color=(0.8, 0.8, 0.8, 1), foreground_color=(0, 0, 0, 1), padding=10)
        self.add_widget(self.feedback_input)

        # Submit button
        submit_btn = Button(
            text="Submit",
            size_hint=(1, 0.15),
            background_color=(0.87, 0.22, 0.27, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            border=(20, 20, 20, 20)
        )
        submit_btn.bind(on_press=self.submit)
        self.add_widget(submit_btn)

    def _update_rect(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def _header(self):
        header = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), padding=(10, 10), spacing=10)

        back_btn = Button(
            text="<",
            size_hint=(None, 1),
            width=50,
            background_color=(0.87, 0.22, 0.27, 1),  # red
            color=(1, 1, 1, 1),
            font_size=20
    )
        header.add_widget(back_btn)
        header.add_widget(Label())  # Filler

        with header.canvas.before:
            Color(0.87, 0.22, 0.27, 1)  # red header background
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(size=lambda inst, val: setattr(self.header_bg, 'size', val))
        header.bind(pos=lambda inst, val: setattr(self.header_bg, 'pos', val))

        return header

    def _footer(self):
        footer = Widget(size_hint=(1, 0.05))
        with footer.canvas.before:
            Color(0.9, 0.2, 0.2, 1)
            footer.bg = Rectangle(size=footer.size, pos=footer.pos)
        footer.bind(size=lambda inst, val: setattr(footer.bg, 'size', val))
        footer.bind(pos=lambda inst, val: setattr(footer.bg, 'pos', val))
        return footer

    def set_rating(self, rating):
        self.rating = rating
        for i, star in enumerate(self.stars):
            star.source = 'star_filled.png' if i < rating else 'star_outline.png'

    def submit(self, instance):
        popup = Popup(
            title="Thank You!",
            content=Label(text=f"You rated {self.rating} star(s)\nFeedback: {self.feedback_input.text}"),
            size_hint=(0.7, 0.4),
        )
        popup.open()


class RatingApp(App):
    def build(self):
        return RatingScreen()


if __name__ == '__main__':
     RatingApp().run()
