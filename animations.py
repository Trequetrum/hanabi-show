from typing import Callable, List, Optional, Tuple, Union
from animation_framework import Animation
from shapes import Shape, Circle, Color
from utility import ratiod

class CirleMove(Animation):

    def __init__(self, 
        start: Tuple[int, int],
        end: Tuple[int, int],
        radius: int,
        color: Color,
        *args, 
        **kwargs
    ):
        self.start = start
        self.end = end
        self.radius = radius
        self.color = color

        super().__init__(*args, **kwargs)

    def get_state(self, time:int) -> List[Shape]:
        if(time > 0 and time < self.duration):

            when = time/self.duration
            current = (
                ratiod(self.start[0], self.end[0], when),
                ratiod(self.start[1], self.end[1], when)
            )

            return [Circle(
                color=self.color,
                pos=current, 
                radius=self.radius
            )]
        
        return []

class CircleTravelAlongAFunction(Animation):

    def __init__(self, 
        start_x: int,
        end_x: int,
        y_at: Callable[[int], int],
        radius: int,
        color: Color,
        *args, 
        **kwargs
    ):
        self.start_x = start_x
        self.end_x = end_x
        self.y_at = y_at
        self.radius = radius
        self.color = color

        super().__init__(*args, **kwargs)


    def get_state(self, time:int) -> List[Shape]:
        if(time > 0 and time < self.duration):

            when = time/self.duration
            x = ratiod(self.start_x, self.end_x, when)
            y = self.y_at(x)

            return [Circle(
                color=self.color,
                pos=(x,y), 
                radius=self.radius
            )]
        
        return []