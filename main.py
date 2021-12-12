from typing import Callable, List, Optional, Tuple, Union
from animation import Animation
from fireworks import AnimateSegment
import gui

def main() -> None:
    fireworks: List[Animation] = [
        AnimateSegment(start=(30,400), end=(600,150), radius=15),
        AnimateSegment(start=(750,400), end=(200,150), radius=10)
    ]
    gui.tkcanvas_animiation_gui(fireworks)


if __name__ == "__main__":
    main()
