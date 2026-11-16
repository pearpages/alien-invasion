from game_stats import GameStats
from scoreboard import Scoreboard


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
