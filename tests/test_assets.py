from assets import Assets


def test_assets_load_the_real_images_wherever_tests_run_from():
    assets = Assets.load()

    assert assets.ship.get_size() == (60, 48)
    assert assets.alien.get_size() == (60, 40)
