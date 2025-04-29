import pygame
import sys
import main_menu
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from loop import game_loop
from teams import inputs, Team
import game_end

pygame.mixer.pre_init(frequency=44100, size=-16, channels=1, buffer=512)
pygame.init()
pygame.mixer.init()

# Music
pygame.mixer.music.load("assets/audio/angry_birds_theme.mp3")
pygame.mixer.music.set_volume(0.8)
pygame.mixer.music.play(-1)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Show splash screen and main menu
running = main_menu.splash_image(screen)
if running == False:
    pygame.quit()
    sys.exit()
running = main_menu.main_menu(screen)

while running:
    if main_menu.play_game:
        # Small delay to transition nicely
        background = pygame.image.load("assets/background-images/trial_background.jpg")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(background, (0, 0))
        pygame.display.flip()
        pygame.time.delay(250)

        # ask for level
        level = inputs.get_level(screen)

        if level == None:
            break
        # Player 1 setup
        name, selected_order = inputs.get_player_name_and_bird_order(screen, 1, False)
        team_1 = Team(name, selected_order)
        pygame.time.delay(1000)
        #team_1 = Team("pawan", ["Bomb", "Bomb",  "Bomb", "Bomb"])               ## for quick testing

        # Player 2 setup
        name_2, selected_order_2 = inputs.get_player_name_and_bird_order(screen, 2, False)
        while name_2 == name:
            name_2, selected_order_2 = inputs.get_player_name_and_bird_order(screen, 2, True)
        #team_2 = Team("pawan-2", ["Red", "Bomb", "Bomb", "Bomb"])          ## for quick testing
        pygame.time.delay(1000)
        team_2 = Team(name_2, selected_order_2)                                    
        # Start the game
        winner = game_loop(screen, team_1, team_2, level, main_menu.sound_on)
        #winner = "pawan"                                                            ## for quick testing
        if winner == False:
            break
        if winner == True:
            continue

        while winner:
            game_end.end_screen(screen, winner)

            if game_end.PLAY_AGAIN:
                game_end.PLAY_AGAIN = False
                winner = game_loop(screen, team_1, team_2, level)

            elif game_end.MAIN_MENU:
                game_end.MAIN_MENU = False
                main_menu.main_menu(screen)
                break  # Break inner loop and go back to main while loop to check play_game again
    else:
        main_menu.main_menu(screen)

pygame.quit()
sys.exit()