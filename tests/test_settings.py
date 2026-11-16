import pytest

from settings import Settings


def test_increase_speed_multiplies_speeds_by_speedup_scale():
    settings = Settings()
    ship, bullet, alien = (
        settings.ship_speed,
        settings.bullet_speed,
        settings.alien_speed,
    )

    settings.increase_speed()

    scale = settings.speedup_scale
    assert settings.ship_speed == pytest.approx(ship * scale)
    assert settings.bullet_speed == pytest.approx(bullet * scale)
    assert settings.alien_speed == pytest.approx(alien * scale)


def test_increase_speed_makes_aliens_worth_more():
    settings = Settings()
    points = settings.alien_points

    settings.increase_speed()

    assert settings.alien_points > points


def test_initialize_dynamic_settings_undoes_speedups():
    settings = Settings()
    start = settings.alien_speed
    settings.increase_speed()

    settings.initialize_dynamic_settings()

    assert settings.alien_speed == start
