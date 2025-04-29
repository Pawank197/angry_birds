import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

PLAY_AGAIN_BOX_WIDTH = SCREEN_WIDTH * 0.1
PLAY_AGAIN_BOX_HEIGHT = SCREEN_WIDTH * 0.1
PLAY_AGAIN_BOX_Y_PCT = 0.5

MAIN_MENU_BOX_WIDTH = SCREEN_WIDTH * 0.1
MAIN_MENU_BOX_HEIGHT = SCREEN_WIDTH * 0.1
MAIN_MENU_BOX_Y_PCT = 0.5

BUTTONS_GAP = SCREEN_WIDTH * 0.15


def end_screen(screen, winner):
    global PLAY_AGAIN, MAIN_MENU
    PLAY_AGAIN = False
    MAIN_MENU = False
    # Load the end screen image
    end_screen_image = pygame.image.load("assets/background-images/end_screen_background.png")
    end_screen_image = pygame.transform.scale(end_screen_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    winner_text = "Winner: " + winner + "!"
    font = pygame.font.Font(None, 90)
    text = font.render(winner_text, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.3))

    play_again_button = pygame.image.load("assets/icons/play_again.png")
    play_again_button = pygame.transform.scale(play_again_button, (PLAY_AGAIN_BOX_WIDTH, PLAY_AGAIN_BOX_HEIGHT))
    main_menu_button = pygame.image.load("assets/icons/main_menu.png")
    main_menu_button = pygame.transform.scale(main_menu_button, (MAIN_MENU_BOX_WIDTH, MAIN_MENU_BOX_HEIGHT))

    play_again_rect = play_again_button.get_rect(topleft = ((SCREEN_WIDTH - BUTTONS_GAP)/2 - PLAY_AGAIN_BOX_WIDTH , SCREEN_HEIGHT * PLAY_AGAIN_BOX_Y_PCT))
    main_menu_rect = main_menu_button.get_rect(topleft = ((SCREEN_WIDTH + BUTTONS_GAP)/2, SCREEN_HEIGHT * MAIN_MENU_BOX_Y_PCT))


    while True:
        screen.blit(end_screen_image, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(play_again_button, play_again_rect)
        screen.blit(main_menu_button, main_menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if play_again_rect.collidepoint(pos):
                    PLAY_AGAIN = True
                    return
                elif main_menu_rect.collidepoint(pos):
                    MAIN_MENU = True
                    return 
        
        pygame.display.flip()   