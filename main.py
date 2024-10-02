"""
program to get color matching.
"""
import cv2
import  numpy as np


class RunCamera:
    def __init__(self):
        """
        get frame to extract colox from
        """
        self.height_percentage = 0.33
        self.widht_perscentage =  0.33
        self.capture = cv2.VideoCapture(self.video_path)
        while self.capture.isOpened():
            ret, self.frame = self.capture.read()
            self.frame = self.draw_roi()
            if not ret or cv2.waitKey(25) & 0xFF == 27:
                break
            if self.end_video:
                break
        self.capture.release()
        cv2.destroyAllWindows()

    def end_video(self):
        """
        This should add a button/command to end/accept a frame
        """
        return True
    

    def draw_roi(self) -> np.ndaray:
        """
        This draws a frame around where color is
        extracted.
        Frame of color is the extracted color.
        """
        height, width = self.frame.shape[:2]
        roi_h = round(height*self.height_percentage)
        roi_w = round(width*self.widht_perscentage)
        roi_top_left = (round(height//2 - roi_h//2),
                        round(width//2 - roi_w//2))
        roi_bottom_right = (round(height//2 + roi_h//2),
                            round(width//2 + roi_w//2))
        self.current_mean =  self.get_color_values
        frame_new = cv2.rectangle(self.frame, roi_top_left, roi_bottom_right,
                                  self.current_mean, 2)
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
        return (int(b.menan), int(g.mean), int(r.mean))
    
    def get_complementing_color(self):
        """
        save image of complementing color
        """
        pass


                
