import pytest

from rules import (
    at_screen_edge,
    can_fire,
    fleet_positions,
    format_score,
    points_for_hits,
    reached_bottom,
    ship_step,
)

# --- fleet_positions ---------------------------------------------------------


def test_default_screen_fits_a_fleet_of_9_columns_by_8_rows():
    positions = fleet_positions(1200, 800, alien_width=60, alien_height=40)

    assert len(positions) == 72
    assert len({x for x, _ in positions}) == 9
    assert len({y for _, y in positions}) == 8


def test_fleet_starts_one_alien_in_and_is_spaced_one_alien_apart():
    positions = fleet_positions(1200, 800, alien_width=60, alien_height=40)

    assert positions[0] == (60, 40)
    assert positions[1] == (180, 40)  # next column: 2 alien widths along
    assert positions[9] == (60, 120)  # next row: 2 alien heights down
    assert positions[-1] == (1020, 600)


def test_fleet_keeps_clear_of_the_right_edge_and_the_bottom():
    positions = fleet_positions(1200, 800, alien_width=60, alien_height=40)

    assert all(x + 60 <= 1200 - 60 for x, _ in positions)
    assert all(y + 40 <= 800 - 3 * 40 for _, y in positions)


def test_no_fleet_when_the_screen_is_too_small():
    assert fleet_positions(150, 800, alien_width=60, alien_height=40) == []


# --- at_screen_edge ----------------------------------------------------------


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (100, 160, False),  # in the middle
        (0, 60, True),  # touching the left side
        (1140, 1200, True),  # touching the right side
        (1, 61, False),  # one pixel from the left side
        (1139, 1199, False),  # one pixel from the right side
    ],
)
def test_at_screen_edge(left, right, expected):
    assert at_screen_edge(left, right, screen_width=1200) is expected


# --- reached_bottom ----------------------------------------------------------


def test_reached_bottom_when_any_alien_touches_it():
    assert reached_bottom([100, 800, 300], screen_height=800)


def test_not_reached_bottom_when_all_aliens_are_above_it():
    assert not reached_bottom([100, 799], screen_height=800)


def test_an_empty_fleet_has_not_reached_bottom():
    assert not reached_bottom([], screen_height=800)


# --- points_for_hits ---------------------------------------------------------


def test_each_alien_hit_scores_its_points():
    assert points_for_hits([1, 1], alien_points=50) == 100


def test_one_bullet_hitting_two_aliens_scores_both():
    assert points_for_hits([2], alien_points=75) == 150


def test_no_hits_score_nothing():
    assert points_for_hits([], alien_points=50) == 0


# --- can_fire ----------------------------------------------------------------


@pytest.mark.parametrize(
    ("on_screen", "expected"), [(0, True), (2, True), (3, False)]
)
def test_can_fire_up_to_the_bullet_limit(on_screen, expected):
    assert can_fire(on_screen, bullets_allowed=3) is expected


# --- ship_step ---------------------------------------------------------------


def step(left=500, moving_left=False, moving_right=False):
    """Call ship_step for a 60-pixel-wide ship on a 1200-pixel screen."""
    return ship_step(
        left=left,
        right=left + 60,
        screen_width=1200,
        speed=1.5,
        moving_left=moving_left,
        moving_right=moving_right,
    )


def test_ship_stays_still_with_no_keys_held():
    assert step() == 0


def test_ship_moves_right_and_left_by_its_speed():
    assert step(moving_right=True) == 1.5
    assert step(moving_left=True) == -1.5


def test_holding_both_keys_cancels_out():
    assert step(moving_left=True, moving_right=True) == 0


def test_ship_stops_at_the_right_side():
    assert step(left=1140, moving_right=True) == 0


def test_ship_stops_at_the_left_side():
    assert step(left=0, moving_left=True) == 0


# --- format_score ------------------------------------------------------------


@pytest.mark.parametrize(
    ("score", "shown"),
    [
        (0, "0"),
        (50, "50"),
        (1234, "1,230"),
        (1_234_567, "1,234,570"),
        # round() sends exact halves to the even ten ("banker's rounding"):
        (1125, "1,120"),
        (1135, "1,140"),
    ],
)
def test_format_score(score, shown):
    assert format_score(score) == shown
