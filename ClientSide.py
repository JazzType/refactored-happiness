import sys, pygame, mygui, clientThread, time, clientGame
from pygame.locals import *
from constants import *

class PokerClient:

    def __init__(self, screen):

        BOXIPWIDTH = WIDTH/3.2
        BOXIPHEIGHT = HEIGHT/16
        BOXPORTWIDTH = WIDTH/3.2
        BOXPORTHEIGHT = HEIGHT/16

        #screen.fill(BACK_SCREEN)
        screen.blit(BG0, (0,0)) #Set background image

        textClient, textClientRect = mygui.print_text('freesansbold.ttf', HEIGHT/15, "Client", WHITE, None, WIDTH/2, HEIGHT/10)
        screen.blit(textClient, textClientRect)

        textIp, textIpRect = mygui.print_text('freesansbold.ttf', HEIGHT/30, "Enter IP : ", WHITE, None, WIDTH/2-BOXIPWIDTH/2-WIDTH/13,HEIGHT/4)
        screen.blit(textIp, textIpRect)

        textPort, textPortRect = mygui.print_text('freesansbold.ttf', HEIGHT/30, "Enter Port : ", WHITE, None, WIDTH/2-BOXPORTWIDTH/2-WIDTH/13,HEIGHT/4+HEIGHT/9.6)
        screen.blit(textPort, textPortRect)

        Button1 = mygui.Button()
        Button1.create_button(screen, BACK_BUTTON, WIDTH/2-WIDTH/6, HEIGHT/2, WIDTH/3, WIDTH/9  ,    0,        "Connect", TEXT_BUTTON)

        input_ip = mygui.TextBox((WIDTH/2-BOXIPWIDTH/2,HEIGHT/4-BOXIPHEIGHT/2,BOXIPWIDTH,BOXIPHEIGHT),command=None,clear_on_enter=True,inactive_on_enter=False)
        input_port = mygui.TextBox((WIDTH/2-BOXPORTWIDTH/2,HEIGHT/4+HEIGHT/10-BOXPORTHEIGHT/2,BOXPORTWIDTH,BOXPORTHEIGHT),command=None,
                        clear_on_enter=True,inactive_on_enter=False, active = False)

        quit = False
        connect = False
        while not quit:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if Button1.pressed(pygame.mouse.get_pos()):
                        connect = True
                        quit = True
                        break
                input_ip.get_event(event)
                input_port.get_event(event)

            input_ip.draw(screen)
            input_port.draw(screen)
            pygame.display.update()

        if connect:
            serIP = input_ip.get_text()
            serPort = input_port.get_text()
            if serIP == "1":
                serIP = "10.42.0.45"
            elif serIP == "2":
                serIP = "172.24.136.242"

            if serPort =="":
                serPort = "1234"
            cliObj = clientThread.ClientThread(str(serIP),int(serPort), screen)

            #Button1.delete_button(screen, BACK_SCREEN)
            screen.blit(BG0, (WIDTH/2-WIDTH/6-10, HEIGHT/2-10), (WIDTH/2-WIDTH/6-10, HEIGHT/2-10,Button1.rect.width+20,Button1.rect.height+20)) #Remove Button surface
            del Button1

            textWait, textWaitRect = mygui.print_text('freesansbold.ttf', HEIGHT/25, "Waiting for server to begin...", WHITE, None, WIDTH/2,HEIGHT/2+HEIGHT/9.6)
            screen.blit(textWait, textWaitRect)
            pygame.display.update()

            begin = cliObj.sock.recv(1024)
            if begin == "begin":
                print "Unpaused"
                clientGame.ClientGame(cliObj.sock, screen)
