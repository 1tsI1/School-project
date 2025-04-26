import pygame
from random import randint
pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font1 = pygame.font.Font(None, 35)
font2 = pygame.font.Font(None, 80)


py, sy, ay = HEIGHT , 0, 0
player = pygame.Rect(WIDTH // 3, py, 100, 86)

state = 'start'
timer = 10

pipes = []
bges = []
pipesScores = []
pipeSpeed = 3
pipeGateSise = 220
pipeGatePos = HEIGHT // 2


bges.append(pygame.Rect(0 ,0, 800, 600))

lives = 3
scores = 0

imgBG = pygame.image.load('images\Bakcground.png')
imgBird = pygame.image.load('images\Bird.png')
imgPT = pygame.image.load('images\Pipedwn.png')
imgPB= pygame.image.load('images\Pipeup.png')

frame = 0

play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
                 
    press = pygame.mouse.get_pressed()
    keys = pygame. key.get_pressed()
    click = press[0] or keys[pygame.K_SPACE]

    if timer > 0:
        timer -= 1

    frame=(frame+0.2) % 6
    pipeSpeed = 3 + scores // 100


    for i in range(len(bges) -1, -1, -1):
        bg = bges[i]
        bg.x -= pipeSpeed // 2

        if bg.right < 0:
            bges.remove(bg)

        if bges[len(bges)-1].right <= WIDTH:
            bges.append(pygame.Rect(bges[len(bges)-1].right ,0, 800, 600))


    for i in range(len(pipes) -1, -1, -1):
        pipe = pipes[i]
        pipe.x -= pipeSpeed

        if pipe.right < 0:
            pipes.remove(pipe)
            if pipe in pipesScores: pipesScores.remove(pipe)

    if state == 'start':
        if click and timer == 0 and len(pipes) == 0:
            state = 'play'

        py += (HEIGHT // 2 - py) * 0.1
        player.y = py
    elif state == 'play':
        if click:
            ay = -2
        else:
            ay = 0

        py += sy
        sy = (sy + ay + 1) * 0.8
        player.y = py

        if len(pipes) == 0 or pipes[len(pipes) - 1].x < WIDTH - 200:
            pipes.append(pygame.Rect(WIDTH, 0, 50, pipeGatePos - pipeGateSise // 2))
            pipes.append(pygame.Rect(WIDTH, pipeGatePos + pipeGateSise // 2, 50, HEIGHT - pipeGatePos + pipeGateSise // 2))

            pipeGatePos += randint (-100, 100)
            if pipeGatePos < pipeGateSise:
               pipeGatePos = pipeGateSise
            elif pipeGatePos > HEIGHT - pipeGateSise:
                pipeGatePos = HEIGHT - pipeGateSise

        if player.top < 0 or player.bottom > HEIGHT:
            state = 'fall'
        for pipe in pipes:
            if player.colliderect(pipe):
                state = 'fall'
            if pipe.right < player.left and pipe not in pipesScores:
                pipesScores.append(pipe)
                scores += 5
    elif state == 'fall':
        sy, ay = 0, 0
        pipeGatePos = HEIGHT // 2
        lives -= 1
        if lives > 0: 
            state = 'start'
            timer = 60
        else:
            state = "game over"
            timer = 180
    else: 
        if timer == 0: play = False
        py += sy
        sy = (sy + ay + 1) * 0.8
        player.y = py
            

    for bg in bges:
        window.blit(imgBG, bg)
    for pipe in pipes:
        if pipe.y == 0: 
            rect = imgPT.get_rect(bottomleft = pipe.bottomleft)
            window.blit(imgPT, rect)
        else:
            rect = imgPB.get_rect(topleft = pipe.topleft)
            window.blit(imgPB, rect) 
        

    image = imgBird.subsurface(100*int(frame), 0, 100, 86)
    image = pygame.transform.rotate(image,-sy*3)
    window.blit(image, player)

    text = font1.render("Очки :" + str(scores), 0, pygame.Color("Yellow"))
    window.blit(text,(10,10))
    text = font1.render("Жизни :" + str(lives), 0, pygame.Color("Yellow"))
    window.blit(text,(10,HEIGHT -30))
          
    pygame.display.update()
    clock.tick(FPS)

text = font1.render("КОНЕЦ ИГРЫ", 0, pygame.Color("Yellow"))
window.blit(text,(WIDTH // 2 -10,HEIGHT // 2))
pygame.display.update()    

pygame.quit()