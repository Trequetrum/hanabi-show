from tkinter import *
from tkinter import ttk
from typing import Callable, List, Tuple
from shapes import Shape, Circle, Color
import rx
from rx import operators as ops

class Animation():

    def __init__(self, duration: int, name: str = ''):
        self.duration = duration
        self.name = name

    def get_state(self, time:int) -> List[Shape]:
        raise NotImplementedError


class Scene(Animation):

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

class Renderer():

    def draw_shapes(self, shape: List[Shape]) -> None:
        raise NotImplementedError
    def clear_shapes(self) -> None:
        raise NotImplementedError


class CanvasRenderer(Renderer):

    canvas: Canvas

    @staticmethod
    def color_str(c: Color):
        return f'#{c.red:02X}{c.green:02X}{c.blue:02X}'

    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw_shape(self, shape: Shape) -> None:
        if(isinstance(shape, Circle)):
            color = CanvasRenderer.color_str(shape.color)

            coords = [
                shape.pos[0] - shape.radius,
                shape.pos[1] - shape.radius,
                shape.pos[0] + shape.radius,
                shape.pos[1] + shape.radius
            ]

            self.canvas.create_oval(*coords, fill=color if shape.fill else '')
    
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
    animation: Animation,
    refresh_rate: int = 50 # milliseconds
) -> Callable[[], None]:

    refresh_rate_s = refresh_rate * 0.001 # seconds
    duration_s = animation.duration * 0.001 # seconds

    def effect() -> None:
        
        rx.interval(refresh_rate_s).pipe(
            ops.take(round(duration_s/refresh_rate_s)),
            ops.map(lambda v: v * refresh_rate),
            ops.map(lambda time: animation.get_state(time)),
            ops.do_action(
                on_next=lambda _: r.clear_shapes(), 
                on_completed=lambda: r.clear_shapes()
            ),
            ops.do_action(
                on_completed=lambda: print("COMPLETE")
            )
        ).subscribe(r.draw_shapes)
    
    return effect
