"""
program to get color matching.
"""
import cv2
import  numpy as np
from colors import \
    ComplementaryColors, TriadColors,\
        SplitComplementaryColors, TetrdicColor,\
            SquareTetradicColors 


class RunCamera:
    def __init__(self):
        """
        get frame to extract colox from
        """
        self.height_padding = 0.30
        self.widht_padding = 0.30
        self.blur_a = 75
        self.blur_b = 75
        #self.capture = cv2.VideoCapture(0)
        #while self.capture.isOpened():
            # manage the frame and average color of ROI
        #    self.c_index, (self.ret, self.frame) = enumerate(self.capture.read())
        #    self.roi_operations(self.get_mean_color, self.frame)

            # get complementary colors and names
        #    self.comp_colors = [ComplementaryColors(self.current_mean).matching,
        #                        TriadColors(self.current_mean).matching,
        #                        SplitComplementaryColors(self.current_mean).matching,
        #                        TetrdicColor(self.current_mean).matching,
        #                        SquareTetradicColors(self.current_mean).matching]
        #    self.comp_names = ['Complementary', 'Triad',
        #                       'Split Complemenntary',
        #                       'Tetradic', 'Square Tetradic']

            # self.display_frame - frame for kivy to display
        #    self.display_frame = self.draw_display_frame()
            #cv2.imshow('frame', display_frame.astype(np.uint8))
            
            # test if keep runing
        #    if not self.ret or cv2.waitKey(25) & 0xFF == 27:
        #        self.draw_display_frame(True)
        #        break
            
        #self.capture.release()
        #cv2.destroyAllWindows()
        self.capture = cv2.VideoCapture(0)

    def get_ret_frame(self):
        """
        Return pre-processed frame

        :output: ret, frame
        """
        self.ret, self.frame = self.capture.read()
        self.roi_operations(self.get_mean_color, self.frame)
        self.frame = self.return_display_frame()
        return self.ret, self.frame

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

    def get_color_strips(self, comp_colors: list, comp_name:str) -> np.ndarray:
        """
        TODO: Remove this to instead create individual kivy widgets(?).
        Return the detected color and suggested complementary colors as a numpy array.

        :param comp_colors: list of the complementary colors
        :param comp_names: sting of the kind of complementary color.
        :return: numpy array- of current mean color + complementary colors + complementary method.
        """
        color_base = np.zeros((int(round(self.frame.shape[0]/10)), int(self.frame.shape[1]), self.frame.shape[2]))
        section_size = round(color_base.shape[1]/(len(comp_colors)+1))
        for c_section, color in enumerate([self.current_mean, *comp_colors]):
            color_base = cv2.rectangle(color_base, (section_size*c_section, 0),
                                       (section_size*(1+c_section), color_base.shape[0]),
                                       color, -1)
        
        color_base = cv2.putText(color_base, comp_name,
                            (0, color_base.shape[0]//2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            color_base.shape[0]/60,
                            self.current_mean,
                            max(2, round(color_base.shape[0]/30)), cv2.LINE_AA)
        color_base = cv2.putText(color_base, comp_name,
                            (0, color_base.shape[0]//2),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            color_base.shape[0]/60,
                            (255-self.current_mean[0],
                             255-self.current_mean[1],
                             255-self.current_mean[2]),
                            max(1, round(color_base.shape[0]/40)), cv2.LINE_AA)
        color_base = cv2.line(color_base, (0, 0), (color_base.shape[1], 0),
                              (255-self.current_mean[0],
                               255-self.current_mean[1],
                               255-self.current_mean[2]),
                               color_base.shape[0]//20)
        return color_base
    
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
