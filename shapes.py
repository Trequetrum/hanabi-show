from typing import Callable, List, Tuple

from utility import clamp_int

class Color():

    def __init__(self, red:int, green:int, blue:int):
        self.red = clamp_int(red,0,255) 
        self.green = clamp_int(green,0,255)
        self.blue = clamp_int(blue,0,255)

class ColorNames():
    BLACK = Color(0,0,0)
    WHITE = Color(255,255,255)
    RED = Color(255,0,0)
    LIME = Color(0,255,0)
    BLUE = Color(0,0,255)
    YELLOW = Color(255,255,0)
    CYAN = Color(0,255,255)
    MAGENTA = Color(255,0,255)
    SILVER = Color(192,192,192)
    GRAY = Color(128,128,128)
    MAROON = Color(128,0,0)
    OLIVE = Color(128,128,0)
    GREEN = Color(0,128,0)
    PURPLE = Color(128,0,128)
    TEAL = Color(0,128,128)
    NAVY = Color(0,0,128)	

class Shape():

    __safe_id: int = 1
    @staticmethod
    def __gen_id() -> int:
        id = Shape.__safe_id
        Shape.__safe_id += 1
        return id

    def __init__(self, 
        fill: bool = True, 
        color: Color = ColorNames.BLACK,
        pos: Tuple[int, int] = (0,0)
    ):
        self.id = Shape.__gen_id()
        self.fill = fill
        self.color = color
        self.pos = pos


class Circle(Shape):
    def __init__(self, radius: int, *args, **kwargs):
        self.radius = radius
        super().__init__(*args, **kwargs)