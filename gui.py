import tkinter as tk
import time
import threading

import config

class MinesweeperGUI:
    def __init__(self, master, size, mines, player, loss_window, win_window, logic, AI, ai_solution=None):
        self.master = master

            
        self.loss_window = loss_window
        self.win_window = win_window
        
        self.ai_solution = ai_solution
        self.logic = logic
        self.AI = AI
        self.size = size 
        self.player = player
        self.mines = mines

        self.setup_game_clock(self.master, size)

        self.images = {
            'mine': tk.PhotoImage(file=config.mine_image),
            'flag': tk.PhotoImage(file=config.flag_image)
        }
        
        self.flag_images = {}  # Dictionary to store flag images for AI winows
        
        self.main_gui_setup(master, size)
     
    def main_gui_setup(self, size):
        self.master.title("Minesweeper")
        # Initialize a grid of buttons with frames
        self.buttons = [[self.create_button(self.master, row + 1, column, config.button_width, config.button_height, size)
                        for column in range(size)] for row in range(size)]

        self.master.resizable(False, False)
        
        window_width = size * config.button_width
        window_height = size * config.button_height
        self.master.minsize(window_width, window_height)
        
        self.center_window(window_width, window_height)     


    def show_ai_solution(self, solution_index,ai_solution):
        top = tk.Toplevel(self.master)
        top.title(f"AI's Solution #{solution_index + 1}")
                
        ai_gui = MinesweeperGUI(top, self.logic.grid_size, self.logic.num_mines, "AI", 
                                self.loss_window, self.win_window, self.logic, self.AI, 
                                ai_solution=ai_solution)

    def overlay_ai_flags(self, ai_solution):
        for row in range(self.logic.grid_size):
            for col in range(self.logic.grid_size):
                button = self.buttons[row][col]
                # If the current cell is flagged by the AI, overlay the flag image
                if (row, col) in ai_solution.flags:
                    if (row, col) not in self.flag_images:
                        self.flag_images[(row, col)] = tk.PhotoImage(file=config.flag_image)
                    button.config(relief=tk.RAISED, image=self.flag_images[(row, col)])
                    button.image = self.flag_images[(row, col)] # add to flag_images global class dict

    def create_button(self, master, row, column, width, height, size):
        # Create a frame to hold the button
        frame = tk.Frame(master)
        frame.grid(row=row, column=column, padx=0, pady=0, sticky="nsew")  # Use sticky to fill the space
        
        # Create the button
        button = tk.Button(frame, width=config.button_width,height=config.button_height)
        
        if self.player != 'AI':
            # left click selects a cell
            button.bind('<Button-1>', lambda event, r=row, c=column: self.on_left_click(r, c)(event))
            # right click bound to setting flags
            button.bind('<Button-3>', lambda event, r=row, c=column: self.on_right_click(r, c)(event))

        button.pack(expand=True, fill='both')  # pack button to fill full frame

        return button

    def center_window(self, width, height):
        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.master.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def on_left_click(self, row, column):
        def callback(event):
            # we need to adjust everything down by one, because an extra row is generated to house the timer and score labels
            logic_row, logic_column  = row - 1, column 
            
            result = self.logic.reveal_cell(logic_row, logic_column)
            button = event.widget

            cell = self.logic.board[logic_row][logic_column]

            self.configure_game_button_state(button, cell)
            # check for a win
            if self.logic.check_for_win():
                self.win_window()
            # else, keep playing
            if result == 'empty':
                to_reveal = self.logic.clear_adjacent_cells(logic_row, logic_column)
                self.clear_adjacent_cells(to_reveal)
            elif result == 'mine':
                self.logic.running = False
                # reveal the board to the player for 5s
                self.reveal_board()

                time.sleep(5) 
                self.loss_window()
            elif cell.is_numbered():
                self.configure_game_button_state(button, cell)
            else:
                print("Error: cell type not allowed")
                exit(1)
            self.update_game_score()
        return callback
    
    def reveal_board(self):
        for row_index, row_entries in enumerate(self.logic.board):
            for col_index, cell in enumerate(row_entries):
                self._update_button_if_not_revealed(row_index, col_index, cell)

    def _update_button_if_not_revealed(self, row_index, col_index, cell):
        if not cell.is_revealed:
            button = self.buttons[row_index][col_index]
            self.configure_game_button_state(button, cell)

    def configure_game_button_state(self, button, cell, action = None):
        if action:
            if action == 'setflag':
                button.config(image=self.images['flag'], width=config.button_width, height=config.button_height )
            elif action == 'unset_flag':
                button.config(relief=tk.RAISED)
                button.config(image='')
        else:
            cell_type = cell.get_type()
            color = config.MINE_COLORMAP.get(cell_type)
            button.config(relief=tk.SUNKEN, state=tk.DISABLED, bg=color)
            if cell.type == 'mine':
                button.config(relief=tk.RAISED, state=tk.DISABLED, bg=color)
                button.config(image=self.images['mine'])
            elif cell.type != 'empty' and cell.type != 'flag':
                button.config(text=cell.type)
        self.master.update()

    def clear_adjacent_cells(self, to_reveal):
        for row, col in to_reveal:
            button = self.buttons[row][col]
            cell = self.logic.board[row][col]
            self.configure_game_button_state(button, cell)
    
    def on_right_click(self, row, column):
        """Handles left click for revealing the tile."""
        def callback(event):
            logic_row, logic_column  = row - 1, column
            
            button = event.widget
            cell = self.logic.board[logic_row][logic_column]
            if button.cget('relief') == tk.SUNKEN:
                return callback 
            else:
                action = self.logic.toggle_flag(logic_row, logic_column)
                self.configure_game_button_state(button, cell, action)

        return callback

    def load_image(self, master):
        # Get the appropriate icon file based on the OS used
        icon_file = config.get_task_tray_icon()

        if icon_file.endswith('.ico'):
            master.iconbitmap(icon_file)
        else:
            tt_img = tk.PhotoImage(file=icon_file)
            master.iconphoto(True, tt_img)

    def setup_game_clock(self, master, size):
        self.timer_label = tk.Label(master, text="Time: 0s")
        self.timer_label.grid(row=0, column=0, columnspan=size//2, sticky="w")

        self.score_label = tk.Label(master, text="Score: 0")
        self.score_label.grid(row=0, column=size//2, columnspan=size//2, sticky="e")
        if not self.logic.running:
            self.start_time = time.time()
            self.logic.running = True
            self.update_game_clock()

    def update_game_clock(self):
        if self.logic.running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.master.after(1000, self.update_game_clock)
    
    def update_game_score(self):
        self.score_label.config(text=f"Score: {self.logic.get_score()}")