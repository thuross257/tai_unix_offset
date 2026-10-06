from bisect import bisect_right
from typing import List, Tuple

LEAP_SECONDS: List[Tuple[int, int]] = [
    (1435708800, 36),  # 2015-07-01: offset 35 -> 36
    (1483228800, 37),  # 2017-01-01: offset 36 -> 37
]

TAI_OFFSET = 8

_THRESHOLDS = [ts for ts, _ in LEAP_SECONDS]
_OFFSETS = [off for _, off in LEAP_SECONDS]


def _offset_at(unix: float) -> int:
    i = bisect_right(_THRESHOLDS, unix)
    if i == 0:
        return TAI_OFFSET
    return _OFFSETS[i - 1]


def _offset_before(unix: float) -> int:
    i = bisect_right(_THRESHOLDS, unix)
    if i == 0:
        return TAI_OFFSET
    return _OFFSETS[i - 1] - 1 if _OFFSETS[i - 1] > TAI_OFFSET else TAI_OFFSET


def unix_to_tai(unix: float) -> float:
    if unix != unix:
        raise ValueError("Unix timestamp must be a finite number")
    return unix + _offset_at(unix)


def tai_to_unix(tai: float) -> float:
    if tai != tai:
        raise ValueError("TAI timestamp must be a finite number")
    off = TAI_OFFSET
    for i, (B, new_off) in enumerate(LEAP_SECONDS):
        off_before = TAI_OFFSET if i == 0 else _OFFSETS[i - 1]
        if B + off_before <= tai < B + off_before + 2:
            return float(B)
        if tai >= B + off_before + 2:
            off = new_off
    return tai - off
