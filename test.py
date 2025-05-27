from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder

KV = '''
<SelectScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: "20dp"
        spacing: "20dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        
        MDLabel:
            text: "Choose Your Role"
            halign: "center"
            font_style: "H4"
            size_hint_y: None
            height: self.texture_size[1]
            padding_y: "20dp"
        
        MDBoxLayout:
            orientation: 'vertical'
            spacing: "20dp"
            size_hint_y: None
            height: "200dp"
            
            MDButton:
                text: "Become Worker"
                size_hint_x: 0.8
                pos_hint: {"center_x": .5}
                on_release: root.on_worker_press()
            
            MDButton:
                text: "Become Employer"
                size_hint_x: 0.8
                pos_hint: {"center_x": .5}
                on_release: root.on_employer_press()
'''

class SelectScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)
    
    def on_worker_press(self):
        print("Worker option selected")
        # Add your navigation logic here
    
    def on_employer_press(self):
        print("Employer option selected")
        # Add your navigation logic here

class SelectApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return SelectScreen()

if __name__ == '__main__':
    SelectApp().run()