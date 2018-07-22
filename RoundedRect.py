import pygame, time, sys
from pygame.locals import *
from pygame import gfxdraw

def RoundedRect(surface, rect, fillColor, outColor, radius):

    Rect = pygame.Rect(rect)
    iRect = pygame.draw.rect(surface, fillColor, (Rect.left+radius, Rect.top +radius, Rect.width-2*radius, Rect.height-2*radius))
    gfxdraw.filled_circle(surface, iRect.topleft[0],iRect.topleft[1], radius, fillColor)
    gfxdraw.aacircle(surface, iRect.topleft[0],iRect.topleft[1], radius, outColor)
    gfxdraw.filled_circle(surface, iRect.bottomleft[0],iRect.bottomleft[1], radius, fillColor)
    gfxdraw.aacircle(surface, iRect.bottomleft[0],iRect.bottomleft[1], radius, outColor)
    gfxdraw.filled_circle(surface, iRect.topright[0],iRect.topright[1], radius, fillColor)
    gfxdraw.aacircle(surface, iRect.topright[0],iRect.topright[1], radius, outColor)
    gfxdraw.filled_circle(surface, iRect.bottomright[0],iRect.bottomright[1], radius, fillColor)
    gfxdraw.aacircle(surface, iRect.bottomright[0],iRect.bottomright[1], radius, outColor)
    r = radius
    pygame.draw.rect(surface, fillColor, (iRect.left, iRect.top-radius, iRect.width, r+iRect.height))
    pygame.draw.rect(surface, fillColor, (iRect.left, iRect.bottom, iRect.width, r))
    pygame.draw.rect(surface, fillColor, (Rect.left, iRect.top, r, iRect.height))
    pygame.draw.rect(surface, fillColor, (iRect.right, iRect.top, r, iRect.height))


    pygame.draw.line(surface, outColor, (iRect.left, iRect.top-r), (iRect.right,iRect.top-r), 1)
    pygame.draw.line(surface, outColor, (iRect.left-r, Rect.top+r), (iRect.left-r,iRect.bottom), 1)
    pygame.draw.line(surface, outColor, (iRect.left, iRect.bottom+r), (iRect.right,iRect.bottom+r), 1)
    pygame.draw.line(surface, outColor, (iRect.right+r, Rect.top+r), (iRect.right+r,iRect.bottom), 1)


WHITE = (255,255,255)
BLACK = ( 0, 0, 0)
RED = ( 255, 0, 0)

pygame.init()
DISPLAYSURF = pygame.display.set_mode((640,480))
DISPLAYSURF.fill(BLACK)
RoundedRect(DISPLAYSURF, (300,200, 200,100), WHITE, RED, 18)
pygame.display.update()

time.sleep(5)
pygame.quit()
sys.exit()