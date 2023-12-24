import pygame
import sys
import random
import json

pygame.init()

# Fenstergröße
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Alien Wars")

# Spieler
player_img = pygame.image.load('img/player.png')
player_img = pygame.transform.scale(player_img, (100, 50))  
player_x, player_y = 50, height // 2 - player_img.get_height() // 2
player_speed = 7

# Geschoss-Eigenschaften
bullet_radius = 5
bullet_speed = 10
bullets = []

# Gegner
enemy_img = pygame.image.load('img/enemy.png')
enemy_img = pygame.transform.scale(enemy_img, (50, 50))  
enemy_speed = 2
enemies = []

# Punktzahl
score = 0
font = pygame.font.Font(None, 36)

# Stern-Eigenschaften
stars = [{'x': random.randint(0, width), 'y': random.randint(0, height), 'speed': random.randint(1, 3)} for _ in range(300)]

clock = pygame.time.Clock()

# Highscore-Datei
highscore_file = 'highscore.json'

def save_highscore(score):
    with open(highscore_file, 'w') as file:
        json.dump(score, file)

def load_highscore():
    try:
        with open(highscore_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return 0

highscore = load_highscore()

# Funktionen
def create_enemy():
    enemy = {'x': width, 'y': random.randint(0, height - enemy_img.get_height())}
    enemies.append(enemy)

def draw_enemies():
    for enemy in enemies:
        screen.blit(enemy_img, (enemy['x'], enemy['y']))

def move_enemies():
    for enemy in enemies:
        enemy['x'] -= enemy_speed

def collision_detection():
    global enemies, bullets, score
    for bullet in bullets:
        for enemy in enemies:
            if (bullet['x'] + bullet_radius > enemy['x'] and
               bullet['x'] - bullet_radius < enemy['x'] + enemy_img.get_width() and
               bullet['y'] + bullet_radius > enemy['y'] and
               bullet['y'] - bullet_radius < enemy['y'] + enemy_img.get_height()):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                break

def check_game_over():
    global score
    for enemy in enemies:
        if enemy['x'] <= 0 or (
            enemy['x'] <= player_x + player_img.get_width() and
            enemy['y'] + enemy_img.get_height() >= player_y and
            enemy['y'] <= player_y + player_img.get_height()
        ):
            return True
    return False

def draw_bullets():
    for bullet in bullets:
        pygame.draw.circle(screen, (0, 255, 0), (bullet['x'], bullet['y']), bullet_radius)

# Neuer Spielzustand
game_active = True

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bullet = {'x': player_x + player_img.get_width(), 'y': player_y + player_img.get_height() // 2}
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and game_active:
        player_y -= player_speed
    elif keys[pygame.K_s] and game_active:
        player_y += player_speed

    player_y = min(max(player_y, 0), height - player_img.get_height())

    if game_active:
        move_enemies()

        if random.randint(1, 75) == 1:
            create_enemy()

        draw_enemies()
        collision_detection()

        for bullet in bullets:
            bullet['x'] += bullet_speed

        bullets = [bullet for bullet in bullets if bullet['x'] < width]

        # Überprüfen, ob die Anzahl der zerstörten Gegner eine Schwelle erreicht hat
        if score > 0 and score % 10 == 0:
            # Geschwindigkeit der Gegner erhöhen, wenn der Spieler eine bestimmte Punktzahl erreicht hat
            enemy_speed += 0.001

        if check_game_over():
            game_active = False
            if score > highscore:  
                highscore = score
                save_highscore(highscore)

        draw_bullets()  

    score_text = font.render(f"Score: {score} Highscore: {highscore}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))

    if not game_active:
        game_over_text = font.render("Game Over! Drücke R zum Neustarten.", True, (255, 0, 0))
        screen.blit(game_over_text, (width // 2 - 200, height // 2))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_active = True
            enemies = []
            bullets = []
            score = 0
            player_y = height // 2 - player_img.get_height() // 2
            if score > highscore:  
                highscore = score
                save_highscore(highscore)

    for star in stars:
        pygame.draw.circle(screen, (255, 255, 255), (star['x'], star['y']), 1)
        star['x'] -= star['speed']
        if star['x'] < 0:
            star['x'] = width
            star['y'] = random.randint(0, height)

    screen.blit(player_img, (player_x, player_y))

    pygame.display.flip()
    clock.tick(60)
