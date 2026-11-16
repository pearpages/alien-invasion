import pytest

from game_stats import GameStats
from scoreboard import (
    Scoreboard,
    high_score_label,
    level_label,
    score_label,
)


def make_scoreboard(stats, ship_image, bounds):
    return Scoreboard(stats, (230, 230, 230), ship_image, bounds)


def test_icons_show_reserve_ships_not_the_one_in_play(ship_image, bounds):
    stats = GameStats(ships_left=3)
    scoreboard = make_scoreboard(stats, ship_image, bounds)

    assert len(scoreboard.ships) == 2


def test_icons_follow_ships_lost(ship_image, bounds):
    stats = GameStats(ships_left=3)
    scoreboard = make_scoreboard(stats, ship_image, bounds)

    stats.ships_left = 2
    scoreboard.prep_ships()

    assert len(scoreboard.ships) == 1


def test_new_high_score_is_recorded(ship_image, bounds):
    stats = GameStats(ships_left=3, score=500, high_score=200)
    scoreboard = make_scoreboard(stats, ship_image, bounds)

    scoreboard.check_high_score()

    assert stats.high_score == 500


def test_lower_score_leaves_the_high_score(ship_image, bounds):
    stats = GameStats(ships_left=3, score=100, high_score=200)
    scoreboard = make_scoreboard(stats, ship_image, bounds)

    scoreboard.check_high_score()

    assert stats.high_score == 200


# --- labels ------------------------------------------------------------------


@pytest.mark.parametrize(
    ("score", "text"), [(0, "Score: 0"), (1234, "Score: 1,230")]
)
def test_score_label(score, text):
    assert score_label(score) == text


def test_high_score_label():
    assert high_score_label(2450) == "High score: 2,450"


def test_level_label():
    assert level_label(3) == "Level: 3"


def test_labels_do_not_overlap_even_with_a_huge_score(ship_image, bounds):
    stats = GameStats(
        ships_left=3, score=9_999_990, high_score=9_999_990, level=99
    )
    scoreboard = make_scoreboard(stats, ship_image, bounds)
    icons = [ship.rect for ship in scoreboard.ships]
    texts = [
        scoreboard.score_rect,
        scoreboard.high_score_rect,
        scoreboard.level_rect,
    ]

    everything = texts + icons
    for i, first in enumerate(everything):
        for second in everything[i + 1 :]:
            assert not first.colliderect(second), (first, second)
    for rect in texts:
        assert bounds.contains(rect)


def test_bottom_is_below_everything_the_scoreboard_draws(ship_image, bounds):
    stats = GameStats(ships_left=3)
    scoreboard = make_scoreboard(stats, ship_image, bounds)
    rects = [
        scoreboard.score_rect,
        scoreboard.high_score_rect,
        scoreboard.level_rect,
        *(ship.rect for ship in scoreboard.ships),
    ]

    assert scoreboard.bottom == max(rect.bottom for rect in rects)
