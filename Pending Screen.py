from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

Window.size = (400, 700)

class JobBox(BoxLayout):
    def __init__(self, job_title, location, salary, date_time, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, size_hint_y=None, height=180, **kwargs)

        with self.canvas.before:
            Color(1, 0, 0, 1)  # red background
            self.rect = RoundedRectangle(radius=[10], pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        info_grid = GridLayout(cols=2, spacing=5, size_hint_y=None, height=160)

        def aligned_label(text, bold=False):
            label = Label(
                text=f"[b]{text}[/b]" if bold else text,
                markup=True,
                halign="left" if bold else "right",
                valign="middle"
            )
            label.bind(size=label.setter('text_size'))
            return label

        info_grid.add_widget(aligned_label("Job Title:", True))
        info_grid.add_widget(aligned_label(job_title))

        info_grid.add_widget(aligned_label("Location:", True))
        info_grid.add_widget(aligned_label(location))

        info_grid.add_widget(aligned_label("Salary:", True))
        info_grid.add_widget(aligned_label(salary))

        info_grid.add_widget(aligned_label("Date & Time:", True))
        info_grid.add_widget(aligned_label(date_time))

        info_grid.add_widget(aligned_label("Status:", True))

        self.add_widget(info_grid)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class PendingJobsScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10)

        # Background color
        with self.canvas.before:
            Color(0.96, 0.93, 0.89, 1)  # light cream
            self.rect = RoundedRectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_background, size=self.update_background)

        # Top bar with back button
        top_bar = BoxLayout(size_hint_y=None, height=50, padding=5, spacing=5)
        top_bar.add_widget(Button(
            text="<", 
            font_size=24,
            background_color=(1, 1, 1, 1),
            color=(1, 0, 0, 1),
            size_hint_x=None, width=50,
            on_press=self.go_back
        ))
        self.add_widget(top_bar)

        # Title
        title = Label(
            text="[b]PENDING JOBS[/b]",
            markup=True,
            font_size=24,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=50,
            halign="center",
            valign="middle"
        )
        title.bind(size=title.setter('text_size'))
        self.add_widget(title)

        # Scroll view for job list
        scroll = ScrollView()
        job_list = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None, padding=10)
        job_list.bind(minimum_height=job_list.setter('height'))

        jobs = [
            ("   ", "    ", "    ", "    "),
            ("      ", "    ", "    ", "    "),
            ("   ", "   ", "    ", "    ")
        ]

        for job in jobs:
            job_list.add_widget(JobBox(*job))

        scroll.add_widget(job_list)
        self.add_widget(scroll)

    def update_background(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def go_back(self, instance):
        App.get_running_app().stop()

class PendingJobsApp(App):
    def build(self):
        return PendingJobsScreen()

if __name__ == '__main__':
    PendingJobsApp().run()
