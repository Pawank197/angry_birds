import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

### POSITIONING PARAMETERS ###
# PADDING_1
PADDING_1 = 0.02
PADDING_2 = 0.01

# PLAY BUTTON
PLAY_BTN_W_PCT = 0.2
PLAY_BTN_H_PCT = 0.2*(0.66)     # Keeping the aspect ratio of the image

# ICON BUTTONS
ICON_BTN_W_PCT = 0.075
ICON_BTN_H_PCT = 0.075

# TOGGLE BUTTONS
TOGGLE_BTN_W_PCT = 0.1
TOGGLE_BTN_H_PCT = 0.1

# INSTRUCTIONS
INSTR_W_PCT = 0.7
INSTR_H_PCT = 0.7

# INSTRUCTION IMAGE
INSTR_IMG_W_PCT = 0.5
INSTR_IMG_H_PCT = 0.5  # Keeping the aspect ratio of the image

# SETTINGS RECTANGLES
SETTINGS_W_PCT = 0.2
SETTINGS_H_PCT = 0.22

# FONT SIZE
FONT_PCT = 0.04


# Game sounds
pygame.init()
pygame.mixer.init()

click_sound = pygame.mixer.Sound("assets/audio/click_sound.wav")
click_sound.set_volume(0.5)

# Initial toggle states
music_on = True
sound_on = True
play_game = False
instructions_open = False

# Font initialization
font = pygame.font.Font(None, int(SCREEN_HEIGHT*FONT_PCT))

def splash_image(screen):
    splash_img = pygame.transform.scale(
        pygame.image.load("assets/background-images/Angry_birds_loading_background.jpg"),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    clock = pygame.time.Clock()
    while True:
        screen.blit(splash_img, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                pygame.time.delay(100)
                return True # Exit splash screen on click

        clock.tick(60)


def main_menu(screen):
    global music_on, sound_on, play_game

    pygame.display.set_caption("Main Menu")

    ### Load and scale images
    main_menu_image = pygame.transform.scale(
        pygame.image.load("assets/background-images/Angry_birds_main_menu_background.png"),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )

    ### Drawing the play button
    PLAY_WIDTH = int(SCREEN_WIDTH * PLAY_BTN_W_PCT)
    PLAY_HEIGHT = int(SCREEN_HEIGHT * PLAY_BTN_H_PCT)
    play_icon = pygame.image.load("assets/icons/image.png")
    play_icon = pygame.transform.scale(play_icon, (PLAY_WIDTH, PLAY_HEIGHT))
    play_button_rect = pygame.Rect((SCREEN_WIDTH - PLAY_WIDTH) / 2, (SCREEN_HEIGHT - PLAY_HEIGHT) / 2,
                                    PLAY_WIDTH, PLAY_HEIGHT)
    

    ### Drawing all the icons
    ICON_WIDTH = int(SCREEN_WIDTH * ICON_BTN_W_PCT)
    ICON_HEIGHT = int(SCREEN_WIDTH * ICON_BTN_H_PCT)

    # INSTRUCTION ICON
    instructions_icon = pygame.image.load("assets/icons/instruction_icon.png")
    instructions_icon = pygame.transform.scale(instructions_icon, (ICON_WIDTH, ICON_HEIGHT))
    instructions_button = instructions_icon.get_rect(bottomright=(SCREEN_WIDTH - SCREEN_WIDTH*PADDING_1, SCREEN_HEIGHT - SCREEN_HEIGHT*PADDING_1))
    

    # SETTINGS ICON
    settings_icon = pygame.image.load("assets/icons/settings_icon.png")
    settings_icon = pygame.transform.scale(settings_icon, (ICON_WIDTH, ICON_HEIGHT))
    settings_button = settings_icon.get_rect(bottomleft=(SCREEN_WIDTH*PADDING_1, SCREEN_HEIGHT - SCREEN_HEIGHT*PADDING_1))

    ### Toggle buttons
    TOGGLE_WIDTH = int(SCREEN_WIDTH * TOGGLE_BTN_W_PCT)
    TOGGLE_HEIGHT = int(SCREEN_WIDTH * TOGGLE_BTN_H_PCT)

    # TOGGLE MUSIC BUTTON
    toggle_on_music_img = pygame.image.load("assets/icons/music_on.png")
    toggle_off_music_img = pygame.image.load("assets/icons/music_off.png")
    toggle_on_music_img = pygame.transform.scale(toggle_on_music_img, (TOGGLE_WIDTH, TOGGLE_HEIGHT))
    toggle_off_music_img = pygame.transform.scale(toggle_off_music_img, (TOGGLE_WIDTH, TOGGLE_HEIGHT))

    # TOGGLE SOUND BUTTON
    toggle_sound_on_img = pygame.image.load("assets/icons/sound_on.png")
    toggle_sound_off_img = pygame.image.load("assets/icons/sound_off.png")
    toggle_sound_on_img = pygame.transform.scale(toggle_sound_on_img, (TOGGLE_WIDTH, TOGGLE_HEIGHT))
    toggle_sound_off_img = pygame.transform.scale(toggle_sound_off_img, (TOGGLE_WIDTH, TOGGLE_HEIGHT))

    ### Loading instruction images
    IMG_WIDTH = int(SCREEN_WIDTH * INSTR_W_PCT * INSTR_IMG_W_PCT)
    IMG_HEIGHT = int(SCREEN_HEIGHT * INSTR_H_PCT * INSTR_IMG_H_PCT)
    imgs = [
            pygame.transform.scale(pygame.image.load(f"assets/instruction-images/image0.png"), (IMG_WIDTH, IMG_HEIGHT)),
            pygame.transform.scale(pygame.image.load(f"assets/instruction-images/image1.png"), (IMG_WIDTH, IMG_HEIGHT)),
            pygame.transform.scale(pygame.image.load(f"assets/instruction-images/image2.png"), (IMG_WIDTH, IMG_HEIGHT))
        ]

    # Instruction rectangle
    instr_rect = pygame.Rect(
        (SCREEN_WIDTH - SCREEN_WIDTH*INSTR_W_PCT) // 2,
        (SCREEN_HEIGHT - SCREEN_HEIGHT*INSTR_H_PCT) // 2,
        int(SCREEN_WIDTH*INSTR_W_PCT), int(SCREEN_HEIGHT*INSTR_H_PCT)
    )
    # Instruction content
    content = [
            {"type": "text",  "data": "> Hit play to start the game."},
            {"type": "text",  "data": "> Select your level."},
            {"type": "image", "data": imgs[0]},
            {"type": "text",  "data": "> Enter your player name and bird order, then press Enter."},
            {"type": "image", "data": imgs[1]},
            {"type": "text",  "data": "> Drag the slingshot to aim and release to shoot."},
            {"type": "image", "data": imgs[2]},
            {"type": "text",  "data": "> There are 4 bird types and three types of blocks."},
            {"type": "text",  "data": "> Destroy the blocks to win the game."},
            {"type": "text",  "data": "> You can use the settings button to toggle music and sound."},
            {"type": "text",  "data": "> You can use the restart button to restart and change the level if you want"},
        ]
    
    # Calculate height of the text
    def calc_height():
        h = 20
        for item in content:
            if item["type"] == "text":
                h += font.get_linesize() + 10
            else:
                h += item["data"].get_height() + 20
        return h

    total_h = calc_height()

    # view only
    view_rect = pygame.Rect(
        instr_rect.left + int(SCREEN_WIDTH*PADDING_2),
        instr_rect.top + int(SCREEN_HEIGHT*PADDING_1*3),
        instr_rect.width - int(SCREEN_WIDTH*PADDING_2*2),
        instr_rect.height - int(SCREEN_HEIGHT*PADDING_1*4)
    )
    

    clock = pygame.time.Clock()
    settings_open = False
    instructions_open = False
    scroll_y = 0
    SCROLL_SPEED = 20

    while True:
        # Background
        screen.blit(main_menu_image, (0, 0))

        # Play button 
        screen.blit(play_icon, play_button_rect)

        # Drawing the instructions and settings icons
        screen.blit(instructions_icon, instructions_button)
        screen.blit(settings_icon, settings_button)

        if settings_open:
            ### SETTINGS PANEL ###
            settings_width, settings_height = int(SCREEN_WIDTH * SETTINGS_W_PCT), int(SCREEN_HEIGHT * SETTINGS_H_PCT)
            settings_rect = pygame.Rect(
                (SCREEN_WIDTH - settings_width) / 2,
                (SCREEN_HEIGHT - settings_height) / 2,
                settings_width, settings_height
            )

            pygame.draw.rect(screen, (255, 255, 255), settings_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 0, 0), settings_rect, 2, border_radius=15)


            ### MUSIC AND SOUND TOGGLES ###
            toggle_music_rect = pygame.Rect(
                settings_rect.left,
                settings_rect.top,
                TOGGLE_WIDTH, TOGGLE_HEIGHT
            )
            toggle_music_img = toggle_on_music_img if music_on else toggle_off_music_img
            screen.blit(toggle_music_img, toggle_music_rect.topleft)

            music_text = font.render("Music", True, (0, 0, 0))
            music_text_rect = music_text.get_rect(center=(toggle_music_rect.centerx, toggle_music_rect.bottom + int(SCREEN_WIDTH*PADDING_2)))
            screen.blit(music_text, music_text_rect)

            toggle_sound_rect = pygame.Rect(
                settings_rect.right - TOGGLE_WIDTH,
                settings_rect.top,
                TOGGLE_WIDTH, TOGGLE_HEIGHT
            )
            toggle_sound_img = toggle_sound_on_img if sound_on else toggle_sound_off_img
            screen.blit(toggle_sound_img, toggle_sound_rect.topleft)

            sound_text = font.render("Sound", True, (0, 0, 0))
            sound_text_rect = sound_text.get_rect(center=(toggle_sound_rect.centerx, toggle_sound_rect.bottom + int(SCREEN_WIDTH*PADDING_2)))
            screen.blit(sound_text, sound_text_rect)
        
        if instructions_open:
            # 1) load the instruction rectangle
            pygame.draw.rect(screen, (255, 255, 255), instr_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 0, 0), instr_rect, 2, border_radius=15)

            # 2) Write header
            header_txt = font.render("INSTRUCTIONS", True, (0, 0, 0))
            header_rect = header_txt.get_rect(center=(instr_rect.centerx, instr_rect.top + int(SCREEN_WIDTH*PADDING_1)))
            screen.blit(header_txt, header_rect)

            # 3) clear the view_rect area
            vp = screen.subsurface(view_rect)
            vp.fill((255, 255, 255))

            # 4) render content at scroll_y
            y_offset = -scroll_y + 10
            for item in content:
                if item["type"] == "text":
                    txt_surf = font.render(item["data"], True, (0, 0, 0))
                    vp.blit(txt_surf, (int(SCREEN_WIDTH*INSTR_W_PCT*PADDING_1), y_offset))
                    y_offset += font.get_linesize() + 10
                else:
                    img = item["data"]
                    vp.blit(img, (int((view_rect.width - img.get_width())/2), y_offset))
                    y_offset += img.get_height() + 20

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click_sound.play()
                pos = event.pos

                if settings_button.collidepoint(pos):
                    if instructions_open:
                        instructions_open = False
                    settings_open = not settings_open

                elif settings_open and toggle_music_rect.collidepoint(pos):
                    music_on = not music_on
                    pygame.mixer.music.set_volume(0.5 if music_on else 0)

                elif settings_open and toggle_sound_rect.collidepoint(pos):
                    sound_on = not sound_on
                    click_sound.set_volume(0.5 if sound_on else 0)

                elif play_button_rect.collidepoint(pos) and not instructions_open and not settings_open:
                    play_game = True
                    return True

                elif instructions_button.collidepoint(pos):
                     if settings_open:
                        settings_open = False
                     instructions_open = not instructions_open

            elif event.type == pygame.MOUSEWHEEL and instructions_open:
                scroll_y -= event.y * SCROLL_SPEED
                # clamp
                max_scroll = max(0, total_h - view_rect.height)
                scroll_y = max(0, min(scroll_y, max_scroll))
        
        pygame.display.flip()
        clock.tick(60)

