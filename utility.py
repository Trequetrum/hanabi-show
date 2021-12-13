def ratiod(start: int, end: int, ratio:float) -> int:
    return round(((end - start) * ratio) + start)

def clamp_int(v:int, min_v:int, max_v:int) -> int:
    return max(min_v, min(max_v, v))