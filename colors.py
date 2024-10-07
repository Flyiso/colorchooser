import colorsys
from abc import ABC, abstractmethod


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
        return [comp_color]

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
        return [comp_1, comp_2]
    
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
        return [comp_1, comp_2]
    
class TetrdicColor(GetMatchingColor):
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
        return [comp_1, comp_2, comp_3]

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
        return [comp_1, comp_2, comp_3]