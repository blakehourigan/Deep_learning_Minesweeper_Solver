import tkinter as tk
import config

class WinSplashScreen: 
    def __init__(self, master, restart_game, destroy_game):
        self.master = master
        self.restart_game = restart_game
        self.exit_game = destroy_game
        self.master.title("You Won!")
        
        self.master.configure(bg='#cccccc')
        
        # Load the image
        self.game_over_image = tk.PhotoImage(file=config.winner_png)
        
        # Determine the size of the image
        image_width = self.game_over_image.width()
        image_height = self.game_over_image.height()

        # Make sure the game over window takes focus over the main application window
        self.master.grab_set()

        # Label displaying the game over image
        image_label = tk.Label(self.master, image=self.game_over_image)
        image_label.pack(pady=10)  # Use pack for simplicity
        
        # Create a frame for the buttons with a specific height
        button_frame_height = 80  # Set the height you want for the buttons
        button_frame = tk.Frame(self.master, height=button_frame_height)
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)
        button_frame.pack_propagate(False)  # Prevent the frame from shrinking to the size of its contents

        # Restart button
        restart_button = tk.Button(button_frame, text="Restart", command=restart_game, bg='green')
        restart_button.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Exit button
        exit_button = tk.Button(button_frame, text="Exit", command=destroy_game, bg='red')
        exit_button.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        # Calculate the total height needed (image + button height + padding)
        total_height = image_height + button_frame_height  # Assume button height ~40px, and add 20px padding

        # Calculate the total width needed (image width + padding)
        total_width = image_width + 20  # Add 20px padding
        
        # Set the window size to accommodate the image and buttons
        self.master.geometry(f"{total_width}x{total_height}+"
                             f"{master.winfo_screenwidth() // 2 - total_width // 2}+"
                             f"{master.winfo_screenheight() // 2 - total_height // 2}")
        # Disable the main window until the game over screen is closed
        master.wait_window(self.master)
