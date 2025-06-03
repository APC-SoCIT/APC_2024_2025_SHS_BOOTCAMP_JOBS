from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window

Window.size = (360, 640)

class SelectScreen(Screen):
    def __init__(self, **kwargs):
        super(SelectScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=30, padding=[40, 80])

        title = Label(
            text="Choose an Option",
            font_size='28sp',
            size_hint=(1, 0.3),
            halign='center',
            valign='middle'
        )
        layout.add_widget(title)

        worker_btn = Button(
            text="Become a Worker",
            size_hint=(1, 0.3),
            font_size='20sp',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        worker_btn.bind(on_release=lambda instance: self.manager.transition_to("worker"))
        layout.add_widget(worker_btn)

        employer_btn = Button(
            text="Become an Employer",
            size_hint=(1, 0.3),
            font_size='20sp',
            background_color=(0.1, 0.7, 0.3, 1)
        )
        employer_btn.bind(on_release=lambda instance: self.manager.transition_to("employer"))
        layout.add_widget(employer_btn)

        self.add_widget(layout)


class WorkerScreen(Screen):
    def __init__(self, **kwargs):
        super(WorkerScreen, self).__init__(**kwargs)
        self.add_widget(Label(text="Welcome, Worker!", font_size='24sp'))


class EmployerScreen(Screen):
    def __init__(self, **kwargs):
        super(EmployerScreen, self).__init__(**kwargs)
        self.add_widget(Label(text="Welcome, Employer!", font_size='24sp'))


class MyScreenManager(ScreenManager):
    def transition_to(self, screen_name):
        self.transition = SlideTransition(direction='left')
        self.current = screen_name


class SelectApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(SelectScreen(name='select'))
        sm.add_widget(WorkerScreen(name='worker'))
        sm.add_widget(EmployerScreen(name='employer'))
        return sm


if __name__ == '__main__':
    SelectApp().run()
    