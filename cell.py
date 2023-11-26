class Cell:
    def __init__(self):
        # default the cell type to blank
        self.number = -1
        self.adjacent_mines = 0
        self.is_empty = False
        self.is_mine = False
        self.is_flagged = False
        self.is_revealed = False
        self.is_blank =  True
        self.is_numbered = False

    def __str__(self):
        return f"\nNumber: {self.number} \n# Adjacent mines: {self.adjacent_mines}\nRevealed: {self.is_revealed}"
    
    def get_number(self):
        return self.number
    
    def set_number(self, number):
        self.number = number
    

