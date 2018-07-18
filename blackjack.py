import tkinter
import random


def load_cards(cards_image):
    suits = ['diamond', 'spade', 'club', 'heart']
    facecards = ['jack', 'queen', 'king']
    extension = 'png'

    for suit in suits:
        for card in range(1, 11):
            name = 'cards/{}_{}.{}'.format(str(card), suit, extension)
            image = tkinter.PhotoImage(file=name)
            cards_image.append((card, image,))

        for face in facecards:
            name = 'cards/{}_{}.{}'.format(face, suit, extension)
            image = tkinter.PhotoImage(file=name)
            cards_image.append((10, image,))


def deal_cards(frame):
    next_card = deck.pop(0)
    tkinter.Label(frame, image=next_card[1], relief='sunken').pack(side='left')
    deck.append(next_card)
    return next_card


ace_card = False
player_cards_drawn = []
dealer_cards_drawn = []
noGamesPlayed = 0


def calculate_scores(cards_drawn):
    score = 0
    global ace_card
    for cards_value in cards_drawn:
        if cards_value == 1 and not ace_card:
            cards_value = 11
            ace_card = True
        score += cards_value
        if score > 21 and ace_card:
            score -= 10
            ace_card = False
    return score


def deal_player():
    player_cards_drawn.append(deal_cards(playerCardFrame)[0])
    player_score = calculate_scores(player_cards_drawn)
    if player_score > 21:
        result.set("Dealer Wins")
    playerScoreLabel.set(player_score)


def deal_dealer():
    dealer_score = calculate_scores(dealer_cards_drawn)
    while 0 < dealer_score < 17:
        dealer_cards_drawn.append(deal_cards(dealerCardFrame)[0])
        dealer_score = calculate_scores(dealer_cards_drawn)
        dealerScoreLabel.set(dealer_score)
    player_score = calculate_scores(player_cards_drawn)
    if player_score > 21:
        result.set('Dealer wins')
    elif dealer_score > 21 or player_score > dealer_score:
        result.set('Player Wins')
    elif dealer_score > player_score:
        result.set('Dealer Wins')
    else:
        result.set('Draw')


def newgame():
    global player_cards_drawn
    global dealer_cards_drawn
    global playerCardFrame
    global dealerCardFrame
    global noGamesPlayed

    player_cards_drawn = []
    dealer_cards_drawn = []
    playerCardFrame.destroy()
    dealerCardFrame.destroy()

    playerScoreLabel.set(0)
    dealerScoreLabel.set(0)
    result.set('Result')

    dealerCardFrame = tkinter.Frame(cardFrame, background='green')
    dealerCardFrame.grid(row=0, column=1, rowspan=2, sticky='ew')

    playerCardFrame = tkinter.Frame(cardFrame, background='green')
    playerCardFrame.grid(row=2, column=1, rowspan=2, sticky='ew')

    deal_player()
    deal_player()
    dealer_cards_drawn.append(deal_cards(dealerCardFrame)[0])
    dealerScoreLabel.set(calculate_scores(dealer_cards_drawn))
    noGamesPlayed += 1
    game_numbers.set(noGamesPlayed)


def shuffle():
    random.shuffle(deck)


mainWindow = tkinter.Tk()
mainWindow.title("Blackjack")
mainWindow.geometry('680x480')
mainWindow.configure(background='green')

topFrame = tkinter.Frame(mainWindow, background='green',)
topFrame.grid(row=0, column=0, sticky='n', columnspan=4)
result = tkinter.StringVar()
resultLabel = tkinter.Label(topFrame, text='Result', textvariable=result, background='green', fg='white')
resultLabel.grid(row=0, column=0, sticky='new')
result.set('Result')
game_numbers = tkinter.IntVar()
tkinter.Label(topFrame, text='Games Played:', background='green', fg='white').grid(row=0, column=2, sticky='n', columnspan=2)
tkinter.Label(topFrame, textvariable=game_numbers, background='green', fg='white').grid(row=0, column=4, sticky='n')


cardFrame = tkinter.Frame(mainWindow, background='green')
cardFrame.grid(row=1, column=1, rowspan=2, columnspan=3, sticky='ew')
cardFrame.configure(relief='sunken', border=2)

# **********Dealer*****************
dealerScoreLabel = tkinter.IntVar()
tkinter.Label(cardFrame, text='Dealer', background='green', fg='white').grid(row=0, column=0, sticky='w')
tkinter.Label(cardFrame, textvariable=dealerScoreLabel, background='green', fg='white').grid(row=1, column=0, sticky='w')

dealerCardFrame = tkinter.Frame(cardFrame, background='green')
dealerCardFrame.grid(row=0, column=1, rowspan=2, sticky='ew')

# **********Player*****************
playerScoreLabel = tkinter.IntVar()
tkinter.Label(cardFrame, text='Player', background='green', fg='white').grid(row=2, column=0, sticky='w')
tkinter.Label(cardFrame, textvariable=playerScoreLabel, background='green', fg='white').grid(row=3, column=0, sticky='w')

playerCardFrame = tkinter.Frame(cardFrame, background='green')
playerCardFrame.grid(row=2, column=1, rowspan=2, sticky='ew')

# **********Buttons*****************
buttonFrame = tkinter.Frame(mainWindow)
buttonFrame.grid(row=3, column=0, sticky='w', columnspan=3)
dealerButton = tkinter.Button(buttonFrame, text='Dealer', command=deal_dealer).grid(row=0, column=0)
playerButton = tkinter.Button(buttonFrame, text='Player', command=deal_player).grid(row=0, column=1)
new_gameButton = tkinter.Button(buttonFrame, text='New Game', command=newgame).grid(row=0, column=2)
shuffleButton = tkinter.Button(buttonFrame, text='Shuffle', command=shuffle).grid(row=0, column=3)

cards = []
load_cards(cards)
deck = list(cards)
shuffle()
print(deck)
newgame()
mainWindow.mainloop()
