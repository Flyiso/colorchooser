"""
program to get color matching.
"""
import cv2
import numpy as np
import kivy  #New
from kivy.uix.camera import Camera  #New
from kivy.graphics.texture import Texture  #Also new


class RunCamera(Camera): # nothing here before
    firstFrame = None # NEW

    def __init__(self):
        """
        get frame to extract colox from  
        """
        self.height_padding = 0.30
        self.widht_padding = 0.30
        self.blur_a = 75
        self.blur_b = 75
        #self.capture = cv2.VideoCapture('http://192.168.0.6:8080/video')

    
    def _camera_loaded(self, *largs):
        if kivy.platform=='android':
            self.texture = Texture.create(size=self.resolution,colorfmt='rgb')
            self.texture_size = list(self.texture.size)
        else:
            super(RunCamera, self)._camera_loaded()

    def on_tex(self, *l):
        if kivy.platform=='android':
            buf = self._camera.grab_frame()
            if not buf:
                return
            frame = self._camera.decode_frame(buf)
            self.image = frame = self.proecss_frame(frame)
            buf = frame.tostring()
            self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        super(RunCamera, self).on_tex(*l)

    def process_frame(self, frame):
        r, g, b = cv2.split(frame)
        frame = cv2.merge((b,g,r))        
        rows, cols, channel = frame.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
        dst = cv2.warpAffine(frame,M,(cols,rows))
        self.frame = cv2.flip(dst,1)
        if self.index==1:
            self.frame = cv2.flip(dst,-1)
        self.frame = self.get_ret_frame()
        return self.frame

    def get_ret_frame(self):
        """
        Return pre-processed frame

        :output: ret, frame
        """
        #self.ret, self.frame = self.capture.read()
        self.frame_width, self.frame_height = self.frame.shape[:2]
        self.roi_operations(self.get_mean_color, self.frame)
        self.frame = self.return_display_frame()
        return self.frame

    def roi_operations(self, roi_method,
                       frame: np.ndarray|None = None) -> np.ndarray:
        """
        This draws a frame around where color is
        extracted.
        Frame of color is the extracted color.
        """
        # use self.if no frame provided

        if frame is None:
            frame = np.copy(self.frame)

        # get/define the area of interest
        height, width = frame.shape[:2]
        roi_w = round(width*(self.widht_padding))
        roi_h = round(height*self.height_padding)
        roi_top_left = (round(roi_h),
                        round(roi_w))
        roi_bottom_right = (round(height - roi_h),
                            round(width - roi_w))
        
        # apply input method
        return_frame = roi_method((roi_top_left[0], roi_bottom_right[0]),
                                  (roi_top_left[1], roi_bottom_right[1]),
                                  frame)
        return return_frame
        
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
    
    def return_display_frame(self, save_img: bool = False) -> np.ndarray:
        """
        TODO: update this to just update current frame with camera+blur
        Create an image displaying camera view, and complementary color options.

        :param save_img: Bool- if image is to be saved
        :return: image to display
        """
        frame = self.roi_operations(self.blur_background)
        #colors = [self.get_color_strips(comp_colors, comp_name) for comp_colors, comp_name 
        #          in zip(self.comp_colors, self.comp_names)]
        #frame_w_maps = np.concatenate([frame, *colors])
        #if save_img is True:
        #    cv2.imwrite('color_img.png', frame_w_maps)
        return frame  #was  frame_w_maps               
