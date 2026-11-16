import pygame

from alien import Alien
from bullet import Bullet
from ship import Ship

# --- Ship --------------------------------------------------------------------


def test_ship_starts_at_the_bottom_center(ship_image, bounds):
    ship = Ship(ship_image, bounds)

    assert ship.rect.midbottom == bounds.midbottom


def test_ship_moves_while_a_key_is_held(ship_image, bounds):
    ship = Ship(ship_image, bounds)
    start = ship.rect.x

    ship.moving_right = True
    for _ in range(10):
        ship.update(speed=2)

    assert ship.rect.x == start + 20


def test_ship_stops_at_the_right_side(ship_image, bounds):
    ship = Ship(ship_image, bounds)

    ship.moving_right = True
    for _ in range(1000):
        ship.update(speed=2)

    assert ship.rect.right == bounds.right


def test_center_ship_brings_it_back(ship_image, bounds):
    ship = Ship(ship_image, bounds)
    ship.moving_left = True
    for _ in range(50):
        ship.update(speed=2)

    ship.center_ship()

    assert ship.rect.midbottom == bounds.midbottom


# --- Alien -------------------------------------------------------------------


def test_alien_starts_where_it_is_told(alien_image):
    alien = Alien(alien_image, 60, 40)

    assert alien.rect.topleft == (60, 40)


def test_alien_moves_by_dx(alien_image):
    alien = Alien(alien_image, 100, 40)

    alien.update(dx=3)
    alien.update(dx=-1)

    assert alien.rect.x == 102


def test_alien_knows_when_it_touches_a_side(alien_image):
    assert Alien(alien_image, 0, 40).check_edges(1200)
    assert Alien(alien_image, 1140, 40).check_edges(1200)
    assert not Alien(alien_image, 500, 40).check_edges(1200)


def test_aliens_can_share_one_image(alien_image):
    first = Alien(alien_image, 0, 0)
    second = Alien(alien_image, 100, 0)

    assert first.image is second.image


# --- Bullet ------------------------------------------------------------------


def test_bullet_starts_at_the_given_point_and_flies_up():
    bullet = Bullet(midtop=(600, 700), size=(3, 15), color=(60, 60, 60))
    assert bullet.rect.midtop == (600, 700)

    bullet.update(speed=10)

    assert bullet.rect.top == 690


def test_bullet_draws_its_color_on_any_surface():
    surface = pygame.Surface((20, 20))
    bullet = Bullet(midtop=(10, 0), size=(3, 15), color=(255, 0, 0))

    bullet.draw(surface)

    assert surface.get_at((10, 5))[:3] == (255, 0, 0)
