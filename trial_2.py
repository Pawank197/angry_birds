import pygame
import math
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

def game_loop(screen):
    clock = pygame.time.Clock()
    dt = 0

    # Fonts (initialize after pygame.init())
    font_small = pygame.font.Font(None, 24)
    font_medium = pygame.font.Font(None, 36)

    # Ball setup
    radius = 40
    start_pos = pygame.Vector2(170, 520)
    player_pos = start_pos.copy()
    velocity = pygame.Vector2(0, 0)
    gravity = 980
    friction = 0.4
    bounce = 0.7

    # Slingshot
    dragging = False
    launch_ready = False
    mouse_start = pygame.Vector2()
    scale_power = 6
    break_threshold_woods = 900
    break_threshold_stones = 1200
    break_threshold_ice = 1050

    # Show trajectory points
    def show_projectile(velocity, start_pos):
        points = []
        if velocity.x == 0:
            return points
        for x in range(int(start_pos.x), 1280, 5):
            t = (x - start_pos.x) / t
            y = start_pos.y + velocity.y * t + 0.5 * gravity * t ** 2
            points.append((x, y))
        return points

    # Blocks
    blocks_woods = [
        pygame.Rect(900, 600, 100, 100),
        pygame.Rect(1010, 490, 100, 100),
    ]
    blocks_stones = [
        pygame.Rect(900, 490, 100, 100),
        pygame.Rect(1010, 380, 100, 100),
    ]
    blocks_ice = [
        pygame.Rect(900, 380, 100, 100),
        pygame.Rect(1010, 600, 100, 100),
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and not launch_ready:
                dragging = True
                mouse_start = pygame.Vector2(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP and dragging:
                dragging = False
                launch_ready = True
                mouse_end = pygame.Vector2(pygame.mouse.get_pos())
                launch_vector = mouse_start - mouse_end
                velocity = launch_vector * scale_power

        # Draw background
        background = pygame.image.load("assets/background-images/trial_background.jpg")
        background = pygame.transform.scale(background, (1280, 720))
        screen.blit(background, (0, 0))

        # Slingshot and trajectory
        if dragging:
            current_mouse = pygame.mouse.get_pos()
            aim_velocity = (mouse_start - current_mouse) * scale_power
            if aim_velocity.x != 0:
                points = show_projectile(aim_velocity, start_pos)
                pygame.draw.lines(screen, "lightgray", False, points, 2)

        slingshot = pygame.image.load("assets/objects/sling.png")
        slingshot = pygame.transform.scale(slingshot, (200 // 3, 400 // 3))
        screen.blit(slingshot, (100, 500))

        bird = pygame.image.load("assets/Birds/Red.png")
        bird = pygame.transform.scale(bird, (40, 40))
        screen.blit(bird, (player_pos.x - radius, player_pos.y - radius))

        # Draw blocks
        for block in blocks_woods:
            pygame.draw.rect(screen, "brown", block)
        for block in blocks_stones:
            pygame.draw.rect(screen, "gray", block)
        for block in blocks_ice:
            pygame.draw.rect(screen, "blue", block)

        if launch_ready:
            screen.blit(font_medium.render(f"Velocity: {int(velocity.length())}", True, "black"), (10, 10))

            player_rect = pygame.Rect(player_pos.x - radius, player_pos.y - radius, radius * 2, radius * 2)

            # --- Handle collision logic (same as yours, grouped for brevity) ---
            def handle_collisions(blocks, break_threshold, color):
                new_blocks = []
                for block in blocks:
                    if player_rect.colliderect(block):
                        if player_pos.x < block.left or player_pos.x > block.right:
                            velocity.x *= -bounce
                        if player_pos.y < block.top or player_pos.y > block.bottom:
                            velocity.y *= -bounce
                        if player_pos.x < block.left:
                            player_pos.x = block.left - radius
                        elif player_pos.x > block.right:
                            player_pos.x = block.right + radius
                        if player_pos.y < block.top:
                            player_pos.y = block.top - radius
                        elif player_pos.y > block.bottom:
                            player_pos.y = block.bottom + radius

                        if velocity.length() > break_threshold:
                            continue
                    new_blocks.append(block)
                return new_blocks

            blocks_woods = handle_collisions(blocks_woods, break_threshold_woods, "brown")
            blocks_stones = handle_collisions(blocks_stones, break_threshold_stones, "gray")
            blocks_ice = handle_collisions(blocks_ice, break_threshold_ice, "blue")

            # Apply physics
            velocity.y += gravity * dt
            player_pos += velocity * dt

            if player_pos.y > screen.get_height() - radius:
                velocity.x -= velocity.x * friction * dt
                player_pos.y = screen.get_height() - radius
                velocity.y *= -bounce
                if abs(velocity.y) < 10:
                    velocity.y = 0

            if player_pos.y < radius:
                player_pos.y = radius
                velocity.y *= -bounce
            if player_pos.x > screen.get_width() - radius:
                player_pos.x = screen.get_width() - radius
                velocity.x *= -bounce
            if player_pos.x < radius:
                player_pos.x = radius
                velocity.x *= -bounce

            if abs(velocity.y) < 10:
                velocity.y = 0
            if abs(velocity.x) < 20:
                velocity.x = 0

            # Reset Button
            reset_button = pygame.Rect(1200, 10, 60, 30)
            pygame.draw.rect(screen, "black", reset_button)
            screen.blit(font_small.render("Reset", True, "white"), (1210, 15))
            if reset_button.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
                player_pos = start_pos.copy()
                velocity = pygame.Vector2(0, 0)
                launch_ready = dragging = False
                mouse_start = pygame.Vector2()

            if velocity.x == 0 and velocity.y == 0:
                player_pos = start_pos.copy()
                velocity = pygame.Vector2(0, 0)
                launch_ready = dragging = False
                mouse_start = pygame.Vector2()

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()

# Run game

screen = pygame.display.set_mode((1280, 720))
game_loop(screen)
sys.exit()