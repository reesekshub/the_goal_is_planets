import math as m
from pygame import *
import pygame.freetype as fr
from random import *
import PlanetV2

# constants
windowScale = 60
scWidth = 16 * windowScale
scHeight = 9 * windowScale
white = (0xff, 0xff, 0xff)
purple = (0xA0, 0x20, 0xf0)
blue = (0, 0, 0xff)
red = (0xff, 0, 0)
yellow = (0xff, 0xff, 0)
black = (0, 0, 0)

# window setup stuff
screen = display.set_mode((scWidth, scHeight))
screen.fill(white)
display.set_caption("Planets Second Try With Collision??!?!?")
paused = False

# initialize planets (radius, mass, pos, vel, color)
planets = []
purp = PlanetV2.Planet(35, 30, math.Vector2(300, 400), math.Vector2(9, 8), purple)
planets.append(purp)
baloo = PlanetV2.Planet(randint(30,60), 30, math.Vector2(randint(110,scWidth-110),
                                randint(110,scHeight-110)), math.Vector2(8, 9), blue)
planets.append(baloo)
# hi = PlanetV2.Planet(randint(30,60), 30, math.Vector2(randint(110,scWidth-110),
#                                 randint(110,scHeight-110)), math.Vector2(5, 9), red)
# planets.append(hi)
# hii = PlanetV2.Planet(randint(30,60), 30, math.Vector2(randint(110,scWidth-110),
#                                 randint(110,scHeight-110)), math.Vector2(11, 9), yellow)
# planets.append(hii)
for p in planets:
    p.draw(screen)

# initialize trails
trails = []
removeFactor = 3
gravity = 2

display.flip()

# animation loop
clock = time.Clock()
running = True
while running:
    screen = display.set_mode((scWidth, scHeight))
    # framerate and background
    clock.tick(60)
    screen.fill(white)

  # kill the trails whose alphas are 0 and update ages via alpha val
    for t in trails:
        if not paused:
            t.color = (t.color[0], t.color[1], t.color[2], t.color[3] - removeFactor)
            if t.color[3] <= removeFactor-1:
                trails.remove(t)
        t.drawTrail(screen)

  # update positions and draw Planets
    for index, p in enumerate(planets):
        if not paused:
            p.vel = Vector2(p.vel.x, p.vel.y + gravity)
            trails.append(PlanetV2.Trail(p.pos, p.color))
            #p.doCollisions(planets[index+1:], screen.get_size())
            p.doCollisions(planets, screen.get_size())
            p.correctWallBounce(screen.get_size(), True)
            p.updatePos()

        p.draw(screen)

  # processing user input
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            paused = not paused
        if e.type == KEYDOWN:
            if e.key == K_UP:
                windowScale += 1
            if e.key == K_DOWN:
                windowScale -= 1
    scWidth = 16 * windowScale
    scHeight = 9 * windowScale

    display.flip()

quit()
