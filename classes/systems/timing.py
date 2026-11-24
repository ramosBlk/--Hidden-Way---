import math


FIXED_TIMESTEP = 1 / 60
MAX_FRAME_DELTA = 0.25


def accumulate_frame_time(frame_delta, accumulator):
    """Return the number of fixed updates due and the remaining fractional time."""
    if not math.isfinite(frame_delta) or frame_delta < 0:
        raise ValueError("frame_delta deve ser um número finito não negativo.")
    if not math.isfinite(accumulator) or accumulator < 0:
        raise ValueError("accumulator deve ser um número finito não negativo.")

    total = accumulator + min(frame_delta, MAX_FRAME_DELTA)
    steps = int((total + 1e-9) / FIXED_TIMESTEP)
    remainder = max(0.0, total - steps * FIXED_TIMESTEP)
    return steps, remainder
