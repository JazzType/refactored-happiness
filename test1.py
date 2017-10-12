from player import *

players = {0:[]}
start = 0
numberOfPlayers = 0
smallBlind = 10
bigBlind = smallBlind*2
def main():
    numberOfPlayers = 5
    for i in range(0,5):
        players[i]=Player(i)

    for i in range(0,5):
        players[i].display()

def func():
    print numberOfPlayers

if __name__ == '__main__':
    main()
    func()
