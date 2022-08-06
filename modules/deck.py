class Deck:
    def __init__(self):
        self.name = 'Deck'
        self.format = 'Standard'
        self.isValid = False
        self.cards = []

class CardInDeck:
    def __init__(self):
        self.id = ''
        self.board = 1
        self.quantity = 0