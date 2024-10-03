"""
program to get color matching.
"""
import cv2
import colorsys
import  numpy as np


class RunCamera:
    def __init__(self):
        """
        get frame to extract colox from
        """
        self.height_padding = 0.20
        self.widht_padding = 0.20
        self.capture = cv2.VideoCapture(0)
        while self.capture.isOpened():
            # manage the frame and average color of ROI
            self.c_index, (ret, self.frame) = enumerate(self.capture.read())
            self.roi_operations(self.get_mean_color, self.frame)

            # get complementary colors and names
            self.comp_colors = [self.get_complementary_color(),
                                self.get_triad_colors(),
                                self.get_split_complementary_colors(),
                                self.get_tetradic_colors(),
                                self.get_square_tetradic_colors()]
            self.comp_names = ['Complementary', 'Triad',
                               'Split Complemenntary',
                               'Tetradic', 'Square Tetradic']

            display_frame = self.draw_display_frame()
            cv2.imshow('frame', display_frame.astype(np.uint8))
            
            # test if keep runing
            if not ret or cv2.waitKey(25) & 0xFF == 27:
                self.draw_display_frame(True)
                break
            
        self.capture.release()
        cv2.destroyAllWindows()

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
        self.current_mean = (int(np.mean(b)), int(np.mean(g)), int(np.mean(r)))
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
                              (int(self.frame.shape[1]*(self.widht_padding/3)),
                               int(self.frame.shape[0]*(self.height_padding/3))),
                              (int(frame.shape[1]-self.frame.shape[1]*(self.widht_padding/3)),
                               int(frame.shape[0]-self.frame.shape[0]*(self.height_padding/3))),
                               self.current_mean, -1)
        frame = cv2.blur(frame, (125, 125))
        frame[roi_square_top_left[0]:roi_square_top_left[1],
              roi_square_bottom_right[0]:roi_square_bottom_right[1]] = roi
        
        frame = cv2.rectangle(frame,
                              (int(self.frame.shape[1]*self.widht_padding),
                               int(self.frame.shape[0]*self.height_padding)),
                               ( int(frame.shape[1]-self.frame.shape[1]*self.widht_padding),
                                 int(frame.shape[0]-self.frame.shape[0]*self.height_padding)
                               ),self.current_mean, 25)
        return frame
    
    def get_complementary_color(self) -> list:
        """
        get color of opposite hue value
        """
        b, g, r = [n/255.0 for n in self.current_mean]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_opposite = (((h*360)+ 180) % 360) / 360
        comp_color = colorsys.hls_to_rgb(h_opposite, l, s)
        comp_color = [round(c*255) for c in comp_color[::-1]]
        return [comp_color]
    
    def get_triad_colors(self) -> list:
        """
        Get the 2 colors to create a triad
        """
        b, g, r = [n/255.0 for n in self.current_mean]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ 120) % 360) / 360
        h_2 = (((h*360)+ 240) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        return [comp_1, comp_2]
    
    def  get_split_complementary_colors(self) -> list:
        """
        get the colors of split complementary harmony
        """
        s_size = 360/12
        b, g, r = [n/255.0 for n in self.current_mean]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ s_size*5) % 360) / 360
        h_2 = (((h*360)+ s_size*7) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        return [comp_1, comp_2]
    
    def  get_tetradic_colors(self) -> list:
        """
        get the colors of split complementary harmony
        """
        s_size = 360/12
        b, g, r = [n/255.0 for n in self.current_mean]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ s_size*4) % 360) / 360
        h_2 = (((h*360)+ s_size*6) % 360) / 360
        h_3 = (((h*360)+ s_size*10) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        comp_3 = [c*255 for c in colorsys.hls_to_rgb(h_3, l, s)[::-1]]
        return [comp_1, comp_2, comp_3]

    def  get_square_tetradic_colors(self) -> list:
        """
        get the colors of split complementary harmony
        """
        s_size = 360/12
        b, g, r = [n/255.0 for n in self.current_mean]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_1 = (((h*360)+ s_size*3) % 360) / 360
        h_2 = (((h*360)+ s_size*6) % 360) / 360
        h_3 = (((h*360)+ s_size*9) % 360) / 360
        comp_1 = [c*255 for c in colorsys.hls_to_rgb(h_1, l, s)[::-1]]
        comp_2 = [c*255 for c in colorsys.hls_to_rgb(h_2, l, s)[::-1]]
        comp_3 = [c*255 for c in colorsys.hls_to_rgb(h_3, l, s)[::-1]]
        return [comp_1, comp_2, comp_3]
    
    def get_color_strips(self, comp_colors: list, comp_name:str) -> np.ndarray:
        """
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
    
    def draw_display_frame(self, save_img: bool = False) -> np.ndarray:
        """
        Create an image displaying camera view, and complementary color options.

        :param save_img: Bool- if image is to be saved
        :return: image to display
        """
        frame = self.roi_operations(self.blur_background)
        colors = [self.get_color_strips(comp_colors, comp_name) for comp_colors, comp_name 
                  in zip(self.comp_colors, self.comp_names)]
        frame_w_maps = np.concatenate([frame, *colors])
        if save_img is True:
            cv2.imwrite('color_img.png', frame_w_maps)
        return frame_w_maps


RunCamera()                
