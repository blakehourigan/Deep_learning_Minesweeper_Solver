from game_manager import GameManager

def main():
    global game_manager
    game_manager = GameManager(restart_game)
    game_manager.start_welcome_screen()

def restart_game():
    global game_manager
    del game_manager
    main()


if __name__ == "__main__":
    main() 