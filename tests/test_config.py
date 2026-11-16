import dataclasses

import pytest

from config import Config


def test_config_cannot_be_changed():
    config = Config()

    with pytest.raises(dataclasses.FrozenInstanceError):
        config.ship_speed = 99


def test_config_values_can_be_overridden_when_created():
    config = Config(screen_width=800, ship_limit=5)

    assert config.screen_width == 800
    assert config.ship_limit == 5
    assert config.screen_height == 800  # untouched default
