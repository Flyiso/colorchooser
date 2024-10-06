import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import BoxLayout


# TODO: add ToCamera class for using camera to find matching color.  
class FromCamera(App):
    def __init__(self, **kwargs):
        self.layout =  BoxLayout(orientation='vertical')

if __name__ == '__main__':
    FromCamera().run()