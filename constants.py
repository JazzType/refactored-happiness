#import pygame, mygui

WIDTH = 640
HEIGHT = 480

CAPTION = "Poker"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 128)

BACK_SCREEN = 60, 60, 100
BACK_BUTTON= 192, 192, 192
TEXT_BUTTON= 0, 0, 0

INITMONEY = 1000

TABLESCALE = 2
PICSIZE = (100, 100)

CARDLENIMG = 43
CARDWIDIMG = 62
CARDLEN = 36
CARDWID = 49
#CARDS= pygame.image.load("images/cards.png")

#BG0 = pygame.image.load("images/bg0.jpg")
#BG0 = pygame.transform.scale(BG0, (WIDTH, HEIGHT))
#BG1 = pygame.image.load("images/bg1.jpg")
#BG1 = pygame.transform.scale(BG1, (WIDTH, HEIGHT))
#PKT1 = pygame.image.load("images/pkt0.png")
#PKT1 = pygame.transform.scale(PKT1, (int(TABLESCALE*HEIGHT/2), HEIGHT/2)) #480 * 240
#SL1 = pygame.image.load("images/slider0.png")
#SL1 = pygame.transform.scale(SL1, (200,4))
#SL2 = pygame.image.load("images/slider1.png")
#SL2 = pygame.transform.scale(SL2, (39,20))

PICSIZE = (int(HEIGHT/4.8), int(HEIGHT/4.8)) # 100 * 100
TBLTOPLEFT = (int(HEIGHT/6), int(HEIGHT/6)) # (80, 80)
TBLWIDTH = HEIGHT
TBLHEIGHT = HEIGHT/2

#Order in which players sit
ORDER = (8, 2, 11, 5, 4, 10, 0, 6, 1, 7, 3, 9)
