import tkinter as tk
import time
import threading

import config

class MinesweeperGUI:
    def __init__(self, master, controller):
        self.master = master
        
        self.controller = controller
        self.setup_game_clock(self.master, self.controller.logic.grid_size)
            
        self.main_gui_setup(self.controller.logic.grid_size)
                  
        self.images = \
        {
            'mine': tk.PhotoImage(file=config.mine_image),
            'flag': tk.PhotoImage(file=config.flag_image)
        }
        
        self.flag_images = {}  
     
    def main_gui_setup(self, size):
        self.master.title("Minesweeper")
        
        # create layout for the elements on the screen
        for i in range(1, size + 1):
            self.master.grid_rowconfigure(i, weight=1) 
        for i in range(size):
            self.master.grid_columnconfigure(i, weight=1)

        self.buttons = [[self.create_button(self.master, row + 1, column) for column in range(size)] for row in range(size)]

        self.master.resizable(False, False)
        
        window_width = size * config.button_width
        window_height = size * config.button_height
        
        self.master.minsize(window_width, window_height)
        
        self.set_window_center(window_width, window_height)     


    def show_ai_solution(self, solution_index,ai_solution):
        top = tk.Toplevel(self.master)
        top.title(f"AI's Solution #{solution_index + 1}")
                
        ai_gui = MinesweeperGUI(top, self.controller)

    def overlay_ai_flags(self, ai_solution):
        for row in range(self.controller.logic.grid_size):
            for col in range(self.controller.logic.grid_size):
                button = self.buttons[row][col]
                # If the current cell is flagged by the AI, overlay the flag image
                if (row, col) in ai_solution.flags:
                    if (row, col) not in self.flag_images:
                        self.flag_images[(row, col)] = tk.PhotoImage(file=config.flag_image)
                    button.config(relief=tk.RAISED, image=self.flag_images[(row, col)])
                    button.image = self.flag_images[(row, col)] # add to flag_images global class dict

    def create_button(self, master, row, column):
        frame = tk.Frame(master)
        frame.grid(row=row, column=column, padx=0, pady=0, sticky="nsew")  # Use sticky to fill the space
        
        button = tk.Button(frame, width=config.button_width,height=config.button_height)
        
        if self.controller.logic.player != 'AI':
            button.bind('<Button-1>', lambda event, r=row, c=column: self.controller.on_left_click(r, c)(event))
            # right click bound to setting flags
            button.bind('<Button-3>', lambda event, r=row, c=column: self.controller.on_right_click(r, c)(event))

        button.pack(expand=True, fill='both')  # pack button to fill full frame

        return button

    def set_window_center(self, width, height):
        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        
        self.master.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    
    def reveal_board(self):
        for row_index, row_entries in enumerate(self.controller.logic.board):
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
            cell = self.controller.logic.board[row][col]
            self.configure_game_button_state(button, cell)
    


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
        if not self.controller.logic.running:
            self.start_time = time.time()
            self.controller.logic.running = True
            self.update_game_clock()

    def update_game_clock(self):
        if self.controller.logic.running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.master.after(1000, self.update_game_clock)
    
    def update_game_score(self):
        self.score_label.config(text=f"Score: {self.controller.logic.get_score()}")