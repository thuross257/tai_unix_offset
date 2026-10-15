# TAI Unix Offset

Maintains the leap-second table and converts between Unix timestamps and International Atomic Time (TAI).

## Usage

```python
from tai_unix_offset import unix_to_tai, tai_to_unix, LEAP_SECONDS, TAI_OFFSET

# Unix 1483228801 is 2017-01-01T00:00:01Z, after the 2016-12-31 leap second.
# TAI is 37 seconds ahead of Unix time at that instant.
assert unix_to_tai(1483228801) == 1483228838

# Inverse for a normal (non-leap) timestamp is exact.
assert tai_to_unix(unix_to_tai(1500000000)) == 1500000000
```

## Why

Unix time reuses the same integer second for both halves of a positive leap
second, so mapping Unix↔TAI across a leap boundary is not a plain addition.
This library encodes the authoritative leap-second history and applies the
correct offset on each side.

The table starts at 2015-07-01 (the 36th leap) and records each subsequent
leap with the Unix timestamp at which the new, higher offset takes effect.
Earlier history is omitted because the systems this targets only need to
reason about recent and future timestamps; carrying 1972–2015 history would
add rows that are never exercised.

## Edge cases

* At a leap boundary `B`, `unix_to_tai(B)` returns the TAI instant at the
  *start* of the leap second (using the pre-jump offset). `unix_to_tai(B + 1)`
  returns one TAI second later — both calls read the same integer Unix second
  but denote distinct atomic instants.
* `tai_to_unix` maps both TAI instants inside a leap second to the same lower
  Unix value `B`. The conversion is therefore many-to-one across a leap second.
* `float("nan")` inputs raise `ValueError`.

## Exports

`LEAP_SECONDS` — `list[tuple[int, int]]` of `(unix_threshold, new_offset)`.
`TAI_OFFSET` — `int`, the offset at Unix time 0 and before the first table entry.
`unix_to_tai(unix: float) -> float`
`tai_to_unix(tai: float) -> float`

## Tests

```
PYTHONPATH=src python -m unittest discover -s tests
```

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

