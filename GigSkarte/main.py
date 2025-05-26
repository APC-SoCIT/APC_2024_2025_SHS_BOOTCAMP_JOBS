from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup



class SignUpScreen(Screen):
    def __init__(self, **kwargs):
        super(SignUpScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=2, padding=20, spacing=10)

        layout.add_widget(Label(text="Email (optional):"))
        self.email = TextInput(multiline=False)
        layout.add_widget(self.email)

        layout.add_widget(Label(text="Phone Number:"))
        self.phone = TextInput(multiline=False, input_filter='int')
        layout.add_widget(self.phone)

        layout.add_widget(Label(text="First Name:"))
        self.first_name = TextInput(multiline=False)
        layout.add_widget(self.first_name)

        layout.add_widget(Label(text="Last Name:"))
        self.last_name = TextInput(multiline=False)
        layout.add_widget(self.last_name)

        layout.add_widget(Label(text="Birthdate (YYYY-MM-DD):"))
        self.birthdate = TextInput(multiline=False)
        layout.add_widget(self.birthdate)

        self.submit_btn = Button(text="Sign Up")
        self.submit_btn.bind(on_press=self.sign_up)
        layout.add_widget(self.submit_btn)

        self.login_switch_btn = Button(text="Already have an account? Log In")
        self.login_switch_btn.bind(on_press=self.go_to_login)
        layout.add_widget(self.login_switch_btn)

        self.add_widget(layout)

    def sign_up(self, instance):
        print("Signed Up with:")
        print(f"Email: {self.email.text}")
        print(f"Phone: {self.phone.text}")
        print(f"First Name: {self.first_name.text}")
        print(f"Last Name: {self.last_name.text}")
        print(f"Birthdate: {self.birthdate.text}")

    def go_to_login(self, instance):
        self.manager.current = 'login'


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = GridLayout(cols=2, padding=20, spacing=10)

        layout.add_widget(Label(text="Phone Number:"))
        self.phone = TextInput(multiline=False, input_filter='int')
        layout.add_widget(self.phone)

        layout.add_widget(Label(text="Birthdate (YYYY-MM-DD):"))
        self.birthdate = TextInput(multiline=False)
        layout.add_widget(self.birthdate)

        self.login_btn = Button(text="Log In")
        self.login_btn.bind(on_press=self.login)
        layout.add_widget(self.login_btn)

        self.signup_switch_btn = Button(text="Don't have an account? Sign Up")
        self.signup_switch_btn.bind(on_press=self.go_to_signup)
        layout.add_widget(self.signup_switch_btn)

        self.add_widget(layout)

    def login(self, instance):
        print("Attempting Login with:")
        print(f"Phone: {self.phone.text}")
        print(f"Birthdate: {self.birthdate.text}")

    def go_to_signup(self, instance):
        self.manager.current = 'signup'


class AuthApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SignUpScreen(name='signup'))
        sm.add_widget(LoginScreen(name='login'))
        return sm


class JobDetailScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)

        header = BoxLayout(size_hint_y=0.1)
        back_button = Button(text="<")  
        header.add_widget(back_button)
        header.add_widget(Label(text="Employer's Name"))
        self.add_widget(header)

        self.add_widget(Label(text="Job: House Cleaning"))
        self.add_widget(Label(text="Location: Makati City"))
        self.add_widget(Label(text="Date & Time: May 25, 2025 - 9:00 AM"))
        self.add_widget(Label(text="Salary: ₱1,500"))

        accept_button = Button(
            text="Accept job offer",
            background_color=(1, 0, 0, 1),  
            size_hint_y=0.2
        )
        accept_button.bind(on_press=self.accept_job)
        self.add_widget(accept_button)

    def accept_job(self, instance):
        popup = Popup(
            title='Job Accepted',
            content=Label(text='You have accepted the job offer.'),
            size_hint=(0.6, 0.4)
        )
        popup.open()


class JobApp(App):
    def build(self):
        return JobDetailsScreen()

if __name__ == '__main__':
    JobApp().run()



if __name__ == '__main__':
    AuthApp().run()

