import pygame

pygame.init()

win = pygame.display.set_mode((500, 500))

win.fill((0,0,0))

i = True
while i:


    color = (255,0,0) #(x ,y ,width , height)
    pygame.draw.rect(win, color, pygame.Rect(400, 400, 200, 50))

    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                i = False