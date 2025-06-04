from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivymd.uix.textfield import MDTextField

from kivymd.font_definitions import theme_font_styles
from kivy.core.window import Window

Window.size = (360, 640)

print(theme_font_styles)

# --- Auth screens ---

class SignUpScreen(Screen):
    def login(self):
        self.manager.current = "login" 
    def sign_up(self):
        first_name = self.ids.first_name.text.strip()
        last_name = self.ids.last_name.text.strip()
        phone = self.ids.phone.text.strip()
        email = self.ids.email.text.strip()
        password = self.ids.password.text.strip()
        birth_month = self.ids.birth_month.text
        birth_day = self.ids.birth_day.text
        birth_year = self.ids.birth_year.text
        
        if not first_name or not last_name or not phone or birth_month == "Month" or birth_day == "Day" or birth_year == "Year" or password == "Password":
            print("Please fill all required fields!")
            return
        
        birthdate = f"{birth_year}-{birth_month.zfill(2)}-{birth_day.zfill(2)}"
        
        print("Signed Up:")
        print(f"First Name: {first_name}")
        print(f"Last Name: {last_name}")
        print(f"Phone: {phone}")
        print(f"Email: {email} (optional)")
        print(f"Birthdate: {birthdate}")
        print(f"Password: {password}")
        
        self.manager.current = "select"

# --- saving to database & to app ---         
        try:
            db.collection('users').document(phone).set({
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'email': email,
                'password': password,
                'birthdate': birthdate
            })
            print("User signed up and data saved!")

            app = MDApp.get_running_app()
            if not hasattr(app, 'session'):
                app.session ={}
                
            app.session['user'] = {
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'email': email,
                'password': password,
                'birthdate': birthdate
            }

            self.manager.current = "select"

        except Exception as e:
            print(f"Error saving data: {e}")


class LoginScreen(Screen):
    def login(self):
        phone = self.ids.phone.text.strip()
        password = self.ids.password.text.strip()
        birth_month = self.ids.birth_month.text
        birth_day = self.ids.birth_day.text
        birth_year = self.ids.birth_year.text
        
        if not phone or birth_month == "Month" or birth_day == "Day" or birth_year == "Year" or password == "Password":
            print("Please fill all required fields!")
            return
        
        birthdate = f"{birth_year}-{birth_month.zfill(2)}-{birth_day.zfill(2)}"
        
        print("Logged In:")
        print(f"Phone: {phone}")
        print(f"Birthdate: {birthdate}")
        print(f"Password: {password}")
        
        self.manager.current = "select"

# --- saving to database & to app ---
        try:
            user_doc = db.collection('users').document(phone).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                if user_data.get('birthdate') == birthdate and user_data_get('password') == password:
                    print("User logged in successfully!")

                    app = MDApp.get_running_app()
                    app.current_user = user_data

                    self.manager.current = "select"
                else:
                    print("Incorrect birthdate or password.")
            else:
                print("User not found. Please sign up first.")
        except Exception as e:
            print(f"Error fetching data: {e}")


# --- Select screen ---

class SelectScreen(Screen):
    def on_worker(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'interests'

    def on_employer(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'job_screen'

# --- Interests screen (Worker flow) ---

class InterestsScreen(Screen):
    def process_interests(self):
        selected = [btn.text for btn in self.ids.grid_layout.children if btn.state == 'down']
        selected.reverse() 
        print("Selected Interests:")
        for item in selected:
            print("-", item)
        
        self.manager.current = 'job_screen_1'

# --- Worker Job Screen ---

class JobScreen1(Screen):
    def on_enter(self):
        print("Entered JobScreen1")
        self.load_jobs_from_db()

    def load_jobs_from_db(self):
        
        self.ids.job_grid_1.clear_widgets()

        try:
            jobs_ref = db.collection('jobs')
            jobs = jobs_ref.stream()

            for job in jobs:
                job_data = job.to_dict()
                title = job_data.get('title', 'No title')
                location = job_data.get('location', 'No location')
                time = job_data.get('time', 'No time')
                salary = job_data.get('salary', 'No salary')

                text = f"{title}\nLocation: {location}\nTime: {time}\nSalary: {salary}"

                card = MDCard(
                    style="outlined",
                    orientation="vertical",
                    padding=dp(10),
                    size_hint=(0.45, None), 
                    height=dp(100),
                    size=(self.ids.job_grid_1.width / 2 - dp(15), dp(100)),
                    ripple_behavior=True,
                )
                card.add_widget(MDLabel(
                    text=text,
                    halign="center",
                    valign="middle",
                    text_size=(card.width - dp(20), None)
                ))


                def on_card_touch(instance, touch, job_data=job_data):
                    if instance.collide_point(*touch.pos):
                        print("Card touched, switching to job_details")
                        details_screen = self.manager.get_screen('job_details')
                        details_screen.job_data = job_data 
                        self.manager.current = 'job_details'

                card.bind(on_touch_down=on_card_touch)

                self.ids.job_grid_1.add_widget(card)

        except Exception as e:
            popup = Popup(
                title='Database Error',
                content=Label(text=f'Failed to load jobs: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()


# --- Job Details Screen (for worker) ---

class JobDetailsScreen(Screen):
    job_data = {}

    def on_pre_enter(self):
        self.ids.job_title.text = f"Job: {self.job_data.get('title', '')}"
        self.ids.job_location.text = f"Location: {self.job_data.get('location', '')}"
        self.ids.job_time.text = f"Date & Time: {self.job_data.get('time', '')}"
        self.ids.job_salary.text = f"Salary: ₱{self.job_data.get('salary', '')}"

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
            md_bg_color=get_color_from_hex('DD3846')
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
            job_data = {
                "title": title,
                "location": location,
                "time": time,
                "salary": salary,
            }

            try:
                db.collection('jobs').add(job_data)
            except Exception as e:
                popup = Popup(
                    title='Database Error',
                    content=Label(text=f'Failed to save job: {e}'),
                    size_hint=(0.6, 0.4)
                )
                popup.open()
                return

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
    current_user = None
    def build(self):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.session = {}

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_file("GigSkarte_ver1.kv")


if __name__ == '__main__':
    CombinedApp().run()
