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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.properties import StringProperty

from kivymd.font_definitions import theme_font_styles
from kivy.core.window import Window

# Database 



# 

Window.size = (360, 640)

print(theme_font_styles)

# Authentication

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

# saving to database & to app (sign up)         
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

# saving to database & to app (log in)
        try:
            user_doc = db.collection('users').document(phone).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                if user_data.get('birthdate') == birthdate and user_data.get('password') == password:
                    print("User logged in successfully!")

                    app = MDApp.get_running_app()
                    app.current_user = user_data

                    if not hasattr(app, 'session'):
                        app.session = {}
                    app.session['user'] = user_data

                    role = user_data.get('role', None)

                    if role == 'worker':
                        interest = user_data.get('interests', [])
                        if interest:
                            self.manager.current = 'job_screen_1'
                        else:
                            self.manager.current = 'interests'
                    elif role == 'employer':
                        self.manager.current = 'job_screen'
                    else:
                        self.manager.current = "select"
                else:
                    print("Incorrect birthdate or password.")
            else:
                print("User not found. Please sign up first.")
        except Exception as e:
            print(f"Error fetching data: {e}")


# User role/type select

class SelectScreen(Screen):
    def on_worker(self):
        self.save_user_role('worker')
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'interests'

    def on_employer(self):
        self.save_user_role('employer')
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'job_screen'

    def save_user_role(self, role):
        try:
            app = MDApp.get_running_app()
            user_id = None
            if hasattr(app, 'session') and 'user' in app.session:
                user_id = app.session['user'].get('phone')
            elif hasattr(app, 'current_user'):
                user_id = app.current_user.get('phone')

            if not user_id:
                print("User ID not found in session or current user!")
                user_id = 'fallback_user'
                return

            doc_ref = db.collection('users').document(user_id)
            doc_ref.set({'role': role}, merge=True)
            print(f"Role '{role}' saved for user {user_id}")

            
            if not hasattr(app, 'session'):
                app.session = {}
            if 'user' not in app.session:
                app.session['user'] = {}

            app.session['user']['role'] = role
            print(f"Session updated with role: {role}")

        except Exception as e:
            print(f"Error saving role: {e}")

# Interests screen (Worker)

class InterestsScreen(Screen):
    def process_interests(self):
        selected = [btn.text for btn in self.ids.grid_layout.children if btn.state == 'down']
        selected.reverse()

        print("Selected Interests:")
        for item in selected:
            print("-", item)

        try:
            app = MDApp.get_running_app()

            user_id = None
            if hasattr(app, 'session') and 'user' in app.session:
                user_id = app.session['user'].get('phone')
            elif hasattr(app, 'current_user'):
                user_id = app.current_user.get('phone')

            if not user_id:
                print("User ID not found in session or current_user!")
                return

            doc_ref = db.collection('users').document(user_id)
            doc_ref.set({'interests': selected}, merge=True)
            print("Interests saved successfully!")

           
            if not hasattr(app, 'session'):
                app.session = {}
            if 'user' not in app.session:
                app.session['user'] = {}

            app.session['user']['interests'] = selected
            print(f"Session updated with interests: {selected}")

        except Exception as e:
            print(f"Error saving interests: {e}")

        self.manager.current = 'job_screen_1'

# Worker Job Screen 

class JobScreen1(Screen):
    def on_enter(self):
        print("Entered JobScreen1")
        self.session_viewed_jobs = 0
        self.total_jobs_loaded = 0 
        self.load_jobs_from_db()
    

    def load_jobs_from_db(self):
        self.ids.job_grid_1.clear_widgets()

        try:
            jobs_ref = db.collection('jobs')
            jobs = jobs_ref.stream()

            job_count = 0

            for job in jobs:
                job_data = job.to_dict()
                job_count += 1

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
                        self.session_viewed_jobs += 1
                        print(f"Jobs viewed this session: {self.session_viewed_jobs}")
                        details_screen = self.manager.get_screen('job_details')
                        details_screen.set_job_details(job_data) 
                        self.manager.current = 'job_details'

                card.bind(on_touch_down=on_card_touch)
                self.ids.job_grid_1.add_widget(card)

            self.total_jobs_loaded = job_count
            print(f"Total jobs loaded: {self.total_jobs_loaded}")

        except Exception as e:
            popup = Popup(
                title='Database Error',
                content=Label(text=f'Failed to load jobs: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

# Job Details Screen

class JobDetailsScreen(Screen):
    job_data = {}

    def set_job_details(self, job_data):
        self.job_data = job_data

    def on_pre_enter(self):
        self.ids.job_title.text = f"Job: {self.job_data.get('title', '')}"
        self.ids.job_location.text = f"Location: {self.job_data.get('location', '')}"
        self.ids.job_time.text = f"Date & Time: {self.job_data.get('time', '')}"
        self.ids.job_salary.text = f"Salary: ₱{self.job_data.get('salary', '')}"

    def accept_job(self):
        job_id = self.job_data.get('id')
        user_id = current_user.get('uid')


        db.collection("jobs").document(job_id).update({
            "status": "accepted",
            "accepted_by": user_id
        })

        db.collection("users").document(user_id).collection("accepted_jobs").add({
            "job_id": job_id,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        popup = Popup(
            title='Job Accepted',
            content=Label(text='You have accepted the job offer.'),
            size_hint=(0.6, 0.4)
        )
        popup.open()

# Employer Job Screen

class JobScreen2(Screen):
    jobs_posted_this_session = 0

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

        JobScreen2.jobs_posted_this_session += 1
        print(f"Jobs Posted This Session: {JobScreen2.jobs_posted_this_session}")

    def load_jobs_from_db(self):
        self.ids.job_grid.clear_widgets()
        
        jobs_ref = db.collection('jobs')
        docs = jobs_ref.stream()

        for doc in docs:
            job = doc.to_dict()
            self.add_card(
                job_title=job.get('job_title', 'No Title'),
                location=job.get('location', 'No Location'),
                time=job.get('time', 'No Time'),
                salary=job.get('salary', 'No Salary')
            )

# Job List Creation

class EditableJobScreen(Screen):
    jobs_added_this_session = 0 

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
            job_screen.load_jobs_from_db()

            self.ids.edit_title.text = ""
            self.ids.edit_location.text = ""
            self.ids.edit_time.text = ""
            self.ids.edit_salary.text = ""

            
            EditableJobScreen.jobs_added_this_session += 1
            print(f"Jobs Added This Session: {EditableJobScreen.jobs_added_this_session}")

            popup = Popup(
                title='Job Added',
                content=Label(text='The job has been added to your list.'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

            self.manager.current = "job_screen"

# Pending Screen
class JobBox(BoxLayout):
    job_title = StringProperty("")
    location = StringProperty("")
    salary = StringProperty("")
    date_time = StringProperty("")


class PendingJobsScreen(Screen):
    def on_kv_post(self, base_widget):
        pass  

    def add_job(self, job_data):
        job_box = JobBox(
            text=f"{job_data.get('title')} - {job_data.get('location')}- {job_data.get('time')} - {job_data.get('salary')}",
            size_hint_y=None,
            height=dp(40),
            job_title=job_data["title"],
            location=job_data["location"],
            salary=job_data["salary"],
            date_time=job_data["date_time"]
        )
        self.ids.job_list.add_widget(job_box)

    def clear_jobs(self):
        self.ids.job_list.clear_widgets()

    def go_back(self):
        App.get_running_app().stop()

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
    
# Accepted Job Screen 
class AcceptedJobsScreen(Screen):
    def on_kv_post(self, base_widget):
        pass

    def add_job(self, job_data):
        job_box = JobBox(
            job_title=job_data["title"],
            location=job_data["location"],
            salary=job_data["salary"],
            date_time=job_data["date_time"]
        )
        self.ids.job_list.add_widget(job_box)

    def clear_jobs(self):
        self.ids.job_list.clear_widgets()

    def go_back(self):
        App.get_running_app().stop() 


if __name__ == '__main__':
    CombinedApp().run()
