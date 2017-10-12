import sys, pygame, mygui, ServerSide, ClientSide
from pygame.locals import *
from constants import *


class Begin:

    def __init__(self):

        pygame.init()
        pygame.display.set_caption(CAPTION)
        screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
        self.load_stuff()

        screen.blit(BG0, (0,0)) #Set background image
        screen.blit(self.TXT_WELCOME, self.TXT_WELCOME_RECT) #Write Welcome

        #Parameters:      surface,      color,       x,   y,   length, height, width,    text,      text_color
        self.BUT_SERVER.create_button(screen, BACK_BUTTON, WIDTH/3, HEIGHT/3.55, WIDTH/3.2,    HEIGHT/6.85,    0,        "Server", TEXT_BUTTON)
        self.BUT_CLIENT.create_button(screen, BACK_BUTTON, WIDTH/3, HEIGHT/1.88, WIDTH/3.2,    HEIGHT/6.85,    0,        "Client", TEXT_BUTTON)

        quit = False
        while not quit :
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    if self.BUT_SERVER.pressed(pygame.mouse.get_pos()):
                        state = 1
                        quit = True
                        break

                    if self.BUT_CLIENT.pressed(pygame.mouse.get_pos()):
                        state = 2
                        quit = True
                        break
            pygame.display.update()

        if state == 1:
            ServerSide.PokerServer(screen)
        elif state == 2:
            ClientSide.PokerClient(screen)

    def load_stuff(self):
        self.BUT_SERVER = mygui.Button()
        self.BUT_CLIENT = mygui.Button()

        self.TXT_WELCOME, self.TXT_WELCOME_RECT = mygui.print_text('freesansbold.ttf', HEIGHT/15, "Welcome", WHITE, None, WIDTH/2, HEIGHT/10)


if __name__ == '__main__':
    Begin()
