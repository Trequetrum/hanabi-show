from random import randint
from typing import Any, List
from shapes import Circle, ColorNames, Point, PurePicture
from animation import Animation, Scene, CircleTravelAlongAFunction, CirleMove
from animation_builder import AnimationBuilder, animate_color, animate_int, animate_point
import gui
from utility import gen_unique_number

def firework_via_builder() -> Animation:
    random_start = Point(randint(50, 750), randint(400, 450))
    random_end = Point(randint(50, 750), randint(50, 150))

    start_pos = lambda: Point(random_start.x, random_start.y)
    end_pos = lambda: Point(random_end.x, random_end.y)

    trunk: Any = AnimationBuilder(
        subject=PurePicture(Circle(
            fill_color=ColorNames.BLACK(),
            line_color=ColorNames.BLACK(),
            line_width=1,
            position=start_pos(),
            radius=15
        )),
        animators=[
            animate_color('fill_color', ColorNames.random(), 1000),
            animate_color('fill_color', ColorNames.random(), 1000, 1000),
            animate_color('fill_color', ColorNames.random(), 1000, 2000),
            animate_color('fill_color', ColorNames.random(), 1000, 3000),
            animate_int('radius', 3, 4000),
            animate_point('position', end_pos(), 4000)
        ],
        duration=4000, 
        name="Trunk"
    )

    peaks: Any = [
        AnimationBuilder(
            subject=PurePicture(Circle(
                fill_color=ColorNames.random(),
                line_color=ColorNames.BLACK(),
                line_width=1,
                position=end_pos(),
                radius=randint(5, 9)
            )), 
            duration=randint(1500,2500), 
            name=f"Peak{x}"
        ) 
        for x in range(10)
    ]

    for peak in peaks:
        peak.add_animators(
            animate_color('fill_color', ColorNames.random(), peak.duration),
            animate_int('radius', 0, peak.duration),
            animate_point(
                'position', 
                Point(
                    end_pos().x + randint(-100, 100),
                    end_pos().y + randint(-100, 100)
                ), 
                peak.duration
            )
        )

    return Scene(
        name=f"Builder Firework {gen_unique_number()}", 
        animations=[(0, trunk)] + [(4000, x) for x in peaks]
    )

def firework_via_subclassing_animiation() -> Animation:
    trunk: Animation = CircleTravelAlongAFunction(
        name="Trunk",
        start_x=30, 
        end_x=550,
        y_at=lambda x: round((x * -0.5) + 400),
        duration=3000,
        radius=15,
        color=ColorNames.YELLOW()
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
            color=ColorNames.CYAN()
        ),
        # Probably easier to just give a start and end location
        CirleMove(
            start=Point(550, 125),
            end=Point(550, 50),
            duration=2000,
            radius=6,
            color=ColorNames.LIME()
        ),
        CirleMove(
            start=Point(550, 125),
            end=Point(450, 200),
            duration=2100,
            radius=7,
            color=ColorNames.NAVY()
        ),
        CirleMove(
            start=Point(550, 125),
            end=Point(650, 250),
            duration=2200,
            radius=8,
            color=ColorNames.GREEN()
        ),
        CirleMove(
            start=Point(550, 125),
            end=Point(500, 400),
            duration=3000,
            radius=9,
            color=ColorNames.PURPLE()
        ),
        CirleMove(
            start=Point(550, 125),
            end=Point(650, 10),
            duration=2300,
            radius=8,
            color=ColorNames.SILVER()
        )
    ]

    for i, p in enumerate(peaks, start=1):
        p.name = f"Peak{i}"

    return Scene(
        name="Subclassing Firework", 
        animations=[(0, trunk)] + list(map(lambda v: (3000, v), peaks))
    )

def main() -> None:
    a = [firework_via_subclassing_animiation()]
    b = [firework_via_builder() for x in range(10)]
    together = Scene(
        name="All At Once",
        animations=[(0, ani) for ani in (a + b)]
    )
    staggered = Scene(
        name="All Staggered",
        animations=[(i * 500, ani) for i, ani in enumerate(a + b)]
    )

    gui.tkcanvas_animiation_gui([*a, *b, together, staggered])



if __name__ == "__main__":
    main()
