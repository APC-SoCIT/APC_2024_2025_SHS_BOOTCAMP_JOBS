from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.write()

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.font_definitions import theme_font_styles
from datetime import datetime, timedelta

import firebase_admin
from firebase_admin import credentials, firestore

print("sumakses")

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_earnings_for_date(user_id, target_date):
    jobs_ref = db.collection("jobs")
    query = jobs_ref.where("worker_id", "==", user_id) \
                    .where("status", "==", "completed") \
                    .where("completed_date", "==", target_date).stream()
    total = 0
    for job in query:
        job_data = job.to_dict()
        total += job_data.get("earnings", 0)
    return total

class TrackingEarningsScreen(MDScreen):
    def update_total_earnings(self):
        try:
            today = int(self.ids.today_earning.text.replace("₱", "").replace(",", ""))
            yesterday = int(self.ids.yesterday_earning.text.replace("₱", "").replace(",", ""))
        except Exception:
            today = 0
            yesterday = 0

        total = today + yesterday
        self.ids.total_amount_label.text = f"₱{total:,}"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session_start_earnings = 0
        self.session_earnings = 0

    def on_enter(self):
        self.update_earnings()
        self.update_total_earnings()

    def update_earnings(self):
        app = MDApp.get_running_app()
        user_id = app.logged_in_user_id or "example_user_id"

        today_date = datetime.now().strftime("%Y-%m-%d")
        yesterday_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        today_earnings = get_earnings_for_date(user_id, today_date)
        yesterday_earnings = get_earnings_for_date(user_id, yesterday_date)

        self.ids.today_earning.text = f"₱{today_earnings:,}"
        self.ids.yesterday_earning.text = f"₱{yesterday_earnings:,}"

        self.update_total_earnings()

        total = today_earnings + yesterday_earnings

        if self.session_start_earnings == 0:
            self.session_start_earnings = total

        self.session_earnings = total - self.session_start_earnings 

        if self.ids.get("earnings_label"):
            self.ids.earnings_label.text = f"Total Earnings: ₱{total:,}"

        print(f"User: {user_id} | Today: ₱{today_earnings}, Yesterday: ₱{yesterday_earnings}, Total: ₱{total}, Session Earnings: ₱{self.session_earnings}")

class EarningsApp(MDApp):
    logged_in_user_id = None 

    def build(self):
        Builder.load_file("tracker.kv")
        return TrackingEarningsScreen()

    def on_view_all_pressed(self):
        print("View All clicked!")

    def set_logged_in_user(self, user_id):
        self.logged_in_user_id = user_id
        print(f"Logged in user set to: {user_id}")

if __name__ == "__main__":
    EarningsApp().run()
