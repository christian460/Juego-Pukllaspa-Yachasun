import pygame
import random
import math
import sys

pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pukllaspa Yachasun")

# Fuentes
font = pygame.font.SysFont('arial', 28)
big_font = pygame.font.SysFont('arial', 48)

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

background = pygame.transform.smoothscale(pygame.image.load("background.jpg"), (800, 600))
# Tamaños
player_size = (64, 64)
bullet_size = (64, 64)
enemy_size = (64, 64)

# Jugador
player_raw = pygame.image.load("darts.png")
player_scaled = pygame.transform.scale(player_raw, player_size)
player_img = pygame.transform.rotate(player_scaled, -90)

# Bala
bullet_raw = pygame.image.load("darts.png")
bullet_scaled = pygame.transform.scale(bullet_raw, bullet_size)
bullet_img = pygame.transform.rotate(bullet_scaled, -90)

# Palabras quechua
word_images = {
    "atoq": pygame.transform.scale(pygame.image.load("fox.png"), enemy_size),
    "michi": pygame.transform.scale(pygame.image.load("cat.png"), enemy_size),
    "alqo": pygame.transform.scale(pygame.image.load("dog.png"), enemy_size),
    "chaska": pygame.transform.scale(pygame.image.load("star.png"), enemy_size),
    "killa": pygame.transform.scale(pygame.image.load("moon.png"), enemy_size),
    "urpi": pygame.transform.scale(pygame.image.load("dove.png"), enemy_size),
}

# Estado inicial
player_x = 368
player_y = 500
player_speed = 0
bullet_x = 0
bullet_y = player_y
bullet_speed = 4
bullet_state = "ready"
lives = 3
score = 0
targets = []
target_word = ""
word_keys = list(word_images.keys())

# Funciones de utilidad
def show_text(text, x, y, font_used=font, color=WHITE):
    rendered = font_used.render(text, True, color)
    screen.blit(rendered, (x, y))

def show_lives():
    show_text(f"Vidas: {lives}", 10, 10)

def show_score():
    show_text(f"Puntaje: {score}", 650, 10)

def player(x, y):
    screen.blit(player_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (
        x + player_img.get_width() // 2 - bullet_img.get_width() // 2,
        y - 10)
    )

def is_collision(target_x, target_y, bullet_x, bullet_y):
    distance = math.sqrt((target_x - bullet_x) ** 2 + (target_y - bullet_y) ** 2)
    return distance < 40  # tolerancia ajustada

def spawn_targets(num=6):
    global targets
    targets = []
    sampled_words = random.sample(word_keys, min(num, len(word_keys)))
    for word in sampled_words:
        img = word_images[word]
        x = random.randint(0, 736)
        y = random.randint(50, 200)
        targets.append({"word": word, "img": img, "x": x, "y": y, "dx": 2})
    return random.choice(sampled_words)

# Primer conjunto de objetivos
target_word = spawn_targets()

clock = pygame.time.Clock()
running = True
while running:
    screen.blit(background, (0, 0))
    show_text("Dispara a: " + target_word.upper(), 270, 10, big_font)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed = -4
            if event.key == pygame.K_RIGHT:
                player_speed = 4
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                bullet_y = player_y
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                player_speed = 0

    # Movimiento del jugador
    player_x += player_speed
    player_x = max(0, min(player_x, 736))

    # Movimiento de la bala
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_speed
    if bullet_y <= 0:
        bullet_y = player_y
        bullet_state = "ready"

    # Movimiento y render de enemigos
    for target in targets:
        target["x"] += target["dx"]
        if target["x"] <= 0 or target["x"] >= 736:
            target["dx"] *= -1
            target["y"] += 40

        screen.blit(target["img"], (target["x"], target["y"]))

        if is_collision(target["x"], target["y"], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            if target["word"] == target_word:
                score += 1
                target_word = spawn_targets()
                break
            else:
                lives -= 1
                if lives == 0:
                    show_text("¡Game Over!", 300, 300, big_font)
                    pygame.display.update()
                    pygame.time.delay(2000)
                    running = False

    player(player_x, player_y)
    show_lives()
    show_score()
    pygame.display.update()
    clock.tick(60)