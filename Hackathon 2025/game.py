# DEVELOPED BY DIEGO AVILA AND MAURO HERNANDEZ
# DIMENSIONAL EMERALD!

import pygame
import sys

pygame.init() #initiates pygame



#Screen
width = 840
height = 620
pygame.display.set_caption("Dimensional Emerald")
screen = pygame.display.set_mode((width, height)) # resolution of 

#Framerate controller
clock = pygame.time.Clock()

# Wizard Sprite Controller
wizardRight = pygame.image.load("sprites\Wizard_Side_Right.png").convert_alpha()
wizardLeft = pygame.image.load("sprites\Wizard_Side_Left.png").convert_alpha()
wizardFallLeft = pygame.image.load("sprites\Wizard_Fall_Left.png").convert_alpha()
wizardFallRight = pygame.image.load("sprites\Wizard_Fall_Right.png").convert_alpha()
wizardCastRight = pygame.image.load("sprites\Wizard_Cast_Right.png").convert_alpha()
wizardCastLeft = pygame.image.load("sprites\Wizard_Cast_Left.png").convert_alpha()
wizardJumpRight = pygame.image.load("sprites\Wizard_Jump_Right.png").convert_alpha()
wizardJumpLeft = pygame.image.load("sprites\Wizard_Jump_Left.png").convert_alpha()
wizardWalkLeft1 = pygame.image.load("sprites\Wizard_Walk1_Left.png").convert_alpha()
wizardWalkLeft2 = pygame.image.load("sprites\Wizard_Walk2_Left.png").convert_alpha()
wizardWalkRight1 = pygame.image.load("sprites\Wizard_Walk1_Right.png").convert_alpha()
wizardWalkRight2 = pygame.image.load("sprites\Wizard_Walk2_Right.png").convert_alpha()
wizard = [wizardRight, wizardLeft]
wizardFall = [wizardFallRight, wizardFallLeft]
wizardCast = [wizardCastRight, wizardCastLeft]
wizardJump = [wizardJumpRight, wizardJumpLeft]
wizardWalkLeft = [wizardWalkLeft1, wizardWalkLeft2]
wizardWalkRight = [wizardWalkRight1, wizardWalkRight2]
wEmtSpc = 120
direction = 0
#Wizard Scale
wScaleX = 14 * 4
wScaleY = 18 * 4

# Movement
wizardPos = [0, 0]
wizardMove = [False, False, False, False]

walkAnimCounter = 0
walkAnimSpeed = 15  # Adjust this for how fast the walking animation switches
walkFrame = 0  # 0 or 1, for toggling between walk1 and walk2

# Collisions
collisionY = False
down = 1

# Gravity
jumpPower = 10
jumpTimer = 0
gravity = 5

# Frame Counter
frames = 0

# Dimensions
color = True
ColorBg = pygame.image.load("maps\Color_Bg.png").convert_alpha()
NoirBg = pygame.image.load("maps\Black_Bg.png").convert_alpha()

# Portal Creation Function
portal = pygame.image.load("sprites\Portal.png").convert_alpha()
portal = pygame.transform.scale(portal, (24, 78))
portalPos = [0, 0]
portalSpawn = False
portalTimer = 0
portalCollision = pygame.Rect(1000, 1000, portal.get_width(), portal.get_height()) # sets portal collision outside of map for convinience

# Emerald
emeraldWidth = 63
emeraldHeight = 87
emerald = pygame.image.load("sprites\Emerald.png").convert_alpha()
emerald = pygame.transform.scale(emerald, (emeraldWidth, emeraldHeight))
emeraldY = height - 120
emeraldX = width - 100
bobbing = True

#Map
colorFloors = []
noirFloors = []
colorWalls = []
noirWalls = []
    
def makeSquare(x, y, width, height, r, g, b, opacity):  
    square = pygame.Surface((width, height), pygame.SRCALPHA)  # Create transparent surface
    square.fill((r, g, b, (opacity * 255)))
    screen.blit(square, (x, y))

#Main game loop
while True:
    frames += 1 # Frame Counter
    jumpTimer += 1
    portalTimer += 1

    if frames % 60 == 0 and bobbing:
        bobbing = False
    elif frames % 60 == 0 and not bobbing:
        bobbing = True
    
    if bobbing and frames % 7 == 0:
        emeraldY -= 1
    elif not bobbing and frames % 7 == 0:
        emeraldY += 1

    # Walk Animation choose thing
    if wizardMove[2] or wizardMove[3]:  # Only update when walking
            walkAnimCounter += 1
            if walkAnimCounter >= walkAnimSpeed:
                walkAnimCounter = 0
                walkFrame = (walkFrame + 1) % 2  # Toggle between 0 and 1

    wizardPos[1] += (wizardMove[0] - wizardMove[1])* -5
    wizardPos[0] += (wizardMove[2] - wizardMove[3]) * 3 # Right Left Controller

    # Color and Noir Dimensions 
    currentBg = [NoirBg, ColorBg]
    screen.fill((0, 0, 0))   
    screen.blit(currentBg[color], (0, 0))

    # Border Floor
    floor = pygame.Rect(0, height, width, 10)
    #Border Walls
    leftWall = pygame.Rect(0, 0, 1, height)
    rightWall = pygame.Rect(width, 0, 1, height)


    # Wizard Animation Handler
    # Portal Spawn Animation
    if portalSpawn:
        wizardCast[direction] = pygame.transform.scale(wizardCast[direction], (wScaleX, wScaleY))
        screen.blit(wizardCast[direction], wizardPos)
        screen.blit(portal, portalPos) # Spawns portal
        portalCollision = pygame.Rect(portalPos[0], portalPos[1], portal.get_width(), portal.get_height()) #portal Collision
    elif not collisionY and not wizardMove[0]: # fall sprite
        wizardFall[direction] = pygame.transform.scale(wizardFall[direction], (wScaleX, wScaleY))
        screen.blit(wizardFall[direction], wizardPos)
    elif wizardMove[0]:
        wizardJump[direction] = pygame.transform.scale(wizardJump[direction], (wScaleX, wScaleY))
        screen.blit(wizardJump[direction], wizardPos)
    elif wizardMove[2] or wizardMove[3]:
        if direction == 0:  # Moving right
            currentWalk = pygame.transform.scale(wizardWalkRight[walkFrame], (wScaleX, wScaleY))
        else:  # Moving left
            currentWalk = pygame.transform.scale(wizardWalkLeft[walkFrame], (wScaleX, wScaleY))
        screen.blit(currentWalk, wizardPos)
    else:
        wizard[direction] = pygame.transform.scale(wizard[direction], (wScaleX, wScaleY))
        screen.blit(wizard[direction], wizardPos)

    # Moves Portal Collision Far after Despawn
    if portalSpawn == False:
        portalCollision = pygame.Rect(10000, 10000, portal.get_width(), portal.get_height()) #portal Collision

    # Wizard Collisions
    wizardCollision = pygame.Rect(wizardPos[0] - 1, wizardPos[1] - 1, wScaleX, wScaleY)
    
    # For the Floor
    if wizardCollision.colliderect(floor):
        font = pygame.font.SysFont("Arial", 72, bold=True)
        lose_text = font.render("YOU LOSE!", True, (255, 0, 0))
        text_rect = lose_text.get_rect(center=(width // 2, height // 2))
        screen.blit(lose_text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        wizardPos = [0, 0]
        color = True
        screen.blit(info_text, text_rect)
        frames = 0
        portalSpawn = False

    else:
        collisionY = False
    
    if color:
        for i in colorFloors:
            if wizardCollision.colliderect(i):
                collisionY = True
                down = 0
        for i in colorWalls:
            if wizardCollision.colliderect(i):
                wizardMove[2] = False
    
    if not color:
        if wizardCollision.colliderect(floor18):
            wizardMove[3] = False
        for i in noirFloors:
            if wizardCollision.colliderect(i):
                collisionY = True
                down = 0
        for i in noirWalls:
            if wizardCollision.colliderect(i):
                wizardMove[2] = False
     
    # For the walls
    if wizardCollision.colliderect(leftWall):
        wizardMove[3] = False
    if wizardCollision.colliderect(rightWall):
        wizardMove[2] = False
        

    # Dimension Changing collision
    if wizardCollision.colliderect(portalCollision) and color:
        color = False
        portalSpawn = False
    elif wizardCollision.colliderect(portalCollision) and not color:
        color = True
        portalSpawn = False

    # What happens when collision with floor
    if collisionY:
        down = 0
    else:
        down = 1

    for event in pygame.event.get(): # Controls every game event ie. Closing tabs, pressing a button
        if event.type == pygame.QUIT:
            sys.exit()

        # Key Controller
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                wizardMove[2] = True
                direction = 0
            if event.key == pygame.K_a:
                wizardMove[3] = True
                direction = 1
            if event.key == pygame.K_e and not portalSpawn:
                portalSpawn = True
                portalTimer = 0
                    # Spawn portal in front of wizard
                if direction == 0:  # Facing right
                    portalPos = [wizardPos[0] + wizard[direction].get_width() + 10, wizardPos[1] - 27]
                else:  # Facing left
                    portalPos = [wizardPos[0] - portal.get_width() - 10, wizardPos[1] - 27]

            # Jump Handler
            if event.key == pygame.K_SPACE and collisionY: # Jump
                wizardMove[0] = True # Sets Jumping Status
                down = 0 # Ignore Gravity
                jumpTimer = 0 # Timer to keep track of time since jump

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                wizardMove[2] = False
            if event.key == pygame.K_a:
                wizardMove[3] = False
            if event.key == pygame.K_r:
                wizardPos = [0, 0]
                color = True
                screen.blit(info_text, text_rect)
                frames = 0
                portalSpawn = False
                

    # Timers
    if jumpTimer == 15: # After 60 frames after jump move up a little higher
        wizardMove[0] = False # Gravity starts again
    if portalTimer == 180:
        portalSpawn = False # erases portal
    # Gravity
    if not wizardMove[0]:
       wizardPos[1] += (gravity * down)


# THE LEVEL IS THE LAST THING LOADED IN
# Map
    makeSquare(0, 100, 200, 15, 34, 139, 34, color)
    floor1 = pygame.Rect(0, 100, 200, 15)
    makeSquare(200, 0, 15, 115, 34, 139, 39, color)
    floor2 = pygame.Rect(200, 0, 15, 115) # Wall
    makeSquare(10, 200, 230, 15, 70, 70, 70, not color) # Noir
    floor3 = pygame.Rect(10, 200, 230, 15) # Noir
    makeSquare(250, 250, 150, 15, 70, 70, 70, not color) # Noir
    floor4 = pygame.Rect(250, 250, 150, 2) # Noir
    makeSquare(400, 65, 15, 200, 70, 70, 70, not color) # Noir
    floor5 = pygame.Rect(400, 55, 15, 200) # Noir wall
    makeSquare(480, 150, 15, 200, 34, 139, 34, color)
    floor6 = pygame.Rect(480, 150, 15, 200) # wall
    makeSquare(265, 335, 220, 15, 34, 139, 34, color)
    floor7 = pygame.Rect(265, 335, 220, 15)
    makeSquare(180, 380, 150, 15, 34, 139, 34, color)
    floor8 = pygame.Rect(180, 380, 150, 15)
    makeSquare(230, 420, 80, 15, 70, 70, 70, not color) # Noir
    floor9 = pygame.Rect(230, 420, 80, 15) # Noir
    makeSquare(280, 600, 200, 15, 70, 70, 70, not color) # Noir
    floor10 = pygame.Rect(280, 600, 200, 15) # Noir
    makeSquare(490, 560, 100, 15, 34, 139, 34, color)
    floor11 = pygame.Rect(490, 560, 100, 15)
    makeSquare(605, 600, 85, 15, 70, 70, 70, not color) # Noir
    floor12 = pygame.Rect(605, 600, 85, 15) # Noir
    makeSquare(604, 300, 15, 300, 34, 139, 34, color)
    floor13 = pygame.Rect(604, 300, 15, 300) # wall
    makeSquare(690, 365, 15, 250, 70, 70, 70, not color) # Noir
    floor14 = pygame.Rect(690, 365, 15, 250) # Noir wall
    makeSquare(705, 600, 200, 15, 34, 139, 34, color)
    floor15 = pygame.Rect(705, 600, 200, 15)
    makeSquare(705, 365, 200, 15, 70, 70, 70, not color) # Noir
    floor16 = pygame.Rect(705, 365, 200, 15) # Noir
    floor17 = pygame.Rect(265, 350, 15, 30) # Hidden green wall
    floor18 = pygame.Rect(225, 215, 15, 30) # Hidden noir wall

    colorFloors = [floor1, floor7, floor8, floor11, floor15]
    noirFloors = [floor3, floor4, floor9, floor10,  floor12, floor16]
    colorWalls = [floor2, floor6, floor13, floor17]
    noirWalls = [floor5, floor14]
    

    # DIMENSIONAL EMERALD
    screen.blit(emerald, (width - 100, emeraldY)) # Emerald
    emeraldCollision = pygame.Rect(width - 100, emeraldY, emerald.get_width(), emerald.get_height())

    if wizardCollision.colliderect(emeraldCollision):
        font = pygame.font.SysFont("Arial", 72, bold=True)
        win_text = font.render("YOU WIN!", True, (255, 255, 0))  # Yellow text
        text_rect = win_text.get_rect(center=(width // 2, height // 2))
        screen.blit(win_text, text_rect)
        pygame.display.update()
        pygame.time.delay(3000)
        wizardPos = [0, 0]
        color = True
        screen.blit(info_text, text_rect)
        frames = 0
        portalSpawn = False

    # INformation text
    if frames < 240:
        font = pygame.font.SysFont("Arial", 22, bold=True)
        info_text = font.render("Get the Dimensional Emerald     Press E to Spawn your portal to to other dimensions", True, (255, 255, 255))
        text_rect = info_text.get_rect(center=(420, height - 50))
        screen.blit(info_text, text_rect)

    pygame.display.update() # New frame every loop
    clock.tick(60) # Game runs at 60 FPS
