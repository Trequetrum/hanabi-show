from typing import Callable, List, Optional, Tuple, Union
from shapes import ColorNames
from animations import Animation, Scene, CircleTravelAlongAFunction, CirleMove
import gui

def main() -> None:

    trunk: Animation = CircleTravelAlongAFunction(
        name="Trunk",
        start_x=30, 
        end_x=550,
        y_at=lambda x: round((x * -0.5) + 400),
        duration=3000,
        radius=15,
        color=ColorNames.YELLOW
    )
    
    peaks: List[Animation] = [
        # We need coord (x=550, y=125) to be on our line
        # picked slope = 0.5
        # solve for b
        # ------ ------ ------
        # y = mx + b
        # 125 = 0.5 * 550 + b
        # b = 125 - 0.5 * 550
        # b = -150
        CircleTravelAlongAFunction(
            start_x=550,
            end_x=450,
            y_at=lambda x: round(x * 0.5 - 150),
            duration=2000,
            radius=5,
            color=ColorNames.CYAN
        ),
        # Probably easier to just give a start and end location
        CirleMove(
            start=(550, 125),
            end=(550, 50),
            duration=2000,
            radius=6,
            color=ColorNames.LIME
        ),
        CirleMove(
            start=(550, 125),
            end=(450, 200),
            duration=2100,
            radius=7,
            color=ColorNames.NAVY
        ),
        CirleMove(
            start=(550, 125),
            end=(650, 250),
            duration=2200,
            radius=8,
            color=ColorNames.GREEN
        ),
        CirleMove(
            start=(550, 125),
            end=(500, 400),
            duration=3000,
            radius=9,
            color=ColorNames.PURPLE
        ),
        CirleMove(
            start=(550, 125),
            end=(650, 10),
            duration=2300,
            radius=8,
            color=ColorNames.SILVER
        )
    ]

    for i, p in enumerate(peaks, start=1):
        p.name = f"Peak{i}"

    together = Scene(
        name="All Together", 
        animations=[(0, trunk)] + list(map(lambda v: (3000, v), peaks))
    )

    gui.tkcanvas_animiation_gui([trunk, *peaks, together])



if __name__ == "__main__":
    main()
