import pygame, time
from constants import *
from pygame.locals import *

class Graphics:

    #List of coordinates for the 12 boys sitting at the table
    BOY0 = (70,30);BOY1 = (170,0);BOY2 = (270,0);BOY3 = (370,0)
    BOY4 = (470,30);BOY5 = (510,140);BOY6 = (470,250);BOY7 = (370,280)
    BOY8 = (270,280);BOY9 = (170,280);BOY10= (70,250);BOY11= (30,140)
    BOYS = (BOY0, BOY1, BOY2, BOY3, BOY4, BOY5, BOY6, BOY7, BOY8, BOY9, BOY10, BOY11 )

    #List of coordinates for the button and textboxes below player picture
    BOYBUT = []
    BOYTXTBOX = [] # Tuple of 3 coordinates. Two different y coordinates and one same x coordinate for the text (x, y1, y2)
    BUTROUNDBET = [(115,150),(175,120),(275,120),(375,120),(445,150),(455,200),(425,235),(175,265),(275,265),(375,265),(135,235),(105,200)]
    for i in range(12):
        BOYBUT.append((BOYS[i][0]+5, BOYS[i][1]+86))
        BOYTXTBOX.append((BOYS[i][0]+50, BOYS[i][1]+94,BOYS[i][1]+108))

    IMGBOY1 = pygame.image.load("images/boy1.png");IMGBOY1 = pygame.transform.scale(IMGBOY1, PICSIZE)
    IMGBOY2 = pygame.image.load("images/boy2.png");IMGBOY2 = pygame.transform.scale(IMGBOY2, PICSIZE)
    IMGBOY3 = pygame.image.load("images/boy3.png");IMGBOY3 = pygame.transform.scale(IMGBOY3, PICSIZE)
    IMGBOY4 = pygame.image.load("images/boy4.png");IMGBOY4 = pygame.transform.scale(IMGBOY4, PICSIZE)
    ALPHA = 180
    IMGBUT1 = pygame.image.load("images/but1.png");IMGBUT1 = pygame.transform.scale(IMGBUT1, (90,30))
    IMGBUT2 = pygame.image.load("images/but0.png");IMGBUT2 = pygame.transform.scale(IMGBUT2, (120,30))
    IMGBUT3 = pygame.image.load("images/but4.png");IMGBUT3 = pygame.transform.scale(IMGBUT3, (200,50))
    IMGBUT4 = pygame.image.load("images/but6.png");IMGBUT4 = pygame.transform.scale(IMGBUT4, (120,30))
    IMGBUT4.fill((255, 255, 255, ALPHA), None, pygame.BLEND_RGBA_MULT)
    IMGBUT5 = pygame.image.load("images/but6.png");IMGBUT5 = pygame.transform.scale(IMGBUT5, (120,30))
    IMGBUT6 = pygame.image.load("images/but7.png");IMGBUT6 = pygame.transform.scale(IMGBUT6, (120,30))
    IMGBUT7 = pygame.image.load("images/but3.png");IMGBUT7 = pygame.transform.scale(IMGBUT7, (90,30))
    IMGBUT8 = pygame.image.load("images/but8.png");IMGBUT8 = pygame.transform.scale(IMGBUT8, (90,30))
    IMGBUT9 = pygame.image.load("images/but7.png");IMGBUT9 = pygame.transform.scale(IMGBUT9, (120,30))
    IMGBUT9.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)

    BUTSTR = ["Check", "Fold", "All-in", "Raise"]
    BUTXY = [(198, 405, 120, 30),(322, 405, 120, 30),(198, 439, 120, 30),(322, 439, 120, 30)]


    def __init__(self):
        self.BUTLIST = [mygui.Button(),mygui.Button(),mygui.Button(),mygui.Button()]
        self.CARDDRAWN = [False,False,False]    #List to check whether flop, turn and river cards are drawn
        self.BUTHOVER = [False, False, False, False] #List to maintain which buttons are being hovered currently
        self.HANDBEGIN = False  #To make sure init_gui() is called just once every hand
        self.ORDERED = False    #To make sure order_players() is called just once

        self.load_cards()

    def order_players(self, myturn, numberOfPlayers):
        if self.ORDERED : return
        order = {0:[]}
        fo = list(ORDER[:numberOfPlayers])
        fo.sort()
        while True:
            if fo[0] == 8:  #8 is the middle player for now
                break
            temp = fo[0]
            del fo[0]
            fo.append(temp)
        fu = range(0, numberOfPlayers)
        while True:
            if fu[0] == myturn:
                break
            temp = fu[0]
            del fu[0]
            fu.append(temp)
        for i in range(0, numberOfPlayers):
            order[fu[i]] = fo[i]

        self.turnMap = order
        self.ORDERED = True

    def init_gui(self, screen, myTurn, turn, numberOfPlayers, myCards, infoFlag, MONEY, NAMES, ROUNDBET) :
        if self.HANDBEGIN : return

        self.draw_bg(screen)   #Draw screen background
        self.draw_table(screen)    #Draw poker table

        #Putting players across the table
        for i in range(numberOfPlayers):
            self.draw_boy(screen,i, myTurn, turn)

        #Putting textbuttons
        for i in range(numberOfPlayers):
            self.draw_boy_box(screen, i, MONEY[i], NAMES[i])

        #Putting betButtons
        for i in range(numberOfPlayers):
            self.draw_boy_bet(screen, i, ROUNDBET[i])

        #Draw init cards
        self.draw_init_cards(screen, myCards, infoFlag)

        #Marking that table cards are not drawn yet.
        for i in range(3):
            self.CARDDRAWN[i] = False
        self.HANDBEGIN = True

    def end_hand(self, screen, infoFlag, winners, winCards, resultRating):
        if infoFlag != 10:
            return
        #For debugging
        print "Hand completed!"
        print "Winners are : " + str(winners)

        #Winner boxes
        self.draw_win_box(screen, winners)

        #Winner cards
        self.draw_winner_cards(screen, winCards)

        #Result
        string = self.result_string(resultRating)
        self.draw_result(screen, string)

        self.HANDBEGIN = False

        pygame.display.update()
        time.sleep(4)

    def result_string(self, rating):
        mapping = {1 : "High Card", 2: "One Pair", 3: "Two Pair", 4: "Three of a kind", 5: "Straight", 6: "Flush",
                    7: "Full House", 8: "Four of a kind", 9: "Straight Flush", 10: "Royal Flush"}

        return mapping[rating]

    def load_cards(self):
        self.cardHearts = []
        self.cardDiamonds = []
        self.cardClubs = []
        self.cardSpades = []
        self.cardHeartsB = []
        self.cardDiamondsB = []
        self.cardClubsB = []
        self.cardSpadesB = []

        for j in range(4):
            for i in range(13):
                card1 = pygame.Surface((CARDLENIMG,CARDWIDIMG), pygame.SRCALPHA, 32)   #Card size 43 * 62
                card1.blit(CARDS, (0, 0), (i*44, j*63, CARDLENIMG, CARDWIDIMG))        #Spacing of 1 pixel between images

                if j == 0:
                    self.cardHeartsB.append(card1)
                    self.cardHearts.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))     #Size is 36 * 49
                elif j == 1:
                    self.cardDiamondsB.append(card1)
                    self.cardDiamonds.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))
                elif j == 2:
                    self.cardClubsB.append(card1)
                    self.cardClubs.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))
                else :
                    self.cardSpadesB.append(card1)
                    self.cardSpades.append(pygame.transform.scale(card1, (CARDLEN,CARDWID)))


    def init_box_coord(self):
        pass

    def draw_bg(self, screen):
        screen.blit(BG1, (0,0))

    def draw_table(self, screen):
        screen.blit(PKT1, TBLTOPLEFT)

    def draw_boy(self, screen, id, myTurn, turn):
        if id == -1 : return
        if id == myTurn and id == turn :
            screen.blit(Graphics.IMGBOY3, Graphics.BOYS[self.turnMap[id]])
        elif id == myTurn and id != turn :
            screen.blit(Graphics.IMGBOY1, Graphics.BOYS[self.turnMap[id]])
        elif id != myTurn and id == turn :
            screen.blit(Graphics.IMGBOY4, Graphics.BOYS[self.turnMap[id]])
        else :
            screen.blit(Graphics.IMGBOY2, Graphics.BOYS[self.turnMap[id]])


    def draw_boy_box(self, screen, i, money, name):
        if i == -1: return
        screen.blit(Graphics.IMGBUT1, Graphics.BOYBUT[self.turnMap[i]])

        textMoney, textMoneyRect = mygui.print_text('freesansbold.ttf', 13, str(money), WHITE, None,Graphics.BOYTXTBOX[self.turnMap[i]][0],Graphics.BOYTXTBOX[self.turnMap[i]][2] )
        textName, textNameRect = mygui.print_text('freesansbold.ttf', 13, name, WHITE, None,Graphics.BOYTXTBOX[self.turnMap[i]][0],Graphics.BOYTXTBOX[self.turnMap[i]][1] )
        screen.blit(textMoney, textMoneyRect)
        screen.blit(textName, textNameRect)

    def draw_win_box(self, screen, winners):
        for i in winners:
            screen.blit(Graphics.IMGBUT7, Graphics.BOYBUT[self.turnMap[i]])
            textWin, textWinRect = mygui.print_text('freesansbold.ttf', 16, "WINNER!", WHITE, None,Graphics.BOYTXTBOX[self.turnMap[i]][0],Graphics.BOYTXTBOX[self.turnMap[i]][2]-5 )
            screen.blit(textWin, textWinRect)

    def draw_result(self, screen, result):
        mygui.Button().create_button_image(screen, Graphics.IMGBUT9, int(TBLWIDTH/2 - (3.5*len(result)))+80, 113 , 7*len(result), 12, result, 11, WHITE)

    def draw_boy_bet(self, screen, i, money):
        obj = mygui.Button()
        screen.blit(PKT1,(Graphics.BUTROUNDBET[self.turnMap[i]][0], Graphics.BUTROUNDBET[self.turnMap[i]][1]),(Graphics.BUTROUNDBET[self.turnMap[i]][0]-80, Graphics.BUTROUNDBET[self.turnMap[i]][1]-80,20+6*11,20))
        if money!="$0":
            obj.create_button_image(screen, Graphics.IMGBUT8, Graphics.BUTROUNDBET[self.turnMap[i]][0], Graphics.BUTROUNDBET[self.turnMap[i]][1] , 20+6*len(money), 15, money, 12, WHITE)


    def draw_big_card(self, screen, card, (posX, posY)):
        if card[0] == 'C':
            if card[1] == 14:
                screen.blit(self.cardClubsB[0],(posX,posY))
            else :
                screen.blit(self.cardClubsB[card[1]-1],(posX,posY))

        elif card[0] == 'H':
            if card[1] == 14:
                screen.blit(self.cardHeartsB[0],(posX,posY))
            else :
                screen.blit(self.cardHeartsB[card[1]-1],(posX,posY))

        elif card[0] == 'D':
            if card[1] == 14:
                screen.blit(self.cardDiamondsB[0],(posX,posY))
            else :
                screen.blit(self.cardDiamondsB[card[1]-1],(posX,posY))

        elif card[0] == 'S':
            if card[1] == 14:
                screen.blit(self.cardSpadesB[0],(posX,posY))
            else :
                screen.blit(self.cardSpadesB[card[1]-1],(posX,posY))

        else : print "Wrong suit! Check your card. :- ",card


    def draw_card(self, screen, card, (posX, posY)):
        if card[0] == 'C':
            if card[1] == 14:
                screen.blit(self.cardClubs[0],(posX,posY))
            else :
                screen.blit(self.cardClubs[card[1]-1],(posX,posY))

        elif card[0] == 'H':
            if card[1] == 14:
                screen.blit(self.cardHearts[0],(posX,posY))
            else :
                screen.blit(self.cardHearts[card[1]-1],(posX,posY))

        elif card[0] == 'D':
            if card[1] == 14:
                screen.blit(self.cardDiamonds[0],(posX,posY))
            else :
                screen.blit(self.cardDiamonds[card[1]-1],(posX,posY))

        elif card[0] == 'S':
            if card[1] == 14:
                screen.blit(self.cardSpades[0],(posX,posY))
            else :
                screen.blit(self.cardSpades[card[1]-1],(posX,posY))

        else : print "Wrong suit! Check your card. :- ",card

    def draw_init_cards(self, screen, myCards, infoFlag):
        INITCARDS = [(50,410), (95,410)]
        if infoFlag == 0:
            self.draw_big_card(screen, myCards[0],INITCARDS[0])
            self.draw_big_card(screen, myCards[1],INITCARDS[1])


    def draw_winner_cards(self, screen, winCards):
        WINCARDS = [(280,125), (320,125)]
        self.draw_card(screen, winCards[0],WINCARDS[0])
        self.draw_card(screen, winCards[1],WINCARDS[1])

    def draw_table_cards(self, screen, infoFlag, tableCards):
        MYCARDXY = [(50,410),(95,410)]
        TABLECARDXY = [(220,180),(260,180),(300,180),(340,180),(380,180)]

        if infoFlag == 1:
             if not self.CARDDRAWN[0]:
                self.draw_card(screen, tableCards[0],(220,180))
                self.draw_card(screen, tableCards[1],(260,180))
                self.draw_card(screen, tableCards[2],(300,180))
                self.CARDDRAWN[0] = True

        elif infoFlag == 2:
             if not self.CARDDRAWN[1]:
                self.draw_card(screen, tableCards[3],(340,180))
                self.CARDDRAWN[1] = True
        elif infoFlag == 3:
             if not self.CARDDRAWN[2]:
                self.draw_card(screen, tableCards[4],(380,180))
                self.CARDDRAWN[2] = True
        elif infoFlag == 10:
            for i in range(5):
                self.draw_card(screen, tableCards[i],TABLECARDXY[i])
            for i in range(3):
                self.CARDDRAWN[i] = True


    def pot_animation(self, screen, num):
        tempList = []
        for i in range(20,0,-1):
            tempList.append(num/i)

        screen.blit(PKT1, (250,int(2*TBLHEIGHT/3+80)),(170,int(2*TBLHEIGHT/3),120,20) )
        testPot = mygui.Button()
        for i in tempList:
            string = "$"+str(i)
            screen.blit(PKT1, (int(TBLWIDTH/2 - (10+3.5*len(string))+80), 2*TBLHEIGHT/3+80), (int(TBLWIDTH/2 - (10+3.5*len(string))),2*TBLHEIGHT/3,20+7*len(string), 20))
            testPot.create_button_image(screen, Graphics.IMGBUT6, int(TBLWIDTH/2 - (10+3.5*len(string)))+80, 2*TBLHEIGHT/3+80 , 20 + 7*len(string), 20, string, 13, WHITE)
            pygame.display.update()
            time.sleep(0.02)

    def mouse_hover(self, screen, toCallAmount):
        MOUSEPOS = pygame.mouse.get_pos()
        for o in range(4):
            if self.BUTLIST[o].hover(MOUSEPOS):
                if not self.BUTHOVER[o]:
                    screen.blit(BG1,(Graphics.BUTXY[o][0],Graphics.BUTXY[o][1]),Graphics.BUTXY[o])
                    if o==0 and toCallAmount != 0:
                        strCall = "Call $"+ str(toCallAmount)
                        self.BUTLIST[o].create_button_image(screen, Graphics.IMGBUT4, Graphics.BUTXY[o][0], Graphics.BUTXY[o][1], Graphics.BUTXY[o][2], Graphics.BUTXY[o][3], strCall, 16, WHITE)
                    else:
                        self.BUTLIST[o].create_button_image(screen, Graphics.IMGBUT4, Graphics.BUTXY[o][0], Graphics.BUTXY[o][1], Graphics.BUTXY[o][2], Graphics.BUTXY[o][3], Graphics.BUTSTR[o], 16, WHITE)

                    pygame.display.update()
                    self.BUTHOVER[o] = True
            else:
                if self.BUTHOVER[o]:
                    if o==0 and toCallAmount != 0:
                        strCall = "Call $"+ str(toCallAmount)
                        self.BUTLIST[o].create_button_image(screen, Graphics.IMGBUT5, Graphics.BUTXY[o][0], Graphics.BUTXY[o][1], Graphics.BUTXY[o][2], Graphics.BUTXY[o][3], strCall, 16, WHITE)
                    else:
                        self.BUTLIST[o].create_button_image(screen, Graphics.IMGBUT5, Graphics.BUTXY[o][0], Graphics.BUTXY[o][1], Graphics.BUTXY[o][2], Graphics.BUTXY[o][3], Graphics.BUTSTR[o], 16, WHITE)


                    pygame.display.update()
                    self.BUTHOVER[o] = False

    def mouse_click(self, screen, event, toCallAmount, maxBet, raiseValue):
        isSend = False
        state = None
        if event.type == MOUSEBUTTONDOWN:
            if self.BUTLIST[0].pressed(pygame.mouse.get_pos()):
                state = toCallAmount
                isSend = True
            elif self.BUTLIST[1].pressed(pygame.mouse.get_pos()):
                state = -1
                isSend = True
            elif self.BUTLIST[2].pressed(pygame.mouse.get_pos()):
                state = maxBet
                isSend = True
            elif self.BUTLIST[3].pressed(pygame.mouse.get_pos()):
                state = raiseValue
                isSend = True

        return isSend, state

    def create_buttons(self, screen, toCallAmount):
        for o in range(4):
            if o==0 and toCallAmount != 0:
                strCall = "Call $"+ str(toCallAmount)
                self.BUTLIST[o].create_button_image(screen, Graphics.IMGBUT5, Graphics.BUTXY[o][0], Graphics.BUTXY[o][1], Graphics.BUTXY[o][2], Graphics.BUTXY[o][3], strCall, 16, WHITE)
            else:
                self.BUTLIST[o].create_button_image(screen, Graphics.IMGBUT5, Graphics.BUTXY[o][0], Graphics.BUTXY[o][1], Graphics.BUTXY[o][2], Graphics.BUTXY[o][3], Graphics.BUTSTR[o], 16, WHITE)


    def slider_remove(self, screen):
        screen.blit(BG1,(440,425),(440,425,200,65))
        pygame.display.update()

    def create_transparent_buttons(self, screen):
        #Create new transparent buttons
        for o in range(4):
            self.BUTLIST[o].create_button_image(screen, Graphics.IMGBUT4, Graphics.BUTXY[o][0], Graphics.BUTXY[o][1], Graphics.BUTXY[o][2], Graphics.BUTXY[o][3], Graphics.BUTSTR[o], 16, WHITE)

    def remove_buttons(self, screen):
        screen.blit(BG1,(198,405),(198,405,244,64)) #Removing any existing button images
