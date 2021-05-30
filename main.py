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

COIN = 15

coin_pos = 0


# ------------------------------------------------------------ main game function
def play():
    pygame.init()  # initialise pygame

    clock = pygame.time.Clock()  # pygame clock

    global running, real_paddle_x, real_paddle_y, move_speed, key_down, direction, LEVEL  # global variables
    global fake_paddle_x, fake_paddle_y, paddle_size, coin_pos, real_paddle_rect, coin_rect, COIN  # global variables

    window = pygame.display.set_mode((WIDTH, HEIGHT))  # initialise window

    game_font = pygame.font.Font("assets/Anonymous_Pro.ttf", 35)

    player_right = pygame.image.load("assets/player_left.gif")
    player_right = pygame.transform.scale(player_right, (paddle_size, paddle_size))

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

    # -------------------------------------------- level
    def level():
        global COIN
        if LEVEL == 1:
            COIN = 2

    # -------------------------------------------- load songs
    hit = pygame.mixer.Sound("assets/hit.wav")
    heart_lose = pygame.mixer.Sound("assets/lost-heart.wav")
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

    def fill_bg_color():  # ---------- fill with bg color
        window.fill((255, 255, 255))

    def coin_random():
        global coin_pos, coin_rect
        if COIN > 0:
            coin_pos = random.randrange(0, 600)
    coin_random()

    def coin():
        global coin_pos, coin_rect

        coin_rect = coin_image.get_rect(center=(coin_pos, coin_pos))
        window.blit(coin_image, coin_rect)

    def coin_collect():
        global real_paddle_rect, coin_rect, fake_paddle_rect, COIN

        if COIN > 0:
            if real_paddle_rect.colliderect(coin_rect) or fake_paddle_rect.colliderect(coin_rect):
                print("collision")
                collect.play()
                COIN -= 1
                coin_random()

    def level_display():
        global LEVEL
        level_surface = game_font.render(f"Level: {int(LEVEL)}", True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(100, 30))
        window.blit(level_surface, level_rect)

        level_surface = game_font.render(f"Lives: {int(LIVES)}", True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(300, 30))
        window.blit(level_surface, level_rect)

    def level_complete():
        global LEVEL
        LEVEL += 1
        level()

    def bg_thing():
        window.blit(bg_image, (0, 0, 0, 0))

    def open_doors():
        pass

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
                if event.key == pygame.K_DOWN:  # move the real paddle up
                    direction = "down"
                    key_down = False
                if event.key == pygame.K_RIGHT:  # move the real paddle up
                    direction = "right"
                    key_down = False
                if event.key == pygame.K_LEFT:  # move the real paddle up
                    direction = "left"
                    key_down = False

        if key_down:
            move_real_paddle()  # fall a function
            move_fake_paddle()  # fall a function

        bg_thing()

        level_display()

        real_paddle()

        border()

        fake_paddle()

        if COIN > 0:
            coin()

        if COIN < 0:
            open_doors()

        coin_collect()

        pygame.display.update()  # update the display

        clock.tick(70)  # fps


# ------------------------------------------------------------ needed if statement
if __name__ == "__main__":
    play()

