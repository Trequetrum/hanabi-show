from typing import Callable, List, Optional, Tuple, Union
from shapes import Shape, Circle, Color
from utility import ratiod

 

class Animation():
    """Describes an animation
    
    To make an animation subclass this class and be sure to include
    1) Duration: Describes how many milliseconds this takes to 
       run to completion
    3) get_state function: A function that describes what is drawn 
       for any given time (again in milliseconds)

    If you do that, the rest of the framework will be able to run
    your animation. Feel free to add as much or as little as you 
    like.
    """

    def __init__(self, duration: int, name: str = ''):
        self.duration = duration
        self.name = name

    def get_state(self, time:int) -> List[Shape]:
        raise NotImplementedError


class Scene(Animation):
    """Combining animations

    Scene takes a list of animations. Each animation must be included 
    in a tuple that describes when that animation starts.
    """

    def __init__(self, animations: List[Tuple[int, Animation]], name: str = ''):
        self.animations = animations
        super().__init__(
            name=name,
            duration=max(
                map(lambda v: v[0] + v[1].duration, animations)
            )
        )

    def get_state(self, time:int) -> List[Shape]:
        shapes = []
        for (start_time, a) in self.animations:
            if(time >= start_time and time <= start_time + a.duration):
                shapes += a.get_state(time - start_time)
        
        return shapes


class CirleMove(Animation):
    """Animation

    Moves a circle from start to end over the course of the duration
    """

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
            current = {
                'x': ratiod(self.start[0], self.end[0], when),
                'y': ratiod(self.start[1], self.end[1], when)
            }

            return [Circle(
                color=self.color,
                pos=current, 
                radius=self.radius
            )]
        
        return []

class CircleTravelAlongAFunction(Animation):
    """Animation

    Moves a circle along the x-axis as described by a function.
    If you give y_at an x-value, it should return a y-value.
    """

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
            current = {
                'x': x,
                'y': self.y_at(x)
            }

            return [Circle(
                color=self.color,
                pos=current, 
                radius=self.radius
            )]
        
        return []