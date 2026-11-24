import math

import pytest

from classes.systems.timing import accumulate_frame_time


@pytest.mark.parametrize(
    "frame_delta, frame_count",
    ((1 / 60, 60), (1 / 30, 30), (1 / 120, 120)),
)
def test_fixed_timestep_is_independent_of_render_rate(frame_delta, frame_count):
    accumulator = 0.0
    update_count = 0

    for _ in range(frame_count):
        steps, accumulator = accumulate_frame_time(frame_delta, accumulator)
        update_count += steps

    assert update_count == 60
    assert accumulator == pytest.approx(0.0, abs=1e-8)


def test_long_pause_is_capped_to_a_bounded_catch_up():
    steps, accumulator = accumulate_frame_time(10.0, 0.0)

    assert steps == 15
    assert accumulator == pytest.approx(0.0)


@pytest.mark.parametrize("value", (-0.1, math.inf, math.nan))
def test_invalid_elapsed_time_is_rejected(value):
    with pytest.raises(ValueError):
        accumulate_frame_time(value, 0.0)
