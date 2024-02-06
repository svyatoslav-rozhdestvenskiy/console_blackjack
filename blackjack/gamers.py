from card_for_print import Card


class Player:

    def __init__(self, name='Player', money=0):
        self.hand = []
        self.card_count = 0
        self.hand_points = 0
        self.name = name
        self.money = money
        self.bet = 0
        self.black_jack = False
        self.losing_hand = False

    def take_card(self):
        from class_game import game
        self.hand.append(game.current_deck.get_deck()[0])
        game.current_deck.pop_deck()
        game.current_deck.set_card_count()
        self.card_count = len(self.hand)
        self.calculate_hand_points()

    def calculate_hand_points(self):
        self.hand_points = 0
        ace_count = 0
        for card in self.hand:
            self.hand_points += Card.card_values[card.rank]
            if card.rank == 'Ace':
                ace_count += 1
        if self.hand_points >= 22 and ace_count > 0:
            while ace_count > 0 and self.hand_points >= 22:
                self.hand_points -= 10
                ace_count -= 1
        if self.hand_points == 21 and len(self.hand) == 2:
            self.black_jack = True
        if self.hand_points > 21:
            self.losing_hand = True

    def place_a_bet(self):
        from class_game import game
        while True:
            bet = input("Сделайте вашу ставку в рублях или напишите 'выход': ")
            if bet.lower() == 'выход':
                game.reason_for_leaving = 'отказ от ставки'
                break
            bet_int = []
            for char in bet.split():
                if ',' in char:
                    char = char.replace(',', '.')
                try:
                    bet_int.append(int(float(char)))
                except ValueError:
                    pass
            if len(bet_int) == 0:
                print("Ошибка ставки, попробуйте ввести число")
                continue
            if bet_int[0] <= 0:
                print("Ошибка ставки, попробуйте сделать ставку больше 0")
                continue
            if bet_int[0] > self.money:
                print('Вам не хватает денег, попробуйте сделать ставку поменьше')
                continue
            self.bet = bet_int[0]
            self.money -= self.bet
            break

    def double_bet(self):
        if self.bet <= self.money:
            self.money -= self.bet
            self.bet *= 2
        else:
            print('Вам не хватило денег на полное удвоение, вы поставили все')
            print(f'Теперь ваша ставка составляет: {self.money} руб')
            self.bet += self.money
            self.money = 0

    def new_game(self):
        self.hand = []
        self.card_count = 0
        self.hand_points = 0
        self.bet = 0
        self.black_jack = False
        self.losing_hand = False


class Dealer(Player):
    def place_a_bet(self):
        from class_game import game
        if game.player.bet > self.money:
            print('Дилер не смог принять вашу ставку, у него закончились деньги')
            print(f'Теперь ваша ставка составляет: {self.money} руб')
            game.player.money = game.player.money + game.player.bet - self.money
            game.player.bet = self.money
        self.bet = game.player.bet
        self.money -= self.bet

    def double_bet(self):
        from class_game import game
        if game.player.bet > (self.money + self.bet):
            print('Дилер не смог принять вашу ставку, у него закончились деньги')
            print(f'Теперь ваша ставка составляет: {self.money + self.bet} руб')
            game.player.money = game.player.money + game.player.bet - (self.money + self.bet)
            game.player.bet = self.money + self.bet
        self.money = self.money + self.bet - game.player.bet
        self.bet = game.player.bet
