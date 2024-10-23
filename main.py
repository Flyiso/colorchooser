from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.uix.widget import Widget
from jnius import autoclass
import colorsys
from abc import ABC, abstractmethod
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import numpy as np
import cv2


CameraInfo = autoclass('android.hardware.Camera$CameraInfo')
CAMERA_INDEX = {'front': CameraInfo.CAMERA_FACING_FRONT, 'back': CameraInfo.CAMERA_FACING_BACK}
Builder.load_file("myapplayout.kv")


class GetMatchingColor(ABC):
    """
    Classes for recieving color matching the input color.
    """
    def __init__(self, base_color):
        self.base = base_color
        self.matching = self.get_colors(base_color)

    @abstractmethod
    def get_colors(self, base_color) -> list:
        """
        Method that return list of color codes
        """
        pass

    @abstractmethod
    def return_name(self) -> str:
        """
        Method returns the display name of the color scheme as string
        """
        pass


class ComplementaryColors(GetMatchingColor):
    def get_colors(self, base_color) -> list:
        """
        get color of opposite hue value

        :return: list of 1 BGR colors-(3 values, 0-255)
        """
        b, g, r = [n/255.0 for n in base_color]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_opposite = (((h*360)+ 180) % 360) / 360
        comp_color = colorsys.hls_to_rgb(h_opposite, l, s)
        comp_color = [round(c*255) for c in comp_color[::-1]]
        return [list(base_color), comp_color]
    
    def return_name(self) -> str:
        """
        Return string name

        :return: str 'Complementary'
        """
        return 'Complementary'


class TriadColors(GetMatchingColor):   
    def get_colors(self, base_color) -> list:
        """
        Get the 2 colors to create a triad

        :return: list of 2 BGR colors-(3 values, 0-255)
        """
        b, g, r = [n/255.0 for n in base_color]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ 120) % 360) / 360
        h_2 = (((h*360)+ 240) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        return [list(base_color), comp_1, comp_2]
    
    def return_name(self) -> str:
        """
        Return string of name as 'readable' name to print.

        :return: str 'Triad'
        """
        return 'Triad'


class SplitComplementaryColors(GetMatchingColor):
    def  get_colors(self, base_color) -> list:
        """
        get the colors of split complementary harmony

        :return: list of 2 BGR colors-(3 values, 0-255)
        """
        s_size = 360/12
        b, g, r = [n/255.0 for n in base_color]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ s_size*5) % 360) / 360
        h_2 = (((h*360)+ s_size*7) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        return [list(base_color), comp_1, comp_2]
    
    def return_name(self) -> str:
        """
        Return string of name as 'readable' name to print.

        :return: str 'Split Complementary'
        """
        return 'Split Complementary'


class TetradicColor(GetMatchingColor):
    def  get_colors(self, base_color) -> list:
        """
        get the colors of tedratic color sheme

        :return: list of 3 BGR colors-(3 values, 0-255)
        """
        s_size = 360/12
        b, g, r = [n/255.0 for n in base_color]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ s_size*4) % 360) / 360
        h_2 = (((h*360)+ s_size*6) % 360) / 360
        h_3 = (((h*360)+ s_size*10) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        comp_3 = [c*255 for c in colorsys.hls_to_rgb(h_3, l, s)[::-1]]
        return [list(base_color), comp_1, comp_2, comp_3]
    
    def return_name(self) -> str:
        """
        Return string of name as 'readable' name to print.

        :return: str 'Tetradic'
        """
        return 'Tetradic'


class  SquareTetradicColors(GetMatchingColor):
    def  get_colors(self, base_color) -> list:
        """
        get the colors of square detradic color scheme

        :return: list of 3 BGR colors-(3 values, 0-255)
        """
        s_size = 360/12
        b, g, r = [n/255.0 for n in base_color]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ s_size*3) % 360) / 360
        h_2 = (((h*360)+ s_size*6) % 360) / 360
        h_3 = (((h*360)+ s_size*9) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        comp_3 = [c*255 for c in colorsys.hls_to_rgb(h_3, l, s)[::-1]]
        return [list(base_color), comp_1, comp_2, comp_3]
    
    def return_name(self) -> str:
        """
        Return string of name as 'readable' name to print.

        :return: str 'Square Tetradic'
        """
        return 'Square Tetradic'


class MatchingWidget(BoxLayout):
    buttons_layout = BoxLayout(orientation='vertical')
    functional_buttons = {}
    color_to_find = 'match'  # match is default/start state- changes to color code
                             # if mode is changed
    last_active = None

    def update_colors(self, to_match):
        self.last_active = to_match
        self.buttons_layout.clear_widgets()
        self.buttons = []
        self.total_width = 480
        color_classes = [ComplementaryColors, TriadColors,
                         SplitComplementaryColors,
                         TetradicColor, SquareTetradicColors]
        for color_class in color_classes:
            color_class = color_class(to_match)
            btn_width_hint = 0.40
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=1)
            for indx, color in enumerate(color_class.matching):
                color_str = ' | '.join([f'{nme}_{str(round(col))}'
                                      for col, nme in zip(color,['R', 'G', 'B'])])
                btn_name = f'  {color_class.return_name()}\n  {color_str}'
                btn_status = 'unavailable'
                
                if indx > 0:
                    btn_name = '\n'.join([f'  {nme} -> {str(round(col))}' for col, nme 
                                          in zip(color, ['R', 'G', 'B'])])
                    btn_width_hint = (0.60/(len(color_class.matching)-1))
                    btn_status = 'de_activated'
                    color = [c / 255 for c in color] + [1]

                    if str(color) == self.color_to_find:
                        btn_status = 'activated'
                    elif self.color_to_find == 'match':
                        btn_status = 'not_activated'
                
                btn = Button(background_normal='',
                             background_color=color,
                             text=btn_name,
                             halign='left',
                             valign='middle',
                             text_size=(self.width*btn_width_hint,
                                        self.height),
                             size_hint=(btn_width_hint, 1)) 
   
                btn.bind(on_press=self.on_press)
                btn.status = btn_status
                
                row_layout.add_widget(btn)
            
            self.buttons_layout.add_widget(row_layout)
        if not self.children:
            self.add_widget(self.buttons_layout)

    def on_press(self, btn_instance):
        """
        notes/plan/idea for button press steps
        """
        if btn_instance.status == 'activated':
            self.color_to_find = 'match'
        if btn_instance.status == 'not_activated':
            self.color_to_find = str(btn_instance.color)
    

        # BUTTON STATUS OPTIONS:
        # 1. not_activated - default/start status
        # 2. activated - status when pressed-only one of this status allowed.
        # 3. de_activated - status indicates unavailability(because other button is activated)
        # 4. unavailable - status of static button that, on press, does not trigger any event.

        # status of first button of each row is to be 'unavailable'
        # check if button press is to select or un-select

        #  if select:
        #       de-activate all other buttons(except first of each row)
        #       set self.color_to_find to button color

        #   if  de_select:
        #       set status of all buttons(except firt of each row) to 'not_activated'
        #       set  self.color_to_find to 'match'
        
        # 'gray-out' all buttons of status 'de_activated'
        #  enhance/mark button of status 'activated'
        #  reset/set appearance to normal of buttons of status 'not_activated', or 'unavailable'
        pass

class CameraWidget(Camera):
    resolution = (640, 480)
    index = CAMERA_INDEX['back']
    blur_a = 55
    blur_b = 55
    height_padding = 0.20
    widht_padding = 0.20

    def on_tex(self, *l):
        if self._camera._buffer is None:
            return None

        super(CameraWidget, self).on_tex(*l)
        self.texture = Texture.create(size=np.flip(self.resolution), colorfmt='rgb')
        frame = self.frame_from_buf()
        # two 'routes' for different camera options. 
        self.mode = self.parent.ids.matching_widget.color_to_find  # get value of this from button widgets'color_to_find' attribute
        if self.mode == 'match':
            self.frame_to_screen_match(frame)
        else:
            self.frame_to_screen_find(frame)

    def frame_from_buf(self):
        w, h = self.resolution
        frame = np.frombuffer(self._camera._buffer.tostring(), 'uint8').reshape((h + h // 2, w))
        frame_bgr = cv2.cvtColor(frame, 93)
        if self.index:
            return np.flip(np.rot90(frame_bgr, 1), 1)
        else:
            return np.rot90(frame_bgr, 3)

    def frame_to_screen_match(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame = frame_rgb
        self.roi_operations(self.get_mean_color, frame_rgb)
        self.detected_mean = self.current_mean
        frame_rgb = self.roi_operations(self.blur_background, frame_rgb)
        self.parent.ids.matching_widget.update_colors(self.detected_mean)
        flipped = np.flip(frame_rgb, 0)
        buf = flipped.tobytes()
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

    def frame_to_screen_find(self, frame):
        """
        This frame to screen displays the camera in 'find mode',
        attempting to match color selected to color in frame
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.frame = frame_rgb
        self.detected_mean = self.parent.ids.matching_widget.last_active
        self.roi_operations(self.get_mean_color, frame_rgb)
        frame_rgb = self.roi_operations(self.blur_background, frame_rgb)
        self.parent.ids.matching_widget.update_colors(self.detected_mean)
        # self.mode returns the targeted color
        # add method to get similarity metrics
        # add method to print/display metrics
        # add method to modify/displayed frame(blur, draw frame...)
        flipped = np.flip(frame_rgb, 0)
        buf = flipped.tobytes()
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
    
    def print_metrics_on_frame(self, frame):
        """
        Display some metrics to indicate camera view to target similarity 
        """
        print(f'mean_to_find: {self.detected_mean}\nmean_found: {self.current_mean}')
        return frame
    
    def blur_background(self,
                        roi_square_top_left: tuple,
                        roi_square_bottom_right: tuple,
                        frame:np.ndarray) -> np.ndarray:
        """
        return image with everything except ROI blurred

        :param roi_square_top_left: tuple- height and width of where ROI start
        :param roi_square_bottom_right: tuple- height and  with of ROI end
        :param frame: numpy array frame to modify.
        :return: input frame (or self.frame) with non-ROI blurred
        """
        roi = np.copy(self.frame[roi_square_top_left[0]:roi_square_top_left[1],
                                 roi_square_bottom_right[0]:roi_square_bottom_right[1]])
        frame = cv2.rectangle(frame,
                              (int(self.frame.shape[1]*(self.widht_padding/1.35)),
                               int(self.frame.shape[0]*(self.height_padding/1.35))),
                              (int(frame.shape[1]-self.frame.shape[1]*(self.widht_padding/1.35)),
                               int(frame.shape[0]-self.frame.shape[0]*(self.height_padding/1.35))),
                               self.current_mean, -1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(frame)
        s = np.clip(s * 1.25, 0, 255).astype(np.uint8)
        frame = cv2.cvtColor(cv2.merge([h, s, v]), cv2.COLOR_HSV2BGR)
        frame = cv2.blur(frame, (self.blur_a, self.blur_b))
        frame[roi_square_top_left[0]:roi_square_top_left[1],
              roi_square_bottom_right[0]:roi_square_bottom_right[1]] = roi
        
        frame = cv2.rectangle(frame,
                              (int(self.frame.shape[1]*(self.widht_padding)),
                               int(self.frame.shape[0]*self.height_padding)),
                               ( int(frame.shape[1]-self.frame.shape[1]*self.widht_padding),
                                 int(frame.shape[0]-self.frame.shape[0]*self.height_padding)
                               ),self.current_mean, 10)
        return frame

    def get_mean_color(self,
                       roi_square_top_left: tuple,
                       roi_square_bottom_right: tuple,
                       frame:np.ndarray) -> np.ndarray:
        """
        get average color inside of ROIblur_background

        :param roi: numpy array- section of image to get color from.
        :return:  np.array- input frame
        """
        b = []
        g = []
        r = []
        roi = frame[roi_square_top_left[0]:roi_square_top_left[1],
                    roi_square_bottom_right[0]:roi_square_bottom_right[1]]

        for row in roi:
            for pxl in row:
                b.append(pxl[0])
                g.append(pxl[1])
                r.append(pxl[2])
        self.current_mean = (int(np.median(b)), int(np.median(g)), int(np.median(r)))
        return self.frame

    def roi_operations(self, roi_method,
                       frame: np.ndarray|None = None) -> np.ndarray:
        """
        This draws a frame around where color is
        extracted.
        Frame of color is the extracted color.
        """

        if frame is None:
            frame = np.copy(self.frame)

        height, width = frame.shape[:2]
        roi_w = round(width*(self.widht_padding))
        roi_h = round(height*self.height_padding)
        roi_top_left = (round(roi_h),
                        round(roi_w))
        roi_bottom_right = (round(height - roi_h),
                            round(width - roi_w))
        
        return_frame = roi_method((roi_top_left[0], roi_bottom_right[0]),
                                  (roi_top_left[1], roi_bottom_right[1]),
                                  frame)
        return return_frame

class MyLayout(BoxLayout):
    pass

class MyApp(App):
    def build(self):
        return MyLayout()

if __name__ == '__main__':
    MyApp().run()
