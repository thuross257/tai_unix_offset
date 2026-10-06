"""TAI Unix Offset — convert between Unix timestamps and International Atomic Time.

Unix time counts seconds since 1970-01-01T00:00:00Z but pauses (via leap
seconds) to stay close to UT1. TAI counts seconds without pausing. The
difference grows each time a leap second is inserted. This module keeps the
authoritative leap-second table and exposes conversions that are exact at
both sides of each leap boundary.
"""

from .core import (
    LEAP_SECONDS,
    TAI_OFFSET,
    unix_to_tai,
    tai_to_unix,
)

__all__ = [
    "LEAP_SECONDS",
    "TAI_OFFSET",
    "unix_to_tai",
    "tai_to_unix",
]
