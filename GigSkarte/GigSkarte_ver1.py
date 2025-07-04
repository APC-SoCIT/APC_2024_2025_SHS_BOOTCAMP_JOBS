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
from datetime import datetime
from kivy.metrics import dp, sp
from kivy.core.text import Label as CoreLabel
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

from kivymd.font_definitions import theme_font_styles
from kivy.core.window import Window

# --- Database ---



# ------------------

Window.size = (380, 740)

print(theme_font_styles)

# Authentication

class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        self.year_list = self.generate_years()

    def generate_years(self):
        current_year = datetime.now().year
        return [str(year) for year in range(current_year, 1969, -1)]
    
    def on_kv_post(self, base_widge):
        self.ids.birth_year.values = self.year_list


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
        
        if not phone or password == "Password": 
            print("Please fill all required fields!")
            return
        
        
        print("Logged In:")
        print(f"Phone: {phone}")
        print(f"Password: {password}")
        
        self.manager.current = "select"

# saving to database & to app (log in)
        try:
            user_doc = db.collection('users').document(phone).get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                if user_data.get('password') == password:
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
                job_data['id'] = job.id
                
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
                    height=dp(120),
                    ripple_behavior=True,
                )
                card.add_widget(MDLabel(
                    text=text,
                    halign="center",
                    valign="middle",
                    text_size=(card.width - dp(20), None), 
                    size_hint_y=(1, None),
                    height=self.get_label_height(text) 
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

    def get_label_height(self, text):
        label = CoreLabel(text=text, font_size=sp(14), halign='center', valign='middle', text_size=(self.ids.job_grid_1.width * 0.45 - dp(20), None))
        label.refresh()
        return label.texture.size[1] + dp(10) 


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
        self.ids.job_number.text = f"Phone Number: {self.job_data.get('phone_number', '')}"
        self.ids.job_employer.text = f"Employer: {self.job_data.get('employer_name', '')}"

    def accept_job(self):
        job_id = self.job_data.get('id')

        if not job_id:
            print("Error: job_id is missing. Cannot accept job.")
            return
        
        app = MDApp.get_running_app()
        user_id = app.current_user.get('phone')

        if user_id is None:
            print("User ID not found!")
            return

        try:
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

            self.manager.current = 'pending_jobs'
        except Exception as e:
            print(f"Error accepting job {e}")

# Employer Job Screen

class JobScreen2(Screen):
    jobs_posted_this_session = 0
    def on_enter(self):
        self.load_jobs_from_db()

    def add_card(self, job_title, location, time, salary, job_id):
        text = f"{job_title}\nLocation: {location}\nTime: {time}\nSalary: {salary}"
        card = MDCard(
            style="filled",
            orientation="vertical",
            padding=dp(10),
            size_hint=(None, None),
            size=(self.ids.job_grid.width / 2 - dp(20), dp(130)),
            ripple_behavior=True,
            md_bg_color=get_color_from_hex('DD3846')
        )
        card.add_widget(MDLabel(
            text=text,
            halign="center",
            valign="middle",
            text_size=(card.width - dp(20), None)
        ))

        card.bind(on_touch_down=lambda instance, touch, job_id=job_id: self.on_card_touch(instance, touch, job_id))

        self.ids.job_grid.add_widget(card)

        JobScreen2.jobs_posted_this_session += 1
        print(f"Jobs Posted This Session: {JobScreen2.jobs_posted_this_session}")

    def on_card_touch(self, instance, touch, job_id):
        if instance.collide_point(*touch.pos):
            print("Card touched, switching to accepted jobs")
            app = MDApp.get_running_app()
            app.current_job_id = job_id
            self.manager.current = 'accepted_jobs' 

    def load_jobs_from_db(self):
        self.ids.job_grid.clear_widgets()
        
        jobs_ref = db.collection('jobs')
        docs = jobs_ref.stream()

        for doc in docs:
            job = doc.to_dict()
            self.add_card(
                job_title=job.get('title', 'No Title'),
                location=job.get('location', 'No Location'),
                time=job.get('time', 'No Time'),
                salary=job.get('salary', 'No Salary'),
                job_id=doc.id
            )

# Job List Creation Screen

class EditableJobScreen(Screen):
    jobs_added_this_session = 0 

    def save_details(self):
        title = self.ids.edit_title.text.strip()
        location = self.ids.edit_location.text.strip()
        time = self.ids.edit_time.text.strip()
        salary = self.ids.edit_salary.text.strip()

        if not title or not location or not time or not salary:
            popup = Popup(
                title='Validation Error',
                content=Label(text='Please fill in all job details.'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            return

        app = MDApp.get_running_app()
        user_id = app.current_user.get('phone') if app.current_user else None

        if not user_id:
            popup = Popup(
                title='User  Error',
                content=Label(text='User  not logged in. Cannot create job.'),
                size_hint=(0.6, 0.4)
            )
            popup.open()
            return

        user_doc = db.collection('users').document(user_id).get()
        employer_name = f"{user_doc.to_dict().get('first_name', '')} {user_doc.to_dict().get('last_name', '')}"

        job_data = {
            "title": title,
            "location": location,
            "time": time,
            "salary": salary,
            "phone_number": user_id,
            "creator_id": user_id,
            "employer_name": employer_name 
        }

        try:
            db.collection('jobs').add(job_data)

            # Clear input fields
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

        except Exception as e:
            popup = Popup(
                title='Database Error',
                content=Label(text=f'Failed to save job: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

# Pending Screen (Worker)

class JobBox(BoxLayout):
    job_title = StringProperty("")
    location = StringProperty("")
    salary = StringProperty("")
    date_time = StringProperty("")
    status = StringProperty("Ongoing")
    job_id = StringProperty("")
    job_number = StringProperty("")

    def complete_job(self):
        app = MDApp.get_running_app()
        try:
            db.collection("jobs").document(self.job_id).update({
                "status": "completed"
            })
            popup = Popup(
                title='Success',
                content=Label(text='Job marked as completed!'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

            feedback_screen = app.root.get_screen('rating_screen')
            feedback_screen.job_id = self.job_id  
            app.root.current = 'rating_screen'

            pending_screen = app.root.get_screen('pending_jobs')
            pending_screen.load_pending_jobs()
        except Exception as e:
            popup = Popup(
                title='Error',
                content=Label(text=f'Could not update job status: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

class PendingJobsScreen(Screen):
    def on_enter(self):
        self.load_pending_jobs()

    def clear_jobs(self):
        self.ids.job_list.clear_widgets()

    def load_pending_jobs(self):
        self.clear_jobs()
        app = MDApp.get_running_app()
        user_id = app.current_user.get('phone') if app.current_user else None
        if not user_id:
            print("No current user found for loading pending jobs.")
            return

        try:
            jobs_ref = db.collection('jobs')
            query = jobs_ref.where('status', '==', 'accepted').where('accepted_by', '==', user_id)
            docs = query.stream()

            any_jobs = False
            for doc in docs:
                job_data = doc.to_dict()
                job_data['id'] = doc.id
                job_data['status'] = "Ongoing"
                self.add_job(job_data)
                any_jobs = True
                print(f"Found job: {job_data}")

            if not any_jobs:
                print("No pending jobs found.")
        except Exception as e:
            print(f"Error loading pending jobs: {e}")

    def add_job(self, job_data):
        print(f"Adding job to UI: {job_data}")
        job_box = JobBox(
            job_title=job_data.get("title", "No title"),
            location=job_data.get("location", "No location"),
            salary=job_data.get("salary", "No salary"),
            date_time=job_data.get("time", "No time"),
            job_number=job_data.get("phone_number", "No number"),
            status=job_data.get("status", "Ongoing"),
            job_id=job_data.get('id', "")
        )

        job_box.size_hint_y = None
        job_box.height = dp(120)

        complete_button = Button(
            text="Complete",
            size_hint=(None, None),
            size=(dp(100), dp(40)),
            pos_hint={"center_x": 0.5}
        )
        complete_button.bind(on_release=lambda x: job_box.complete_job())
        job_box.add_widget(complete_button)

        self.ids.job_list.add_widget(job_box)
    
# Accepted Job Screen (Employer)

class AcceptedJobsScreen(Screen):
    def on_enter(self):

        self.load_accepted_jobs()

    def clear_jobs(self):
        self.ids.job_list.clear_widgets()

    def add_job(self, job_data):

        class JobBox(BoxLayout):
            job_title = StringProperty("")
            location = StringProperty("")
            salary = StringProperty("")
            date_time = StringProperty("")
            status = StringProperty("Accepted")
            job_number= StringProperty("")
            job_id = StringProperty("")

        job_box = JobBox(
            job_title=job_data.get("title") or "No title",
            location=job_data.get("location") or "No location",
            salary=str(job_data.get("salary") or "No salary"),
            date_time=job_data.get("time") or "No time",
            job_number=job_data.get("phone_number", "No number"),
            status=job_data.get("status") or "Accepted",

            job_id=job_data.get("id") or ""
        )
        self.ids.job_list.add_widget(job_box)

    def load_accepted_jobs(self):
        """Query Firestore and load accepted jobs for the logged-in employer."""
        self.clear_jobs()
        app = MDApp.get_running_app()
        user_id = None      
        try:
            user_id = app.current_user.get('phone')
        except Exception as e:
            print(f"[AcceptedJobsScreen] Failed to get current user id: {e}")

        print(f"[AcceptedJobsScreen] Loading accepted jobs for user_id: {user_id}")

        if not user_id:
            print("[AcceptedJobsScreen] No logged in employer user ID found.")
            label = MDLabel(
                text="Please log in to view accepted jobs.",
                halign="center",
                theme_text_color="Hint",
                font_style="Subtitle1",
                size_hint_y=None,
                height=dp(50)
            )
            self.ids.job_list.add_widget(label)
            return

        try:
            jobs_ref = firestore.client().collection('jobs')

            query_1 = jobs_ref.where('status', '==', 'accepted').where('creator_id', '==', user_id)
            query_2 = jobs_ref.where('status', '==', 'accepted').where('creator_id', '==', 'fallback_user')

            docs_1 = list(query_1.stream())
            docs_2 = list(query_2.stream())

            total_docs = docs_1 + docs_2
            any_jobs = False

            for doc in total_docs:
                job_data = doc.to_dict()
                print(f"[AcceptedJobsScreen] Job loaded: {job_data}")
                job_data['id'] = doc.id
                self.add_job(job_data)
                any_jobs = True

            if not any_jobs:
                print("[AcceptedJobsScreen] No accepted jobs found for employer.")
                label = MDLabel(
                    text="No accepted jobs found.",
                    halign="center",
                    theme_text_color="Hint",
                    font_style="Subtitle1",
                    size_hint_y=None,
                    height=dp(50)
                )
                self.ids.job_list.add_widget(label)

        except Exception as e:
            print(f"[AcceptedJobsScreen] Error loading accepted jobs: {e}")
            popup = Popup(
                title='Database Error',
                content=Label(text=f'Failed to load accepted jobs: {e}'),
                size_hint=(0.6, 0.4)
            )
            popup.open()

    def go_back(self):
        self.manager.current = "job_screen"

# --- Feedback ---
class StarButton(ButtonBehavior, Image):
    def __init__(self, index, callback, **kwargs):
        super().__init__(**kwargs)
        self.index = index
        self.callback = callback
        self.source = 'star_outline.jpg'

    def on_press(self):
        self.callback(self.index)

class RatingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stars = []
        self.rating = 0

    def on_kv_post(self, base_widget):
        for i in range(5):
            star = StarButton(index=i + 1, callback=self.set_rating)
            self.stars.append(star)
            self.ids.star_layout.add_widget(star)

    def set_rating(self, rating):
        self.rating = rating
        for i, star in enumerate(self.stars):
            star.source = 'star_filled.jpg' if i < rating else 'star_outline.jpg'

    def submit(self):
        popup = Popup(
            title="Thank You!",
            content=Label(text=f"You rated {self.rating} star(s)\nFeedback: {self.ids.feedback_input.text}"),
            size_hint=(0.7, 0.4),
        )
        popup.open()

class CombinedApp(MDApp):
    current_user = None
    def build(self):
        return Builder.load_file("GigSkarte_ver1.kv")

if __name__ == '__main__':
    CombinedApp().run()