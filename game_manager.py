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

        self.logic = MinesweeperLogic(controller= self, **config.DIFFICULTIES["Beginner"])

    def start_welcome_screen(self, welcome_class):
        self.current_screen = welcome_class(self.root, self.start_game)
        self.root.mainloop()

    def start_game(self, difficulty, player):
        self.clear_screen()

        self.logic.player = player
        
        self.logic.grid_size = config.DIFFICULTIES[difficulty]['size']
        self.logic.num_mines = config.DIFFICULTIES[difficulty]['mines']
        
        self.current_screen = MinesweeperGUI(self.root, self)
        self.GUI = self.current_screen
    
    def show_win_screen(self) -> None:
        """ clear the gui and show the winner splash screen """
        self.clear_screen()
        self.current_screen = WinSplashScreen(self.root, self.restart_game, self.destroy_game)
    
    def show_loss_screen(self) -> None:
        self.clear_screen()
        self.current_screen = EndSplashScreen(self.root, self.restart_game, self.destroy_game)

    def clear_screen(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def restart_game(self) -> None:
        self.clear_screen()
        self.start_welcome_screen(WelcomeScreen)
        
    def destroy_game(self) -> None:
        self.clear_screen()
        self.root.destroy()

    def on_left_click(self, row, column):
        def callback(event):
            logic_row, logic_column  = row - 1, column  # row decremented by one because an extra row in the gui contains the timer and score labels
            
            cell = self.logic.reveal_cell(logic_row, logic_column)
            button = event.widget

            self.GUI.configure_game_button_state(button, cell)
            
            if self.logic.check_for_win():
                self.root.after(5000, lambda: self.show_win_screen())
            elif cell.is_empty:
                to_reveal = self.logic.clear_adjacent_cells(logic_row, logic_column)
                self.GUI.clear_adjacent_cells(to_reveal)
            elif cell.is_mine:
                self.logic.running = False
                self.GUI.reveal_board()
                self.root.after(5000, lambda: self.show_loss_screen())
            elif cell.is_numbered:
                self.GUI.configure_game_button_state(button, cell)
            else:
                self.GUI.show_error("ERROR", "cell type not allowed")
                self.root.after(10000, self.destroy_game)
            self.GUI.update_game_score()
        return callback
    
    def on_right_click(self, row, column):
        """ handles flagging of tiles """
        def callback(event):
            logic_row, logic_column  = row - 1, column  # row decremented by one because an extra row in the gui contains the timer and score labels
            button = event.widget
            cell = self.logic.select_cell(logic_row, logic_column)
            if button.cget('relief') == tk.SUNKEN:
                return callback 
            else:
                action = self.logic.toggle_flag(logic_row, logic_column)
                self.GUI.configure_game_button_state(button, cell, action)

        return callback