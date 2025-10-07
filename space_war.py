import pygame
from pygame.sprite import Sprite, Group
import sys
import os

# --- Settings ---
class Settings:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.alien_points = 10

# --- Ship ---
class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        try:
            self.image = pygame.image.load('images/ship.jpg')
            self.image = pygame.transform.scale(self.image, (60, 40))
        except pygame.error as e:
            print(f"Error loading ship image: {e}. Using default rectangle.")
            self.image = pygame.Surface([60, 40])
            self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed
        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

# --- Bullet ---
class Bullet(Sprite):
    def __init__(self, ai_settings, screen, ship):
        super().__init__()
        self.screen = screen
        try:
            self.image = pygame.image.load('images/bullet.png')
            self.image = pygame.transform.scale(self.image, (ai_settings.bullet_width, ai_settings.bullet_height))
        except pygame.error as e:
            print(f"Error loading bullet image: {e}. Using default rectangle.")
            self.image = pygame.Surface([ai_settings.bullet_width, ai_settings.bullet_height])
            self.image.fill(ai_settings.bullet_color)
        self.rect = self.image.get_rect()
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.speed = ai_settings.bullet_speed

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

# --- Alien ---
class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        try:
            self.image = pygame.image.load('images/alien.jpg')
            self.image = pygame.transform.scale(self.image, (40, 40))
        except pygame.error as e:
            print(f"Error loading alien image: {e}. Using default rectangle.")
            self.image = pygame.Surface([40, 40])
            self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def update(self):
        self.x += self.ai_settings.alien_speed * self.ai_settings.fleet_direction
        self.rect.x = self.x

# --- Game Functions ---
def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.rect.right >= ai_settings.screen_width or alien.rect.left <= 0:
            for alien in aliens.sprites():
                alien.rect.y += ai_settings.fleet_drop_speed
                alien.x = float(alien.rect.x)
            ai_settings.fleet_direction *= -1
            break

def check_fleet_bottom(ai_settings, aliens, stats, screen):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            print("Game over: Aliens reached bottom!")
            stats.game_over = True
            return

def create_fleet(ai_settings, screen, aliens):
    print("Creating fleet...")
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = available_space_x // (2 * alien_width)
    number_rows = 5
    available_space_y = (ai_settings.screen_height - 3 * alien_height - ai_settings.screen_height // 3)
    number_rows = min(number_rows, available_space_y // (2 * alien_height))
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            alien = Alien(ai_settings, screen)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            alien.rect.y = alien_height + 2 * alien_height * row_number
            aliens.add(alien)

def check_events(ai_settings, screen, ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True
            elif event.key == pygame.K_LEFT:
                ship.moving_left = True
            elif event.key == pygame.K_SPACE:
                new_bullet = Bullet(ai_settings, screen, ship)
                bullets.add(new_bullet)
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False
            elif event.key == pygame.K_LEFT:
                ship.moving_left = False

def update_screen(ai_settings, screen, ship, aliens, bullets, stats):
    print("Updating screen...")
    screen.fill(ai_settings.bg_color)
    bullets.draw(screen)
    ship.blitme()
    aliens.draw(screen)
    # Score
    score_str = f"Score: {stats.score}"
    font = pygame.font.SysFont(None, 48)
    score_image = font.render(score_str, True, (0, 0, 0), ai_settings.bg_color)
    screen.blit(score_image, (10, 10))
    # Game won
    if len(aliens) == 0:
        print("Game won!")
        win_message = "You Won!"
        win_image = font.render(win_message, True, (0, 255, 0), ai_settings.bg_color)
        screen.blit(win_image, (ai_settings.screen_width // 2 - 100, ai_settings.screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()
    # Game Over
    if stats.game_over:
        print("Displaying Game Over...")
        game_over_message = "Game Over"
        game_over_image = font.render(game_over_message, True, (255, 0, 0), ai_settings.bg_color)
        screen.blit(game_over_image, (ai_settings.screen_width // 2 - 100, ai_settings.screen_height // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        sys.exit()
    pygame.display.flip()

# --- Game Stats ---
class GameStats:
    def __init__(self):
        self.score = 0
        self.game_over = False

def main():
    print("Starting game...")
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    stats = GameStats()
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    create_fleet(ai_settings, screen, aliens)

    while True:
        check_events(ai_settings, screen, ship, bullets)  # اصلاح: bulbs به bullets
        ship.update()
        bullets.update()
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
        if collisions:
            stats.score += ai_settings.alien_points * len(collisions)
        check_fleet_edges(ai_settings, aliens)
        check_fleet_bottom(ai_settings, aliens, stats, screen)
        aliens.update()
        update_screen(ai_settings, screen, ship, aliens, bullets, stats)

if __name__ == "__main__":
    main()