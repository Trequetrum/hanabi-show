
_count = 0
def gen_unique_number() -> int:
    "TODO: Fix this. This is a hack to get unique numbers. Fine for now"

    global _count
    _count += 1
    return _count

def ratiod(start: int, end: int, ratio:float) -> int:
    return round(((end - start) * ratio) + start)

def clamp_int(v:int, min_v:int, max_v:int) -> int:
    return max(min_v, min(max_v, v))
