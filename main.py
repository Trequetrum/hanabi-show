
from tkinter import *
from tkinter import ttk
from typing import Callable, List, Optional, Tuple, Union
from animation import Animation, CanvasRenderer, create_render_thunk
from fireworks import CircleLineFirework

def main() -> None:

    root = Tk()

    canvas = Canvas(root, bg="white", height=450, width=800)
    canvas.pack(side=LEFT)

    fireworks: List[Animation] = [
        CircleLineFirework(start=(30,400), end=(600,150), radius=15),
        CircleLineFirework(start=(750,400), end=(200,150), radius=10)
    ]

    # If the rederer is implemented correctly, render_fireworks is an
    # impotent function with no arguements.
    rederer = CanvasRenderer(canvas)
    render_fireworks = create_render_thunk(rederer, fireworks)

    button_frame = ttk.Frame(root, padding=10)
    button_frame.pack(side=RIGHT, fill=Y)

    ttk.Label(
        button_frame, 
        text="Run Your Animation!"
    ).pack(side=TOP)

    ttk.Button(
        button_frame, 
        text="Go", 
        command=render_fireworks
    ).pack(side=TOP)

    ttk.Button(
        button_frame, 
        text="Quit", 
        command=root.destroy
    ).pack(side=TOP)

    root.mainloop()


if __name__ == "__main__":
    main()
