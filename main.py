# main.py
from game_manager import GameManager
from welcome import WelcomeScreen

def main():
    game_manager = GameManager()
    game_manager.start_welcome_screen(WelcomeScreen)

if __name__ == "__main__":
    main()