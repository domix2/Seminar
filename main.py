import sys
import pygame
import os
import time
import random
import sqlite3 
from igrica.utillities import collide
from igrica import Enemy, Player

pygame.font.init()

conn = sqlite3.connect("igra.db")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score INTEGER, level "
          "INTEGER)")

# Postavljanje prozora i sve vezano za njega
WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")


# Učitavanje slika za glavni brod i ostale brodove
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Glavni brod koji igrač koristi
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Učitavanje lasera
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Učitavanje pozadinske slike
Background = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

def main():

    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("arial", 30)
    lost_font = pygame.font.SysFont("arial", 40)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5
    player = Player(300, 630)
    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    def redraw_window():  # funkcija zadužena za prikaz svega na prozoru
        WINDOW.blit(Background, (0, 0))
        #ispis teksta na ekranu
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))  # pogledati na netu RGB kodove
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))


        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("Game over!!",1, (255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

        
    while run:
        clock.tick(FPS) # pomoću ove funkcije igra bez problema se pokreće bilo koji uređaj na 60 FPS
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                game_over(player, level)
                run = False
            else:
                continue

        if len(enemies) == 0: # funkcija koja definira ako nema više neprijatelja na ekranu mijenja se na novi lvl.
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red",
                                                                                                             "blue",
                                                                                                             "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  # omogućuje ako igrač pritisne x za izlazak iz igre - igrica se gasi

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # Pomak ulijevo
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # Pomak udesno
            player.x += player_vel
        if keys[pygame.K_w] and player.y + player_vel > 0:  # Pomak prema gore
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # Pomak prema dolje
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.score += 1
                player.health -= 10
                enemies.remove(enemy)


            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel,enemies)



def main_menu():
    title_font = pygame.font.SysFont("Arial" , 50)
    button_font = pygame.font.SysFont("Arial", 30)
    main_font = pygame.font.SysFont("Arial", 30)

    global player_id

    # Quit button parameters
    quit_button_width = 200
    quit_button_height = 50
    quit_button_x = WIDTH / 2 - quit_button_width / 2
    quit_button_y = HEIGHT - 200

    quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, quit_button_width, quit_button_height)
    quit_button_color = (255, 0, 0)
    quit_button_text = main_font.render("Quit", True, (255, 255, 255))

    run = True
    while run:
        WINDOW.blit(Background, (0, 0))
        title_label = title_font.render("Space Invaders", 1, (255, 255, 255))

        start_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
        pygame.draw.rect(WINDOW, (0, 150, 0), start_button)
        pygame.draw.rect(WINDOW, (255, 255, 255), start_button, 3)
        start_label = button_font.render("Start Game", 1, (255, 255, 255))

        highscore_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 70, 200, 50)
        pygame.draw.rect(WINDOW, (0, 128, 0), highscore_button)
        pygame.draw.rect(WINDOW, (255, 255, 255), highscore_button, 3)

        highscore_label = button_font.render("Highscore", 1, (255, 255, 255))
        WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 300))
        WINDOW.blit(start_label, (WIDTH / 2 - start_label.get_width() / 2, HEIGHT / 2 + 10))
        WINDOW.blit(highscore_label, (WIDTH / 2 - highscore_label.get_width() / 2, HEIGHT / 2 + 80))
        pygame.draw.rect(WINDOW, quit_button_color, quit_button_rect)
        WINDOW.blit(quit_button_text, (quit_button_x + quit_button_width / 2 - quit_button_text.get_width() / 2,
                                       quit_button_y + quit_button_height / 2 - quit_button_text.get_height() / 2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        run = False
                        main()

                    if quit_button_rect.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                    if highscore_button.collidepoint(mouse_pos):
                        if pygame.mouse.get_pressed()[0] == 1:
                            high_scores = get_high_scores()
                            display_highscores()
def get_high_scores():
    c.execute("SELECT * FROM players ORDER BY score DESC LIMIT 5")  # Get the top 5 high scores
    high_scores = c.fetchall()
    return high_scores
def display_highscores():
    conn = sqlite3.connect("igra.db")
    c = conn.cursor()

    c.execute("SELECT * FROM players ORDER BY score DESC")
    highscores = c.fetchall()

    title_font = pygame.font.SysFont("Arial", 50)
    button_font = pygame.font.SysFont("Arial", 30)
    main_font = pygame.font.SysFont("Arial", 30)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        WINDOW.blit(Background, (0, 0))
        title_label = title_font.render("Highscores", 1, (255, 255, 255))
        WINDOW.blit(title_label, (WIDTH / 2 - title_label.get_width() / 2, 50))

        return_button = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2 + 250, 200, 50)
        pygame.draw.rect(WINDOW, (128, 128, 128), return_button)
        pygame.draw.rect(WINDOW, (255, 255, 255), return_button, 3)
        return_label = button_font.render("Return", 1, (255, 255, 255))
        WINDOW.blit(return_label, (WIDTH / 2 - return_label.get_width() / 2, HEIGHT / 2 + 255))

        y_offset = 150
        for score in highscores:
            player_id = score[0]
            player_name = score[1]
            player_score = score[2]
            player_level = score[3]

            score_label = main_font.render(f"{player_id}. {player_name} - Score: {player_score} - Level: {player_level}"
                                           , 1,
                                           (255, 255, 255))
            WINDOW.blit(score_label, (WIDTH / 2 - score_label.get_width() / 2, y_offset))
            y_offset += 50
            mouse_pos = pygame.mouse.get_pos()
            if return_button.collidepoint(mouse_pos):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        main_menu()
                        run = False
        pygame.display.update()


def save_name(player_name, score, level):
    c.execute("SELECT COUNT(*) FROM players")
    row_count = c.fetchone()[0]
    max_rows = 9
    if row_count >= max_rows:
        excess_rows = row_count - max_rows + 1
        c.execute(f"DELETE FROM players WHERE id IN (SELECT id FROM players ORDER BY id ASC LIMIT {excess_rows})")

    c.execute("INSERT INTO players (name, score, level) VALUES (?, ?, ?)", (player_name, score, level))
    conn.commit()
    player_id = c.lastrowid
    popup_font = pygame.font.SysFont("Arial", 30)
    popup_text = popup_font.render("Name saved successfully!", True, (255, 255, 255))
    WINDOW.blit(Background, (0, 0))
    WINDOW.blit(popup_text, (WIDTH / 2 - popup_text.get_width() / 2, HEIGHT / 2 - popup_text.get_height() / 2))
    pygame.display.update()
    time.sleep(2)
    return player_id

def game_over(player, level):
    run = True
    input_box = pygame.Rect(WIDTH / 2 - 100, HEIGHT / 2, 200, 50)
    input_box_color = (255, 255, 255)
    input_text = ""
    input_font = pygame.font.SysFont("Arial", 30)
    text_surface = input_font.render("Enter your name:", True, (255, 255, 255))

    name_saved = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text != "":
                        save_name(input_text, player.score, level)
                        name_saved = True
                        run = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        WINDOW.blit(Background, (0, 0))

        if not name_saved:
            pygame.draw.rect(WINDOW, input_box_color, input_box)
            pygame.draw.rect(WINDOW, (0, 0, 0), input_box, 2)
            input_surface = input_font.render(input_text, True, (0, 0, 0))
            input_x = input_box.x + (input_box.width - input_surface.get_width()) / 2
            input_y = input_box.y + (input_box.height - input_surface.get_height()) / 2
            WINDOW.blit(input_surface, (input_x, input_y))
            WINDOW.blit(text_surface, (WIDTH / 2 - text_surface.get_width() / 2, HEIGHT / 2 - 50))

        pygame.display.update()

    run = True
    start_time = pygame.time.get_ticks()
    while run:
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 3000:
            main_menu()
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        WINDOW.blit(Background, (0, 0))
        main_menu()
        pygame.display.update()

main_menu ()
conn.close()





