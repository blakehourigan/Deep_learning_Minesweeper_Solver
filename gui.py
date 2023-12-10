import tkinter as tk
from tkinter import messagebox
import time

import config

class MinesweeperGUI:
    def __init__(self, master, controller):
        self.master = master
        
        self.controller = controller
        
            
                  
        self.images = \
        {
            'mine': tk.PhotoImage(file=config.mine_image),
            'flag': tk.PhotoImage(file=config.flag_image)
        }
        
        self.flag_images = {}  
     
    def main_gui_setup(self, size) -> None:
        self.master.title("Minesweeper")
        self.setup_game_clock(self.master, self.controller.logic.grid_size)
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

    def create_button(self, master, row, column) -> tk.Button:
        frame = tk.Frame(master)
        frame.grid(row=row, column=column, padx=0, pady=0, sticky="nsew")  # Use sticky to fill the space
        
        button = tk.Button(frame, width=config.button_width,height=config.button_height)
        
        if self.controller.logic.player != 'AI':
            button.bind('<Button-1>', lambda event, r=row, c=column: self.controller.on_left_click(r, c)(event))
            # right click bound to setting flags
            button.bind('<Button-3>', lambda event, r=row, c=column: self.controller.on_right_click(r, c)(event))

        button.pack(expand=True, fill='both')  # pack button to fill full frame

        return button

    def set_window_center(self, width, height) -> None:
        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        
        self.master.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
    
    def reveal_board(self) -> None:
        for row_index, row_entries in enumerate(self.controller.logic.board):
            for col_index, cell in enumerate(row_entries):
                self._update_button_if_not_revealed(row_index, col_index, cell)

    def _update_button_if_not_revealed(self, row_index, col_index, cell) -> None:
        if not cell.is_revealed:
            button = self.buttons[row_index][col_index]
            self.configure_game_button_state(button, cell)

    def configure_game_button_state(self, button, cell, action = None) -> None:
        if action:
            if action == 'setflag':
                button.config(image=self.images['flag'], width=config.button_width, height=config.button_height)
            elif action == 'unset_flag':
                button.config(relief=tk.RAISED, image='')
        else:
            if cell.is_mine:
                color = config.MINE_COLORMAP['mine']
                button.config(relief=tk.RAISED, state=tk.DISABLED, bg=color, image=self.images['mine'])
            elif cell.is_numbered:
                color = config.MINE_COLORMAP.get(cell.get_number())
                button.config(relief=tk.SUNKEN, state=tk.DISABLED,text=cell.get_number(), bg=color, fg='white')
            elif cell.is_empty:
                color = config.MINE_COLORMAP['empty']
                button.config(relief=tk.SUNKEN, state=tk.DISABLED, text='', bg=color)
            self.master.update()

    def clear_adjacent_cells(self, to_reveal) -> None:
        for row, col in to_reveal:
            button = self.buttons[row][col]
            cell = self.controller.logic.board[row][col]
            self.configure_game_button_state(button, cell)

    def load_image(self, master) -> None:
        # Get the appropriate icon file based on the OS used
        icon_file = config.get_task_tray_icon()

        if icon_file.endswith('.ico'):
            master.iconbitmap(icon_file)
        else:
            tt_img = tk.PhotoImage(file=icon_file)
            master.iconphoto(True, tt_img)

    def setup_game_clock(self, master, size) -> None:
        self.timer_label = tk.Label(master, text="Time: 0s")
        self.timer_label.grid(row=0, column=0, columnspan=size//2, sticky="w")

        self.score_label = tk.Label(master, text=f"Score: {self.controller.logic.get_score()}")
        self.score_label.grid(row=0, column=size//2, columnspan=size//2, sticky="e")
        if not self.controller.logic.running:
            self.start_time = time.time()
            self.controller.logic.running = True
            self.update_game_clock()

    def update_game_clock(self) -> None:
        if self.controller.logic.running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}s")
            self.master.after(1000, self.update_game_clock)
    
    def update_game_score(self) -> None:
        self.score_label.config(text=f"Score: {self.controller.logic.get_score()}")
    
    def show_error(self, title, message) -> None:
        messagebox.showinfo(title, message)
        
    def handle_right_click(self, row, column) -> None:
        pass