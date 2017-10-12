import sys, pygame, mygui, serverThread, serverGame
from pygame.locals import *
from constants import *

class PokerServer:

    def load_stuff(self):
        self.TXT_SERVER, self.TXT_SERVER_RECT = mygui.print_text('freesansbold.ttf', HEIGHT/15, "Server", WHITE, None, WIDTH/2, HEIGHT/10)
        self.TXT_IP, self.TXT_IP_RECT = mygui.print_text('freesansbold.ttf', HEIGHT/30, "Host IP : "+self.serIP, WHITE, None, WIDTH/2, HEIGHT/4)
        self.TXT_PORT, self.TXT_PORT_RECT = mygui.print_text('freesansbold.ttf', HEIGHT/30, "Port : " + str(self.serPort), WHITE, None, WIDTH/2, HEIGHT/4 + HEIGHT/10)
        self.TXT_CLIENTS, self.TXT_CLIENTS_RECT = mygui.print_text('freesansbold.ttf', HEIGHT/30, "# of Clients : "+ str(self.serClients), WHITE, None, WIDTH/2, HEIGHT/4 + HEIGHT/5)

        self.BUT_START = mygui.Button()

    def gui(self, screen, isButton):
        screen.blit(BG0, (0,0)) # Set background image

        screen.blit(self.TXT_SERVER, self.TXT_SERVER_RECT)
        screen.blit(self.TXT_IP, self.TXT_IP_RECT)
        screen.blit(self.TXT_PORT, self.TXT_PORT_RECT)
        screen.blit(self.TXT_CLIENTS, self.TXT_CLIENTS_RECT)

    def __init__(self, screen):

        self.serObj = serverThread.ServerThread()

        self.serIP = self.serObj.get_ip()
        self.serPort = self.serObj.get_port()
        self.serClients = self.serObj.get_num_of_clients()

        self.load_stuff()

        isButton = False
        self.gui(screen, isButton)

        quit = False
        while not quit :
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN and isButton:
                    if self.BUT_START.pressed(pygame.mouse.get_pos()):
                        quit = True
                        break

            self.serClients = self.serObj.get_num_of_clients()
            if self.serClients>0 :
                if not isButton:
                    isButton = True
                    self.BUT_START = mygui.Button()
                    self.BUT_START.create_button(screen, BACK_BUTTON, WIDTH/3, 2*HEIGHT/3, WIDTH/3.2,    HEIGHT/6.85,    0,  "Start", TEXT_BUTTON)

            else:
                if isButton:
                    screen.blit(BG0, (self.BUT_START.rect.left-10,self.BUT_START.rect.top-10), (self.BUT_START.rect.left-10,self.BUT_START.rect.top-10,self.BUT_START.rect.width+20,
                                        self.BUT_START.rect.height+20))
                    del self.BUT_START
                    isButton = False


            screen.blit(BG0, self.TXT_CLIENTS_RECT.topleft, self.TXT_CLIENTS_RECT)
            self.TXT_CLIENTS, self.TXT_CLIENTS_RECT = mygui.print_text('freesansbold.ttf', HEIGHT/30, "# of Clients : "+ str(self.serClients), WHITE, None, WIDTH/2, HEIGHT/4 + HEIGHT/5)
            screen.blit(self.TXT_CLIENTS, self.TXT_CLIENTS_RECT)

            pygame.display.update()

        serverGame.main(screen, self.serObj.clients)
