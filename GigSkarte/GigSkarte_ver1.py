from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.label import Label


# --- Database ---
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)


# --- Auth screens ---

class SignUpScreen(Screen):
    def sign_up(self):
        email = self.ids.email.text
        phone = self.ids.phone.text
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        birthdate = self.ids.birthdate.text

        print("Signed Up:")
        print(f"Email: {email}")
        print(f"Phone: {phone}")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Birthdate: {birthdate}")

        self.manager.current = 'select'

class LoginScreen(Screen):
    def login(self):
        phone = self.ids.phone.text
        birthdate = self.ids.birthdate.text

        print("Logged In:")
        print(f"Phone: {phone}")
        print(f"Birthdate: {birthdate}")

        self.manager.current = 'select'


# --- Select screen ---

class SelectScreen(Screen):
    def on_worker(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'interests'  # worker flow goes to interests first

    def on_employer(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'job_screen'  # employer flow goes to job screen with add


# --- Interests screen (Worker flow) ---

class InterestsScreen(Screen):
    def process_interests(self):
        selected = [btn.text for btn in self.ids.grid_layout.children if btn.state == 'down']
        selected.reverse()  # because children are reversed
        print("Selected Interests:")
        for item in selected:
            print("-", item)
        # After selecting interests, show worker jobs screen
        self.manager.current = 'job_screen_1'



# --- Worker Job Screen (no add job button) ---

class JobScreen1(Screen):
    def spinner_clicked(self, value):
        self.ids.spinner_id.text = f'{value}'

    def show_job_details(self):
        self.manager.current = 'job_details'


# --- Job Details Screen (for worker) ---

class JobDetailsScreen(Screen):
    def accept_job(self):
        popup = Popup(
            title='Job Accepted',
            content=Label(text='You have accepted the job offer.'),
            size_hint=(0.6, 0.4)
        )
        popup.open()


# --- Employer Job Screen (with add job button) ---

class JobScreen2(Screen):
    def add_card(self, job_title, location, time, salary):
        text = f"{job_title}\nLocation: {location}\nTime: {time}\nSalary: {salary}"
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


# --- Editable Job Screen (for employers to add jobs) ---

class EditableJobScreen(Screen):
    def save_details(self):
        title = self.ids.edit_title.text.strip()
        location = self.ids.edit_location.text.strip()
        time = self.ids.edit_time.text.strip()
        salary = self.ids.edit_salary.text.strip()

        if title and location and time and salary:
            job_screen = self.manager.get_screen('job_screen')
            job_screen.add_card(title, location, time, salary)

            self.ids.edit_title.text = ""
            self.ids.edit_location.text = ""
            self.ids.edit_time.text = ""
            self.ids.edit_salary.text = ""

            popup = Popup(
                title='Job Added',
                content=Label(text='The job has been added to your list.'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

            self.manager.current = "job_screen"



class CombinedApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("GigSkarte_ver1.kv")


if __name__ == '__main__':
    CombinedApp().run()

