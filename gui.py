from tkinter import ttk, Tk, Canvas, TOP, BOTTOM, LEFT, RIGHT, Y, X
from typing import List
from animation import Animation
from rendering import CanvasRenderer, RenderThunk

def tkcanvas_animiation_gui(animations: List[Animation]) -> None:
    """ Mega-simple GUI: 
    
    Lets you run a list of animations.
    The name of each animation is used as a lable for a button
    that runs the animation in a tkinter canvas.
    """
    root = Tk()

    canvas = Canvas(root, bg="white", height=450, width=800)
    canvas.pack(side=LEFT)

    rederer = CanvasRenderer(canvas)

    button_frame = ttk.LabelFrame(
        root,
        padding=10,
        text="Run Your Animation!"
    )
    button_frame.pack(side=RIGHT, fill=Y, pady=(5,0))

    for a in animations:
        ttk.Button(
            button_frame, 
            text=a.name, 
            command=RenderThunk(rederer, a).render
        ).pack(side=TOP, fill=X)

    ttk.Button(
        button_frame, 
        text="Quit", 
        command=root.destroy
    ).pack(side=BOTTOM, fill=X)

    root.mainloop()
    
