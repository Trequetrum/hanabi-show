import copy
from animation import Animation
from typing import Any, Callable, List, TypeVar
from shapes import Picture, Point, Shape, Color
from utility import clamp_int, ratiod


class AnimationBuilder(Animation):
    def __init__(self, 
        subject: Picture,
        duration: int,
        animators: List[Callable[[Picture], Callable[[int], None]]] = [],
        *args, **kwargs
    ):
        self._subject = subject
        self._animators: List[Callable[[int], None]] = []
        self.add_animators(*animators)
        super().__init__(duration, *args, **kwargs)

    def add_animators(self, *setters: Callable[[Picture], Callable[[int], None]]) -> None:
        self._animators += [f(self._subject) for f in setters]
        
    def get_state(self, time:int) -> List[Shape]:
        if(time > 0 and time < self.duration):

            for setter in self._animators:
                setter(time)
            return self._subject.get_shapes()
        
        return []
        
T = TypeVar('T')

def animate_property(
    prop: str, 
    target: T, 
    duration: int, 
    start_time: int, 
    update: Callable[[T,T,T,int,int], T|None]
):
    def curry_source(src: Any):
        prop_val: T = getattr(src, prop)
        init: T | None = None
        def curry_time(time: int):
            nonlocal init
            local_time = time - start_time
            if local_time > 0:
                if init is None: init = copy.copy(getattr(src, prop))
                newval = update(prop_val, init, target, local_time, duration)
                if not (newval is None): setattr(src, prop, newval)
        return curry_time
    return curry_source

def int_setter_linear(int: int, start:int, target:int, time:int, duration:int):
    when = time/duration
    return ratiod(start, target, when)

def animate_int(prop: str, target: int, duration: int, start: int = 0):
    return animate_property(prop, target, duration, start, int_setter_linear)

def point_setter_linear(point: Point, start: Point, target: Point, time: int, duration: int):
    when = time/duration
    point.x = ratiod(start.x, target.x, when)
    point.y = ratiod(start.y, target.y, when)

def animate_point(prop: str, target: Point, duration: int, start:int = 0):
    return animate_property(prop, target, duration, start, point_setter_linear)

def color_setter_linear(color: Color, start: Color, target: Color, time: int, duration: int):
    when = time/duration
    color.red = clamp_int(ratiod(start.red, target.red, when), 0 ,255)
    color.green = clamp_int(ratiod(start.green, target.green, when), 0 ,255)
    color.blue = clamp_int(ratiod(start.blue, target.blue, when), 0 ,255)

def animate_color(prop: str, target: Color, duration: int, start:int = 0):
    return animate_property(prop, target, duration, start, color_setter_linear)

