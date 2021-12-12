from tkinter import *
from tkinter import ttk
from typing import Callable, List, Optional, Tuple, Union
import rx
from rx import operators as ops
from animation import Animation, Shape, Circle
from utility import *

class AnimateSegment(Animation):

    def __init__(self, 
        start_x: int,
        end_x: int,
        y_at: Callable[[int], int],
        duration: int, # milliseconds
        radius: int,
        color: str
    ):
        self.start_x = start_x
        self.end_x = end_x
        self.y_at = y_at
        self.duration = duration
        self.radius = radius
        self.color = color

    def get_state(self, time:int) -> List[Shape]:
        clamp_time = max(0, min(time, self.duration))
        when = clamp_time/self.duration
        x = ratiod(self.start_x, self.end_x, when)
        y = self.y_at(x)

        return [Circle(
            color=self.color,
            pos=(x,y), 
            radius=self.radius
        )]