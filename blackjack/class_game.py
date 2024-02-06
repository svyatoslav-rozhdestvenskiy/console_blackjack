from gamers import Player, Dealer
from deck import CardDeck
import card_for_print


class Game:
    player = Player()
    dealer = Dealer()
    current_deck = CardDeck()
    reason_for_leaving = ''
    deposit = 0

    def game_initialization(self):
        print('''
Добро пожаловать в консольный блэкджек!!!
            ''')
        while True:
            name = input("Введите свое имя: ")
            name_confirmation = input("Подтвердите свое имя: ")
            if name_confirmation != name:
                print("Имена не совпадают, попробуйте еще раз")
                continue
            break
        while True:
            deposit = input("Внесите депозит в рублях: ")
            deposit_int = []
            for char in deposit.split():
                if ',' in char:
                    char = char.replace(',', '.')
                try:
                    deposit_int.append(int(float(char)))
                except ValueError:
                    pass
            if len(deposit_int) == 0:
                print("Введите число!")
                continue
            deposit_int = deposit_int[0]
            if deposit_int == 0:
                print('Вы внесли 0 рублей.\nБез денег играть не получится, попробуйте внести депозит')
                continue
            elif deposit_int < 0:
                print("Вы запросили отрицательный депозит, казино вам пока ничего не должно!")
                continue
            while True:
                confirm_deposit = input(f'Вы уверены что хотите внести {deposit_int} руб? (Да/Нет): ')
                if confirm_deposit.lower() == 'да' or confirm_deposit.lower() == 'нет':
                    break
                else:
                    print('Пожалуйста, введите "да" или "нет"')
                    continue
            if confirm_deposit.lower() == 'да':
                break
            else:
                continue
        self.deposit = deposit_int
        self.dealer.name = 'Dealer'
        self.dealer.money = deposit_int * 2
        self.player.name = name.capitalize()
        self.player.money = deposit_int

    def start_game(self):
        self.reason_for_leaving = ''
        self.player.new_game()
        self.dealer.new_game()
        self.current_deck.new_deck_creator()
        print(f'\n{self.player.name}, ваш баланс составляет {self.player.money} руб')
        self.player.place_a_bet()
        self.dealer.place_a_bet()
        if self.reason_for_leaving != '':
            pass
        else:
            for i in range(2):
                self.player.take_card()
                self.dealer.take_card()
            self.print_hands()
            self.player_move()

    def player_move(self):

        def enter_action():
            while True:
                if self.player.card_count == 2:
                    answer = input("удвоить | еще | пас | помощь : ")
                else:
                    answer = input("еще | пас | помощь : ")
                answer = answer.lower()
                answer = answer.strip(' !,.?')
                if answer == 'у':
                    answer = 'удвоить'
                if answer == 'е':
                    answer = 'еще'
                if answer == 'п':
                    answer = 'пас'
                if self.player.card_count != 2 and answer == 'удвоить':
                    print("Сейчас вы не можете удвоить ставку")
                    continue
                if answer == '':
                    continue
                elif answer == 'помощь' or answer == 'помошь':
                    print("""
В игре блэкджек вам нужно набрать как можно больше очков, но не больше чем 21. 
Если вы наберете больше 21, то автоматически проиграете! 
Каждая карта дает определенное количество очков и чем больше у вас карт, тем больше вероятность перебрать. 
Ваша задача набрать очков больше чем у дилера. 
Дилер будет в любом случае добирать карты, если у него меньше 17 очков.

После раздачи вы можете удвоить свою ставку и взять еще всего 1 карту, для этого напишите 'удвоить' или 'у'
Вы можете написать 'еще' или 'е' и добрать себе на руку еще одну карту
А также вы можете написать 'пас' или 'п' чтобы закончить набор и ход перейдет к дилеру
                    """)
                    continue
                elif (answer != 'пас') and (answer != 'удвоить') and (answer != 'еще'):
                    print('Некорректная команда, для справки введите "помощь"')
                    continue
                else:
                    return answer

        was_doubling = False
        while True:
            if self.player.losing_hand:
                print("Печально. У вас перебор")
                break
            if was_doubling:
                break
            if self.player.black_jack:
                print("Поздравляем! У вас блэкджек!")
                break
            if self.player.hand_points == 21:
                print('Вы набрали 21 очко, теперь ход за дилером')
                break
            action = enter_action()
            if action == 'удвоить':
                self.player.double_bet()
                self.dealer.double_bet()
                self.player.take_card()
                self.print_hands()
                was_doubling = True
                continue
            if action == 'еще':
                self.player.take_card()
                self.print_hands()
                continue
            if action == 'пас':
                break
        if self.player.losing_hand:
            self.identify_winner()
        else:
            self.dealer_move()

    def dealer_move(self):
        while True:
            if self.dealer.hand_points >= 17:
                break
            else:
                self.dealer.take_card()
                continue
        self.print_hands(hidden=False)
        self.identify_winner()

    def identify_winner(self):
        if self.player.losing_hand:
            self.calculate_lose()
        else:
            if self.player.hand_points > self.dealer.hand_points:
                self.calculate_win()
            elif self.player.hand_points == self.dealer.hand_points:
                self.calculate_draw()
            elif self.dealer.losing_hand:
                print('У дилера перебор')
                self.calculate_win()
            else:
                self.calculate_lose()

    def finish_game(self):
        print('\nИгра окончена')
        print(f'\nВы внесли {self.deposit} руб, а вывести смогли {self.player.money} руб.\n')
        if self.reason_for_leaving == 'отказ от ставки':
            if self.deposit < self.player.money:
                print('Поздравляем! Вам удалось вовремя остановится и забрать выигрыш\n')
            elif self.deposit == self.player.money:
                print('Это была равная игра! С чем пришел с тем и ушел, тоже неплохо\n')
            else:
                print('Нам жаль, но сегодня удача покинула вас. Приходите в следующий раз и получится выиграть\n')

        if self.reason_for_leaving == 'Дилер разорен':
            print('Это невозможно!!! Вам удалось разорить казино!!!')
            print('Приходите в следующий раз, а мы пока программу настроим\n')
        if self.reason_for_leaving == 'Игрок разорен':
            print('К сожалению вы просадили все деньги в казино\n')

    def calculate_win(self):
        if self.player.black_jack:
            if self.dealer.money < (self.player.bet * 0.5):
                self.player.money += self.dealer.money + self.player.bet
                self.dealer.money = 0
                self.reason_for_leaving = 'Дилер разорен'
            else:
                self.player.money += self.player.bet * 2.5
                self.dealer.money -= self.dealer.bet * 0.5
        else:
            self.player.money += self.player.bet * 2
        if self.dealer.money <= 0:
            self.reason_for_leaving = 'Дилер разорен'
        print('Поздравляем с победой')

    def calculate_lose(self):
        self.dealer.money += self.player.bet * 2
        if self.player.money <= 0:
            self.reason_for_leaving = 'Игрок разорен'
        print('В этой партии вам не удалось взять вверх, но не расстраивайтесь')

    def calculate_draw(self):
        self.player.money += self.player.bet
        self.dealer.money += self.dealer.bet
        print('Ничья')

    def print_hands(self, hidden=True):
        print('\nКарты дилера:\n')
        if hidden:
            print(card_for_print.ascii_version_of_hidden_card(self.dealer.hand))
        else:
            print(card_for_print.ascii_version_of_card(self.dealer.hand))
        print('\nВаши карты:\n')
        print(card_for_print.ascii_version_of_card(self.player.hand))
        if hidden:
            print(f'\nКоличество ваших очков: {self.player.hand_points}\n')
        else:
            print(f'\nКоличество ваших очков: {self.player.hand_points}')
            print(f'Количество очков дилера: {self.dealer.hand_points}\n')


game = Game()
