import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

### POSITITONAL PARAMETERS ###
# PADDING
PADDING = 0.01

## LEVEL RECTANGLE
# dimensions
LEVEL_RECT_WIDTH = SCREEN_WIDTH/3
LEVEL_RECT_HEIGHT = SCREEN_HEIGHT/2

LEVEL_EASY_WIDTH = SCREEN_WIDTH/10
LEVEL_EASY_HEIGHT = SCREEN_HEIGHT/15

LEVEL_MEDIUM_WIDTH = SCREEN_WIDTH/10
LEVEL_MEDIUM_HEIGHT = SCREEN_HEIGHT/15

LEVEL_HARD_WIDTH = SCREEN_WIDTH/10
LEVEL_HARD_HEIGHT = SCREEN_HEIGHT/15

LEVEL_GAP = SCREEN_HEIGHT/20



## BOX
# dimensions
INPUT_BOX_WIDTH = 9*SCREEN_WIDTH/16
INPUT_BOX_HEIGHT = 7*SCREEN_HEIGHT/9
# position
INPUT_BOX_X = (SCREEN_WIDTH - INPUT_BOX_WIDTH)/2
INPUT_BOX_Y = (SCREEN_HEIGHT - INPUT_BOX_HEIGHT)/2


## NAME BOX
# dimensions
NAME_BOX_WIDTH = 5*SCREEN_WIDTH/16
NAME_BOX_HEIGHT = SCREEN_HEIGHT/18

## BIRD OPTIONS AND BOXES
# boxes dimensions
BIRD_BOX_WIDTH = SCREEN_WIDTH/16
BIRD_BOX_HEIGHT = SCREEN_WIDTH/16
# birds dimensions
BIRD_WIDTH = BIRD_BOX_WIDTH*0.6
BIRD_HEIGHT = BIRD_BOX_HEIGHT*0.6
# boxes position. 5x + 4x = INPUT_BOX_WIDTH
BIRD_BOX_X = INPUT_BOX_X + SCREEN_WIDTH/16
BIRD_BOX_GAP = SCREEN_WIDTH/16


## SELECTED BIRDS BOXES
# boxes dimensions
SELECTED_BIRD_BOX_WIDTH = BIRD_BOX_WIDTH*0.6
SELECTED_BIRD_BOX_HEIGHT = BIRD_BOX_HEIGHT*0.6
# boxes position
SELECTED_BIRD_BOX_X = INPUT_BOX_X + (INPUT_BOX_WIDTH - 7*SELECTED_BIRD_BOX_WIDTH)/2
SELECTED_BIRD_BOX_GAP = SELECTED_BIRD_BOX_WIDTH

# RESET ORDER BUTTON
RESET_ORDER_BUTTON_WIDTH = INPUT_BOX_WIDTH/7
RESET_ORDER_BUTTON_HEIGHT = INPUT_BOX_HEIGHT/14



class inputs:
    def get_level(screen):
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, int(SCREEN_WIDTH*0.030))
        level_input_rect = pygame.Rect(
            (SCREEN_WIDTH - LEVEL_RECT_WIDTH)/2,
            (SCREEN_HEIGHT - LEVEL_RECT_HEIGHT)/2,
            LEVEL_RECT_WIDTH,
            LEVEL_RECT_HEIGHT
        )

        level_text = font.render("Select Level", True, "black")
        level_text_rect = level_text.get_rect(center=(SCREEN_WIDTH/2, level_input_rect.top + LEVEL_RECT_HEIGHT/6))

        # LEVEL_BOX position
        LEVEL_BOX_X = (SCREEN_WIDTH - LEVEL_EASY_WIDTH)/2
        LEVEL_BOX_Y_HARD = level_input_rect.bottom - LEVEL_RECT_HEIGHT/10 - LEVEL_HARD_HEIGHT
        LEVEL_BOX_Y_MEDIUM = LEVEL_BOX_Y_HARD - LEVEL_GAP - LEVEL_MEDIUM_HEIGHT
        LEVEL_BOX_Y_EASY = LEVEL_BOX_Y_MEDIUM - LEVEL_GAP - LEVEL_EASY_HEIGHT


        level_easy_rect = pygame.Rect(
            LEVEL_BOX_X,
            LEVEL_BOX_Y_EASY,
            LEVEL_EASY_WIDTH,
            LEVEL_EASY_HEIGHT
        )

        level_medium_rect = pygame.Rect(
            LEVEL_BOX_X,
            LEVEL_BOX_Y_MEDIUM,
            LEVEL_MEDIUM_WIDTH,
            LEVEL_MEDIUM_HEIGHT
        )

        level_hard_rect = pygame.Rect(
            LEVEL_BOX_X,
            LEVEL_BOX_Y_HARD,
            LEVEL_HARD_WIDTH,
            LEVEL_HARD_HEIGHT
        )
        level_easy_text = font.render("Easy", True, "white")
        level_easy_text_rect = level_easy_text.get_rect(center=(level_easy_rect.center))

        level_medium_text = font.render("MEDIUM", True, "white")
        level_medium_text_rect = level_medium_text.get_rect(center=(level_medium_rect.center))

        level_hard_text = font.render("HARD", True, "white")
        level_hard_text_rect = level_hard_text.get_rect(center=(level_hard_rect.center))

        while True:
            pygame.draw.rect(screen, "skyblue", level_input_rect, border_radius=30)
            pygame.draw.rect(screen, "yellow", level_easy_rect, border_radius=20)
            pygame.draw.rect(screen, "yellow", level_medium_rect, border_radius=20)
            pygame.draw.rect(screen, "yellow", level_hard_rect, border_radius=20)
            screen.blit(level_text, level_text_rect)
            screen.blit(level_easy_text, level_easy_text_rect)
            screen.blit(level_medium_text, level_medium_text_rect)
            screen.blit(level_hard_text, level_hard_text_rect)
            pygame.draw.rect(screen, "black", level_input_rect, 2, border_radius=30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if level_easy_rect.collidepoint(event.pos):
                        return "easy"
                    elif level_medium_rect.collidepoint(event.pos):
                        return "medium"
                    elif level_hard_rect.collidepoint(event.pos):
                        return "hard"
            pygame.display.flip()

    def get_player_name_and_bird_order(screen, team_number, repeating):
        input_box = pygame.Rect(INPUT_BOX_X, INPUT_BOX_Y, INPUT_BOX_WIDTH, INPUT_BOX_HEIGHT)
        font = pygame.font.Font(None, int(SCREEN_WIDTH*0.03))
        font_2 = pygame.font.Font(None, int(SCREEN_WIDTH*0.015))
        clock = pygame.time.Clock()

        name_rect = pygame.Rect((SCREEN_WIDTH - NAME_BOX_WIDTH)/2, input_box.top + SCREEN_HEIGHT/8, NAME_BOX_WIDTH, NAME_BOX_HEIGHT)
        text = ""

        # Load bird images
        Red = pygame.transform.scale(pygame.image.load("assets/Birds/Red.png"), (BIRD_WIDTH, BIRD_HEIGHT))
        Chuck = pygame.transform.scale(pygame.image.load("assets/Birds/Chuck.png"), (BIRD_WIDTH, BIRD_HEIGHT))
        Blues = pygame.transform.scale(pygame.image.load("assets/Birds/Blues.png"), (BIRD_WIDTH, BIRD_HEIGHT))
        Bomb = pygame.transform.scale(pygame.image.load("assets/Birds/Bomb.png"), (BIRD_WIDTH, BIRD_HEIGHT))

        Birds = [
            {"name": "Red", "image": Red, "rect": pygame.Rect(BIRD_BOX_X, name_rect.bottom + SCREEN_HEIGHT/6, BIRD_BOX_WIDTH, BIRD_BOX_HEIGHT)},
            {"name": "Chuck", "image": Chuck, "rect": pygame.Rect(BIRD_BOX_X + 2*BIRD_BOX_GAP, name_rect.bottom + SCREEN_HEIGHT/6, BIRD_BOX_WIDTH, BIRD_BOX_HEIGHT)},
            {"name": "Blues", "image": Blues, "rect": pygame.Rect(BIRD_BOX_X + 4*BIRD_BOX_GAP, name_rect.bottom + SCREEN_HEIGHT/6, BIRD_BOX_WIDTH, BIRD_BOX_HEIGHT)},
            {"name": "Bomb", "image": Bomb, "rect": pygame.Rect(BIRD_BOX_X + 6*BIRD_BOX_GAP, name_rect.bottom + SCREEN_HEIGHT/6, BIRD_BOX_WIDTH, BIRD_BOX_HEIGHT)}
        ]

        bird_images = {bird["name"]: bird["image"] for bird in Birds}

        selected_birds_rect = [
            pygame.Rect(SELECTED_BIRD_BOX_X, name_rect.bottom + SCREEN_HEIGHT/3.1, SELECTED_BIRD_BOX_WIDTH, SELECTED_BIRD_BOX_HEIGHT),
            pygame.Rect(SELECTED_BIRD_BOX_X + 2*SELECTED_BIRD_BOX_GAP, name_rect.bottom + SCREEN_HEIGHT/3.1, SELECTED_BIRD_BOX_WIDTH, SELECTED_BIRD_BOX_HEIGHT),
            pygame.Rect(SELECTED_BIRD_BOX_X + 4*SELECTED_BIRD_BOX_GAP, name_rect.bottom + SCREEN_HEIGHT/3.1, SELECTED_BIRD_BOX_WIDTH, SELECTED_BIRD_BOX_HEIGHT),
            pygame.Rect(SELECTED_BIRD_BOX_X + 6*SELECTED_BIRD_BOX_GAP, name_rect.bottom + SCREEN_HEIGHT/3.1, SELECTED_BIRD_BOX_WIDTH, SELECTED_BIRD_BOX_HEIGHT)
        ]

        reset_order_rect = pygame.Rect((SCREEN_WIDTH - RESET_ORDER_BUTTON_WIDTH)/2, input_box.bottom - SCREEN_HEIGHT/6, RESET_ORDER_BUTTON_WIDTH, RESET_ORDER_BUTTON_HEIGHT)

        selected_order = []

        done = False
        name_active = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if name_rect.collidepoint(event.pos):
                        name_active = True
                    else:
                        name_active = False

                    for bird in Birds:
                        if bird["rect"].collidepoint(event.pos) and bird["name"] not in selected_order:
                            if len(selected_order) < 4:
                                selected_order.append(bird["name"])
                    if reset_order_rect.collidepoint(event.pos):
                        selected_order = []

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(text) > 0 and len(selected_order) == 4:
                        done = True
                    elif name_active:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif len(text) < 15:
                            text += event.unicode
                

            # Draw screen
            pygame.draw.rect(screen, "skyblue", input_box, border_radius=20)
            team_number_text = font.render(f"TEAM - {team_number}", True, "black")
            team_number_rect = team_number_text.get_rect(center=(SCREEN_WIDTH / 2, input_box.top + INPUT_BOX_HEIGHT/15))
            screen.blit(team_number_text, team_number_rect)

            # Draw name input
            pygame.draw.rect(screen, "white", name_rect)
            if name_active:
                txt_surface = font.render(text or "", True, "black")
            else:
                txt_surface = font.render(text or "Enter name...", True, "black")
            screen.blit(txt_surface, (name_rect.left + PADDING*SCREEN_WIDTH/2, name_rect.top + PADDING*SCREEN_HEIGHT))
            pygame.draw.rect(screen, "black", name_rect, 2)

            prompt = font_2.render("Enter your name", True, "red")
            screen.blit(prompt, (name_rect.left + PADDING*SCREEN_WIDTH, name_rect.bottom + PADDING*SCREEN_HEIGHT))

            # Draw birds
            select_text = font.render("Click to select bird order", True, "black")
            select_text_rect = select_text.get_rect(center=(SCREEN_WIDTH/2, name_rect.bottom + SCREEN_HEIGHT/10))
            screen.blit(select_text, select_text_rect)

            # Draw reset buttons
            pygame.draw.rect(screen, "black", reset_order_rect)
            reset_text = font_2.render("Reset Order", True, "white")
            reset_text_rect = reset_text.get_rect(center=reset_order_rect.center)
            screen.blit(reset_text, reset_text_rect)

            for bird in Birds:
                pygame.draw.rect(screen, "white", bird["rect"], border_radius=20)
                image = bird["image"]
                image_rect = image.get_rect(center=bird["rect"].center)
                screen.blit(image, image_rect)

            for idx, bird_name in enumerate(selected_order):
                rect = selected_birds_rect[idx]
                pygame.draw.rect(screen, "white", rect, border_radius=10)
                image = bird_images[bird_name]
                image_rect = image.get_rect(center=rect.center)
                screen.blit(image, image_rect)

            # Prompt if not ready
            if len(text) == 0 or len(selected_order) < 4:
                Prompt = font_2.render("Please enter name and select 4 birds. Same name is not allowed!", True, "red")
                if repeating:
                        warning = font_2.render("Same name is not allowed!", True, "red")
                        warning_rect = warning.get_rect(center=(SCREEN_WIDTH // 2, team_number_rect.bottom + (SCREEN_HEIGHT / 25)))
                        screen.blit(warning, warning_rect)
                Prompt_rect = Prompt.get_rect(center=(SCREEN_WIDTH/2, reset_order_rect.bottom + SCREEN_HEIGHT/35))
                screen.blit(Prompt, Prompt_rect)

            pygame.display.flip()
            clock.tick(60)

        return text, selected_order

class Team:
    def __init__(self, name, selected_order):
        self.name = name
        self.selected_order = selected_order
