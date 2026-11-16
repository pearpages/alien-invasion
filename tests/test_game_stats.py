from game_stats import GameStats


def test_new_stats_start_at_level_1_with_no_score():
    stats = GameStats(ships_left=3)

    assert stats == GameStats(ships_left=3, score=0, level=1, high_score=0)


def test_reset_starts_a_new_game_but_keeps_the_high_score():
    stats = GameStats(ships_left=0, score=500, level=4, high_score=900)

    stats.reset(ship_limit=3)

    assert stats == GameStats(ships_left=3, score=0, level=1, high_score=900)
