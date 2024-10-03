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
        self.height_percentage = 0.33
        self.widht_perscentage =  0.33
        self.capture = cv2.VideoCapture(0)
        while self.capture.isOpened():
            ret, self.frame = self.capture.read()
            self.frame = self.draw_roi()
            self.frame = self.get_complementing_color()
            if not ret or cv2.waitKey(25) & 0xFF == 27:
                self.get_complementing_color(True)
                break
            frame_resised = cv2.resize(self.frame,
                                       (self.frame.shape[0]//2,
                                        self.frame.shape[1]//2))
            cv2.imshow('frame', frame_resised)
        self.capture.release()
        cv2.destroyAllWindows()

    def end_video(self):
        """
        This should add a button/command to end/accept a frame
        """
        return False

    def draw_roi(self) -> np.ndarray:
        """
        This draws a frame around where color is
        extracted.
        Frame of color is the extracted color.
        """
        width, height = self.frame.shape[:2]
        roi_w = round(width*self.widht_perscentage)
        roi_h = round(height*self.height_percentage)
        roi_top_left = (round(width//2 - roi_w//2),
                        round(height//2 - roi_h//2))
        roi_bottom_right = (round(width//2 + roi_w//2),
                            round(height//2 + roi_h//2))
        self.current_mean =  self.get_color_values(self.frame[roi_top_left[0]:roi_bottom_right[0],
                                                              roi_top_left[1]:roi_bottom_right[1]])
        frame_new = cv2.rectangle(self.frame, roi_top_left, roi_bottom_right,
                                  self.current_mean, 3)
        return frame_new
        
    def get_color_values(self, roi: np.ndarray) -> tuple:
        """
        return color value for ROI

        :param roi: numpy array- section of image to get color from.
        """
        b = []
        g = []
        r = []
        for row in roi:
            for pxl in row:
                b.append(pxl[0])
                g.append(pxl[1])
                r.append(pxl[2])
        return (int(np.mean(b)), int(np.mean(g)), int(np.mean(r)))
    
    def get_complementing_color(self, save: bool = False):
        """
        save image of complementing color
        TODO: Update this to manage lightness
        TODO: Improve color selection
        """
        print(f'Getting mathching color to {self.current_mean}...')
        b, g, r = [n/255.0 for n in self.current_mean]
        h, l, s = colorsys.rgb_to_hls(r, b, g)
        h_opposite = (((h*360)+ 180) % 360) / 360
        comp_color = colorsys.hls_to_rgb(h_opposite, l, s)
        comp_color = [round(c*255) for c in comp_color[::-1]]
        print(f'detected opposite color was: {comp_color}')
        final_img = cv2.rectangle(self.frame, (0, 0),
                                  (self.frame.shape[1],
                                   self.frame.shape[0]),
                                  comp_color, 15)  
        if save is True:
            print('saves image...')
            cv2.imwrite('color_img.png', final_img)
        return final_img


RunCamera()                
