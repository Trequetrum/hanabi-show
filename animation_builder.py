import copy
from animation import Animation
from typing import Any, Callable, List, TypeVar
from shapes import Picture, Point, Shape, Color
from utility import clamp_int, ratiod


class AnimationBuilder(Animation):
    """Animate properties on a subject (Picture)

    Be careful, 
    """
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
    start_time: int,
    # The ideal type here would be something like
    # Callable[T, T, int, ...], T|None]
    # but python type hints don't allow that as of yet. The current
    # work-around is to type out an overload for each additional arg
    # or kwarg and I can't be bothered to do that for a little bit of 
    # extra type safety.
    setter: Callable[..., T|None],
    **kwargs: Any
):
    def curry_source(src: Any):
        prop_val: T = getattr(src, prop)
        init: T | None = None
        def curry_time(time: int):
            nonlocal init
            local_time = time - start_time
            if local_time > 0:
                if init is None: init = copy.deepcopy(getattr(src, prop))
                newval = setter(prop_val, init, local_time, **kwargs)
                if not (newval is None): setattr(src, prop, newval)
        return curry_time
    return curry_source

# Setters always have the form 
#
#   fn(property: T, initial:T, time:int, * , ...kwargs: Any) -> T | None
#
# Where '...kwargs' means zero or more keyword arguements (as apposed
# to a function that must accept all keyword args '**kwargs'). 
# animate_property just passes any kwargs its given unchanged to the
# setter. This lets you create a setter with any number of arguements

def _int_setter_linear(property: int, initial:int, time:int, *, target:int, duration:int) -> int:
    "Type: UpdaterFunction[int]"
    when = time/duration
    return ratiod(initial, target, when)

def _point_setter_linear(property: Point, initial: Point, time: int, *, target: Point, duration: int) -> None:
    "UpdaterFunction for Points"
    when = time/duration
    property.x = ratiod(initial.x, target.x, when)
    property.y = ratiod(initial.y, target.y, when)

def _color_setter_linear(property: Color, initial: Color, time: int, *, target: Color, duration: int) -> None:
    "UpdaterFunction for Colors"
    when = time/duration
    property.red = clamp_int(ratiod(initial.red, target.red, when), 0 ,255)
    property.green = clamp_int(ratiod(initial.green, target.green, when), 0 ,255)
    property.blue = clamp_int(ratiod(initial.blue, target.blue, when), 0 ,255)

def _vertices_setter_linear(property: List[Point], initial: List[Point], time: int, *, target: List[Point], duration: int) -> None:
    "UpdaterFunction for a list of points"
    for p, i, t in zip(property, initial, target):
        _point_setter_linear(p, i, time, target=t, duration=duration)

# animate_property is a bit unweildy from an API perspective. It gives
# you almost too much flexibility. So here we define a public api for
# some ways to animate certain types of properties. These just defer
# to animate_property underneith.

def animate_int(prop: str, target: int, duration: int, start: int = 0):
    return animate_property(prop, start, _int_setter_linear, target=target, duration=duration)

def animate_point(prop: str, target: Point, duration: int, start:int = 0):
    return animate_property(prop, start, _point_setter_linear, target=target, duration=duration)

def animate_color(prop: str, target: Color, duration: int, start:int = 0):
    return animate_property(prop, start, _color_setter_linear, target=target, duration=duration)

def animate_vertices(prop: str, target: List[Point], duration: int, start:int = 0):
    return animate_property(prop, start, _vertices_setter_linear, target=target, duration=duration)