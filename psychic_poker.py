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
    #               0            1        2            3            4      5       6            7               8
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

    def printHand(self):
        return [str(a) for a in self.cards]

    def calculateRank(self):
        FaceValue = '23456789TJQKA'
        def getCardRank(str):
            return FaceValue.index(str)
        number_of_suits = len(set(map(Card.getSuit,self.cards)))
        # print number_of_suits
        figures_list = sorted(map(Card.getFaceValue, self.cards),key=getCardRank,reverse=True)
        # print figures_list
        def checkConsecutiveFig(fig_list):
            for i in range(len(fig_list)-1):
                if not (FaceValue.index(fig_list[i]) - FaceValue.index(fig_list[i+1]) == 1):
                    return False
            return True

        # for card in self.cards:
        #     print card, ":",
        # print
        if number_of_suits == 1:
            # print checkConsecutiveFig(figures_list),figures_list
            return Hand.allRanks.index('straight-flush') if checkConsecutiveFig(figures_list) else Hand.allRanks.index('flush')
        if figures_list[0] == figures_list[3] or figures_list[1] == figures_list[4]:
            
            return Hand.allRanks.index('four-of-a-kind')
        if figures_list[0] == figures_list[2] and figures_list[3] == figures_list[4]:
            return Hand.allRanks.index('full-house')
        if figures_list[0] == figures_list[1] and figures_list[2] == figures_list[4]:
            return Hand.allRanks.index('full-house')
        if checkConsecutiveFig(figures_list):
            return Hand.allRanks.index('straight')
        if figures_list[0] == figures_list[2] or figures_list[1] == figures_list[3] or figures_list[2] == figures_list[4]:
            return Hand.allRanks.index('three-of-a-kind')
        distinct = len(set(figures_list))
        if distinct == 3:
            return Hand.allRanks.index('two-pairs')
        if distinct == 4:
            return Hand.allRanks.index('one-pair')
        return Hand.allRanks.index('highest-card')

def getComb(stuff):
    for L in range(0, len(stuff)+1):
        for subset in itertools.combinations(stuff, L):
            if subset:
                yield list(subset)

def getBestComb(cards):
    five = cards[:5]
    best = Hand(five)
    for _ in xrange(0, 5):
        for variation in getComb(xrange(0, 5)):
            # hand = Hand(five)
            hand = (Hand(cards[:5]))
            for addFromDeck, removeFromHand in enumerate(variation):
                hand.replace(removeFromHand, cards[5+addFromDeck])
            if hand > best:
                best = hand
    print Hand.printHand(best)
    return best

def getProcessed(hand_plus_deck):
    # print list(hand_plus_deck.split())
    # print " -- ENTER -- "
    cards_obj_list = map(Card,hand_plus_deck.split())
    bestComb = getBestComb(cards_obj_list)
    if bestComb:
        return bestComb
    else:
        return " -- EXIT --"

def main():
    # print
    for line in open(sys.argv[1]):
        
        # print line.strip()
        print getProcessed(line.rstrip('\n'))
        

if __name__ == "__main__":
	main()
