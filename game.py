import pygame
from player import Player
from enemy import Enemy
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    SPAWN_DELAY,
    GROUND_LEVEL,
)


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Contra Clone")
    clock = pygame.time.Clock()

    player = Player((80, GROUND_LEVEL))
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    enemy_event = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_event, SPAWN_DELAY)

    score = 0
    font = pygame.font.SysFont(None, 32)
    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == enemy_event:
                enemy = Enemy(WIDTH + 40)
                enemies.add(enemy)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot(bullets)

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()
        enemies.update()

        # collisions
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        score += len(hits)
        if pygame.sprite.spritecollide(player, enemies, False):
            running = False

        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (100, 50, 20), (0, GROUND_LEVEL, WIDTH, HEIGHT - GROUND_LEVEL))
        all_sprites = pygame.sprite.Group(player, bullets, enemies)
        all_sprites.draw(screen)

        score_surf = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()
