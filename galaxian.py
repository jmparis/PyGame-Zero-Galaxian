# Galaxian

from random import randint

import pgzrun
from pgzero.actor import Actor
from pgzero.game import screen
from pgzero.keyboard import keyboard

WIDTH  = 600
HEIGHT = 800

bullet = Actor('bullet', center=(0, -10))
ship   = Actor('ship', center=(300, 700))
backY  = count = game_over = 0
aliens = []

for a in range(0, 8):
    aliens.append(Actor('alien0', center=(200 + (a * 50), 200)))
    aliens[a].status = 0
    aliens[a].side = int(a / 4)

for a in range(0, 8):
    aliens.append(Actor('alien0', center=(200 + (a * 50), 250)))
    aliens[a + 8].status = 0
    aliens[a + 8].side = int(a / 4)


def draw():
    screen.blit("background", (0, 0))
    screen.blit("stars", (0, backY))
    screen.blit("stars", (0, backY - 800))
    bullet.draw()
    draw_aliens()
    if game_over != 1 or (game_over == 1 and count % 2 == 0):
        ship.draw()


def update():
    global backY, count
    count += 1
    if game_over == 0:
        backY += 0.2
        if backY > 800:
            backY = 0
        if bullet.y > -10:
            bullet.y -= 5
        if keyboard.left  and ship.x > 50:
            ship.x -= 4
        if keyboard.right and ship.x < 550:
            ship.x += 4
        if keyboard.space:
            if bullet.y < 0:
                bullet.pos = (ship.x, 700)
        update_aliens()


def draw_aliens():
    for alien in range(0, 16):
        if aliens[alien].status < 5:
            aliens[alien].draw()


def update_aliens():
    global game_over
    for alien in range(0, 16):
        aliens[alien].image = "alien0"
        if count % 30 < 15:
            aliens[alien].image = "alien1"
        if count % 750 < 375:
            aliens[alien].x -= 0.4
        else:
            aliens[alien].x += 0.4
        if aliens[alien].collidepoint(bullet.pos) and aliens[alien].status < 2:
            aliens[alien].status = 2
            bullet.y = -10
        if aliens[alien].colliderect(ship):
            game_over = 1
        if randint(0, 1000) == 1 and aliens[alien].status == 0:
            aliens[alien].status = 1
        if aliens[alien].status == 1:
            fly_alien(alien)
        if 1 < aliens[alien].status < 5:
            aliens[alien].image = "alien" + str(aliens[alien].status)
            aliens[alien].status += 1


def fly_alien(alien):
    if aliens[alien].side == 0:
        if aliens[alien].angle < 180:
            aliens[alien].angle += 2
            aliens[alien].x -= 1
            if aliens[alien].angle < 90:
                aliens[alien].y -= 1
        if aliens[alien].angle >= 90:
            aliens[alien].y += 2
        if aliens[alien].angle >= 180:
            aliens[alien].angle = 180
            aliens[alien].x += 1
    else:
        if aliens[alien].angle > -180:
            aliens[alien].angle -= 2
            aliens[alien].x += 1
            if aliens[alien].angle > -90:
                aliens[alien].y -= 1
        if aliens[alien].angle <= -90:
            aliens[alien].y += 2
        if aliens[alien].angle <= -180:
            aliens[alien].angle = -180
            aliens[alien].x -= 1


pgzrun.go()     # Must be last line
