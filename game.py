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


class Game:
    """The game itself: input, one frame of logic, and drawing.

    Each frame of the loop in run() does three separate jobs:

    - handle(event): turn one input event into what the player wants.
    - step(): move the world forward one frame.
    - draw(screen): paint the world on any surface.

    Only run() touches the real window, clock and mouse cursor, so tests
    can drive a game with made-up events and no window.
    """

    def __init__(self, config: Config, assets: Assets, high_score: int = 0):
        """Set up a game waiting for the player to click Play.

        high_score is the best score from earlier games, if any.
        """
        self.config = config
        self.assets = assets
        self.difficulty = Difficulty.starting(config)
        bounds = pygame.Rect(0, 0, config.screen_width, config.screen_height)

        # Create an instance to store game statistics,
        #   and create a scoreboard.
        self.stats = GameStats(
            ships_left=config.ship_limit, high_score=high_score
        )
        self.sb = Scoreboard(self.stats, config.bg_color, assets.ship, bounds)

        # 1 moves the fleet right; -1 moves it left.
        self.fleet_direction = 1

        self.ship = Ship(assets.ship, bounds)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start the game in an inactive state.
        self.game_active = False
        # The loop in run() keeps going until the player quits.
        self.running = True
        # Frames left to hold still after a crash; 0 means play on.
        self.pause_frames = 0

        # Make the Play button.
        self.play_button = Button("Play", bounds.center)

    def run(self, screen: pygame.Surface):
        """Run the game in a real window until the player quits."""
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                self.handle(event)
            self.step()
            self.draw(screen)

            # Show the mouse cursor only while waiting for Play.
            pygame.mouse.set_visible(not self.game_active)
            pygame.display.flip()
            clock.tick(60)

    def handle(self, event: pygame.event.Event):
        """Respond to one keyboard, mouse or window event."""
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._check_play_button(event.pos)
        elif event.type == pygame.KEYDOWN:
            self._check_keydown_events(event)
        elif event.type == pygame.KEYUP:
            self._check_keyup_events(event)

    def start(self):
        """Start a new game from level 1, keeping the high score."""
        # Back to level 1 speeds, with the fleet moving right.
        self.difficulty = Difficulty.starting(self.config)
        self.fleet_direction = 1
        self.pause_frames = 0

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

    def step(self):
        """Move the world forward one frame; nothing happens until Play."""
        if not self.game_active:
            return
        if self.pause_frames > 0:
            # Hold still after a crash; the loop keeps drawing and
            # reading input, so the window never freezes.
            self.pause_frames -= 1
            return
        self.ship.update(self.difficulty.ship_speed)
        self._update_bullets()
        self._update_aliens()

    def draw(self, screen: pygame.Surface):
        """Paint the current state of the game on screen."""
        screen.fill(self.config.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw(screen)
        self.ship.draw(screen)
        self.aliens.draw(screen)

        # Draw the score information.
        self.sb.draw(screen)

        # Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw(screen)

    def _check_play_button(self, mouse_pos: tuple[int, int]):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.start()

    def _check_keydown_events(self, event: pygame.event.Event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.running = False
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event: pygame.event.Event):
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
        # Lose the ship that was hit, then see if any are left.
        self.stats.ships_left -= 1
        self.sb.prep_ships()

        if self.stats.ships_left > 0:
            # Get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause for a moment before the new fleet starts moving.
            self.pause_frames = self.config.hit_pause_frames
        else:
            self.game_active = False

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
