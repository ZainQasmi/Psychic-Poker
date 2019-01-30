import itertools
import sys

class Card(object):
    FaceValue = 'A23456789TJQK'
    Suit = 'CDHS'

    def __init__(self, card):
        self.card = card

    def __str__(self):
        return self.card

    def getSuit(self):
        return self.card[1]

    def getFaceValue(self):
        return self.card[0]

class Hand(object):
    # Ranks =        0           1        2            3            4      5       6            7               8
    allRanks = 'highest-card one-pair two-pairs three-of-a-kind straight flush full-house four-of-a-kind straight-flush'.split()

    def __init__(self, cards):
        self.cards = cards
        self.handRank = None

    def __str__(self):
        if not self.handRank:
            self.handRank = self.calculateRank()
        return self.allRanks[self.handRank]
    
    def __int__(self):
        if not self.handRank:
            self.handRank = self.calculateRank()
        return self.handRank

    def __gt__(self,arg):
        return int(self) > int(arg)

    def replace(self, index, card):
        self.cards[index] = card
        self.handRank = None

    # Helper function to return a list of Cards in Hand 
    def printHand(self):
        return [str(a) for a in self.cards]

    # Program engine. Hand rank is calculated here
    def calculateRank(self):
        
        number_of_suits = len(set(map(Card.getSuit,self.cards)))
        FaceValue = '23456789TJQKA'
        FaceValue_straight = 'A23456789TJQK' #Inefficient fix to get right consecutive cards for straight-flush
        figures_list = sorted(map(Card.getFaceValue, self.cards),key=lambda myStr:FaceValue.index(myStr),reverse=True)
        figures_list_straight = sorted(map(Card.getFaceValue, self.cards),key=lambda myStr:FaceValue_straight.index(myStr),reverse=True)
        
        def checkConsecutiveFig(fig_list, isTrue = None):
            for i in range(len(fig_list)-1):
                if isTrue:
                    if not (FaceValue_straight.index(fig_list[i]) - FaceValue_straight.index(fig_list[i+1]) == 1):
                        return False    
                else:
                    if not (FaceValue.index(fig_list[i]) - FaceValue.index(fig_list[i+1]) == 1):
                        return False
            return True

        # Reference for Ranks https://youtu.be/bOyZbYjUcZg - Royal Flush not included for some reason
        setOfPairs = len(set(figures_list))
        if number_of_suits == 1:
            return Hand.allRanks.index('straight-flush') if checkConsecutiveFig(figures_list) else Hand.allRanks.index('flush')
        elif figures_list[0] == figures_list[3] or figures_list[1] == figures_list[4]:
            return Hand.allRanks.index('four-of-a-kind')
        elif figures_list[0] == figures_list[2] and figures_list[3] == figures_list[4]:
            return Hand.allRanks.index('full-house')
        elif figures_list[0] == figures_list[1] and figures_list[2] == figures_list[4]:
            return Hand.allRanks.index('full-house')
        elif checkConsecutiveFig(figures_list_straight, True):
            return Hand.allRanks.index('straight')
        elif figures_list[0] == figures_list[2] or figures_list[1] == figures_list[3] or figures_list[2] == figures_list[4]:
            return Hand.allRanks.index('three-of-a-kind')
        elif setOfPairs == 3:
            return Hand.allRanks.index('two-pairs')
        elif setOfPairs == 4:
            return Hand.allRanks.index('one-pair')
        else:
            return Hand.allRanks.index('highest-card')

# Yields combination of numbers to replace cards with
def getComb(stuff):
    for L in range(0, len(stuff)+1):
        for subset in itertools.combinations(stuff, L):
            if subset:
                yield list(subset)

# Generates combinations of all possible Hands from the given deck and see which has the highest rank
def getBestComb(cards):
    tempBest = Hand(cards[:5])
    for _ in xrange(0, 5):
        for variation in getComb(xrange(0, 5)):
            hand = (Hand(cards[:5]))
            for addFromDeck, removeFromHand in enumerate(variation):
                hand.replace(removeFromHand, cards[5+addFromDeck])
            if hand > tempBest:
                tempBest = hand
    # print ' '.join(Hand.printHand(tempBest)), "lol"
    return ' '.join(Hand.printHand(tempBest)),str(tempBest)

def getProcessed(hand_plus_deck):
    cards_obj_list = map(Card,hand_plus_deck.split())
    bestComb = getBestComb(cards_obj_list)
    if bestComb:
        return bestComb
    else:
        return "Failed"

def main():
    # for line in sys.stdin:
    for line in open(sys.argv[1]):
        lline = list(line.rstrip('\n'))
        bestCards, rank = getProcessed(line.rstrip('\n'))
        print 'Hand:',''.join(lline[:len(lline)/2]),'Deck:',''.join(lline[len(lline)/2+1:]),'Best hand:',bestCards,rank
    else:
        return

if __name__ == "__main__":
    main()
