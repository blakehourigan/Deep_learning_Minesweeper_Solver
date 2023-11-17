# welcome.py
import tkinter as tk

import config

class WelcomeScreen:
    def __init__(self, master, start_game_callback):
        self.master = master
        self.start_game_callback = start_game_callback
        master.title("Welcome to Minesweeper")
        
        # Get the appropriate icon file based on the OS being used
        icon_file = config.get_task_tray_icon()

        if icon_file.endswith('.ico'):
            master.iconbitmap(icon_file)
        else:
            tt_img = tk.PhotoImage(file=icon_file)
            master.iconphoto(True, tt_img)

        tk.Label(master, text="Welcome to Minesweeper! Choose your difficulty:").pack()

        self.difficulty = tk.StringVar(master)
        self.difficulty.set("Beginner")  # default value
        
        options = list(config.DIFFICULTIES.keys())  # Get difficulties from config
        
        # Create the OptionMenu and assign it to self.option_menu
        self.option_menu = tk.OptionMenu(master, self.difficulty, *options)
        self.option_menu.pack()
        
        play_options = ['Player', 'AI']
        
        self.player = tk.StringVar(master)
        self.player.set('Player')
        
        self.player_menu = tk.OptionMenu(master, self.player, *play_options)
        self.player_menu.pack()
        
        # set initial difficulty color based on default value
        self.update_color()
        
        # Trace the variable to change the OptionMenu color
        self.difficulty.trace("w", self.update_color)
        self.player.trace("w", self.update_color)

        tk.Button(master, text="Start Game", command=self.on_start_game).pack()
        
        self.center_window(config.welc_width, config.welc_height)  # Set the size of the window defined in config

    def on_start_game(self):
        difficulty = self.difficulty.get()
        player = self.player.get()
        self.start_game_callback(difficulty, player)  # Call the callback with the selected difficulty

    def update_color(self, *args):
        """ update the color of the buttons based on current selections """
        self.option_menu.config(bg=self.get_difficulty_color(), activebackground=self.get_difficulty_color())
        self.player_menu.config(bg=self.get_player_color(), activebackground=self.get_player_color())

        # Additionally, bind the hover events to reset the color
        self.option_menu.bind("<Enter>", lambda e: self.option_menu.config(bg=self.get_difficulty_color()))
        self.option_menu.bind("<Leave>", lambda e: self.option_menu.config(bg=self.get_difficulty_color()))

        self.player_menu.bind("<Enter>", lambda e: self.player_menu.config(bg=self.get_player_color()))
        self.player_menu.bind("<Leave>", lambda e: self.player_menu.config(bg=self.get_player_color()))

    def get_difficulty_color(self):
        """ get the color for the difficulty button """
        difficulty = self.difficulty.get()
        if difficulty == "Beginner":
            return "green"
        elif difficulty == "Intermediate":
            return "yellow"
        elif difficulty == "Expert":
            return "red"
        return "white"

    def get_player_color(self):
        """ get color for player button """
        player = self.player.get()
        if player == "Player":
            return "blue"
        elif player == "AI":
            return "red"
        return "white"
    
    def center_window(self, width, height):
        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate position x and y coordinates
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.master.geometry(f'{width}x{height}+{int(x)}+{int(y)}')
