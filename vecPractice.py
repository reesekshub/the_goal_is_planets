from pygame import *
import math as m
import random


width = 1000
height = 500
screen = display.set_mode((width, height))
white = (0xff, 0xff, 0xff)
black = (0, 0, 0)
red = (0xff, 0, 0)
screen.fill(black)


def drawArrow(points: tuple, color):
    draw.aaline(screen, color, points[0], points[0]+points[1])
    arrowSize = points[1].length() * .05
    head = Surface((arrowSize, arrowSize))
    head.fill(black)
    draw.polygon(head, color, ((0, 0), (arrowSize, arrowSize/2),
                               (0, arrowSize)))
    head.set_colorkey(black)
    end = points[0] + points[1]
    angle = m.atan2(-(end.y-points[0].y), end.x-points[0].x)
    angle = m.degrees(angle)
    aroe = transform.rotate(head, angle)
    aroeRect = aroe.get_rect(center=end)
    screen.blit(aroe, aroeRect)


center = Vector2(width / 2, height / 2)
zero = Vector2(0,0)

vectors = []
pos1 = center
bound = 150
pos2 = Vector2(random.randrange(bound, width-bound),
               random.randrange(bound, height-bound))
axis = pos2-pos1
overlap = axis.length() * .5

first = True
running = True
while first and running:
    screen.fill(black)

    drawArrow((zero, pos1), white)
    drawArrow((zero, pos2), white)
    drawArrow((pos1, axis), red)


    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN and e.key == K_RIGHT:
            first = False

    display.flip()


axisN = axis.normalize()

second = True
while second and running:
    screen.fill(black)

    drawArrow((zero, pos1), white)
    drawArrow((zero, pos2), white)
    drawArrow((pos1, axis), white)
    drawArrow((pos1, axisN), red)

    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN and e.key == K_RIGHT:
            second = False

    display.flip()

radussies = pos1.length() + pos2.length()
# scaling them, to be substituted with momenta
pos1overlap = (overlap * pos1.length()) / radussies
pos2overlap = (overlap * pos2.length()) / radussies
# scaling the position to move
pos1move = pos1overlap * -axisN
pos2move = pos2overlap * axisN

third = True
while third and running:
    screen.fill(black)

    # position and axis vectors
    drawArrow((zero, pos1), white)
    drawArrow((zero, pos2), white)
    drawArrow((pos1, axis), white)
    # where they are going to move, scaled
    drawArrow((pos1, pos1move), red)
    drawArrow((pos2, pos2move), red)
    # moved positions
    drawArrow((zero, pos1 + pos1move), white)
    drawArrow((zero, pos2 + pos2move), white)

    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN and e.key == K_RIGHT:
            third = False

    display.flip()

quit()
