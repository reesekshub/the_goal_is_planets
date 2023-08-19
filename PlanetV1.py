from pygame import *

gravity = 2


class Planet:
    def __init__(self, radius: int, mass: int, pos: Vector2, vel: Vector2, color):
        self.radius = radius
        self.mass = mass
        self.pos = math.Vector2(pos)
        self.vel = math.Vector2(vel)
        self.color = color

    def draw(self, screen):
        draw.circle(screen, self.color,
                    (self.pos.x, self.pos.y), self.radius)

  # returns rect of planet as (left coord, top coord, width, height)
    def getRect(self):
        return Rect(self.pos.x - self.radius, self.pos.y - self.radius,
                    self.radius, self.radius)

  # returns rect of planet in the NEXT frame, accounting for velocity
    def getRectFuture(self):
        return Rect(self.pos.x - self.radius + self.vel.x,
                    self.pos.y - self.radius + self.vel.y,
                    self.radius, self.radius)

  # bounces off the walls
    def updatePos(self, screen):
        s = screen.get_size()
      # gravity
        self.vel = math.Vector2(self.vel.x, self.vel.y + gravity)
      # bounce off walls
        planetRect = self.getRectFuture()  # check to update BEFORE it hits
        if planetRect.x + planetRect.width * 2 > s[0] or planetRect.x < 0:
            self.vel = math.Vector2(-self.vel.x, self.vel.y)
        if planetRect.y + planetRect.height * 2 > s[1] or planetRect.y < 0:
            self.vel = math.Vector2(self.vel.x, -(self.vel.y - gravity))
      # update position
        self.pos += self.vel


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
