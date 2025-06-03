from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')
Config.write()

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

import firebase_admin
from firebase_admin import credentials, firestore

print("sumakses")

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  
    firebase_admin.initialize_app(cred)

db = firestore.client()

def get_total_earnings(user_id):
    jobs_ref = db.collection("jobs")
    query = jobs_ref.where("worker_id", "==", user_id).where("status", "==", "completed").stream()

    total = 0
    for job in query:
        job_data = job.to_dict()
        total += job_data.get("earnings", 0)

    return total

print("Test Earnings:", get_total_earnings("test_user_id_001"))


class TrackingEarningsScreen(MDScreen):
    session_start_earnings = 0

    def track_earnings(self):
        user_id = "example"  

        total = get_total_earnings(user_id)

    if self.session_start_earnings == 0:
        self.session_start_earnings = total

    session_earnings = total - self.session_start_earnings

class EarningsApp(MDApp):
    def build(self):
        Builder.load_file("tracker.kv")
        return TrackingEarningsScreen()

    def on_view_all_pressed(self):
        print("View All clicked!")


if __name__ == "__main__":
    EarningsApp().run()
