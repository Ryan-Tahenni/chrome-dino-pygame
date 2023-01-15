# https://www.youtube.com/watch?v=AY9MnQ4x3zk

import pygame as pg
from time import strftime
from random import randrange
from sys import exit

currentime = strftime("%d-%m-%Y %H-%M-%S") # the current time in this format: day-month-year hour-minute-second
logfile = open(f"logs/game {currentime}.log", "x") # create a .log file named game + the current time (this will log all the major events that happened)

def score_render(): # function that increases the score, if the score is a multiple of 100, play the milestone sound
    global score, hi_score

    score = int(pg.time.get_ticks() / 100 - start)
    if hi_score < score:
        hi_score = score

    score_surf = font.render(f"HI: {hi_score}    SCORE: {score}", False, "#494949").convert_alpha()
    score_rect = score_surf.get_rect(center = (1000, 10))
    window.blit(score_surf, score_rect)

    if score % 100 == 0 and score != 0:
        logfile.write(f"log: milestone {score} points: {pg.time.get_ticks()}\n")

        pg.mixer.Sound.stop(point_milestone_sound)
        pg.mixer.Sound.play(point_milestone_sound)

def ground_move(): # function that makes a scrolling illusion
    g1_rect.x -= int(score * 0.01) + 5
    g2_rect.x -= int(score * 0.01) + 5
    if g1_rect.right <= 0:
        g1_rect.left = 2400
    if g2_rect.right <= 0:
        g2_rect.left = 2400
    window.blit(ground_surf, g1_rect)
    window.blit(ground_surf_2, g2_rect)


def cacti_render(): # function that regroups all of the three cactuses
    single_cactus()
    tri_cactus()
    small_cactus()

def single_cactus():
    global game_on

    cactus_rect.x -= int(score * 0.01) + 5

    if cactus_rect.right <= 0:
        cacback("cac")
    if dino_rect.colliderect(cactus_rect):
        
        cacback("tricac")
        cacback("cac")
        cacback("minicac")

        logfile.write(f"log: game-over-singcactus: {pg.time.get_ticks()} ms\n")
        game_on = False
    
    window.blit(cactus_surf, cactus_rect)

def tri_cactus():
    global game_on

    tricac_rect.x -= int(score * 0.01) + 5

    if tricac_rect.right <= 0:
        cacback("tricac")
    if dino_rect.colliderect(tricac_rect):

        cacback("tricac")
        cacback("cac")
        cacback("minicac")

        logfile.write(f"log: game-over-tricactus: {pg.time.get_ticks()} ms\n")
        game_on = False
    if tricac_rect.colliderect(cactus_rect):
        cacback("tricac")
    window.blit(tricac_surf, tricac_rect)

def small_cactus():
    global game_on

    smallcac_rect.x -= int(score * 0.01) + 5

    if smallcac_rect.right <= 0:
        cacback("minicac")
    if dino_rect.colliderect(smallcac_rect):

        cacback("tricac")
        cacback("cac")
        cacback("minicac")

        logfile.write(f"log: game-over-smallcactus: {pg.time.get_ticks()} ms\n")
        game_on = False
    if smallcac_rect.colliderect(cactus_rect) or smallcac_rect.colliderect(tricac_rect):
        cacback("minicac")
    
    window.blit(smallcac_surf, smallcac_rect)

def cacback(cactype: str): # function that makes the cactus go back to the right side of the screen
    if cactype == "tricac":
        tricac_rect.left = randrange(1280, 2560, 1)
    elif cactype == "cac":
        cactus_rect.left = randrange(1280, 2560, 1)
    elif cactype == "minicac":
        smallcac_rect.left = randrange(1280, 2560, 1)
    else:
        print('error, wrong type: must be "tricac", "cac" or "minicac"')


def dino(): # function that animates the dinosaur and makes it fall
    global dino_gravity, dino_surf, d_walk_index
    dino_gravity += 1
    dino_rect.y += dino_gravity
    if dino_rect.bottom >= FLOOR_GAME:
        dino_rect.bottom = FLOOR_GAME

        d_walk_index += 0.1
        dino_surf = d_walk[int(d_walk_index) % 2]
    else:
        dino_surf = dino_jump
    window.blit(dino_surf, dino_rect)

pg.init()

# title
pg.display.set_caption("Chrome Dino Game (Desktop)")

# game icon
icon = pg.image.load("ressources/img/dino.png")
pg.display.set_icon(icon)

window = pg.display.set_mode((1280, 360))

clock = pg.time.Clock()
font = pg.font.Font("ressources/font/PressStart2P.ttf", 15)
start = 0
hi_score = 0
FLOOR_GAME = 250
game_on = False

# title screen
title_surf = pg.image.load("ressources/img/titlescreen.png")

# ground
ground_surf = pg.image.load("ressources/img/ground.png").convert_alpha()
ground_surf_2 = pg.image.load("ressources/img/ground.png").convert_alpha()
g1_rect = ground_surf.get_rect(midleft = (0, FLOOR_GAME - 11))
g2_rect = ground_surf.get_rect(midleft = (2400, FLOOR_GAME - 11))

# dinosaur
dino_jump = pg.image.load("ressources/img/dino.png").convert_alpha()
d_run_1 = pg.image.load("ressources/img/dinorun1.png").convert_alpha()
d_run_2 = pg.image.load("ressources/img/dinorun2.png").convert_alpha()
d_walk = [d_run_1, d_run_2]
d_walk_index = 0
dino_gravity = 0.0
dino_surf = d_walk[d_walk_index]
dino_rect = dino_surf.get_rect(bottomright = (180, FLOOR_GAME - 150))

# single cactus
cactus_surf = pg.image.load("ressources/img/cactus.png").convert_alpha()
cactus_rect = cactus_surf.get_rect(bottomleft = (1280, FLOOR_GAME))

# tricactus
tricac_surf = pg.image.load("ressources/img/tricactus.png").convert_alpha()
tricac_rect = tricac_surf.get_rect(bottomleft = (1280*2 - 1280/2 , FLOOR_GAME))

# smallcactus
smallcac_surf = pg.image.load("ressources/img/minicactus.png").convert_alpha()
smallcac_rect = smallcac_surf.get_rect(bottomleft = (1280*2 - 1280/2 , FLOOR_GAME))

# sounds
jump_sound = pg.mixer.Sound("ressources/audio/dinojumpsound.wav")
point_milestone_sound = pg.mixer.Sound("ressources/audio/100pointsound.wav")

logfile.write(f"log: app-started: {pg.time.get_ticks()} ms\n")
while True:
    for event in pg.event.get(): # event loop
        if game_on == True:
            if event.type == pg.MOUSEBUTTONDOWN and dino_rect.bottom >= FLOOR_GAME: # if the mouse button is down, then jump
                dino_gravity = -17.5
                pg.mixer.Sound.play(jump_sound)
                logfile.write(f"log: jumped-mouse: {pg.time.get_ticks()} ms\n")
            if event.type == pg.KEYDOWN:
                if (event.key == pg.K_SPACE or event.key == pg.K_UP) and dino_rect.bottom >= FLOOR_GAME: # if the space or up arrow button is down, then jump
                    dino_gravity = -17.5
                    pg.mixer.Sound.play(jump_sound)
                    logfile.write(f"log: jumped-k_up-k_space: {pg.time.get_ticks()} ms\n")
        else:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE: # if the game is over and the user presses space, it will restart the game
                    logfile.write(f"log: game-session-started: {pg.time.get_ticks()} ms\n")
                    cactus_rect.left = 1280
                    game_on = True
                    start = int(pg.time.get_ticks()/100)
                    
        if event.type == pg.QUIT:
            logfile.write(f"log: high-score: {hi_score}\n")
            logfile.write(f"log: quit: {pg.time.get_ticks()} ms\n")
            logfile.close()
            pg.quit()
            exit()

    if game_on == True:
        window.fill("#FFFFFF")

        # Score
        score_render()

        # Ground
        ground_move()

        # Dinosaur
        dino()

        # Cactuses
        cacti_render()

    else:
        window.blit(title_surf, (0, 0)) # title screen

    pg.display.update()
    clock.tick(60)
