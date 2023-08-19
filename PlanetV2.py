from pygame import *
import math as m

gravity = 2

font.init()

class Planet:
    def __init__(self, radius: int, mass: int, pos: Vector2, vel: Vector2, color):
        self.radius = radius
        self.mass = mass
        self.pos = math.Vector2(pos)
        self.vel = math.Vector2(vel)
        self.color = color
        self.contacted = False

    def draw(self, screen):
        if self.contacted:
            draw.circle(screen, (0, 0, 0),
                        (self.pos.x, self.pos.y), self.radius)
        else:
            draw.circle(screen, self.color,
                        (self.pos.x, self.pos.y), self.radius)
            theFont = font.SysFont('Comic Sans MS', 30)
            textSurf = theFont.render(str(self.mass), False, (0, 0, 0))
            screen.blit(textSurf, (self.pos.x, self.pos.y))

  # returns rect of planet in the NEXT frame, accounting for velocity
    def getRectFuture(self):
        return Rect(self.pos.x - self.radius + self.vel.x,
                    self.pos.y - self.radius + self.vel.y,
                    self.radius, self.radius)

    def getFuturePos(self):
        return Vector2(self.pos + self.vel)

  # bounces off the walls
    def updatePos(self):
      # update position
        self.pos += self.vel

    def doCollisions(self, planets: list, s: tuple):
        for o in planets:
            contact = False
            if self is not o:
                position = o.getFuturePos()
                dist = self.pos.distance_to(position)

                if self.willTouch(o):
                    self.fixOverlap(o, s)
                    self.collideVels(o)

    # check if they will touch in the FUTURE dammit
    def willTouch(self, other):
        dist = self.getFuturePos().distance_to(other.getFuturePos())
        return True if dist <= self.radius + other.radius else False

    # makes sure the balls aren't inside each other
    def fixOverlap(self, other, s: tuple):
        dist = self.getFuturePos() - other.getFuturePos()
        # momenta
        pself = self.vel.length() * self.mass
        pother = other.vel.length() * other.mass
        pTotal = pself + pother

        # overlaps based on momenta
        overlapDepth = self.radius + other.radius - dist.length()
        selfOverlap = (overlapDepth * pself) / pTotal
        otherOverlap = (overlapDepth * pother) / pTotal

        moveDir = dist.normalize()

        # move those balls

        selfMove = -moveDir * selfOverlap
        #self.pos += selfMove
        otherMove = moveDir * otherOverlap
        #other.pos += otherMove

        # check if either moves off the page, if so move both by the overlap distance
        futureSelf = Planet(self.radius, self.mass, self.pos + selfMove, self.vel, (0,0,0))
        futureOther = Planet(other.radius, other.mass, other.pos + otherMove, other.vel, (0,0,0))
        shiftAmt = futureSelf.correctWallBounce(s, False)
        shiftAmt += futureOther.correctWallBounce(s, False)
        self.pos -= shiftAmt
        other.pos -= shiftAmt


    # straight from https://en.wikipedia.org/wiki/Elastic_collision
    def collideVels(self, other):
        massTermSelf = (other.mass * 2) / (other.mass + self.mass)
        massTermOther = (self.mass * 2) / (other.mass + self.mass)
        distSelfToOther = self.pos - other.pos
        dotProdAndCenterSelf = Vector2(self.vel - other.vel).dot(distSelfToOther) / distSelfToOther.magnitude() ** 2
        dotProdAndCenterOther = Vector2(other.vel - other.vel).dot(-distSelfToOther) / distSelfToOther.magnitude() ** 2

        self.vel -= massTermSelf * dotProdAndCenterSelf * distSelfToOther
        other.vel -= massTermOther * dotProdAndCenterOther * (-distSelfToOther)

    def correctWallBounce(self, s: tuple, actuallyMove: bool):
        futurePos = self.getFuturePos() if actuallyMove else self.pos
        shiftAmount = Vector2(0, 0)  # corrects for too much movement because of overlap corrections

        # Right edge
        penDepth = (futurePos.x + self.radius) - s[0]
        if penDepth > 0:
            if actuallyMove:
                self.pos = Vector2(self.pos.x - penDepth, self.pos.y)
                self.vel = Vector2(-self.vel.x, self.vel.y)
            shiftAmount = Vector2(shiftAmount.x - penDepth, shiftAmount.y)

        # Left Edge
        penDepth = self.radius - futurePos.x
        if penDepth > 0:
            if actuallyMove:
                self.pos = Vector2(self.pos.x + penDepth, self.pos.y)
                self.vel = Vector2(-self.vel.x, self.vel.y)
            shiftAmount = Vector2(shiftAmount.x + penDepth, shiftAmount.y)

        # Bottom
        penDepth = (futurePos.y + self.radius) - s[1]
        if penDepth > 0:
            if actuallyMove:
                self.pos = Vector2(self.pos.x, self.pos.y - penDepth)
                self.vel = Vector2(self.vel.x, -(self.vel.y - gravity))
            shiftAmount = Vector2(shiftAmount.x, shiftAmount.y - penDepth)

        # Top
        penDepth = self.radius - futurePos.y
        if penDepth > 0:
            if actuallyMove:
                self.pos = Vector2(self.pos.x, self.pos.y + penDepth)
                self.vel = Vector2(self.vel.x, -self.vel.y)
            shiftAmount = Vector2(shiftAmount.x, shiftAmount.y + penDepth)

        self.pos -= shiftAmount
        return shiftAmount


class Trail:
    def __init__(self, location: Vector2, colour):
        self.rad = 2
        self.loc = Vector2(location.x - self.rad, location.y - self.rad)
        self.color = colour + (128,)

  # draws onto a transparent-capable surface and puts that on screen
    def drawTrail(self, screen: Surface):
        circle = Surface((self.rad*2, self.rad*2), SRCALPHA)
        draw.circle(circle, self.color, (self.rad, self.rad), self.rad)
        screen.blit(circle, self.loc)
        