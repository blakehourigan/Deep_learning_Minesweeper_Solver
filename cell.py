# cell.py

class Cell:
    def __init__(self):
        # default the cell type to blank
        self.type = "blank"
        self.adjacent_mines = 0
        self.is_mine = False
        self.is_flagged = False
        self.is_revealed = False

    def __str__(self):
        return f"\nType: {self.type} \n# Adjacent mines: {self.adjacent_mines}\nRevealed: {self.is_revealed}"
    
    def get_type(self):
        return self.type
    
    def set_type(self, type):
        self.type = type
    
    def is_numbered(self):
        return self.type in {'1', '2', '3', '4', '5'}
