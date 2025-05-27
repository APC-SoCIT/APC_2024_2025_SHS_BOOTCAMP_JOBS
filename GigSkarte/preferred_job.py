from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class InterestsScreen(Screen):
    def __init__(self, **kwargs):
        super(InterestsScreen, self).__init__(**kwargs)

        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        main_layout.add_widget(Label(text="Choose Your Interest", font_size=28, size_hint=(1, 0.1)))

        main_layout.add_widget(Label(text="What kind of work are you into? Or what do you need help with?", 
                                     font_size=18, size_hint=(1, 0.1)))

        self.grid = GridLayout(cols=2, spacing=10, size_hint=(1, 0.7))

        self.interest_buttons = []
        interests = [
            "House Cleaning", "Laundry Folding & Ironing", "Dishwashing", "Gardening & Yardwork",
            "Home Organizing", "Dog Walking", "Pet Sitting", "Bathing & Grooming",
            "Elderly Assistance", "Babysitting", "Homework Tutoring", "Grocery Shopping",
            "Watering Plants", "Washing Clothes", "Taking out the Trash",
            "Decluttering Shelves", "Cleaning the Toilet", "Wiping Windows"
        ]

        for interest in interests:
            btn = ToggleButton(text=interest, size_hint_y=None, height=40)
            self.interest_buttons.append(btn)
            self.grid.add_widget(btn)

        main_layout.add_widget(self.grid)

        next_btn = Button(text="Next", size_hint=(1, 0.1), background_color=(0.2, 0.6, 0.8, 1))
        next_btn.bind(on_press=self.process_interests)
        main_layout.add_widget(next_btn)

        self.add_widget(main_layout)

    def process_interests(self, instance):
        selected = [btn.text for btn in self.interest_buttons if btn.state == 'down']
        print("Selected Interests:")
        for item in selected:
            print("-", item)


class TestApp(App):
    def build(self):
        return InterestsScreen()


if __name__ == '__main__':
    TestApp().run()
