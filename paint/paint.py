import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()
    
screen.fill((0, 0, 0))

rect_baseLayer = pygame.Surface((640, 480))
rect_prevX = -1
rect_prevY = -1
rect_currentX = -1
rect_currentY = -1
rect_isMousedown = False 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)    

color = WHITE
radius = 5
mode = ""

pen_prevX = 0
pen_prevY = 0
isMouseDown = False

def calculateRect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

previous_values = []

run = True 
while run:
    # screen.fill(BLACK)
    pen_currentX = pen_prevX
    pen_currentY = pen_prevY
    # alt and ctrl 
    pressed = pygame.key.get_pressed()
    alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
    ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]


    for event in pygame.event.get():

        # Mouse Button---------------
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                isMouseDown = True
                rect_isMousedown = True 
                rect_currentX =  event.pos[0]
                rect_currentY =  event.pos[1]
                rect_prevX =  event.pos[0]
                rect_prevY =  event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            rect_isMousedown = False 
            rect_baseLayer.blit(screen, (0, 0))
            if event.button == 1: 
                isMouseDown = False

        if event.type == pygame.MOUSEMOTION:
            if rect_isMousedown == True:
                rect_currentX =  event.pos[0]
                rect_currentY =  event.pos[1]
            # if mouse moved, add point to list
            pen_currentX =  event.pos[0]
            pen_currentY =  event.pos[1]
               
        #----------------------------
        
        # Close pygame---------------
        if event.type == pygame.QUIT:
                run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and ctrl_held:
                run = False
            if event.key == pygame.K_F4 and alt_held:
                run = False
            if event.key == pygame.K_ESCAPE:
                run = False
        #----------------------------

        # push r / g / b / w / y --> Color selection
        # Color selection------------ 
            if event.key == pygame.K_r and ctrl_held == False:
                # screen.fill(BLACK)
                color = RED
            if event.key == pygame.K_g:
                # screen.fill(BLACK)
                color = GREEN
            if event.key == pygame.K_b:
                # screen.fill(BLACK)
                color = BLUE
            if event.key == pygame.K_w:
                # screen.fill(BLACK)
                color = WHITE
            if event.key == pygame.K_y:
                # screen.fill(BLACK)
                color = YELLOW

        # ctrl + delete == delete all:
            if event.key == pygame.K_DELETE and ctrl_held:
                screen.fill(BLACK)

        #---------------------------

        # Radius shrink / grow------
            if event.key == pygame.K_1: 
                radius += 5
            if event.key == pygame.K_0:
                radius -= 5
        #----------------------------

        # pen / rect / circle / eraser------ 
            # push ctrl + r --> Draw rectangle
            # push ctrl + c --> Draw circle
            # push ctrl + e --> Eraser
            # push ctrl + p --> Pen

            if ctrl_held and event.key == pygame.K_r:
                # screen.fill(BLACK)
                mode = 'rectangle'
            if ctrl_held and event.key == pygame.K_c:
                # screen.fill(BLACK)
                mode = 'circle'
            if ctrl_held and event.key == pygame.K_e:
                # screen.fill(BLACK)
                mode = 'eraser'
            if ctrl_held and event.key == pygame.K_p:
                # screen.fill(BLACK)
                mode = 'pen'
        #------------------------------------
       
        # choose mode ---------------------------------------

        if mode == 'rectangle':
            if rect_isMousedown == True and rect_prevX != -1 and rect_prevY != -1 and rect_currentX != -1 and rect_currentY != -1:
                screen.blit(rect_baseLayer, (0, 0))
                r = calculateRect(rect_prevX, rect_prevY, rect_currentX, rect_currentY)
                pygame.draw.rect(screen, color,pygame.Rect(r), radius)


        if mode == 'pen':
            if isMouseDown == True:
                pygame.draw.line(screen, color, (pen_prevX, pen_prevY), (pen_currentX, pen_currentY), radius)
            pen_prevX = pen_currentX
            pen_prevY = pen_currentY

        if mode == 'eraser':
            if isMouseDown == True:
                pygame.draw.line(screen, BLACK, (pen_prevX, pen_prevY), (pen_currentX, pen_currentY), radius + 10)
            pen_prevX = pen_currentX
            pen_prevY = pen_currentY

        if mode == 'circle':
            if rect_isMousedown == True and rect_prevX != -1 and rect_prevY != -1 and rect_currentX != -1 and rect_currentY != -1:
                screen.blit(rect_baseLayer, (0, 0))
                r = calculateRect(rect_prevX, rect_prevY, rect_currentX, rect_currentY)
                pygame.draw.circle(screen, color, (rect_currentX, rect_currentY), radius * 10, radius)
        #---------------------------------------------------
    
    pygame.display.update(0, 0, 640, 20)
    
    pygame.display.flip() 
    clock.tick(60)