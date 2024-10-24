### IMPORT LIBRARIES
import random


### CLASSES
class Card:
    def __init__(self, suit, value):
        assert 1 <= suit <= 4 and 1 <= value <= 13
        self._suit = suit
        self._value = value

    def getValue(self):
        return self._value

    def getSuit(self):
        return self._suit
    
    def __str__(self):
        suit = ['Diamonds', 'Hearts', 'Clubs', 'Spades']
        return f'{self._value} of {suit[self._suit - 1]}'
    

class CardDeck:
    def __init__(self):
        self.reset()
    
    def shuffle(self):
        random.shuffle(self._deck)

    def getCard(self):
        return self._deck.pop(0)
    
    def size(self):
        return len(self._deck)
    
    def reset(self):
        self._deck = [Card(suit, value) for suit in range(1, 5) for value in range(1, 14)]


### FUNCTIONS



### MAIN
def main():
    deck = CardDeck()
    deck.shuffle()
    while deck.size() > 0:
        card = deck.getCard()
        print(f'Card {card} has value {card.getValue()}')


if __name__ == '__main__':
    main()