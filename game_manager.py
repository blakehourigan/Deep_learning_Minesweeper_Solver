# game_manager.py
import tkinter as tk

from gui import MinesweeperGUI
import config
from game_over import EndSplashScreen
from winner import WinSplashScreen
from welcome import WelcomeScreen
from logic import MinesweeperLogic

class GameManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.current_screen = None

    def start_welcome_screen(self, welcome_class):
        self.current_screen = welcome_class(self.root, self.start_game)
        self.root.mainloop()

    def start_game(self, difficulty, player):
        settings = config.DIFFICULTIES.get(difficulty, config.DIFFICULTIES["Beginner"])
        # Clear any existing screen and start the game
        self.clear_screen()
        logic = MinesweeperLogic(**settings)                           # Create an instance of the logic class to use here 
        game_config = {
            'root': self.root,
            'settings': settings,
            'player': player,
            'on_win': self.show_win_screen,
            'on_loss': self.show_end_screen,
            'logic': MinesweeperLogic(**settings),
            'AI': None
        }
        self.current_screen = MinesweeperGUI(game_config)

    def show_win_screen(self):
        """ clear the gui and show the winner splash scree """
        self.clear_screen()
        self.current_screen = WinSplashScreen(self.root, self.restart_game, self.destroy_game)
    
    def show_end_screen(self):
        """ Clear the current GUI and show the end game splash screen """
        self.clear_screen()
        self.current_screen = EndSplashScreen(self.root, self.restart_game, self.destroy_game)

    def clear_screen(self):
        # This method clears the GUI, which could be hiding or destroying widgets
        for widget in self.root.winfo_children():
            widget.destroy()

    def restart_game(self):
        # This method restarts the game, calling start_welcome_screen again
        self.clear_screen()
        self.start_welcome_screen(WelcomeScreen)
        
    def destroy_game(self):
        self.clear_screen()
        self.root.destroy()
