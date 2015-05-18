import mcpi.minecraft as minecraft
#import mcpi.block as block
from mcpi.block import *
from mcpi.entity import *
import time
from math import *
import server

class Turtle:
    def __init__(self,mc=None):
        if mc:
             self.mc = mc
        else:
             self.mc = minecraft.Minecraft.create(server.address)
        self.block = BEDROCK
        self.width = 1
        self.pen = True
        self.directionIn()
        self.pitch = 0
        self.positionIn()
        self.delayTime = 0.05
        self.nib = []
        self.turtleType = PLAYER
        self.playerId = self.mc.getPlayerId()
        self.turtleId = self.playerId

    def turtle(self,turtleType):
        if self.turtleType == turtleType:
            return
        if self.turtleType and self.turtleType != PLAYER:
            self.mc.removeEntity(self.turtleId)
        self.turtleType = turtleType
        if turtleType == PLAYER:
            self.turtleId = self.playerId
        elif turtleType:
            self.turtleId = self.mc.spawnEntity(turtleType,
                                                self.position.x,self.position.y,self.position.z,
                                                "{NoAI:1}")
        self.positionOut()
        self.directionOut()
        
    def follow(self): # deprecated
        self.turtle(PLAYER)
        
    def nofollow(self): # deprecated
        if self.turtleType == PLAYER:
            self.turtle(None)

    def penwidth(self,w):
        self.nib = []
        self.width = int(w)
        if self.width >= 0 and self.width <= 2:
            return
        r2 = self.width * self.width / 4.
        for x in range(-self.width//2 - 1,self.width//2 + 1):
            for y in range(-self.width//2 - 1, self.width//2 + 1):
                for z in range(-self.width//2 -1, self.width//2 + 1):
                    if x*x + y*y + z*z <= r2:
                        self.nib.append(minecraft.Vec3(x,y,z))
        
    def goto(self,x,y,z):
        self.position.x = x
        self.position.y = y
        self.position.z = z
        self.positionOut()
        self.delay()

    def verticalangle(self,angle):
        self.pitch = -angle
        self.directionOut()

    def angle(self,angle):
        self.rotation = -angle
        self.directionOut()
        
    def penup(self):
        self.pen = False

    def pendown(self):
        self.pen = True

    def penblock(self, block):
        self.block = block

    def positionIn(self):
        self.position = self.mc.player.getPos()

    def positionOut(self):
        if self.turtleType:
            self.mc.entity.setPos(self.turtleId,self.position)

    def delay(self):
        if self.delayTime > 0:
            time.sleep(self.delayTime)

    def directionIn(self):
        self.rotation = self.mc.player.getRotation()
        self.pitch = self.mc.player.getPitch()

    def directionOut(self):
        self.pitch %= 360.
        self.rotation %= 360

        if self.turtleType:
            pitch = self.pitch
            rotation = self.rotation

            if pitch >= 270:
                pitch = pitch - 360.
            elif pitch >= 90:
                pitch = 180. - pitch
                rotation = (rotation + 180.) % 360.

            self.mc.entity.setRotation(self.turtleId, rotation)
            self.mc.entity.setPitch(self.turtleId, pitch)

    def pendelay(self, t):
        self.delayTime = t

    def left(self, angle):
        self.right(-angle)

    def right(self, angle):
        self.rotation += angle
        self.directionOut()
        self.delay()

    def up(self, angle):
        self.pitch -= angle
        self.directionOut()
        self.delay()

    def down(self, angle):
        self.up(-angle)

    def go(self, distance):
        pitch = self.pitch * pi/180.
        rot = self.rotation * pi/180.
        dx = cos(-pitch) * sin(-rot)
        dy = sin(-pitch)
        dz = cos(-pitch) * cos(-rot)
        newX = self.position.x + dx * distance
        newY = self.position.y + dy * distance
        newZ = self.position.z + dz * distance
        self.drawLine(self.position.x, self.position.y, self.position.z,
                        newX, newY, newZ)
        self.position.x = newX
        self.position.y = newY
        self.position.z = newZ
        self.positionOut()
        self.delay()

    def back(self, distance):
        pitch = self.pitch * pi/180.
        rot = self.rotation * pi/180.
        dx = - cos(-pitch) * sin(-rot)
        dy = - sin(-pitch)
        dz = - cos(-pitch) * cos(-rot)
        newX = self.position.x + dx * distance
        newY = self.position.y + dy * distance
        newZ = self.position.z + dz * distance
        self.drawLine(self.position.x, self.position.y, self.position.z,
                        newX, newY, newZ)
        self.position.x = newX
        self.position.y = newY
        self.position.z = newZ
        self.positionOut()
        self.delay()

    def drawPoint(self, x, y, z):
        if self.pen and self.width > 0:
            if self.width == 1:
                self.mc.setBlock(x,y,z,self.block)
            elif self.width == 2:
                self.mc.setBlocks(x-1,y,z-1,x,y+1,z,self.block)
            else:
                for point in self.nib:
                    self.mc.setBlock(x+point.x,y+point.y,z+point.z,self.block)
        if self.delayTime > 0:
            self.position.x = x
            self.position.y = y
            self.position.z = z
            self.positionOut()
            self.delay()

    def drawLine(self, x1, y1, z1, x2, y2, z2):
        if not self.pen and self.delayTime == 0:
            return
        x1 = int(x1)
        y1 = int(y1)
        z1 = int(z1)
        x2 = int(x2)
        y2 = int(y2)
        z2 = int(z2)
        point = [x1,y1,z1]
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        x_inc = -1 if dx < 0 else 1
        l = abs(dx)
        y_inc = -1 if dy < 0 else 1
        m = abs(dy)
        z_inc = -1 if dz < 0 else 1
        n = abs(dz)
        dx2 = l << 1
        dy2 = m << 1
        dz2 = n << 1
    
        if l >= m and l >= n:
            err_1 = dy2 - l
            err_2 = dz2 - l
            for i in range(0,l-1):
                self.drawPoint(point[0], point[1], point[2])
                if err_1 > 0:
                    point[1] += y_inc
                    err_1 -= dx2
                if err_2 > 0:
                    point[2] += z_inc
                    err_2 -= dx2
                err_1 += dy2
                err_2 += dz2
                point[0] += x_inc
        elif m >= l and m >= n:
            err_1 = dx2 - m;
            err_2 = dz2 - m;
            for i in range(0,m-1):
                self.drawPoint(point[0], point[1], point[2])
                if err_1 > 0:
                    point[0] += x_inc
                    err_1 -= dy2
                if err_2 > 0:
                    point[2] += z_inc
                    err_2 -= dy2
                err_1 += dx2
                err_2 += dz2
                point[1] += y_inc
        else:
            err_1 = dy2 - n;
            err_2 = dx2 - n;
            for i in range(0, n-1):
                self.drawPoint(point[0], point[1], point[2])
                if err_1 > 0:
                    point[1] += y_inc
                    err_1 -= dz2
                if err_2 > 0:
                    point[0] += x_inc
                    err_2 -= dz2
                err_1 += dy2
                err_2 += dx2
                point[2] += z_inc
        self.drawPoint(point[0], point[1], point[2])
    

if __name__ == "__main__":
    t = Turtle()
    t.pendelay(0.01)
    t.penwidth(1)
    t.penblock(GLASS)
    t.turtle(HORSE)
    for i in range(7):
        print i
        t.go(100)
        t.right(180.0-180./7)
    t.penup()
    t.turtle(None)