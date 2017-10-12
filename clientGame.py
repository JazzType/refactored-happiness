import sys, pygame, mygui, serverThread, time, player, json, main
from pygame.locals import *
from constants import *
from operator import sub
from graphics import *


class ClientGame:
    def __init__(self, clientSocket, screen):

        print "Inside ClientGame : init method"

        # self.test(screen)
        self.main(clientSocket, screen)


    def recv(self, clientSocket):


        jsonData = clientSocket.recv(4196)
        if not jsonData:
            print "No data received from server.\nRestarting Game."
            main.Begin()
            sys.exit()

        data = jsonData.split("::")
        jsonCards = data[0]
        self.exTurn = self.turn  #Keeping last player's turn
        self.myTurn = int(data[1])
        jsonPlayers = data[2]
        jsonTblCards= data[3]
        jsonThings = data[4]
        self.winners = data[5]

        self.myCards = json.loads(jsonCards)
        self.tableCards = json.loads(jsonTblCards)
        self.winners = json.loads(self.winners)
        self.things = json.loads(jsonThings)
        self.turn = int(self.things[0])
        self.numberOfPlayers = int(self.things[1])
        self.exPot = self.pot    #Keeping the previous round's pot
        self.pot = int(self.things[2])
        self.toCallAmount = int(self.things[3])
        self.infoFlag = int(self.things[4])
        self.winCards = self.things[5]
        self.maxBet = self.things[6]
        self.resultRating = int(self.things[7])

        jsonPlayers = json.loads(jsonPlayers)
        self.players = {0:[]}
        for key in jsonPlayers:
            obj = player.Player(jsonPlayers[key]['turn'], jsonPlayers[key]['name'])
            obj.fold = jsonPlayers[key]['fold']
            obj.pot = jsonPlayers[key]['pot']
            obj.money = jsonPlayers[key]['money']
            obj.currentRoundBet = jsonPlayers[key]['currentRoundBet']
            obj.isActive = jsonPlayers[key]['isActive']

            self.players[key] = obj

        self.NAMES = []
        self.MONEY = []
        self.ROUNDBET = []
        for o in range(self.numberOfPlayers):
            self.NAMES.append(self.players[str(o)].name)
            self.MONEY.append("$"+str(self.players[str(o)].money))
            self.ROUNDBET.append("$"+str(self.players[str(o)].currentRoundBet))

    def main(self, clientSocket, screen):

        self.turn = -1
        self.pot = 0
        g = Graphics()

        while 1:

            self.recv(clientSocket)
            self.update_game()
            g.order_players(self.myTurn, self.numberOfPlayers)
            g.init_gui(screen, self.myTurn, self.turn, self.numberOfPlayers, self.myCards, self.infoFlag, self.MONEY, self.NAMES, self.ROUNDBET)
            self.update_screen(screen, g)

            if self.myTurn == self.turn:

                g.create_buttons(screen, self.toCallAmount) #Creating all 4 buttons
                slider1 = mygui.Slider(screen,(450,450),(self.toCallAmount, self.maxBet))    #Creating the raise slider

                pygame.display.update() #Displaying the buttons

                quit = False
                while not quit:
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit()

                        #Slider event handle
                        slider1.event_slider(event, pygame.mouse.get_pos())
                        slider1.slider_update(screen)

                        #Mouse Hover handling
                        g.mouse_hover(screen, self.toCallAmount)

                        #Mouse click handling
                        isSend, state = g.mouse_click(screen, event, self.toCallAmount, self.maxBet, slider1.getValue())

                        #Sending data if button clicked
                        if isSend == True:
                            data = clientSocket.send(str(state))
                            if not data:
                                print "Server not receiving data.\nRestarting Game."
                                main.Begin()
                                sys.exit()

                            quit = True
                            break

            else:
                g.remove_buttons(screen)
                g.create_transparent_buttons(screen)
                g.slider_remove(screen)

                pygame.display.update()

            g.end_hand(screen, self.infoFlag, self.winners, self.winCards, self.resultRating)   #Result and winner display
            pygame.display.update()

    def update_screen(self, screen, g):

        print "Turn ", self.turn, "ExTurn ", self.exTurn
        g.draw_boy(screen, self.turn, self.myTurn, self.turn)    #Redrawing the current player's image
        g.draw_boy_box(screen, self.turn, self.MONEY[self.turn], self.NAMES[self.turn])    #Redrawing current player's text box

        g.draw_boy(screen, self.exTurn, self.myTurn, self.turn)   #Redrawing the last player's image
        g.draw_boy_box(screen, self.exTurn, self.MONEY[self.exTurn], self.NAMES[self.exTurn])   #Redrawing the last player's text box

        for i in range(self.numberOfPlayers):
            g.draw_boy_bet(screen, i, self.ROUNDBET[i])    #Draw every player's current round bet.

        g.draw_table_cards(screen, self.infoFlag, self.tableCards)    #Draw the cards to be placed on table.

        #Display pot
        if self.pot>0 and self.pot-self.exPot>0:
            g.pot_animation(screen, self.pot)


    def update_game(self):
        self.MONEY = []
        self.ROUNDBET= []
        for o in range(self.numberOfPlayers):
            self.MONEY.append("$"+str(self.players[str(o)].money))
            self.ROUNDBET.append("$"+str(self.players[str(o)].currentRoundBet))

    def test(self, screen):

        self.players = {0:[]}
        self.players['0'] = player.Player(0,"Safal")
        self.players['1'] = player.Player(1,"Avantika")
        self.players['2'] = player.Player(2,"Lalit")
        self.players['3'] = player.Player(3,"Kariryaa")
        self.players['4'] = player.Player(4,"Aneja")
        self.players['5'] = player.Player(5,"Raman")
        self.players['6'] = player.Player(6,"Ankita")
        self.players['7'] = player.Player(7,"Bhavya")
        self.players['8'] = player.Player(8,"Bhavya")
        self.players['9'] = player.Player(9,"Bhavya")
        self.players['10'] = player.Player(10,"Bhavya")
        self.players['11'] = player.Player(11,"Bhavya")
        self.players['12'] = player.Player(12,"Bhavya")

        self.players['0'].currentRoundBet = 10
        self.players['1'].currentRoundBet = 20

        self.myTurn = 3
        self.turn = 2
        self.numberOfPlayers = 12

        self.winner = 1
        self.winCards = (('H',2),('C',9))
        self.toCallAmount = 20
        self.pot = 100
        self.myCards = (('C',5),('H',7))
        self.tableCards = [('H',9),('D',2),('C',12),('S',7),('H',11)]

        self.infoFlag = 0
        self.NAMES = []
        self.MONEY = []
        self.ROUNDBET=[]
        for i in range(self.numberOfPlayers):
            self.NAMES.append(self.players[str(i)].name)
            self.MONEY.append("$"+str(self.players[str(i)].money))
            self.ROUNDBET.append("$"+str(self.players[str(i)].currentRoundBet))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption(CAPTION)
    screen = pygame.display.set_mode((WIDTH,HEIGHT))#Create Window
    ClientGame(None, screen)
