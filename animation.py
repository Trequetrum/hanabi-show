from typing import Any, Callable, List, Tuple
from shapes import ColorNames, Point, Shape, Circle, Color
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
    in a tuple that describes when that animation starts. Since Scenes
    can be aribrarily nested, this lets you build complex animations 
    from more primitive ones.
    """

    def __init__(self, animations: List[Tuple[int, Animation]], name: str = ''):
        self._animations = animations
        super().__init__(
            name=name,
            duration=max(
                map(lambda v: v[0] + v[1].duration, animations)
            )
        )

    def get_state(self, time:int) -> List[Shape]:
        shapes = []
        for (start_time, a) in self._animations:
            if(time >= start_time and time <= start_time + a.duration):
                shapes += a.get_state(time - start_time)
        
        return shapes


class CirleMove(Animation):
    """Animation

    Moves a circle from start to end over the course of the duration
    """

    def __init__(self, 
        start: Point,
        end: Point,
        radius: int,
        color: Color,
        *args, 
        **kwargs
    ):
        self._start = start
        self._end = end

        self._init_circle = Circle(
            position=Point(0, 0),
            fill_color=color,
            line_color=ColorNames.YELLOW(),
            line_width=2, 
            radius=radius
        )

        super().__init__(*args, **kwargs)

    def get_state(self, time:int) -> List[Shape]:
        if(time > 0 and time < self.duration):

            when = time/self.duration

            self._init_circle.position = Point(
                x=ratiod(self._start.x, self._end.x, when),
                y=ratiod(self._start.y, self._end.y, when)
            )

            return [self._init_circle]
        
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
        *args, **kwargs
    ):
        self._start_x = start_x
        self._end_x = end_x
        self._y_at = y_at

        self._init_circle = Circle(
            position=Point(0,0),
            fill_color=color,
            radius=radius
        )

        super().__init__(*args, **kwargs)


    def get_state(self, time:int) -> List[Shape]:
        if(time > 0 and time < self.duration):

            when = time/self.duration
            x = ratiod(self._start_x, self._end_x, when)
            self._init_circle.position = Point(
                x=x,
                y=self._y_at(x)
            )

            return [self._init_circle]
        
        return []
