import pygame, random

ssize = (600,600)
limit = 6


def draw_serpinski_carpet(center, iter_count, colour):

    block = ssize[0]// (3**iter_count)
    self_rect = [center[0]-block//2, center[1]-block//2, block, block]
    colour = [(colour[i] + random.randint(0,25))%255 for i in [0,1,2]]

    pygame.draw.rect(screen, colour, self_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            10/0

    pygame.display.flip()

    if iter_count < limit:

        draw_serpinski_carpet([center[0] - block, center[1] - block], iter_count+1, colour)
        draw_serpinski_carpet([center[0], center[1] - block], iter_count+1, colour)
        draw_serpinski_carpet([center[0] + block, center[1] - block], iter_count+1, colour)

        draw_serpinski_carpet([center[0] - block, center[1]], iter_count+1, colour)
        draw_serpinski_carpet([center[0] + block, center[1]], iter_count+1, colour)

        draw_serpinski_carpet([center[0] - block, center[1] + block], iter_count+1, colour)
        draw_serpinski_carpet([center[0], center[1] + block], iter_count+1, colour)
        draw_serpinski_carpet([center[0] + block, center[1] + block], iter_count+1, colour)
    else:
        return

pygame.init()

screen = pygame.display.set_mode(ssize)
screen.fill((0,0,0))

draw_serpinski_carpet([ssize[0]//2, ssize[1]//2], 1, (255))


input()
