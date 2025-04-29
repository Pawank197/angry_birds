import pygame
import math
import sys
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

##### GROUND IS AT 87% OF THE SCREEN HEIGHT, WHICH WE GOT FROM THE BACKGROUND #####

winner = ""

### POSITIONING ###
## SLING ##
# dimensions
SLING_WIDTH = SCREEN_WIDTH / 35
SLING_HEIGHT = SLING_WIDTH * 180 / 71
# band offset
BAND_OFFSET_X = SLING_WIDTH * 0.2
BAND_OFFSET_Y = SLING_HEIGHT * 0.15
# position
SLING_X_PCT = 0.17
SLING_Y_PCT = 0.87 - SLING_HEIGHT / SCREEN_HEIGHT                                       # 87% to make it look like the slingshot is on the ground

## BIRDS ##
# dimensions of all birds
BIRD_WIDTH = SCREEN_WIDTH/50
BIRD_HEIGHT = SCREEN_WIDTH/50
# slingshot bird position
SLINGSHOT_BIRD_X_PCT = 0.17
SLINGSHOT_BIRD_Y_PCT = (SCREEN_HEIGHT*(SLING_Y_PCT+0.03))/SCREEN_HEIGHT                 # 3% to make it look like the bird is in the slingshot
# how far (at most) you can pull the bird from its rest
MAX_PULL = SCREEN_WIDTH * 0.05
# position of the not-selected birds            screen.blit(level_text, level_text_rect)
NOT_SELECTED_BIRD_X_PCT = 0.10
NOT_SELECTED_BIRD_Y_PCT = 0.90
NOT_SELECTED_BIRD_GAP = 5*BIRD_WIDTH/4

## WIND ##
LINE_COUNT    = 3
LINE_COLOR    = (255, 255, 255)   # light bluish with some alpha
LINE_LENGTH   = SCREEN_WIDTH * 0.2
LINE_SPEED    = SCREEN_WIDTH/8              # pixels/sec

## Restart button ##
RESTART_BUTTON_WIDTH = SCREEN_WIDTH * 0.075
RESTART_BUTTON_HEIGHT = SCREEN_HEIGHT * 0.05
RESTART_BUTTON_X_PCT = 0.91
RESTART_BUTTON_Y_PCT = 0.02

## SCORE ## 256/57
SCORE_WIDTH = SCREEN_WIDTH/3
SCORE_HEIGHT = SCORE_WIDTH*57/256
SCORE_RECT_Y_PCT = 0.05

## BLOCKS ##
# dimensions
BLOCK_WIDTH = SCREEN_WIDTH/30
BLOCK_HEIGHT = SCREEN_WIDTH/30
# position
BLOCK_X_PCT_1 = 0.04
BLOCK_X_PCT_2 = (SCREEN_WIDTH*BLOCK_X_PCT_1 + 21*BLOCK_WIDTH/20)/SCREEN_WIDTH
BLOCK_X_PCT_3 = (SCREEN_WIDTH*BLOCK_X_PCT_2 + 21*BLOCK_WIDTH/20)/SCREEN_WIDTH
BLOCK_Y_PCT_1 = (0.87-BLOCK_HEIGHT/SCREEN_HEIGHT)                                       # 87% to make it look like the blocks are on the ground
BLOCK_Y_PCT_2 = (SCREEN_HEIGHT*BLOCK_Y_PCT_1 - 21*BLOCK_HEIGHT/20)/SCREEN_HEIGHT
BLOCK_Y_PCT_3 = (SCREEN_HEIGHT*BLOCK_Y_PCT_2 - 21*BLOCK_HEIGHT/20)/SCREEN_HEIGHT
BLOCK_Y_PCT_4 = (SCREEN_HEIGHT*BLOCK_Y_PCT_3 - 21*BLOCK_HEIGHT/20)/SCREEN_HEIGHT
BLOCK_Y_PCT_5 = (SCREEN_HEIGHT*BLOCK_Y_PCT_4 - 21*BLOCK_HEIGHT/20)/SCREEN_HEIGHT

EXPLOSION_RADIUS = BLOCK_WIDTH*1.5

### BLOCK POSITIONS ###
block_positions = [
    pygame.Rect(BLOCK_X_PCT_1*SCREEN_WIDTH, BLOCK_Y_PCT_1*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_2*SCREEN_WIDTH, BLOCK_Y_PCT_1*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_3*SCREEN_WIDTH, BLOCK_Y_PCT_1*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_1*SCREEN_WIDTH, BLOCK_Y_PCT_2*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_2*SCREEN_WIDTH, BLOCK_Y_PCT_2*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_3*SCREEN_WIDTH, BLOCK_Y_PCT_2*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_1*SCREEN_WIDTH, BLOCK_Y_PCT_3*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_2*SCREEN_WIDTH, BLOCK_Y_PCT_3*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_3*SCREEN_WIDTH, BLOCK_Y_PCT_3*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_1*SCREEN_WIDTH, BLOCK_Y_PCT_4*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_2*SCREEN_WIDTH, BLOCK_Y_PCT_4*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_3*SCREEN_WIDTH, BLOCK_Y_PCT_4*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_1*SCREEN_WIDTH, BLOCK_Y_PCT_5*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_2*SCREEN_WIDTH, BLOCK_Y_PCT_5*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
    pygame.Rect(BLOCK_X_PCT_3*SCREEN_WIDTH, BLOCK_Y_PCT_5*SCREEN_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT),
]


def generate_random_postions(positions):

    random.shuffle(positions)

    return {
        "wood":  [{"rect": pos, "hp": 1500, "max_hp": 1500, "hp_bar_timer": 90, "hit_status": False, "type": "wood"} for pos in positions[0:5]],
        "stone": [{"rect": pos, "hp": 2500, "max_hp": 2500, "hp_bar_timer": 90, "hit_status": False, "type": "stone"} for pos in positions[5:10]],
        "ice":   [{"rect": pos, "hp": 2000, "max_hp": 2000, "hp_bar_timer": 90, "hit_status": False, "type": "ice"} for pos in positions[10:15]],
    }

player_1_blocks_positions = generate_random_postions(block_positions)

player_2_blocks_positions = {"wood": [], "stone": [], "ice": []}

for type, blocks in player_1_blocks_positions.items():
    for block in blocks:
        new_rect = block["rect"].copy()
        new_rect.x = SCREEN_WIDTH - new_rect.x - BLOCK_WIDTH
        player_2_blocks_positions[type].append({
            "rect": new_rect,
            "hp":   block["hp"],
            "max_hp":  block["max_hp"],
            "hp_bar_timer": block["hp_bar_timer"],
            "hit_status": block["hit_status"],
            "type": block["type"],
        })



def load_assets(team_1, team_2):
    """
    Load and cache all game assets before entering the main loop.
    Returns a dict of preloaded images.
    """ 
    assets = {}
    # Background
    bg = pygame.image.load("assets/background-images/trial_background.jpg").convert()
    assets['background'] = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Slingshot images
    sling_raw = pygame.image.load("assets/objects/sling.png").convert_alpha()
    sling_scaled = pygame.transform.scale(sling_raw, (int(SLING_WIDTH), int(SLING_HEIGHT)))
    assets['sling'] = sling_scaled
    assets['sling_flipped'] = pygame.transform.flip(sling_scaled, True, False)

    # Block textures
    assets['wood'] = pygame.transform.scale(
        pygame.image.load("assets/objects/wood.png").convert_alpha(), (BLOCK_WIDTH, BLOCK_HEIGHT)
    )
    assets['stone'] = pygame.transform.scale(
        pygame.image.load("assets/objects/stones.png").convert_alpha(), (BLOCK_WIDTH, BLOCK_HEIGHT)
    )
    assets['ice'] = pygame.transform.scale(
        pygame.image.load("assets/objects/ice.png").convert_alpha(), (BLOCK_WIDTH, BLOCK_HEIGHT)
    )

    # hit sounds
    # Load the converted WAV files
    assets['wood-hit'] = pygame.mixer.Sound("assets/audio/wood_hit.mp3")
    assets['stone-hit'] = pygame.mixer.Sound("assets/audio/stone_hit.mp3")
    assets['ice-hit'] = pygame.mixer.Sound("assets/audio/ice_hit.wav")

    # Bounce sound
    assets['bounce'] = pygame.mixer.Sound("assets/audio/ball_bounce.wav")

    # Releasing the bird sound
    assets['release'] = pygame.mixer.Sound("assets/audio/releasing_sling.wav")

    # Bird sprites (load unique keys for both teams)
    assets['birds'] = {}
    keys = set(team_1.selected_order + team_2.selected_order)
    for key in keys:
        img = pygame.image.load(f"assets/Birds/{key}.png").convert_alpha()
        assets['birds'][key] = img

    # Load the animation frames for the explosion
    assets['explosion_frames'] = []
    for i in range(1, 8):
        frame = pygame.image.load(f"assets/animation-explosion/{i}.png").convert_alpha()
        assets['explosion_frames'].append(pygame.transform.scale(frame, (BLOCK_WIDTH*3, BLOCK_HEIGHT*3)))

    assets['score'] = pygame.transform.scale(pygame.image.load("assets/icons/score.png"), (SCORE_WIDTH, SCORE_HEIGHT))
    return assets


def game_loop(screen, team_1, team_2, level, sound_on):
    clock = pygame.time.Clock()
    dt = 0

    # Initializing two types of font
    font_small = pygame.font.Font(None, 30)
    font = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 60)

    # Load assets
    assets = load_assets(team_1, team_2)

    # We got two players, so we create two dictionaries for each of them
    players = [
        {"name": team_1.name,
         "selected_order": team_1.selected_order,
         "start_pos": pygame.Vector2((SLINGSHOT_BIRD_X_PCT + 0.02)*SCREEN_WIDTH, SLINGSHOT_BIRD_Y_PCT*SCREEN_HEIGHT),
         "player_pos": pygame.Vector2((SLINGSHOT_BIRD_X_PCT + 0.02)*SCREEN_WIDTH, SLINGSHOT_BIRD_Y_PCT*SCREEN_HEIGHT),
         "velocity": pygame.Vector2(0, 0),
         "blocks": player_1_blocks_positions,
         "sling": pygame.Rect(SCREEN_WIDTH*SLING_X_PCT, SCREEN_HEIGHT*SLING_Y_PCT, SLING_WIDTH, SLING_HEIGHT),
         "not_selected_birds":[
             pygame.Rect(SCREEN_WIDTH*NOT_SELECTED_BIRD_X_PCT + 2*NOT_SELECTED_BIRD_GAP, SCREEN_HEIGHT*NOT_SELECTED_BIRD_Y_PCT, BIRD_WIDTH, BIRD_HEIGHT),
             pygame.Rect(SCREEN_WIDTH*NOT_SELECTED_BIRD_X_PCT + NOT_SELECTED_BIRD_GAP, SCREEN_HEIGHT*NOT_SELECTED_BIRD_Y_PCT, BIRD_WIDTH, BIRD_HEIGHT),
             pygame.Rect(SCREEN_WIDTH*NOT_SELECTED_BIRD_X_PCT, SCREEN_HEIGHT*NOT_SELECTED_BIRD_Y_PCT, BIRD_WIDTH, BIRD_HEIGHT),
         ],
         "blocks_remaining": 15,
         "explosion_damage_on": True,
         "explosion_damage": 0,
         "explosion_centre": pygame.Vector2(0, 0),
         "blast_done": False,
         "bomb_disappear": False,
         "animation_explosion_on": False,
         "animation_frame_no": 0,
         "animation_frame_timer": 10
         },
        {"name": team_2.name, 
         "selected_order": team_2.selected_order,
         "start_pos": pygame.Vector2(SCREEN_WIDTH - SLINGSHOT_BIRD_X_PCT*SCREEN_WIDTH - BIRD_WIDTH, SLINGSHOT_BIRD_Y_PCT*SCREEN_HEIGHT),
         "player_pos": pygame.Vector2(SCREEN_WIDTH - SLINGSHOT_BIRD_X_PCT*SCREEN_WIDTH - BIRD_WIDTH, SLINGSHOT_BIRD_Y_PCT*SCREEN_HEIGHT),
         "velocity": pygame.Vector2(0, 0),
         "blocks": player_2_blocks_positions,
         "sling": pygame.Rect(SCREEN_WIDTH*(1-SLING_X_PCT) - SLING_WIDTH, SCREEN_HEIGHT*SLING_Y_PCT, SLING_WIDTH, SCREEN_HEIGHT),
         "not_selected_birds":[
             pygame.Rect(SCREEN_WIDTH*(1-NOT_SELECTED_BIRD_X_PCT) - 2*NOT_SELECTED_BIRD_GAP - BIRD_WIDTH, SCREEN_HEIGHT*NOT_SELECTED_BIRD_Y_PCT, BIRD_WIDTH, BIRD_HEIGHT),
             pygame.Rect(SCREEN_WIDTH*(1-NOT_SELECTED_BIRD_X_PCT) - NOT_SELECTED_BIRD_GAP - BIRD_WIDTH, SCREEN_HEIGHT*NOT_SELECTED_BIRD_Y_PCT, BIRD_WIDTH, BIRD_HEIGHT),
             pygame.Rect(SCREEN_WIDTH*(1-NOT_SELECTED_BIRD_X_PCT) - BIRD_WIDTH, SCREEN_HEIGHT*NOT_SELECTED_BIRD_Y_PCT, BIRD_WIDTH, BIRD_HEIGHT),
         ],
         "blocks_remaining": 15,
         "explosion_damage_on": True,
         "explosion_damage": 0,
         "explosion_centre": pygame.Vector2(0, 0),
         "blast_done": False,
         "bomb_disappear": False,
         "animation_explosion_on": False,
         "animation_frame_no": 0,
         "animation_frame_timer": 10
         }
    ]

    # Set the initial player
    current_player = 0
    Birds_damage_multiplier = {
        "Red" : {
            "wood": 1,
            "stone": 1,
            "ice": 1
        },
        "Chuck" : {
            "wood": 1.25,
            "stone": 0.75,
            "ice": 0.75
        },
        "Blues" : {
            "wood": 0.75,
            "stone": 0.75,
            "ice": 1.25
        },
        "Bomb" : {
            "wood": 0.75,
            "stone": 1.25,
            "ice": 0.75,
        }
    }

    # Anchors
    for i in (0,1):
        sling = players[i]["sling"]
        players[i]["band_anchors"] = (
            pygame.Vector2(sling.left + BAND_OFFSET_X, sling.top + BAND_OFFSET_Y),
            pygame.Vector2(sling.right - BAND_OFFSET_X, sling.top + BAND_OFFSET_Y)
        )

    # Wind lines
    wind_lines = []
    for i in range(LINE_COUNT):
        y = SCREEN_HEIGHT * (0.2 + 0.6 * i / (LINE_COUNT-1))
        x = random.uniform(-LINE_LENGTH, SCREEN_WIDTH)
        wind_lines.append(pygame.Vector2(x, y))

    # Universal variables
    gravity = 980
    friction = 0.4
    bounce = 0.7
    ground_y = 0.87*SCREEN_HEIGHT - BIRD_HEIGHT/2
    friction_on = False                             ## friction if off at the beginning and gets activated when the bird hits the ground for the first time 
    wind = 0.7
    
    TOTAL_FRAMES = len(assets["explosion_frames"])


    # slingshot variables
    dragging = False
    launch_ready = False
    mouse_start = pygame.Vector2()
    scale_power = 20

    # Projected trajectory
    def show_projectile(velocity, start_pos):
        points = []
        if velocity.x == 0:
            return points
        for x in range(int(start_pos.x), int(SCREEN_WIDTH*(1-current_player)), 10*(1-2*current_player)):
            t = (x - start_pos.x) / velocity.x
            y = start_pos.y + velocity.y * t + 0.5 * gravity * t ** 2
            points.append((int(x), int(y)))
        return points
    # Draw the restart button
    restart_button = pygame.Rect(SCREEN_WIDTH*RESTART_BUTTON_X_PCT, SCREEN_HEIGHT*RESTART_BUTTON_Y_PCT, RESTART_BUTTON_WIDTH, RESTART_BUTTON_HEIGHT)
    restart_text = font_small.render("Restart", True, "black")
    restart_text_rect = restart_text.get_rect(center=restart_button.center)

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            
            if event.type == pygame.MOUSEBUTTONDOWN and not launch_ready:
                if restart_button.collidepoint(event.pos):
                    # Restart the game
                    return True
                else:
                    dragging = True
                    mouse_start = pygame.Vector2(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEBUTTONUP and dragging:
                # Play the release sound and release the bird
                pull = players[current_player]["player_pos"] - players[current_player]["start_pos"]
                vol = min(1, pull.length() / MAX_PULL)
                if sound_on:
                    assets['release'].set_volume(vol)
                    assets['release'].play()
                dragging = False
                launch_ready = True
                players[current_player]["velocity"] = (-pull) * scale_power

            


        # Update
        # Draw the background (use preloaded)
        screen.blit(assets['background'], (0, 0))

        # Draw the scores
        screen.blit(assets['score'], ((SCREEN_WIDTH-SCORE_WIDTH)/2, SCREEN_HEIGHT*SCORE_RECT_Y_PCT))
        score_1 = font_large.render(f"{players[0]['blocks_remaining']}", True, "black")
        score_2 = font_large.render(f"{players[1]['blocks_remaining']}", True, "black")
        screen.blit(score_1, ((SCREEN_WIDTH-SCORE_WIDTH)/2 + SCORE_WIDTH/20, SCREEN_HEIGHT*SCORE_RECT_Y_PCT + SCORE_HEIGHT/2.75))
        screen.blit(score_2, ((SCREEN_WIDTH+SCORE_WIDTH)/2 - SCORE_WIDTH/7, SCREEN_HEIGHT*SCORE_RECT_Y_PCT + SCORE_HEIGHT/2.75))

        # Draw the restart button
        pygame.draw.rect(screen, "yellow", restart_button, border_radius=10)
        screen.blit(restart_text, restart_text_rect)
        # wind animation
        if level != "easy":
            direction = -1 if current_player == 0 else 1
            for pos in wind_lines:
                pos.x += LINE_SPEED * dt * direction
                # wrap around
                if pos.x > SCREEN_WIDTH:
                    pos.x = -LINE_LENGTH
                elif pos.x < -LINE_LENGTH:
                    pos.x = SCREEN_WIDTH
            wind_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            for pos in wind_lines:
                start = (int(pos.x),     int(pos.y))
                end   = (int(pos.x+LINE_LENGTH), int(pos.y))
                pygame.draw.line(wind_surf, LINE_COLOR, start, end, 3)
            screen.blit(wind_surf, (0,0))

        # Draw the slingshot
        screen.blit(assets['sling'], players[0]['sling'])
        screen.blit(assets['sling_flipped'], players[1]['sling'])

        # Draw the trajectory
        last_stretch_time = 0
        if dragging:
            now = pygame.time.get_ticks()
            current_mouse = pygame.Vector2(pygame.mouse.get_pos())
            start = players[current_player]["start_pos"]
            pull = current_mouse - start

            # clamp the length
            if pull.length() > MAX_PULL:
                pull.scale_to_length(MAX_PULL)

            # clamp the x position
            if current_player == 0:
                pull.x = min(pull.x, 0)
            else:
                pull.x = max(pull.x, 0)


            # update where the bird is drawn
            players[current_player]["player_pos"] = start + pull
            bird_center = players[current_player]["player_pos"]
            anchor1, anchor2 = players[current_player]["band_anchors"]
            
            BAND_COLOR = (48, 22, 8)
            BAND_WIDTH = 10 

            pull_len = (bird_center - players[current_player]["start_pos"]).length()
            max_len  = MAX_PULL
            width = int(10 * (1 - pull_len/max_len) + 2)  # between 2 and 12px

            # draw each band from anchor to bird
            pygame.draw.line(screen, BAND_COLOR, anchor1, bird_center, BAND_WIDTH)
            pygame.draw.line(screen, BAND_COLOR, anchor2, bird_center, BAND_WIDTH)
            points = show_projectile(pull * scale_power, players[current_player]["player_pos"])
            if len(points) > 1 and level != "hard":
                pygame.draw.lines(screen, "lightgray", False, points, 2)

        # Draw the slingshot birds
        for i in (0, 1):
            if i == current_player and players[current_player]["bomb_disappear"]:
                continue
            key = players[i]['selected_order'][0]
            bird_img = assets['birds'][key]
            bird_scaled = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
            if i == 1:
                bird_scaled = pygame.transform.flip(bird_scaled, True, False)
            blit_pos = (players[i]['player_pos'].x - BIRD_WIDTH/2, players[i]['player_pos'].y - BIRD_HEIGHT/2)
            screen.blit(bird_scaled, blit_pos)

        # Draw the not-selected birds
        for i in (0, 1):
            for idx, rect in enumerate(players[i]['not_selected_birds']):
                key = players[i]['selected_order'][idx + 1]
                bird_img = assets['birds'][key]
                bird_scaled = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
                if i == 1:
                    bird_scaled = pygame.transform.flip(bird_scaled, True, False)
                screen.blit(bird_scaled, rect)

        
        # Draw the blocks
        wood = assets['wood']
        stone = assets['stone']
        ice = assets['ice']

        for i in range(2):  # Loop through both players
            for block in players[i]["blocks"]["wood"]:
                if block["hp"] > 0:
                    screen.blit(wood, block["rect"].topleft)
            for block in players[i]["blocks"]["stone"]:
                if block["hp"] > 0:
                    screen.blit(stone, block["rect"].topleft)
            for block in players[i]["blocks"]["ice"]:
                if block["hp"] > 0:
                    screen.blit(ice, block["rect"].topleft)

        # Animation of the explosion
        if players[current_player]["animation_explosion_on"]:
            if players[current_player]["animation_frame_timer"] > 0:
                players[current_player]["animation_frame_timer"] -= 1
                screen.blit(assets['explosion_frames'][players[current_player]["animation_frame_no"]], (players[current_player]["explosion_centre"].x - BLOCK_WIDTH*1.5, players[current_player]["explosion_centre"].y - BLOCK_HEIGHT*1.5))
            elif players[current_player]["animation_frame_no"] < TOTAL_FRAMES - 1:
                players[current_player]["animation_frame_no"] += 1
                players[current_player]["animation_frame_timer"] = 15
            else: 
                time = pygame.time.get_ticks()
                # show hp bars
                for block_list in players[1-current_player]["blocks"].values():
                    for block in block_list:
                        if block["hp"] > 0 and block["hit_status"] and block["hp_bar_timer"]:
                            # Draw an hp bar
                            if block["hp_bar_timer"] > 0:
                                bar_h = int(SCREEN_HEIGHT*0.01)
                                bar_w = int(BLOCK_WIDTH*0.5)

                                bar_fill = int(bar_w*block["hp"]/block["max_hp"])
                                bar_rem = bar_w - bar_fill

                                bar_x, bar_y = block["rect"].x - bar_w/4, block["rect"].y + bar_h
                                bar_fill_rect = pygame.Rect(bar_x, bar_y, bar_fill, bar_h)
                                bar_rem_rect = pygame.Rect(bar_x+bar_fill, bar_y, bar_rem, bar_h)

                                pygame.draw.rect(screen, (255, 0, 0), bar_fill_rect)
                                pygame.draw.rect(screen, (0, 0, 0), bar_rem_rect)
                                block["hp_bar_timer"] -= 1
                            else:
                                block["hit_status"] = False
                if time > 2000:
                    reset()

        # Applying physics, collision handling, and updating positions
        if launch_ready and not players[current_player]["bomb_disappear"]:
            screen.blit(font.render(f"Velocity: {int(players[current_player]["velocity"].length())}", True, "black"), (10, 10))
            player_rect = pygame.Rect(players[current_player]["player_pos"].x - BIRD_WIDTH/2, players[current_player]["player_pos"].y - BIRD_HEIGHT/2, BIRD_WIDTH, BIRD_HEIGHT)

            def explosion_damage(blast_centre, blast_radius, damage, block_dict, target_player_idx, blast_done):
                if blast_done:
                    return
                for block_list in block_dict.values():
                    for block in block_list:
                        if block["hp"] <= 0:
                            continue
                        dist = pygame.math.Vector2(block["rect"].center).distance_to(blast_centre)
                        if dist <= blast_radius:
                            block["hp"] -= damage
                            block["hp_bar_timer"] = 90
                            block["hit_status"] = True


            # Collision with the block
            def handle_collision(blocks):
                new_blocks = []
                for block in blocks:
                    if block["hp"] > 0:
                        if block["hit_status"]:
                            # Draw an hp bar
                            if block["hp_bar_timer"] > 0:

                                bar_h = int(SCREEN_HEIGHT*0.01)
                                bar_w = int(BLOCK_WIDTH*0.5)

                                bar_fill = int(bar_w*block["hp"]/block["max_hp"])
                                bar_rem = bar_w - bar_fill

                                bar_x, bar_y = block["rect"].x - bar_w/4, block["rect"].y + bar_h
                                bar_fill_rect = pygame.Rect(bar_x, bar_y, bar_fill, bar_h)
                                bar_rem_rect = pygame.Rect(bar_x+bar_fill, bar_y, bar_rem, bar_h)

                                pygame.draw.rect(screen, (255, 0, 0), bar_fill_rect)
                                pygame.draw.rect(screen, (0, 0, 0), bar_rem_rect)
                                block["hp_bar_timer"] -= 1
                            
                            elif block["hp_bar_timer"] <= 0:
                                block["hit_status"] = False
                            

                        if player_rect.colliderect(block["rect"]):
                            # Play the hit sound based on block type
                            MAX_BOUNCE_VELOCITY = 1000
                            if sound_on:
                                vol = min(1, players[current_player]["velocity"].length() / MAX_BOUNCE_VELOCITY)
                                assets[f"{block['type']}-hit"].set_volume(vol)
                                assets[f"{block['type']}-hit"].play()
                            block["hit_status"] = True

                            # Calculate the collision normal vector
                            normal = (pygame.Vector2(player_rect.center) - pygame.Vector2(block["rect"].center)).normalize()

                            # Reflect the current player's velocity (not the opponent's!)
                            players[current_player]["velocity"] = players[current_player]["velocity"].reflect(normal) * bounce

                            # Adjust the player's position to prevent sticking
                            if players[current_player]["player_pos"].x < block["rect"].left or players[current_player]["player_pos"].x > block["rect"].right:
                                players[current_player]["player_pos"].x = block["rect"].left - BIRD_WIDTH/2 if players[current_player]["player_pos"].x < block["rect"].left else block["rect"].right + BIRD_WIDTH/2
                            if players[current_player]["player_pos"].y < block["rect"].top or players[current_player]["player_pos"].y > block["rect"].bottom:
                                players[current_player]["player_pos"].y = block["rect"].top - BIRD_HEIGHT/2 if players[current_player]["player_pos"].y < block["rect"].top else block["rect"].bottom + BIRD_HEIGHT/2

                            # Subtract HP based on the speed of impact, the type of block and bird
                            block["hp"] -= int(players[current_player]["velocity"].length() * Birds_damage_multiplier[players[current_player]["selected_order"][0]][block["type"]])
                            if players[current_player]["selected_order"][0] == "Bomb" and players[current_player]["explosion_damage_on"] and players[current_player]["blast_done"] == False:
                                players[current_player]["explosion_damage_on"] = False
                                players[current_player]["explosion_damage"] = int(players[current_player]["velocity"].length() * 0.4)
                                players[current_player]["explosion_centre"] = players[current_player]["player_pos"].copy()
                                explosion_damage(
                                                players[current_player]["explosion_centre"],
                                                EXPLOSION_RADIUS,
                                                players[current_player]["explosion_damage"],
                                                players[1-current_player]["blocks"],
                                                1-current_player,
                                                players[current_player]["blast_done"]
                                            )

                                players[current_player]["blast_done"] = True
                                players[current_player]["bomb_disappear"] = True
                                players[current_player]["animation_explosion_on"] = True
                        
                        new_blocks.append(block)
                return new_blocks
            
            
            # Apply collision detection to the opponent's blocks (as expected)
            players[1 - current_player]["blocks"]["wood"] = handle_collision(players[1-current_player]["blocks"]["wood"])
            players[1 - current_player]["blocks"]["stone"] = handle_collision(players[1-current_player]["blocks"]["stone"])
            players[1 - current_player]["blocks"]["ice"] = handle_collision(players[1-current_player]["blocks"]["ice"])

            # calculating the blocks remaining
            remaining = 0
            for block_list in players[1-current_player]["blocks"].values():
                for block in block_list:
                    if block["hp"] > 0:
                        remaining += 1
            # Update the blocks remaining for the current player
            players[1-current_player]["blocks_remaining"] = remaining

            # Gravity and friction
            players[current_player]["velocity"].y += gravity * dt
            if level != "easy":
                players[current_player]["velocity"].x -= players[current_player]["velocity"].x*wind * dt
            if friction_on:
                players[current_player]["velocity"].x -= players[current_player]["velocity"].x*friction*dt
            players[current_player]["player_pos"] += players[current_player]["velocity"] * dt

            # Bounce
            if players[current_player]["player_pos"].y >= ground_y:
                MAX_BOUNCE_VELOCITY = 1000
                vol = min(1, players[current_player]["velocity"].length() / MAX_BOUNCE_VELOCITY)
                if sound_on:
                    assets['bounce'].set_volume(vol)
                    assets['bounce'].play()
                players[current_player]["player_pos"].y = ground_y
                players[current_player]["velocity"].y *= -bounce
                friction_on = True      
            
            def reset():
                nonlocal current_player, launch_ready, friction_on, dragging, mouse_start

                # See if the match ended
                if players[1-current_player]["blocks_remaining"] == 0:
                    winning_text = font_large.render(f"{players[current_player]['name']} wins!", True, "black")
                    screen.blit(winning_text, (SCREEN_WIDTH/2 - winning_text.get_width()/2, SCREEN_HEIGHT/2 - winning_text.get_height()/2))
                    pygame.display.flip()
                    pygame.time.delay(2000)   
                    nonlocal running
                    running = False
                    global winner
                    winner = players[1-current_player]["name"]
                
                if running:
                    # Reset the bird position and velocity
                    players[current_player]["velocity"] = pygame.Vector2(0, 0)
                    players[current_player]["player_pos"] = players[current_player]["start_pos"].copy()
                    players[current_player]["blast_done"] = False
                    players[current_player]["explosion_damage_on"] = True
                    players[current_player]["bomb_disappear"] = False
                    players[current_player]["animation_explosion_on"] = False
                    players[current_player]["animation_frame_no"] = 0

                    # make the hp bar timer back to 90
                    for block_list in players[1-current_player]["blocks"].values():
                        for block in block_list:
                            block["hp_bar_timer"] = 90
                            block["hit_status"] = False

                    # Now change the bird order for this player
                    temp = players[current_player]["selected_order"][0]
                    players[current_player]["selected_order"].pop(0)
                    players[current_player]["selected_order"].append(temp)

                    # 

                    # change the player
                    current_player = 1 - current_player

                    # Show the current player's turn
                    text_surface = font_large.render(f"{players[current_player]['name']}'s turn", True, "white")
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
                    screen.blit(text_surface, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(2000)

                    # change slingshot parameters
                    friction = 0.4
                    launch_ready = False
                    friction_on = False
                    dragging = False
                    mouse_start = pygame.Vector2()
            
            # Reset conditions
            if players[current_player]["player_pos"].x >= 1600 - BIRD_WIDTH/2 or players[current_player]["player_pos"].x <= BIRD_WIDTH/2 or players[current_player]["player_pos"].y <= BIRD_HEIGHT/2 or players[current_player]["player_pos"].y >= 900 - BIRD_HEIGHT/2 or players[current_player]["velocity"].length() < 30:
                pygame.time.delay(500)
                reset()
            if players[current_player]["velocity"].x*(1-2*current_player)<0 and level == "easy":
                friction = 1
            
        # Draw the screen
        pygame.display.flip()
        dt = clock.tick(60) / 1000
    
    return winner