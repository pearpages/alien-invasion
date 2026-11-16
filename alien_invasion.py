import sys
from time import sleep

import pygame

from alien import Alien
from assets import Assets
from bullet import Bullet
from button import Button
from config import Config
from difficulty import Difficulty
from game_stats import GameStats
from rules import can_fire, fleet_positions, points_for_hits, reached_bottom
from scoreboard import Scoreboard
from ship import Ship


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self, config: Config, screen: pygame.Surface, assets: Assets):
        """Set up a game that draws on screen, using config and assets."""
        self.config = config
        self.screen = screen
        self.assets = assets
        self.clock = pygame.time.Clock()
        self.difficulty = Difficulty.starting(config)
        bounds = screen.get_rect()

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(ships_left=config.ship_limit)
        self.sb = Scoreboard(self.stats, config.bg_color, assets.ship, bounds)

        # 1 moves the fleet right; -1 moves it left.
        self.fleet_direction = 1

        self.ship = Ship(assets.ship, bounds)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        self.game_active = False

        # Make the Play button.
        self.play_button = Button("Play", bounds.center)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update(self.difficulty.ship_speed)
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Back to level 1 speeds, with the fleet moving right.
            self.difficulty = Difficulty.starting(self.config)
            self.fleet_direction = 1

            # Reset the game statistics.
            self.stats.reset(self.config.ship_limit)
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if can_fire(len(self.bullets), self.config.bullets_allowed):
            new_bullet = Bullet(
                self.ship.rect.midtop,
                (self.config.bullet_width, self.config.bullet_height),
                self.config.bullet_color,
            )
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update(self.difficulty.bullet_speed)

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            self.stats.score += points_for_hits(
                map(len, collisions.values()), self.difficulty.alien_points
            )
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.difficulty = self.difficulty.next_level(self.config)

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update(self.difficulty.alien_speed * self.fleet_direction)

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        bottoms = (alien.rect.bottom for alien in self.aliens)
        if reached_bottom(bottoms, self.config.screen_height):
            # Treat this the same as if the ship got hit.
            self._ship_hit()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien_image = self.assets.alien
        alien_width, alien_height = alien_image.get_size()

        for x, y in fleet_positions(
            self.config.screen_width,
            self.config.screen_height,
            alien_width,
            alien_height,
        ):
            # Every alien shares the one image loaded at start-up.
            self.aliens.add(Alien(alien_image, x, y))

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        width = self.config.screen_width
        if any(alien.check_edges(width) for alien in self.aliens):
            self._change_fleet_direction()

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.config.fleet_drop_speed
        self.fleet_direction *= -1

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.config.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw(self.screen)
        self.ship.draw(self.screen)
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.draw(self.screen)

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw(self.screen)

        pygame.display.flip()


def main():
    """Build everything the game needs, connect it, and run the game.

    This is the only place that creates the window and loads files; every
    class receives what it needs from here.
    """
    pygame.init()
    config = Config()
    screen = pygame.display.set_mode(
        (config.screen_width, config.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    assets = Assets.load()

    AlienInvasion(config, screen, assets).run_game()


if __name__ == "__main__":
    main()
