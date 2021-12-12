from typing import List

def ratiod(start: int, end: int, ratio:float) -> int:
    return round(((end - start) * ratio) + start)
