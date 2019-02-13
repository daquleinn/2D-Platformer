# initialisation ---------------------------------------------------
import pygame
import time

# settings file read ------------------------------
config = open("Settings.txt", "r")
settings = config.read().split("z")
config.close()

res = settings[0].split("x")
resolution = []
for nums in res:
    resolution.append(int(nums))

# detect actual monitor size
display = pygame.display.set_mode((0, 0))
infoObject = pygame.display.Info()
monitorResolution = [infoObject.current_w, infoObject.current_h]
# print(monitorResolution)

gameDisplay = pygame.display.set_mode(resolution,16)

if settings[2] == "1":
    pygame.display.toggle_fullscreen()

# pygame.font.init()
pygame.init()

# colour definitions -----------------------------------------------
white = (240, 240, 240)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (80, 80, 80)

# initilization ------------------------------------------------------
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# variables --------------------------------------------------------

jumpTics = 0
#size = [int(resolution[0] / 24.7), int(resolution[1] / 9.36)]
scale = int(resolution[0] / 24.7)
speed = scale/5
jumpHeight = 1.15*speed
print(speed, jumpHeight)
global gameOver
gameOver = False


class sprite():
    registry = []

    def __init__(self, x, y, size, sType, colour):
        for n in range(2):
            size[n]=float(size[n])*scale          
        self.registry.append(self)
        self.x = x*scale
        self.y = y*scale
        self.size = size
        self.sType = sType
        self.colour = colour
        if self.sType != "Map":
            self.vx = 0
            self.vy = 0
            self.timeLeave = 0
            self.onGround = False
            if self.sType == "Player":
                self.health = 100
                self.iTime = 0
                    
    def up(self, jumpTics):
        if player.onGround == True:
            self.timeLeave = pygame.time.get_ticks()  # current time
            self.vy = - jumpHeight
        self.onGround = False
        return

    def left(self):
        self.vx = -speed
        return

    def right(self):
        self.vx = speed
        return

    def damage(self):
        if self.sType != "Player":
            print("Type Error")
        else:
            if self.health > 10:
                if pygame.time.get_ticks() > self.iTime:
                    self.health -= 10
                    self.iTime = pygame.time.get_ticks()+150
            else:
                self.health = 0
                global gameOver
                gameOver = True

                
    def kill(self):
        del self


#sprites --------------------------------------------------------------------------------

# spriteName = sprite(x, y, [width, height], type, colour)

player = sprite(3, 9, [1, 1.6], "Player", blue)
map1 = sprite(-100, ((resolution[1] - resolution[1] /48)/scale), [1000, resolution[1] / 40], "Map", black)
map2 = sprite(6, 9, [1.5, 0.5], "Map", black)
map3 = sprite(2, 7, [2,1.5], "Map", black)
map4 = sprite(11,3, [1,8], "Map", black)
map5 = sprite(-15,-5,[1,20], "Map",black)
spike1 = sprite(11.5,13.5,[19.3,0.6],"EnemyS",red)
map6 = sprite(15,3, [1,8], "Map", black)
map7 = sprite(25,3, [1,8], "Map", black)
map8 = sprite(30,3, [1,11], "Map", black)
map9 = sprite(35,8, [7,1], "Map", black)


def gameEnd(score):
    print("GAME OVER")
    print("SCORE: "+str(score))
    time.sleep(0.5)
    end()

def end():
    pygame.quit()
    pygame.joystick.quit()
    quit()


# collision detection --------------------------------------------------------
def spriteColide():
    cols = []
    for n in range(len(sprite.registry)):
        for m in range(len(sprite.registry)):
            if n != m:
                if sprite.registry[n].x + sprite.registry[n].size[0] >= sprite.registry[m].x and \
                   sprite.registry[n].x <= sprite.registry[m].x + sprite.registry[m].size[0] and \
                   sprite.registry[n].y + sprite.registry[n].size[1] >= sprite.registry[m].y and \
                   sprite.registry[n].y <= sprite.registry[m].y + sprite.registry[m].size[1]:
                    col = n, m
                    cols.append(col)
    # print(cols)
    return cols

while gameOver == False:
    
    keys = pygame.key.get_pressed()
    if keys[119] or keys[32]:
        jumpTics += 1
        player.up(jumpTics)
    else:
        jumpTics = 0
    if keys[97]:
        player.left()
    if keys[100]:
        player.right()
        
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            end()
        if event.type == pygame.KEYDOWN:
            # print(event.key)
            if event.key == 292:
                pygame.display.toggle_fullscreen()
            if event.key == 119 or event.key == 32:  # w
                player.up(jumpTics)
            if event.key == 97:  # a
                player.left()
            if event.key == 100:  # d
                player.right()
        if event.type == pygame.KEYUP:
            if event.key == 119 or event.key == 32:  # w
                if player.vy == -speed:
                    player.vy = 0
            if event.key == 97:  # a
                if player.vx == -speed:
                    player.vx = 0
            if event.key == 100:  # d
                if player.vx == speed:
                    player.vx = 0

        if event.type == pygame.JOYAXISMOTION:
            print("Joy", event)
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joy button pressed", event)

    # joystick-----------------------------------

    joystick_count = pygame.joystick.get_count()
    # print("count",joystick_count)

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        hats = joystick.get_numhats()
        for i in range(hats):
            hat = joystick.get_hat(i)
            if hat == (1, 0):
                # right
                vx = speed
            elif hat == (-1, 0):
                # left
                vx = -speed
            elif hat == (0, 1):
                # up
                vy = -speed
            elif hat == (0, -1):
                # down
                vy = speed
            elif hat == (0, 0):
                vy = 0
                vx = 0
            # print(hat)

    # joystick.get_axis(0)
    # if event.type == pygame.JOYBUTTONDOWN:
    #        if joystick.get_button(9)==1:


    player.x += player.vx
    player.y += player.vy

    colisions = spriteColide()

    if colisions != []:
        colFlag = 0
        for n in range(len(colisions)):
            colision = colisions[n]
            spriteA = sprite.registry[int(colision[0])]
            spriteB = sprite.registry[int(colision[1])]
            
            if spriteB.sType == "Map" and spriteA.sType != "Map":
                if spriteA.sType == "Player":
                    colFlag += 1
                sides = ""
                if spriteA.vy >= 0 and spriteA.y < spriteB.y and (spriteA.y + spriteA.size[1]) >= spriteB.y and (
                        spriteA.x + spriteA.size[0] > spriteB.x and spriteA.x < spriteB.x + spriteB.size[0]):
                    sides = sides + "u"
                if spriteA.vy <= 0 and spriteA.y + spriteA.size[1] > spriteB.y + spriteB.size[1] and spriteA.y <= (
                        spriteB.y + spriteB.size[1]) and (
                        spriteA.x + spriteA.size[0] > spriteB.x and spriteA.x < spriteB.x + spriteB.size[0]):
                    sides = sides + "d"
                if spriteA.vx >= 0 and spriteA.x < spriteB.x and (
                        spriteA.x + spriteA.size[0]) >= spriteB.x and spriteA.y + spriteA.size[
                    1] > spriteB.y and spriteA.y < spriteB.y + spriteB.size[1]:
                    sides = sides + "l"
                if spriteA.vx <= 0 and spriteA.x + spriteA.size[0] > spriteB.x + spriteB.size[
                    0] and spriteA.x <= spriteB.x + spriteB.size[0] and spriteA.y + spriteA.size[
                    1] > spriteB.y and spriteA.y < spriteA.y + spriteA.size[1]:
                    sides = sides + "r"

                if sides == "u":                    
                    spriteA.timeLeave = pygame.time.get_ticks()  # current time
                    spriteA.onGround = True
                    #print(pygame.time.get_ticks())
                    spriteA.vy = 0
                    spriteA.y = spriteB.y - (spriteA.size[1])
                elif sides == "d":
                    spriteA.vy = 0
                    spriteA.y = spriteB.y + (spriteB.size[1])
                elif sides == "l":
                    #spriteA.onGround = True #
                    spriteA.vx = 0
                    spriteA.x = spriteB.x - (spriteA.size[0])
                elif sides == "r":
                    #spriteA.onGround = True #
                    spriteA.vx = 0
                    spriteA.x = spriteB.x + (spriteB.size[0])
                elif sides == "dr":
                    if (spriteB.x + spriteB.size[0] - spriteA.x) > (spriteB.y + spriteB.size[1] - spriteA.y):
                        spriteA.vy = 0
                        spriteA.y = spriteB.y + spriteB.size[1]
                    else:
                        spriteA.vx = 0
                        spriteA.x = spriteB.x + spriteB.size[0]
                elif sides == "dl":
                    if ((spriteA.x + spriteA.size[0]) - spriteB.x) > (spriteB.y + spriteB.size[1] - spriteA.y):
                        spriteA.vy = 0
                        spriteA.y = spriteB.y + spriteB.size[1]
                    else:
                        spriteA.vx = 0
                        spriteA.x = spriteB.x - spriteA.size[0]
                elif sides == "ul":
                    #spriteA.onGround = True #
                    if (spriteA.x + spriteA.size[0] - spriteB.x) > (spriteA.y + spriteA.size[1] - spriteB.y):
                        spriteA.vy = 0
                        spriteA.y = spriteB.y - spriteA.size[1]
                    else:
                        spriteA.vx = 0
                        spriteA.x = spriteB.x - spriteA.size[0]
                elif sides == "ur":
                    #spriteA.onGround = True #
                    if (spriteB.x + spriteB.size[0] - spriteA.x) > (spriteA.y + spriteA.size[1] - spriteB.y):
                        spriteA.vy = 0
                        spriteA.y = spriteB.y - spriteA.size[1]
                    else:
                        spriteA.vx = 0
                        spriteA.x = spriteB.x + spriteB.size[0]

                        # if the two are equal then it will pick the second option
                elif sides == "udl":
                    spriteA.vx = 0
                    spriteA.x = spriteB.x - spriteA.size[0]
                elif sides == "udr":
                    spriteA.vx = 0
                    spriteA.x = spriteB.x + spriteB.size[0]
                elif sides == "ulr":
                    spriteA.vy = 0
                    spriteA.y = spriteB.y - spriteA.size[1]
                elif sides == "dlr":
                    spriteA.vy = 0
                    spriteA.y = spriteB.y + spriteB.size[1]
                else:
                    break
                    #print(sides)
            elif spriteA.sType == "Player" and (spriteB.sType == "EnemyM" or spriteB.sType == "EnemyS"):
                spriteA.damage()
                

                
        if colFlag == 0:
            player.onGround = False
    else:
        player.onGround = False
    #print(player.onGround)
    #gravity--------------------------------------------------
                    
    if False == player.onGround:
        player.vy = player.vy + 1.5*((pygame.time.get_ticks()-player.timeLeave)/1000) # v = u + a*t
        #print((pygame.time.get_ticks()-player.timeLeave)/1000) #log

  
    """
    else:
        for n in range(len(sprites)-1):
            sprites[n+1].colour=black

    for n in range(len(sprite.registry)):
        if sprite.sType!="Map":
            sprite[n].vy=sprite[n].vy+9.81*
            
    """  # v=u+at

    
    #Display
    
    
    
    camX = player.x - (resolution[0]/2)
    #camY = player.y - (resolution[1]/2)
    
    gameDisplay.fill(white)
    #health bar
    pygame.draw.rect(gameDisplay, black, (21.5*scale,0.4*scale,3*scale,0.6*scale))
    if player.health != 0:
        pygame.draw.rect(gameDisplay, red, (21.6*scale,0.5*scale,2.8*scale*player.health/100,0.4*scale))
    
    for n in range(len(sprite.registry)):
        pygame.draw.rect(gameDisplay, sprite.registry[n].colour, (sprite.registry[n].x-camX, sprite.registry[n].y, sprite.registry[n].size[0], sprite.registry[n].size[1]))

    clock.tick(60)
    
    pygame.display.update()

gameEnd(player.x-resolution[0]/3)
