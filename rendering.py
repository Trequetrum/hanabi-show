import tkinter.font as tkfont
import tkinter as tk
from tkinter import ttk, Canvas, ALL
from typing import Any, Callable, Dict, List, Tuple, TypedDict
import rx
from rx import operators as ops
from shapes import Arc, BoxCoords, Line, Oval, Polygon, PrimitiveShape, Rectangle, Shape, Circle, Color, Text
from animations import Animation
from utility import gen_unique_number

class Renderer():
    """Abstract Class

    Renderer contains all the details regarding rendering to a given 
    API. It's a wrapper class. By implementing this you can render 
    using HTML, tkinter canvas, kinter turtle, or even microsft paint
    (as examples) without needing to implement anything else.
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

    Be warned! Testing here has been minimal. 
    """

    @staticmethod
    def color_str(c: Color):
        "Outputs a string in the format that tk canvas expects"
        return '' if not c.visible else f'#{c.red:02X}{c.green:02X}{c.blue:02X}'

    def __init__(self, canvas: Canvas) -> None:
        self.canvas = canvas
        self.layers: Dict[str, Dict[int, ConvasSceneToken]] = dict()

    def create_default_shape(self, shape: Shape) -> int:
        """ Canvas tracks items by ID but also by what type of thing
        they are. We use this to tell canvas what type of thing is
        attached to each ID, then we never worry about that again,
        we can safely update afterward.
        """
        if isinstance(shape, Text):
            return self.canvas.create_text(0,0)
        if isinstance(shape, Circle) or isinstance(shape, Oval):
            return self.canvas.create_oval(0,0,0,0)
        if isinstance(shape, Line):
            return self.canvas.create_line(0,0,0,0)
        if isinstance(shape, Polygon):
            return self.canvas.create_polygon(0,0,0,0,0,0)
        if isinstance(shape, Rectangle):
            return self.canvas.create_rectangle(0,0,0,0)
        if isinstance(shape, Arc):
            return self.canvas.create_arc(0,0,0,0)

        raise NotImplementedError

    def update_shape(self, item_dict: Dict[int, ConvasSceneToken], shape: Shape) -> None:
        """Updating shapes
        Most drawn shapes on the canvas are described by some set of
        coordinates (how many depends on the type of thing) and a 
        dictionary of options.

        Here we set update_item_config and update_item_coords 
        depending on what is being updated.
        """
        update_item_config: Any = dict()
        update_item_coords: List[int] = []

        canvas_item = item_dict[shape.id]

        if isinstance(shape, Text):
            update_item_coords = [shape.position.x, shape.position.y]
            update_item_config['fill'] = CanvasRenderer.color_str(shape.color)
            update_item_config['text'] = shape.text
            update_item_config['font'] = dict()
            font_config: Any = dict()
            if shape.font_family != "default":
                font_config['family'] = shape.font_family
            if shape.font_size > 0:
                font_config['size'] = shape.font_size
            font_config['weight'] = "bold" if shape.font_bold else "normal"
            font_config['slant'] = "italic" if shape.font_slant else "roman"
            font_config['underline'] = 1 if shape.font_underline else 0
            font_config['overstrike'] = 1 if shape.font_underline else 0
            update_item_config['font'] = tkfont.Font(**font_config)

        if isinstance(shape, PrimitiveShape):
            update_item_config['fill'] = CanvasRenderer.color_str(shape.fill_color)
            update_item_config['outline'] = CanvasRenderer.color_str(shape.line_color)
            update_item_config['width'] = shape.line_width
        
        if isinstance(shape, BoxCoords):
            update_item_coords = [
                shape.upper_left.x,
                shape.upper_left.y,
                shape.lower_right.x,
                shape.lower_right.y
            ]

        if isinstance(shape, Circle):
            update_item_coords = [
                shape.position.x - shape.radius,
                shape.position.y - shape.radius,
                shape.position.x + shape.radius,
                shape.position.y + shape.radius
            ]
        
        if isinstance(shape, Line) or isinstance(shape, Polygon):
            v_tex_s = map(lambda p: [p.x, p.y], shape.vertices)
            update_item_coords = [j for sub in v_tex_s for j in sub]

        if isinstance(shape, Arc):
            update_item_config['start'] = shape.start
            update_item_config['extent'] = shape.extent
            if shape.style == Arc.STYLE_ARC:
                update_item_config['style'] = tk.ARC
            elif shape.style == Arc.STYLE_CHORD:
                update_item_config['style'] = tk.CHORD
            else:
                update_item_config['style'] = tk.PIESLICE

        self.canvas.coords(canvas_item['id'], *update_item_coords)
        self.canvas.itemconfigure(canvas_item['id'], **update_item_config)


    def update_animation_layer(self, layer: str, shapes: List[Shape]) -> None:
        """How this works:

            1. Grab the current layer (make a new one if nessesary)
            2. Create items in the canvas for any new shapes
            3. Update all the shapes
            4. Delete all items in the canvas that don't have a 
               matching shape in the list of shapes
            5. profit
        
        Sode note: Step 4 is managed with somthing akin to a dirty
        bit you might see in an operating system's memory management
        scheme
        """

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
                self.canvas.delete(token['id'])
            else:
                item_dict[id]['dirty'] = False


    def clear_animation_layer(self, layer: str) -> None:
        self.canvas.delete((layer))


    def clear_everything(self) -> None:
        self.canvas.delete(ALL)


class RenderThunk():
    """Run an animation
    
    This class has a single function `render` returns a thunk that runs 
    the given animation in the given rederer.
    """

    def __init__(self,
        renderer: Renderer, 
        animation: Animation,
        refresh_rate: int = 50 # milliseconds
    ):
        self.renderer = renderer
        self.animation = animation
        self.refresh_rate = refresh_rate # milliseconds
        self._refresh_rate_s = refresh_rate * 0.001 # seconds
        self._duration_s = animation.duration * 0.001 # seconds


    def render(self) -> None:
        
        layer_name = f"""{self.animation.name}_{gen_unique_number()}
            """.translate({ord(c):None for c in ' \n\t\r'})


        rx.interval(self._refresh_rate_s).pipe(
            ops.take_until_with_time(self._duration_s),
            ops.take(round(self._duration_s/self._refresh_rate_s + 0.5)),
            ops.map(lambda v: v * self.refresh_rate),
            ops.map(lambda time: self.animation.get_state(time)),
            ops.do_action(on_completed=lambda: 
                self.renderer.clear_animation_layer(layer_name)
            )
        ).subscribe(lambda shapes: 
            self.renderer.update_animation_layer(layer_name, shapes)
        )
