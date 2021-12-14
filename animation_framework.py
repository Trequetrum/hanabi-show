from tkinter import *
from tkinter import ttk
from typing import Any, Callable, Dict, List, Tuple, TypedDict
import rx
from rx import operators as ops
from shapes import Shape, Circle, Color
from animations import Animation


class Renderer():
    """Abstract Class

    Renderer contain all the details about the specifics of rendering
    to a given API. It's a wrapper class. By implementing this you 
    can render using HTML, tkinter canvas, or kinter turtle without
    needing to implement anything else. 
    """
    def update_animation_layer(self, layer: str, shapes: List[Shape]) -> None:
        raise NotImplementedError
    def clear_animation_layer(self, layer: str) -> None:
        raise NotImplementedError
    def clear_everything(self) -> None:
        raise NotImplementedError


class ConvasSceneToken(TypedDict):
    "A helper class for CanvasRenderer"
    id: int
    dirty: bool


class CanvasRenderer(Renderer):
    """A Canvas Renderer Implementation

    This is a partial implementation as it currently only renders
    circles. Good enough to test out.
    """

    @staticmethod
    def color_str(c: Color):
        "Outputs a string in the format that tk canvas expects"
        return f'#{c.red:02X}{c.green:02X}{c.blue:02X}'

    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self.layers: Dict[str, Dict[int, ConvasSceneToken]] = dict()

    def create_default_shape(self, shape: Shape) -> int:
        """ Canvas tracks items by ID but also by what type of thing
        they are. We use this to tell canvas what type of thing is
        attached to each ID, then we never worry about that again,
        we can safely update afterward.
        """
        if isinstance(shape, Circle):
            return self.canvas.create_oval(0,0,0,0)

        raise NotImplementedError

    def update_shape(self, item_dict: Dict[int, ConvasSceneToken], shape: Shape) -> None:
        """Updating shapes
        Most drawn shapes on the canvas are described by some set of
        coordinates (how many depends on the type of thing) and an
        optional dictionary of options.

        Here we set update_item_config and update_item_coords 
        depending on what is being updated.
        """
        update_item_config: Any = dict()
        update_item_coords: List[int] = []

        color = CanvasRenderer.color_str(shape.color)
        update_item_config['fill'] = color if shape.fill else ''

        canvas_item = item_dict[shape.id]
        
        if isinstance(shape, Circle):
            update_item_coords = [
                shape.pos['x'] - shape.radius,
                shape.pos['y'] - shape.radius,
                shape.pos['x'] + shape.radius,
                shape.pos['y'] + shape.radius
            ]  
        else:
            raise NotImplementedError

        self.canvas.coords(canvas_item['id'], *update_item_coords)
        self.canvas.itemconfigure(canvas_item['id'], **update_item_config)


    def update_animation_layer(self, layer: str, shapes: List[Shape]) -> None:
        if not layer in self.layers:
            self.layers[layer] = dict()
        
        item_dict = self.layers[layer]

        for shape in shapes:
            if not shape.id in item_dict:
                new_id = self.create_default_shape(shape)
                self.canvas.itemconfigure(new_id, tags=layer)
                item_dict[shape.id] = {
                    'id': new_id,
                    'dirty': False
                }

        for shape in shapes:
            # assert shape.id in item_dict
            item_dict[shape.id]['dirty'] = True
            self.update_shape(item_dict, shape)
        
        for (id, token) in list(item_dict.items()):
            if token['dirty'] == False:
                del item_dict[id]
                self.canvas.delete(id)
            else:
                item_dict[id]['dirty'] = False

    def clear_animation_layer(self, layer: str) -> None:
        self.canvas.delete(layer)

    def clear_everything(self) -> None:
        self.canvas.delete(ALL)


def flatten_to_shapes(time: int, fireworks: List[Animation]) -> List[Shape]:
    t = map(lambda v: v.get_state(time), fireworks)
    return [item for sublist in t for item in sublist]


count = 0
def gen_layer_name(prefix):
    "TODO: Fix this. This is a hack to get unique names."

    global count
    count += 1
    return f"{prefix}_{count}"

def create_render_thunk(
    r: Renderer, 
    animation: Animation,
    refresh_rate: int = 50 # milliseconds
) -> Callable[[], None]:
    """Run an animation
    
    This funtion returns a thunk that runs the given animation in the 
    given rederer. That makes it easy to instrament this thunk to be
    run by various UIs
    """

    refresh_rate_s = refresh_rate * 0.001 # seconds
    duration_s = animation.duration * 0.001 # seconds

    def thunk_effect() -> None:
        
        layer_name = gen_layer_name(animation.name)

        rx.interval(refresh_rate_s).pipe(
            ops.take(round(duration_s/refresh_rate_s)),
            ops.map(lambda v: v * refresh_rate),
            ops.map(lambda time: animation.get_state(time)),
            ops.do_action( 
                on_completed=lambda: r.update_animation_layer(layer_name, [])
            )
        ).subscribe(
            lambda shapes: r.update_animation_layer(layer_name, shapes)
        )
    
    return thunk_effect
