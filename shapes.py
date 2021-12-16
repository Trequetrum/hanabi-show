import random as rand
from typing import Any, Callable, List, Tuple, TypedDict
from dataclasses import dataclass, field

from utility import clamp_int, gen_unique_number

class Color():
    "Describes and RGB color. Set invisible if any inputs are negative"

    def __init__(self, red:int, green:int, blue:int):
        self.visible = not (red < 0 or green < 0 or blue < 0)
        self.red = clamp_int(red,0,255) 
        self.green = clamp_int(green,0,255)
        self.blue = clamp_int(blue,0,255)


class ColorNames():
    """Generate an RGB color based on a name. These are generated to
    ensure that if you grab one and mutate it later, the color BLACK
    hasn't been changed here.
    """
    NONE = lambda: Color(-1,-1,-1)
    BLACK = lambda: Color(0,0,0)
    WHITE = lambda: Color(255,255,255)
    RED = lambda: Color(255,0,0)
    LIME = lambda: Color(0,255,0)
    BLUE = lambda: Color(0,0,255)
    YELLOW = lambda: Color(255,255,0)
    CYAN = lambda: Color(0,255,255)
    MAGENTA = lambda: Color(255,0,255)
    SILVER = lambda: Color(192,192,192)
    GRAY = lambda: Color(128,128,128)
    MAROON = lambda: Color(128,0,0)
    OLIVE = lambda: Color(128,128,0)
    GREEN = lambda: Color(0,128,0)
    PURPLE = lambda: Color(128,0,128)
    TEAL = lambda: Color(0,128,128)
    NAVY = lambda: Color(0,0,128)

    @staticmethod
    def random():
        return Color(
            rand.randint(0,255),
            rand.randint(0,255),
            rand.randint(0,255)
        )

@dataclass
class Point():
    x: int
    y: int

@dataclass
class Shape():
    id:int = field(default_factory=gen_unique_number)

@dataclass
class Text(Shape):
    position: Point = field(default_factory=lambda:Point(0,0))
    color: Color = field(default_factory=ColorNames.BLACK)
    text: str = ''
    font_family: str = "default"
    font_size: int = -1
    font_bold: bool = False 
    font_slant: bool = False
    font_underline: bool = False
    font_overstrike: bool = False

@dataclass
class PrimitiveShape(Shape):
    fill_color: Color = field(default_factory=ColorNames.BLACK)
    line_color: Color = field(default_factory=ColorNames.BLACK)
    line_width: int = 1 # Pixels

@dataclass
class Circle(PrimitiveShape):
    radius: int = 5
    position: Point = field(default_factory=lambda:Point(0,0))

@dataclass
class Line(PrimitiveShape):
    """A line can consist of any number of segments connected end 
    end. Specified by a series of vertices (Point(x, y))
    """
    vertices: List[Point] = field(default_factory=lambda:[])

@dataclass
class Polygon(PrimitiveShape):
    """Describes a polygon
    
    Its geometry is specified as a series of vertices [(x0, y0), 
    (x1, y1), … (xn, yn)], but the actual perimeter includes one more
    segment from (xn, yn) back to (x0, y0).
    """
    vertices: List[Point] = field(default_factory=lambda:[])

@dataclass
class BoxCoords():
    upper_left: Point = field(default_factory=lambda:Point(0,0))
    lower_right: Point = field(default_factory=lambda:Point(0,0))

@dataclass
class Rectangle(PrimitiveShape, BoxCoords):
    "A rectangle is defined by box coordinates"

@dataclass
class Oval(PrimitiveShape, BoxCoords):
    "The ellipse is fit into a rectangle defined by box coordinates"

@dataclass
class Arc(PrimitiveShape, BoxCoords):
    "a wedge-shaped slice taken out of an ellipse"

    STYLE_CHORD = 926383806
    STYLE_PIESLICE = 926383807
    STYLE_ARC = 926383808

    start: int = 0 # Degrees
    extent: int = 360 # Degrees
    style: int = STYLE_PIESLICE

class Picture():
    """A picture generates a list of shapes"""
    def get_shapes(self) -> List[Shape]:
        raise NotImplementedError

class PurePicture(Picture):
    "A single shape is a list of shapes"
    def __init__(self, shape: Shape) -> None:
        self._shape = shape

    def __getattr__(self, name):
        return getattr(self._shape, name)
    
    def __setattr__(self, name, value):
        if(name == "_shape"):
            super().__setattr__(name, value)
        else:
            setattr(self._shape, name, value)

    def get_shapes(self) -> List[Shape]:
        return [self._shape]