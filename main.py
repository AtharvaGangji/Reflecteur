# ------------------------------------------------------------ imports
import pygame, random

# ------------------------------------------------------------ variables
running = True
real_paddle_x = 100
real_paddle_y = 100

fake_paddle_x = 200
fake_paddle_y = 200

move_speed = 5
key_down = False
direction = ""

player_down = pygame.image.load("assets/player_down.gif")
player_down = pygame.transform.scale(player_down, (50, 50))
player_face = player_down
player_face_fake = player_down

paddle_size = 50

real_paddle_rect = None
fake_paddle_rect = None
coin_rect = None

WIDTH = 1000
HEIGHT = 600

LEVEL = 1
LIVES = 3

COIN = int(0)

coin_pos_x = 0
coin_pos_y = 0

last_pos_x = 0
last_pos_y = 0

door_size = 100

door_open_rect = None
door_open_rect2 = None

block_list_level_3 = []

blocks_made = False

spike_pos_x = 250
spike_pos_y = 50

instruction = 0

spike_rect = None
spike_rect2 = None
spike_rect3 = None
spike_rect4 = None


# ------------------------------------------------------------ main game function
def play():
    pygame.init()  # initialise pygame

    clock = pygame.time.Clock()  # pygame clock

    global running, real_paddle_x, real_paddle_y, move_speed, key_down, direction, LEVEL, coin_pos_y  # global variables
    global fake_paddle_x, fake_paddle_y, paddle_size, coin_pos_x, real_paddle_rect, coin_rect, COIN  # global variables
    global last_pos_x, last_pos_y, door_size, blocks_made, spike_pos_x, spike_pos_y, spike_rect  # global variables
    global spike_rect2, spike_rect3, spike_rect4, instruction  # global variables

    window = pygame.display.set_mode((WIDTH, HEIGHT))  # initialise window

    game_font = pygame.font.Font("assets/Anonymous_Pro.ttf", 35)
    instruction_font = pygame.font.Font("assets/Anonymous_Pro.ttf", 21)

    player_right = pygame.image.load("assets/player_left.gif")
    player_right = pygame.transform.scale(player_right, (paddle_size, paddle_size))

    door_open = pygame.image.load("assets/door.png")
    door_open = pygame.transform.scale(door_open, (door_size, door_size))

    player_left = pygame.image.load("assets/player_right.gif")
    player_left = pygame.transform.scale(player_left, (paddle_size, paddle_size))

    player_up = pygame.image.load("assets/player_up.gif")
    player_up = pygame.transform.scale(player_up, (paddle_size, paddle_size))

    player_down = pygame.image.load("assets/player_down.gif")
    player_down = pygame.transform.scale(player_down, (paddle_size, paddle_size))

    bg_image = pygame.image.load("assets/bg image 1.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    coin_image = pygame.image.load("assets/coin_image.gif")
    coin_image = pygame.transform.scale(coin_image, (35, 35))

    block_image = pygame.image.load("assets/block.png")
    block_image = pygame.transform.scale(block_image, (50, 50))

    spike_image = pygame.image.load("assets/spike_bar.gif")
    spike_image = pygame.transform.scale(spike_image, (spike_pos_x, spike_pos_y))

    # -------------------------------------------- load songs
    hit = pygame.mixer.Sound("assets/hit.wav")
    lose = pygame.mixer.Sound("assets/lost-heart.wav")
    collect = pygame.mixer.Sound("assets/collect.wav")

    # -------------------------------------------- functions
    def real_paddle():  # ---------- real paddle
        global real_paddle_rect
        real_paddle_rect = pygame.Rect(real_paddle_x, real_paddle_y, paddle_size, paddle_size)  # (x, y, width, height)
        window.blit(player_face, real_paddle_rect)

    def fake_paddle():  # ---------- fake paddle
        global fake_paddle_rect
        fake_paddle_rect = pygame.Rect(fake_paddle_x, fake_paddle_y, paddle_size, paddle_size)  # (x, y, width, height)
        window.blit(player_face_fake, fake_paddle_rect)

    def restart():
        global real_paddle_x, real_paddle_y, fake_paddle_x, fake_paddle_y

        if LEVEL == 1:
            real_paddle_x = 100
            real_paddle_y = 100
            fake_paddle_x = 200
            fake_paddle_y = 200
        elif LEVEL == 2:
            real_paddle_x = WIDTH - 100
            real_paddle_y = HEIGHT - 100
            fake_paddle_x = 10
            fake_paddle_y = 10
        elif LEVEL == 3:
            real_paddle_x = WIDTH - 100
            real_paddle_y = 10
            fake_paddle_x = 10
            fake_paddle_y = 10
        elif LEVEL == 4:
            real_paddle_x = WIDTH
            real_paddle_y = 0
            fake_paddle_x = 0
            fake_paddle_y = 0

        real_paddle()
        fake_paddle()
        coin_random()
        coin()

    def fill_bg_color():  # ---------- fill with bg color
        window.fill((255, 255, 255))

    def coin_random():
        global coin_pos_x, coin_pos_y, coin_rect, last_pos_y, last_pos_x
        if COIN > 0:
            coin_pos_x = random.randrange(30, 950)
            coin_pos_y = random.randrange(30, 600)

            if coin_pos_x - last_pos_x <= 1 and coin_pos_y - last_pos_y <= 1:
                coin_random()
            else:
                last_pos_x = coin_pos_x
                last_pos_y = coin_pos_y
    coin_random()

    def coin_level_4():
        if spike_rect.colliderect(coin_rect) or spike_rect2.colliderect(coin_rect) or spike_rect3.colliderect(coin_rect) or \
                spike_rect4.colliderect(coin_rect):
            coin_random()
            coin()

    def coin():
        global coin_pos_x, coin_rect, coin_pos_y, spike_rect

        coin_rect = coin_image.get_rect(center=(coin_pos_x, coin_pos_y))
        window.blit(coin_image, coin_rect)

    def coin_collect():
        global real_paddle_rect, coin_rect, fake_paddle_rect, COIN

        if COIN > 0:
            if real_paddle_rect.colliderect(coin_rect) or fake_paddle_rect.colliderect(coin_rect):
                print("collision")
                collect.play()
                COIN -= int(1)
                coin_random()

    def level():
        global COIN
        if LEVEL == 1:
            COIN = 2
        if LEVEL == 2:
            COIN = 4
        if LEVEL == 3:
            COIN = 6
        if LEVEL == 4:
            COIN = 8
        coin_random()
        coin()
        restart()
    level()

    def level_display():
        global LEVEL
        level_surface = game_font.render(f"Level: {int(LEVEL)}", True, (255, 255, 255))
        level_rect = level_surface.get_rect(center = (100, 30))
        window.blit(level_surface, level_rect)

        level_surface = game_font.render(f"Lives: {int(LIVES)}", True, (255, 255, 255))
        level_rect = level_surface.get_rect(center = (300, 30))
        window.blit(level_surface, level_rect)

    def tutorial_text():
        if instruction < 6:
            tutorial_surface = instruction_font.render("Watch the itch page to know how to play", True, (255, 255, 255))
            tutorial_rect = tutorial_surface.get_rect(center = (520, 540))
            window.blit(tutorial_surface, tutorial_rect)

    def level_complete():
        global LEVEL
        LEVEL += 1

    def live_is_0():
        global LEVEL, LIVES
        if LIVES <= 0:
            LEVEL = 0
            LIVES = 3
            level_complete()
            level()

    def lives_minus():
        global LIVES
        LIVES -= 1
        restart()
        live_is_0()

    def bg_thing():
        window.blit(bg_image, (0, 0, 0, 0))

    def open_doors(x):
        global door_open_rect, door_open_rect2
        if x == 1:
            door_open_rect = pygame.Rect(10, 0, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect)

            door_open_rect2 = pygame.Rect(WIDTH - 100, HEIGHT - 100, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect2)
        elif x == 2:
            door_open_rect = pygame.Rect(500, 100, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect)

            door_open_rect2 = pygame.Rect(0, 500, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect2)
        elif x == 3:
            door_open_rect = pygame.Rect(500, 100, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect)

            door_open_rect2 = pygame.Rect(800, 10, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect2)
        elif x == 4:
            door_open_rect = pygame.Rect(10, 0, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect)

            door_open_rect2 = pygame.Rect(WIDTH - 100, HEIGHT - 100, door_size, door_size)  # (x, y, width, height)
            window.blit(door_open, door_open_rect2)
        elif x == 5:
            pass

    def inside_door():
        global door_open_rect, door_open_rect2, real_paddle_rect, fake_paddle_rect
        if real_paddle_rect.colliderect(door_open_rect) and fake_paddle_rect.colliderect(door_open_rect2) or \
                fake_paddle_rect.colliderect(door_open_rect) and real_paddle_rect.colliderect(door_open_rect2):
            hit.play()
            level_complete()
            level()

    def block_level_2():
        global fake_paddle_x, real_paddle_x, fake_paddle_y, real_paddle_y  # global variables

        block_level_2_rect = pygame.Rect(400, 90, 50, 50)  # (x, y, width, height)
        window.blit(block_image, block_level_2_rect)

        if real_paddle_rect.colliderect(block_level_2_rect):
            if direction == "up":
                real_paddle_y += 5
            elif direction == "down":
                real_paddle_y -= 5
            elif direction == "right":
                real_paddle_x -= 5
            elif direction == "left":
                real_paddle_x += 5
        if fake_paddle_rect.colliderect(block_level_2_rect):
            if direction == "up":
                fake_paddle_y -= 5
            elif direction == "down":
                fake_paddle_y += 5
            elif direction == "right":
                fake_paddle_x += 5
            elif direction == "left":
                fake_paddle_x -= 5

    def make_blocks_level_3():
        global block_list_level_3, blocks_made

        block_level_3_x_pos = 720
        block_level_3_y_pos = 200

        block_list_level_3.append(pygame.Rect(block_level_3_x_pos, 0, 50, 50))
        block_list_level_3.append(pygame.Rect(block_level_3_x_pos, 50, 50, 50))
        block_list_level_3.append(pygame.Rect(block_level_3_x_pos, 100, 50, 50))
        block_list_level_3.append(pygame.Rect(block_level_3_x_pos, 150, 50, 50))
        block_list_level_3.append(pygame.Rect(block_level_3_x_pos, 200, 50, 50))
        block_list_level_3.append(pygame.Rect(770, block_level_3_y_pos, 50, 50))
        block_list_level_3.append(pygame.Rect(820, block_level_3_y_pos, 50, 50))
        block_list_level_3.append(pygame.Rect(870, block_level_3_y_pos, 50, 50))
        block_list_level_3.append(pygame.Rect(920, block_level_3_y_pos, 50, 50))
        block_list_level_3.append(pygame.Rect(970, block_level_3_y_pos, 50, 50))

        blocks_made = True

    def block_level_3():
        global fake_paddle_x, real_paddle_x, fake_paddle_y, real_paddle_y  # global variables

        for x in block_list_level_3:
            window.blit(block_image, x)

    def check_block_collision_level_3():
        global real_paddle_y, real_paddle_x, fake_paddle_y, fake_paddle_x  # global variables

        for x in block_list_level_3:
            if fake_paddle_rect.colliderect(x):
                if direction == "up":
                    fake_paddle_y -= 5
                elif direction == "down":
                    fake_paddle_y += 5
                elif direction == "right":
                    fake_paddle_x += 5
                elif direction == "left":
                    fake_paddle_x -= 5
            if real_paddle_rect.colliderect(x):
                if direction == "up":
                    real_paddle_y += 5
                elif direction == "down":
                    real_paddle_y -= 5
                elif direction == "right":
                    real_paddle_x -= 5
                elif direction == "left":
                    real_paddle_x += 5

    def make_spike_level_4():
        global spike_rect, spike_rect2, spike_rect3, spike_rect4
        spike_rect = pygame.Rect(500, 100, spike_pos_x, spike_pos_y)
        spike_rect2 = pygame.Rect(100, 184, spike_pos_x, spike_pos_y)
        spike_rect3 = pygame.Rect(500, 500, spike_pos_x, spike_pos_y)
        spike_rect4 = pygame.Rect(200, 350, spike_pos_x, spike_pos_y)

        window.blit(spike_image, spike_rect)
        window.blit(spike_image, spike_rect2)
        window.blit(spike_image, spike_rect3)
        window.blit(spike_image, spike_rect4)

    def spike_collision_level_4():
        global spike_rect, spike_rect2, spike_rect3, spike_rect4

        if real_paddle_rect.colliderect(spike_rect) or real_paddle_rect.colliderect(spike_rect2) or \
                real_paddle_rect.colliderect(spike_rect3) or real_paddle_rect.colliderect(spike_rect4):
            lose.play()
            lives_minus()
        if fake_paddle_rect.colliderect(spike_rect) or fake_paddle_rect.colliderect(spike_rect2) or \
                fake_paddle_rect.colliderect(spike_rect3) or fake_paddle_rect.colliderect(spike_rect4):
            lose.play()
            lives_minus()

    def move_real_paddle():  # ---------- move real paddle
        global real_paddle_x, real_paddle_y, move_speed, direction, player_face  # globals

        if direction == "up":
            real_paddle_y -= move_speed
            fill_bg_color()
            player_face = player_up
        elif direction == "down":
            real_paddle_y += move_speed
            fill_bg_color()
            player_face = player_down
        elif direction == "left":
            real_paddle_x -= move_speed
            fill_bg_color()
            player_face = player_left
        elif direction == "right":
            real_paddle_x += move_speed
            fill_bg_color()
            player_face = player_right

    def move_fake_paddle():  # ---------- move fake paddle
        global fake_paddle_x, fake_paddle_y, move_speed, direction, player_face_fake  # globals

        if direction == "up":
            fake_paddle_y += move_speed
            fill_bg_color()
            player_face_fake = player_down
        elif direction == "down":
            fake_paddle_y -= move_speed
            fill_bg_color()
            player_face_fake = player_up
        elif direction == "left":
            fake_paddle_x += move_speed
            fill_bg_color()
            player_face_fake = player_right
        elif direction == "right":
            fake_paddle_x -= move_speed
            fill_bg_color()
            player_face_fake = player_left

    def border():
        global fake_paddle_x, fake_paddle_y, real_paddle_x, real_paddle_y  # globals

        if fake_paddle_x <= 0:
            fake_paddle_x = 0
        if real_paddle_x <= 0:
            real_paddle_x = 0
        if fake_paddle_y <= 0:
            fake_paddle_y = 0
        if real_paddle_y <= 0:
            real_paddle_y = 0

        if fake_paddle_x >= WIDTH - paddle_size:
            fake_paddle_x = WIDTH - paddle_size
        if real_paddle_x >= WIDTH - paddle_size:
            real_paddle_x = WIDTH - paddle_size
        if fake_paddle_y >= HEIGHT - paddle_size:
            fake_paddle_y = HEIGHT - paddle_size
        if real_paddle_y >= HEIGHT - paddle_size:
            real_paddle_y = HEIGHT - paddle_size

    # -------------------------------------------- main while loop
    while running:
        for event in pygame.event.get():
            # --------------- Quit Window
            if event.type == pygame.QUIT:  # Quit window if close button pressed
                running = False
            # --------------- Track button down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Escape Button Quit Window
                    running = False
                if event.key == pygame.K_r:  # Escape Button Quit Window
                    restart()
                if event.key == pygame.K_UP:  # move the real paddle up
                    direction = "up"
                    key_down = True
                if event.key == pygame.K_DOWN:  # move the real paddle up
                    direction = "down"
                    key_down = True
                if event.key == pygame.K_RIGHT:  # move the real paddle up
                    direction = "right"
                    key_down = True
                if event.key == pygame.K_LEFT:  # move the real paddle up
                    direction = "left"
                    key_down = True

            # --------------- Track button up
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:  # move the real paddle up
                    direction = "up"
                    key_down = False
                    instruction += 1
                if event.key == pygame.K_DOWN:  # move the real paddle up
                    direction = "down"
                    key_down = False
                    instruction += 1
                if event.key == pygame.K_RIGHT:  # move the real paddle up
                    direction = "right"
                    key_down = False
                    instruction += 1
                if event.key == pygame.K_LEFT:  # move the real paddle up
                    direction = "left"
                    key_down = False
                    instruction += 1

        if key_down:
            move_real_paddle()  # fall a function
            move_fake_paddle()  # fall a function

        bg_thing()

        level_display()

        real_paddle()

        border()

        fake_paddle()

        if LEVEL == 1:
            tutorial_text()

        if COIN > 0:
            coin()

        if COIN <= 0:
            open_doors(LEVEL)
            if not LEVEL >= 6:
                inside_door()

        if LEVEL == 2:  # check if level 2
            block_level_2()

        if not blocks_made:
            make_blocks_level_3()

        if LEVEL == 3:  # check if level 3
            block_level_3()
            check_block_collision_level_3()

        if LEVEL == 4:  # check if level 4
            make_spike_level_4()
            spike_collision_level_4()
            coin_level_4()

        coin_collect()

        pygame.display.update()  # update the display

        clock.tick(70)  # fps


# ------------------------------------------------------------ needed if statement
if __name__ == "__main__":
    play()
