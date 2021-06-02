'''
Created on May 14, 2021

@author: Sam Hecht
'''


import pygame
import random
import os


pygame.font.init()
pygame.mixer.init()

from Asteroids import player
from Asteroids import asteroid
from Asteroids import alien



BEAT_1 = pygame.mixer.Sound(os.path.join('Sound Effects', 'beat1.wav'))
BEAT_2 = pygame.mixer.Sound(os.path.join('Sound Effects', 'beat2.wav'))



FPS = 60

WIDTH,HEIGHT = 800,800
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")



BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

PADDING = 10

scoreboard = []
names = []
win_message = ""

FONT = pygame.font.Font(pygame.font.get_default_font(), 20)
FONT_BIG = pygame.font.Font(pygame.font.get_default_font(), 40)

def draw_window(count, players, asteroids, aliens, breaking_objects, are_teammates):
    WINDOW.fill(BLACK)
    for p in players:
        draw_extra_lives(p)
        WINDOW.blit(p.score_text, (WIDTH - p.score_text.get_width() - PADDING, max(p.player_number - 1, 0) * p.score_text.get_height() + PADDING))
        
    #draw_player(count, player_2, WHITE)
        if not p.is_losing_life and not p.is_hyperspacing:
            draw_player(count, p)
        else:
            draw_breaking_animation(p, p.respawn_timer)
        draw_bullets(p)
        
    if are_teammates and len(players) == 2:
        combined_score = FONT.render(str(players[0].score + players[1].score), 1, WHITE)
        WINDOW.blit(combined_score, (400 - p.score_text.get_width()/2, PADDING))
        
        
    draw_asteroids(asteroids)
    draw_aliens(aliens)
    
    
    draw_breaking_objects_animation(breaking_objects) 
    pygame.display.update()
        
        
def draw_extra_lives(player_x):
    for i in range(player_x.lives):
        extra_live_player = player.Player(30 + 27*i, -10 + 40 * max(player_x.player_number,1), player_x.player_number)
        pygame.draw.line(WINDOW, player_x.COLOR, extra_live_player.points[0], extra_live_player.points[1], 2)
        pygame.draw.line(WINDOW, player_x.COLOR, extra_live_player.points[1], extra_live_player.points[2], 2)
        pygame.draw.line(WINDOW, player_x.COLOR, extra_live_player.points[3], extra_live_player.points[4], 2)

def draw_player(count, player):
    pygame.draw.line(WINDOW, player.COLOR, player.points[0], player.points[1], 3)
    pygame.draw.line(WINDOW, player.COLOR, player.points[1], player.points[2], 3)
    pygame.draw.line(WINDOW, player.COLOR, player.points[3], player.points[4], 3)
    if player.flash and count % 4 == 1:
        pygame.draw.polygon(WINDOW, player.COLOR, player.points[5:], 3)
        
def draw_bullets(player):
    for bullet in player.bullets:
        bullet.bounds = pygame.draw.circle(WINDOW, player.COLOR, (bullet.x, bullet.y), bullet.RADIUS)
        


def draw_asteroids(asteroids):
    for aster in asteroids:
        aster.bounds = pygame.draw.polygon(WINDOW, WHITE, aster.points, 3)
    
    
def check_player_v_player_collisions(players, are_teammates):
    
    for bullet in players[0].bullets:
        if bullet.bounds.colliderect(players[1].bounds) and not players[1].is_losing_life:
            players[1].start_breaking_animation()
            players[0].bullets.remove(bullet)
            players[0].update_score(0, None, True)
            break
    for bullet in players[1].bullets:
        if bullet.bounds.colliderect(players[0].bounds) and not players[0].is_losing_life:
            players[0].start_breaking_animation()
            players[1].bullets.remove(bullet)
            players[1].update_score(0, None, True)
            break
    if players[0].bounds.colliderect(players[1].bounds) and not players[0].is_losing_life and not players[1].is_losing_life:
        for p in players:
            p.start_breaking_animation()
            p.update_score(0, None, True)        
    
        

def check_collisions(p, asteroids, aliens, breaking_objects):
    p.reset_bounds()
    #pygame.draw.rect(WINDOW, GREEN, p.bounds)
        
    for aster in asteroids:
        if p.bounds.colliderect(aster.bounds):
            breaking_objects.append(aster)
            aster.split_asteroid(asteroids, p)
            p.start_breaking_animation()
            continue
            
        for bullet in p.bullets:
            if bullet.bounds.colliderect(aster.bounds):
                breaking_objects.append(aster)
                aster.split_asteroid(asteroids, p)
                p.bullets.remove(bullet)
                break
            
        for ufo in aliens:
            if ufo.bounds.colliderect(aster.bounds):
                breaking_objects.append(aster)
                aster.split_asteroid(asteroids)
                breaking_objects.append(ufo)
                ufo.break_ufo(aliens)
                break
            for bullet in ufo.bullets:
                if bullet.bounds.colliderect(aster.bounds):
                    breaking_objects.append(aster)
                    aster.split_asteroid(asteroids)
                    ufo.bullets.remove(bullet)
                    break
            
               
    
    for ufo in aliens:
        if p.bounds.colliderect(ufo.bounds):
            breaking_objects.append(ufo)
            ufo.break_ufo(aliens, p)
            p.start_breaking_animation()
            break
        for bullet in p.bullets:
            if bullet.bounds.colliderect(ufo.bounds):
                breaking_objects.append(ufo)
                ufo.break_ufo(aliens, p)
                p.bullets.remove(bullet)
                break
        for bullet in ufo.bullets:
            if bullet.bounds.colliderect(p.bounds):
                p.start_breaking_animation()
                ufo.bullets.remove(bullet)
                break
    
    
    
    
def draw_game_over_text(p):
    game_over_text = FONT.render("Game Over! Score: " + str(p.score), 1, WHITE)
    WINDOW.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2, HEIGHT/2 - game_over_text.get_height()/2))
    pygame.display.update()
    


def draw_breaking_animation(p, breaking_timer):
    p.move_lines()
    for l in p.lines:
        if l.duration > breaking_timer:
            pygame.draw.line(WINDOW, p.COLOR, l.p1, l.p2, 2)
        else:
            p.lines.remove(l)
        

def draw_aliens(aliens):
    for ufo in aliens:
        ufo.bounds = pygame.draw.polygon(WINDOW, WHITE, ufo.points[:10], 2)
        pygame.draw.line(WINDOW, WHITE, ufo.points[10], ufo.points[11], 2)
        for bullet in ufo.bullets:
            bullet.bounds = pygame.draw.circle(WINDOW, WHITE, (bullet.x, bullet.y), bullet.RADIUS)
            
            
def draw_breaking_objects_animation(breaking_objects):
    for obj in breaking_objects:
        obj.handle_breaking_animation()
        for dot in obj.dots:
            pygame.draw.circle(WINDOW, WHITE, ((dot.x, dot.y)), dot.RADIUS)
        if len(obj.dots) == 0:
            breaking_objects.remove(obj)

def handle_sound(count, played_beat_1, old_whole_number) -> (bool, int):
 
    FREQUENCY = max(30, 71 - (count/(FPS*3)))
    
    if count // FREQUENCY > old_whole_number and played_beat_1:
        old_whole_number += 1
        BEAT_2.play()
        return (False, old_whole_number)
    elif count // FREQUENCY > old_whole_number and not played_beat_1:
        old_whole_number += 1
        BEAT_1.play()
        return (True, old_whole_number)
    return (played_beat_1, old_whole_number)

def main(are_two_players, are_aliens, are_asteroids, are_teammates):
    global win_message
    players = []
    win_message = ""
    if not are_two_players:
        players.append(player.Player(WIDTH/2, HEIGHT/2 + 5, 0))
    else:
        players.append(player.Player(WIDTH/2 + 150, HEIGHT/2 + 5, 1))
        players.append(player.Player(WIDTH/2 - 150, HEIGHT/2 + 5, 2))
    asteroids = []
    aliens = []
    breaking_objects = []
    wave = 0
    
    clock = pygame.time.Clock()
    run = True
    count = 0
    
    wave_timer = 60
    
    played_beat_1 = False
    old_whole_number = -1
    
    while run:
        if len(asteroids) == 0 and len(aliens) == 0 and are_asteroids and wave_timer == 0:
            wave_timer += 1
        elif wave_timer != 0 and wave_timer < FPS:
            wave_timer += 1
        elif len(asteroids) == 0 and len(aliens) == 0 and are_asteroids and wave_timer == FPS:
            wave_timer = 0
            count = 0
            old_whole_number = -1
            played_beat_1 = False
            if (not are_two_players and players[0].score <= 50000) or are_two_players and players[0].score + players[1].score <= 50000:
                wave += 1
            for _ in range(wave + 3):
                potential_asteroid = asteroid.Asteroid()
                while players[0].get_double_bounds().colliderect(potential_asteroid.bounds) or (are_two_players and players[1].get_double_bounds().colliderect(potential_asteroid.bounds)):
                    potential_asteroid = asteroid.Asteroid()
                asteroids.append(potential_asteroid)
        elif not are_asteroids and len(aliens) == 0 and are_aliens and wave_timer == FPS:
            count = 0
            old_whole_number = -1
            played_beat_1 = False
            aliens.append(alien.Alien((are_two_players and ((players[0].score + players[1].score)//40000 > 0)) or players[0].score//40000 > 0))
        count+=1
        #count = count % 4
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if not are_two_players:
                    if event.key == pygame.K_SPACE and not players[0].is_losing_life:
                        players[0].add_bullet()
                    if event.key == pygame.K_r:
                        run = False
                        main(are_two_players, are_aliens, are_asteroids, are_teammates)
                    if event.key == pygame.K_l:
                        players[0].lives += 1
                    if event.key == pygame.K_s:
                        players[0].score += 10000
                    if event.key == pygame.K_z and players[0].hyperspace_timer == 0 and players[0].respawn_timer == 0:
                        players[0].hyperspace()
                        players[0].hyperspace_timer += 1
                else:
                    if event.key == pygame.K_y:
                        players[0].score += 10000
                    if event.key == pygame.K_PERIOD and not players[0].is_losing_life:
                        players[0].add_bullet()    
                    if event.key == pygame.K_BACKQUOTE and not players[1].is_losing_life:
                        players[1].add_bullet()
                    if event.key == pygame.K_COMMA and players[0].hyperspace_timer == 0 and players[0].respawn_timer == 0:
                        players[0].hyperspace()
                        players[0].hyperspace_timer += 1  
                    if event.key == pygame.K_1 and players[1].hyperspace_timer == 0 and players[1].respawn_timer == 0:
                        players[1].hyperspace()
                        players[1].hyperspace_timer += 1 
                
        for aster in asteroids:
            aster.handle_movement()
        for ufo in aliens:
            ufo.handle_movement(aliens)
            if are_two_players:
                ufo.handle_bullets(players[int(random.random() * 2)])
            else:
                ufo.handle_bullets(players[0])
        for p in players:
            if not p.is_losing_life and not p.is_hyperspacing:
                keys_pressed = pygame.key.get_pressed()
                p.handle_movement(keys_pressed)
                check_collisions(p, asteroids, aliens, breaking_objects)
                if p.player_number <= 1 and not are_teammates and are_two_players:
                    check_player_v_player_collisions(players, are_teammates)
            elif p.hyperspace_timer >= 30:
                p.hyperspace_timer = 0
                p.is_hyperspacing = False
            elif p.hyperspace_timer >= 1:
                p.hyperspace_timer += 1
            elif p.respawn_timer <= 60:
                p.respawn_timer += 1       
            else:
                offset = 150 * p.player_number if p.player_number <= 1 else -150
                dont_respawn = False
                for aster in asteroids:
                    
                    if player.Player(WIDTH/2 + offset, HEIGHT/2 + 5, p.player_number).get_double_bounds().colliderect(aster.bounds):
                        dont_respawn = True
                        break
                for ufo in aliens:
                    if player.Player(WIDTH/2 + offset, HEIGHT/2 + 5, p.player_number).get_double_bounds().colliderect(ufo.bounds):
                        dont_respawn = True
                        break
                if are_two_players:
                    other_index = 0 if players.index(p) == 1 else 1
                    for bullet in players[other_index].bullets:
                        if player.Player(WIDTH/2 + offset, HEIGHT/2 + 5, p.player_number).get_double_bounds().colliderect(bullet.bounds):
                            dont_respawn = True
                            break

                if not dont_respawn:
                    p.respawn_timer = 0
                    player_out_of_lives = p.lose_life(offset)
                    if (player_out_of_lives and not are_two_players) or (player_out_of_lives and are_two_players and players[other_index].lives == 0) or (player_out_of_lives and are_two_players and not are_teammates and not are_aliens and not are_asteroids):
                        run = False
                        if (are_teammates and are_two_players) or not are_two_players:
                            score = players[0].score if not are_two_players else players[0].score + players[1].score
                            index = 0
                            while index < len(scoreboard) and int(scoreboard[index][3:]) > score:
                                index += 1
                            aliens_num = 1 if are_aliens else 0
                            asteroids_num = 1 if are_asteroids else 0
                            scoreboard.insert(index, str(p.player_number) + str(aliens_num) + str(asteroids_num) + str(score))
                            if len(scoreboard) > 10:
                                scoreboard.pop(10)
                            run = False
                            high_score_name_writer(index)
                        else:
                            died_second_index = players.index(p)
                            died_first_index = 0 if died_second_index == 1 else 1
                            win_message = str(players[died_second_index].player_number) + str(players[died_second_index].score) if players[died_second_index].score >= players[died_first_index].score else str(players[died_first_index].player_number) + str(players[died_first_index].score)
                            run = False
                        gamemode_selector()
                    
        if are_aliens and count >= (21-wave) * 60 and random.random() * (997 + wave + count//(1200)) > 998 and len(aliens) < 2 and len(asteroids) > 0:
        #if count == 1:  
            aliens.append(alien.Alien((are_two_players and ((players[0].score + players[1].score)//40000 > 0)) or players[0].score//40000 > 0))
        
       # player_2.handle_movement(keys_pressed) 
        for p in players:
            p.handle_bullets()
        
        handle_sound_return = handle_sound(count + wave, played_beat_1, old_whole_number)
        played_beat_1 =  handle_sound_return[0]
        old_whole_number = handle_sound_return[1]
        #p.handle_thrust_timer()
       # player_2.handle_bullets()
        draw_window(count, players, asteroids, aliens, breaking_objects, are_teammates)
        
        
def high_score_name_writer(index):
    clock = pygame.time.Clock()
    run = True
    name = ""
    ENTER_NAME_TEXT = FONT_BIG.render("ENTER NAME:", 1, WHITE)
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                gamemode_selector()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    names.insert(index, name)
                    run = False
                    gamemode_selector()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 8:
                    name += event.unicode
        
        name_text = FONT_BIG.render(name, 1, WHITE)
        
        WINDOW.fill(BLACK)
        WINDOW.blit(ENTER_NAME_TEXT, (400 - ENTER_NAME_TEXT.get_width()/2, 300 - ENTER_NAME_TEXT.get_height()/2))

        WINDOW.blit(name_text, (400 - name_text.get_width()/2, 400 - name_text.get_height()/2))
        pygame.display.update()
        

def gamemode_selector():
    clock = pygame.time.Clock()
    run = True
    two_player_checkbox_fill = 1
    asteroids_checkbox_fill = 0
    aliens_checkbox_fill = 0
    teammates_checkbox_fill = 1
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if TWO_PLAYER_CHECKBOX.collidepoint(position):
                    two_player_checkbox_fill = 0 if two_player_checkbox_fill == 1 else 1
                elif ASTEROIDS_CHECKBOX.collidepoint(position):
                    asteroids_checkbox_fill = 0 if asteroids_checkbox_fill == 1 else 1
                elif ALIENS_CHECKBOX.collidepoint(position):
                    aliens_checkbox_fill = 0 if aliens_checkbox_fill == 1 else 1
                elif TEAMMATES_CHECKBOX.collidepoint(position):
                    teammates_checkbox_fill = 0 if teammates_checkbox_fill == 1 else 1
                elif START_RECT.collidepoint(position):
                    run = False
                elif SCOREBOARD_RECT.collidepoint(position) and len(scoreboard) > 0:
                    run = False
                    display_scoreboard()

        
        draw_gamemode_selection_screen(two_player_checkbox_fill, aliens_checkbox_fill, asteroids_checkbox_fill, teammates_checkbox_fill)
    if (two_player_checkbox_fill == 0 and teammates_checkbox_fill == 1) or aliens_checkbox_fill == 0 or asteroids_checkbox_fill == 0:
        main(two_player_checkbox_fill == 0, aliens_checkbox_fill == 0, asteroids_checkbox_fill == 0, teammates_checkbox_fill == 0)
    else:
        gamemode_selector()

START_TEXT = FONT_BIG.render("START", 1, WHITE)
X_OFFSET = 10
Y_OFFSET = 12
START_RECT = pygame.Rect(400 - START_TEXT.get_width()/2 - X_OFFSET, 650 - START_TEXT.get_height()/2 - X_OFFSET, START_TEXT.get_width() + 2*X_OFFSET, START_TEXT.get_height() + 2*X_OFFSET)

CHECKBOX_OFFSET = 20
TWO_PLAYER_TEXT = FONT_BIG.render("Two Player?", 1, WHITE)
TWO_PLAYER_CHECKBOX = pygame.Rect(400 + TWO_PLAYER_TEXT.get_width()/2 + CHECKBOX_OFFSET - TWO_PLAYER_TEXT.get_height()/2, 350 - TWO_PLAYER_TEXT.get_height()/2, TWO_PLAYER_TEXT.get_height(), TWO_PLAYER_TEXT.get_height())

ASTEROIDS_TEXT = FONT_BIG.render("Asteroids?", 1, WHITE)
ASTEROIDS_CHECKBOX = pygame.Rect(400 + ASTEROIDS_TEXT.get_width()/2 + CHECKBOX_OFFSET - ASTEROIDS_TEXT.get_height()/2, 200 - ASTEROIDS_TEXT.get_height()/2, ASTEROIDS_TEXT.get_height(), ASTEROIDS_TEXT.get_height())

ALIENS_TEXT = FONT_BIG.render("Aliens?", 1, WHITE)
ALIENS_CHECKBOX = pygame.Rect(400 + ALIENS_TEXT.get_width()/2 + CHECKBOX_OFFSET - ALIENS_TEXT.get_height()/2, 50 - ALIENS_TEXT.get_height()/2, ALIENS_TEXT.get_height(), ALIENS_TEXT.get_height())

TEAMMATES_TEXT = FONT_BIG.render("Teammates?", 1, WHITE)
TEAMMATES_CHECKBOX = pygame.Rect(400 + TEAMMATES_TEXT.get_width()/2 + CHECKBOX_OFFSET - TEAMMATES_TEXT.get_height()/2, 500 - TEAMMATES_TEXT.get_height()/2, TEAMMATES_TEXT.get_height(), TEAMMATES_TEXT.get_height())

SCOREBOARD_TEXT = FONT_BIG.render("SCOREBOARD", 1, WHITE)
SCOREBOARD_RECT = pygame.Rect(400 - SCOREBOARD_TEXT.get_width()/2 - X_OFFSET, 750 - SCOREBOARD_TEXT.get_height()/2 - X_OFFSET, SCOREBOARD_TEXT.get_width() + 2*X_OFFSET, SCOREBOARD_TEXT.get_height() + 2*X_OFFSET)


def draw_gamemode_selection_screen(two_player_checkbox_fill, aliens_checkbox_fill, asteroids_checkbox_fill, teammates_checkbox_fill):
    WINDOW.fill(BLACK)
    
    WINDOW.blit(START_TEXT, (START_RECT.x + X_OFFSET, START_RECT.y + Y_OFFSET))
    pygame.draw.rect(WINDOW, WHITE, START_RECT, 1, 20)
    
    
    WINDOW.blit(TWO_PLAYER_TEXT, (400 - TWO_PLAYER_TEXT.get_width()/2 - TWO_PLAYER_TEXT.get_height()/2, 350 - TWO_PLAYER_TEXT.get_height()/2))
    pygame.draw.rect(WINDOW, WHITE, TWO_PLAYER_CHECKBOX, two_player_checkbox_fill, 5)
    
    WINDOW.blit(ASTEROIDS_TEXT, (400 - ASTEROIDS_TEXT.get_width()/2 - ASTEROIDS_TEXT.get_height()/2, 200 - ASTEROIDS_TEXT.get_height()/2))
    pygame.draw.rect(WINDOW, WHITE, ASTEROIDS_CHECKBOX, asteroids_checkbox_fill, 5)
    
    WINDOW.blit(ALIENS_TEXT, (400 - ALIENS_TEXT.get_width()/2 - ALIENS_TEXT.get_height()/2, 50 - ALIENS_TEXT.get_height()/2))
    pygame.draw.rect(WINDOW, WHITE, ALIENS_CHECKBOX, aliens_checkbox_fill, 5)

    if two_player_checkbox_fill == 0:
        WINDOW.blit(TEAMMATES_TEXT, (400 - TEAMMATES_TEXT.get_width()/2 - TEAMMATES_TEXT.get_height()/2, 500 - TEAMMATES_TEXT.get_height()/2))
        pygame.draw.rect(WINDOW, WHITE, TEAMMATES_CHECKBOX, teammates_checkbox_fill, 5)
    
    
    
    if len(scoreboard) > 0:
        WINDOW.blit(SCOREBOARD_TEXT, (400 - SCOREBOARD_TEXT.get_width()/2, 750 - SCOREBOARD_TEXT.get_height()/2 - X_OFFSET + Y_OFFSET))
        pygame.draw.rect(WINDOW, WHITE, SCOREBOARD_RECT, 1, 20)
    
    if win_message != "":
        COLOR = BLUE if int(win_message[0]) == 1 else RED
        WINNER_TEXT = FONT_BIG.render("WINS WITH A SCORE OF: " + str(win_message[1:]), 1, COLOR)
        WINDOW.blit(WINNER_TEXT, (400 - WINNER_TEXT.get_width()/2, 575 - WINNER_TEXT.get_height()/2))
        winning_player = player.Player(400 - WINNER_TEXT.get_width()/2 - 30, 568, int(win_message[0]))
        draw_player(0, winning_player)
        
        
    pygame.display.update()
    
    
BACK_TEXT = FONT_BIG.render("BACK", 1, WHITE)
BACK_RECT = pygame.Rect(400 - BACK_TEXT.get_width()/2 - X_OFFSET, 750 - BACK_TEXT.get_height()/2 - X_OFFSET, BACK_TEXT.get_width() + 2*X_OFFSET, BACK_TEXT.get_height() + 2*X_OFFSET)

def display_scoreboard():
    clock = pygame.time.Clock()
    run = True
    WINDOW.fill(BLACK)    
    x_offset = 20
    y_offset = 10
    num = int(random.random() * 8)
    

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                if BACK_RECT.collidepoint(position):   
                    run = False
                    gamemode_selector()
                
        for i in range(len(scoreboard)):
            rendered_scoreboard_text = FONT_BIG.render(str(i + 1) + ")  " + str(names[i]) + "  -  Score: " + str(scoreboard[i][3:]), 1, WHITE)
            WINDOW.blit(rendered_scoreboard_text, (25, 50 + i * 60))
            increment = 0
            if scoreboard[i][0] == "0":
                draw_player(0, player.Player(25 + rendered_scoreboard_text.get_width() + x_offset + increment, 50 + i*60 + y_offset, 0))
                increment += 45
            else:
                draw_player(0, player.Player(25 + rendered_scoreboard_text.get_width() + x_offset + increment, 50 + i*60 + y_offset, 1))
                increment += 30
                draw_player(0, player.Player(25 + rendered_scoreboard_text.get_width() + x_offset + increment, 50 + i*60 + y_offset, 2))
                increment += 45
            if scoreboard[i][1] == "1":
                points = []
                for point in alien.Alien.ALIEN_POINTS:
                    points.append((-point[0] + 25 + rendered_scoreboard_text.get_width() + x_offset + increment, -point[1] + 50 + i*60 + 15))
                
                pygame.draw.polygon(WINDOW, WHITE, points[:10], 2)
                pygame.draw.line(WINDOW, WHITE, points[10], points[11], 2)
                increment += 40
            if scoreboard[i][2] == "1":
                points = []
                
                for point in asteroid.Asteroid.ASTEROIDS[num]:
                    points.append((point[0] * 2 + 25 + rendered_scoreboard_text.get_width() + x_offset + increment, -point[1] * 2 + 50 + i*60 + 15))
                    
                
                pygame.draw.polygon(WINDOW, WHITE, points, 3)
    
        WINDOW.blit(BACK_TEXT, (400 - BACK_TEXT.get_width()/2, 750 - BACK_TEXT.get_height()/2 - X_OFFSET + Y_OFFSET))
        pygame.draw.rect(WINDOW, WHITE, BACK_RECT, 1, 20)
        
        pygame.display.update()
if __name__ == "__main__":
    gamemode_selector()
    
    
    
    
    
    