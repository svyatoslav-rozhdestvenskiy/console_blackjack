from class_game import game
import time


def main():
    game.game_initialization()
    while game.reason_for_leaving == '':
        game.start_game()
    game.finish_game()
    time.sleep(30)


if __name__ == '__main__':
    main()
