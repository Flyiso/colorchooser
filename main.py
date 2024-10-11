import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.graphics.texture import Texture
#from kivy.lang import Builder  #New
from camera import RunCamera
from  colors import ComplementaryColors, TriadColors, SplitComplementaryColors, TetradicColor, SquareTetradicColors


class CamApp(App):

    def build(self):
        self.img1=Image()
        self.button_pressed = False
        self.comp_color_classes = [ComplementaryColors, TriadColors,
                                   SplitComplementaryColors,
                                   TetradicColor, SquareTetradicColors]
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.img1)

        self.buttons_layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.buttons_layout)

        self.camera = RunCamera()
        Clock.schedule_interval(self.update_camera, 1.0/33.0)
        return self.layout

    def update_camera(self, dt):
        ret, frame = self.camera.get_ret_frame()
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        self.mean_bgr = self.camera.current_mean[::-1]
        self.total_width = self.camera.frame_width
        self.total_height = self.camera.frame_height
        self.layout.width = self.total_width
        if self.button_pressed:
            self.display_match()
        self.update_buttons()

        self.img1.texture = texture1

    def update_buttons(self):
        if self.button_pressed:
            return
        self.buttons_layout.clear_widgets()
        self.buttons = []

        for color_class in self.comp_color_classes:
            color_class = color_class(self.mean_bgr)
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=1, height=0)
            btn_name = color_class.return_name()
            btn_width_hint = 0.25
            
            for indx, color in enumerate(color_class.matching):
                if indx > 0:
                    btn_name = ' '.join([str(round(col)) for col in color[::-1]])
                    btn_width_hint = (1/(len(color_class.matching)-1))
                btn = Button(background_color=[c/255 for c in color] + [1],
                             text=btn_name,
                             halign='left',
                             valign='middle',
                             text_size=((self.total_width*btn_width_hint)*0.85, None),
                             size_hint=(btn_width_hint, 1))
                row_layout.add_widget(btn)
                self.buttons.append(btn)
            self.buttons_layout.add_widget(row_layout)

        def display_match(self):
            # method to display how well numeric value indicating
            # camera view match what is
            # current value of self.active_color
            pass
        
        def press_button(self, btn):
            # add some kind of logic to exit if button pressed is not active?

            # de-selcect button 
            if self.button_pressed:
                self.button_pressed = False
                self.active_color = None
                return
            # press button:
            self.active_color = btn.background_color
            self.button_pressed = True
            # Mark button/update border color of pressed button
            # de-activate all buttons except pressed one
            # make de-activated buttons somewhat less saturated



if __name__ == '__main__':
    CamApp().run()
    #cv2.destroyAllWindows()