import tkinter as tk
from typing import Callable

from gui import MinesweeperGUI
import config
from game_over import EndSplashScreen
from winner import WinSplashScreen
from welcome import WelcomeScreen
from logic import MinesweeperLogic

class GameManager:
    
    def __init__(self, restart_function) -> None:
        self.restart_function = restart_function
        
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        
        self.logic = MinesweeperLogic(self)
        self.GUI = MinesweeperGUI(self.root, self)

        self.win_screen = WinSplashScreen(self.restart_game, self.destroy_game)
        self.end_screen = EndSplashScreen(self.restart_game, self.destroy_game)
        
        self.show_welcome_screen = WelcomeScreen()

    def start_welcome_screen(self) -> None:
        self.show_welcome_screen.show_welcome_screen(self.root, self.start_game)
        self.root.mainloop()

    def start_game(self, difficulty, player) -> None:
        self.clear_screen()
        
        self.create_game_board(difficulty, player)
        
        self.current_screen = self.GUI
        self.GUI = self.current_screen
    
    def create_game_board(self, difficulty, player):
        self.logic.player = player
        self.logic.set_difficulty(config.DIFFICULTIES[difficulty]['size']) 
        self.logic.set_mines(config.DIFFICULTIES[difficulty]['mines'])
        self.logic.create_board()
        self.GUI.main_gui_setup(self.logic.grid_size)
    
    def show_win_screen(self) -> None:
        """ clear the gui and show the winner splash screen """
        self.clear_screen()
        self.win_screen.show_win_screen(self.root)
    
    def show_loss_screen(self) -> None:
        self.clear_screen()
        self.end_screen.show_end_screen(self.root)

    def clear_screen(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def restart_game(self) -> None:
        self.destroy_game()
        self.restart_function()             # we need to change this to destroy the game manager and 
        
    def destroy_game(self) -> None:
        self.clear_screen()
        self.root.destroy()

    def on_left_click(self, row, column) -> Callable:
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
    
    def on_right_click(self, row, column) -> Callable:
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