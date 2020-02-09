# to do: multiple players, multiple decks,
# insurance & even money (both only valid when dealer is showing ace),
# allow doubling down on split? have bet after initial deal?

from colorama import Fore, Style
import random
import copy

suits = ('C','D','H','S')
suitdict = {'C': "\u2663", 'D': "\u2666", 'H': "\u2665", 'S': "\u2660"}

ranks = ('2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A')
rankdict = {'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class card:
    def __init__(self,rank='',suit=''):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        if self.suit == 'D' or self.suit == 'H':
            return str(Fore.RED + self.rank + suitdict[self.suit] + Style.RESET_ALL)
        else:
            return self.rank + suitdict[self.suit]

class hand:
    def __init__(self):
        self.cards = []
        self.val = 0
        self.Aces = 0 # number of aces being treated as 10
    
    def addcard(self,card):
        self.cards.append(card)
        if card.rank == 'A':
            if self.val <= 10:
                self.val += 11
                self.Aces += 1
            elif self.val > 10:
                self.val += 1
        else:
            self.val += rankdict[card.rank]
        
        # fix problems with overvalued aces
        if self.val > 21 and self.Aces > 0:
            if self.val <= 21 + (self.Aces - 1)*10:
                self.val -= (self.Aces - 1)*10
                self.Aces = 1
            elif self.val > 21 + (self.Aces - 1)*10:
                self.val -= (self.Aces)*10
                self.Aces = 0

def seewhowon(ph,dh):
    if (ph.val > dh.val and ph.val <= 21) or (ph.val <= 21 and dh.val > 21):
        print('You win')
        return 1
    elif (ph.val < dh.val and dh.val <= 21) or (dh.val <= 21 and ph.val > 21) or (dh.val > 21 and ph.val > 21):
        print('You lose')
        return -1
    else:
        print('It\'s a tie')
        return 0

fulldeck = list()
for ss in suits:
    for rr in ranks:
        fulldeck.append(card(rr,ss))        
tempdeck = copy.deepcopy(fulldeck)

pile = 1000
print('\nWelcome to Blackjack. Enter ctrl+d to quit')
while pile > 0:
    phand = hand()
    dhand = hand()
    bet = '0'
    surrendered = False
    NBJ = False
    paction = ''
    
    print('\n==================================')
    while True:
        print('You have', pile, 'chips')
        bet = input('How much do you want to bet? ')
        if bet == 'q':
            raise SystemExit
        bet = int(bet)
        if bet > pile or bet < 0:
            print('Bad input')
            continue
        else:
            break
    
    # initial deal. delete "0,"
    for _ in range(0,2):
        tempcard = random.choice(tempdeck)
        phand.addcard(tempcard)
        tempdeck.remove(tempcard)
        
        tempcard = random.choice(tempdeck)
        dhand.addcard(tempcard)
        tempdeck.remove(tempcard)
    
    # inital display of hands. dealer's second card is hidden
    print('\nYour hand [', phand.cards[0], 'and', phand.cards[1], ']; value =', phand.val)
    print('Dealer\'s hand [', dhand.cards[0], 'and ?? ]; value = ??')

    # check for natural blackjack. make it part of hand class
    if phand.val == 21 and dhand.val < 21:
        print('You got a natural blackjack')
        NBJ = True
    elif phand.val == 21 and dhand.val == 21:
        print('You both got natural blackjacks')

    # add code allowing only h, s, or q after the first loop
    while phand.val < 21:
        paction = input('h = hit, s = stand, d = double down, t = split, r = surrender: ')
        if paction == 's':
            break
        elif paction == 'r':
            surrendered = True
            break
        elif paction == 'i' and dhand.cards[0].rank != 'A':
            print('Can\'t choose this option')
            continue
        elif paction == 'i' and dhand.cards[0].rank == 'A':
            # add something for this; changes whether player has NBJ or not 
            break
        elif paction == 'h':
            tempcard = random.choice(tempdeck)
            phand.addcard(tempcard)
            tempdeck.remove(tempcard)
            print('Your hand [', *phand.cards, ']; value =', phand.val)
            if phand.val == 21:
                print('You got 21')
                break
            elif phand.val > 21:
                print('You busted')
                break
        elif (paction == 'd' or paction == 't') and (pile < 2*bet):
            print('Don\'t have enough chips for this option')
            continue
        elif paction == 'd':
            bet *= 2
            tempcard = random.choice(tempdeck)
            phand.addcard(tempcard)
            tempdeck.remove(tempcard)
            print('Your hand: [', *phand.cards, ']; value =', phand.val)
            if phand.val == 21:
                print('You got 21')
            elif phand.val > 21:
                print('You busted')
            break
        elif paction == 't' and phand.cards[0].rank != phand.cards[1].rank:
            print('Can\'t split this hand')
            continue
        elif paction == 't' and phand.cards[0].rank == phand.cards[1].rank:
            phand1 = hand()
            phand1.addcard(phand.cards[0])
            tempcard = random.choice(tempdeck)
            phand1.addcard(tempcard)
            tempdeck.remove(tempcard)
            while True:
                print('\nYour first hand: [', *phand1.cards, ']; value =', phand1.val)
                paction1 = input('Hit or stand? ')
                if paction1 != 'h': break
                elif paction1 == 'h':
                    tempcard = random.choice(tempdeck)
                    phand1.addcard(tempcard)
                    tempdeck.remove(tempcard)
                    if phand1.val == 21:
                        print('First hand got 21')
                        break
                    elif phand1.val > 21:
                        print('First hand busted')
                        break
                
            phand2 = hand()
            phand2.addcard(phand.cards[1])
            tempcard = random.choice(tempdeck)
            phand2.addcard(tempcard)
            tempdeck.remove(tempcard)
            while True:
                print('\nYour second hand: [', *phand2.cards, ']; value =', phand2.val)
                paction2 = input('Hit or stand? ')
                if paction2 != 'h': break
                elif paction2 == 'h':
                    tempcard = random.choice(tempdeck)
                    phand2.addcard(tempcard)
                    tempdeck.remove(tempcard)
                    if phand2.val == 21:
                        print('Second hand got 21')
                        break
                    elif phand2.val > 21:
                        print('Second hand busted')
                        break
            break

    # dealer goes last. can add code to change hit/stand choice if he has 17 with an ace
    print('Dealer\'s hand: [', dhand.cards[0], 'and', dhand.cards[1], ']; value =', dhand.val)       
    while dhand.val < 17 and NBJ == False and surrendered == False:
        tempcard = random.choice(tempdeck)
        dhand.addcard(tempcard)
        tempdeck.remove(tempcard)
        print('Dealer\'s hand: [', *dhand.cards, ']; value =', dhand.val)
        if dhand.val == 21:
            print('Dealer got 21')
            break
        elif dhand.val > 21:
            print('Dealer busts')
            break
            
    # see who won
    if paction == 's' or paction == 'h' or paction == 'd':
        pile += (bet*seewhowon(phand,dhand))
    elif NBJ == True:
        pile += int(1.5*bet)
    elif paction == 'r':
        pile -= int(0.5*bet)
    elif paction == 't':
        pile += (bet*seewhowon(phand1,dhand)) + (bet*seewhowon(phand2,dhand))
    
    if pile == 0:
        print('You are out of chips')
        break
    # reshuffle the deck
    tempdeck = copy.deepcopy(fulldeck)