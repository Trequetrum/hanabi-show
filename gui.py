from tkinter import *
from tkinter import ttk
from typing import Callable, List, Optional, Tuple, Union
from animation_framework import Animation, CanvasRenderer, create_render_thunk

def tkcanvas_animiation_gui(animations: List[Animation]) -> None:
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
            command=create_render_thunk(rederer, a)
        ).pack(side=TOP, fill=X)

    ttk.Button(
        button_frame, 
        text="Quit", 
        command=root.destroy
    ).pack(side=BOTTOM, fill=X)

    root.mainloop()
    
