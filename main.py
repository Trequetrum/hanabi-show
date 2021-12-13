from typing import Callable, List, Optional, Tuple, Union
from animation_framework import Animation, Scene
from shapes import ColorNames
from animations import CircleTravelAlongAFunction, CirleMove
import gui

def main() -> None:

    trunk = CircleTravelAlongAFunction(
        name="trunk",
        start_x=30, 
        end_x=550,
        y_at=lambda x: round((x * -0.5) + 400),
        duration=3000,
        radius=15,
        color=ColorNames.YELLOW
    )

    # start @ (x=550, y=125)
    # solve for b
    # y = mx + b
    # 125 = 0.5 * 550 + b
    # b = -(0.5 * 550 - 125)
    # b = -150
    peak1 = CircleTravelAlongAFunction(
        name="peak1",
        start_x=550,
        end_x=450,
        y_at=lambda x: round(x * 0.5 - 150),
        duration=2000,
        radius=5,
        color=ColorNames.CYAN
    )

    peaks = [
        CirleMove(
            start=(550, 125),
            end=(550, 50),
            duration=2000,
            radius=5,
            color=ColorNames.LIME
        ),
        CirleMove(
            start=(550, 125),
            end=(450, 200),
            duration=2100,
            radius=5,
            color=ColorNames.NAVY
        ),
        CirleMove(
            start=(550, 125),
            end=(650, 250),
            duration=2200,
            radius=5,
            color=ColorNames.GREEN
        ),
        CirleMove(
            start=(550, 125),
            end=(500, 400),
            duration=3000,
            radius=5,
            color=ColorNames.PURPLE
        ),
        CirleMove(
            start=(550, 125),
            end=(650, 10),
            duration=2300,
            radius=5,
            color=ColorNames.SILVER
        )
    ]

    together = Scene(
        name="together", 
        animations=[
            (0, trunk),
            (3000, peak1),
        ] + list(map(lambda v: (3000, v), peaks))
    )

    gui.tkcanvas_animiation_gui([trunk, peak1, together])


if __name__ == "__main__":
    main()
