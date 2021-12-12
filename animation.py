from tkinter import *
from tkinter import ttk
from typing import Callable, List, Tuple
import rx
from rx import operators as ops

class Shape():
    fill: bool
    color: str

class Circle(Shape):
    pos: Tuple[int, int]
    radius: int

    def __init__(self, pos:Tuple[int, int], radius: int, color="black", fill=True):
        self.pos = pos
        self.radius = radius
        self.fill = fill
        self.color = color

class Animation():

    def get_state(self, time:int) -> List[Shape]:
        raise NotImplementedError


class Renderer():

    def draw_shapes(self, shape: List[Shape]) -> None:
        raise NotImplementedError
    def clear_shapes(self) -> None:
        raise NotImplementedError


class CanvasRenderer(Renderer):

    canvas: Canvas

    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw_shape(self, shape: Shape) -> None:
        if(isinstance(shape, Circle)):
            coords = [
                shape.pos[0] - shape.radius,
                shape.pos[1] - shape.radius,
                shape.pos[0] + shape.radius,
                shape.pos[1] + shape.radius
            ]
            self.canvas.create_oval(*coords, fill=shape.color if shape.fill else '')
    
    def draw_shapes(self, shapes: List[Shape]) -> None:
        for s in shapes:
            self.draw_shape(s)

    def clear_shapes(self) -> None:
        self.canvas.delete(ALL)


def flatten_to_shapes(time: int, fireworks: List[Animation]) -> List[Shape]:
    t = map(lambda v: v.get_state(time), fireworks)
    return [item for sublist in t for item in sublist]


def create_render_thunk(
    r: Renderer, 
    animations: List[Animation],
    refresh_rate: int = 50 # milliseconds
) -> Callable[[], None]:

    refresh_rate_s = refresh_rate * 0.001 # seconds

    def effect() -> None:
        
        rx.interval(refresh_rate_s).pipe(
            ops.take(round(10/refresh_rate_s)),
            ops.map(lambda v: v * refresh_rate),
            ops.map(lambda time: flatten_to_shapes(time, animations)),
            ops.do_action(
                on_next=lambda _: r.clear_shapes(), 
                on_completed=lambda: r.clear_shapes()
            )
        ).subscribe(r.draw_shapes)
    
    return effect

    