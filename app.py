import kivy
from kivy.app import MDApp
from kivy.uix.button import MDRaisedButton
from kivy.uix.gridlayout import MDBoxLayout


class MainApp(MDApp):
    def build(self):
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(MDRaisedButton(
            text='Click Here',
            pos_hint={'center_x':.5,'center_y':.0},
            size_hint=(None, None))
            )
        return layout

if __name__ == '__main__':
    MainApp().run()