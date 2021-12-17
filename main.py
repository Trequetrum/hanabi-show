from animation import Scene
import gui
import examples

def main() -> None:
    a = examples.firework_via_subclassing_animiation()
    b = [examples.firework_via_builder() for x in range(10)]
    together = Scene(
        name="All At Once",
        animations=[(0, ani) for ani in [a, *b]]
    )
    staggered = Scene(
        name="All Staggered",
        animations=[(i * 500, ani) for i, ani in enumerate([a, *b])]
    )

    gui.tkcanvas_animiation_gui([a, *b, together, staggered])


if __name__ == "__main__":
    pass# main()
