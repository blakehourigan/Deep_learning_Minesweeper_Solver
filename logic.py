import random

from cell import Cell

class MinesweeperLogic:
    NEIGHBOR_POSITIONS = \
        [(-1, -1), (-1, 0), (-1, 1),  
         (0, -1),           (0, 1),   
         (1, -1), (1, 0), (1, 1)]     
        
    CORRECT_FLAG_POINTS = 20 
    
    def __init__(self, size, mines):
        self.num_mines = mines
        self.grid_size = size
        
        self.board = self.create_board()
        self.mine_coords = set()
        
        self.num_moves = 0
        self.user_score = 0
        
        self.running = False
        self.player = None
        


    def create_board(self) -> list:
        board = [[Cell() for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        return board

    def fill_board(self) -> None:
        self.generate_mines()
        self.fill_numbers_or_empty()
        self.count_current_score()
        
    def generate_mines(self) -> None:
        while len(self.mine_coords) < self.num_mines:
            row, column = self.get_random_cell()
            if self.can_place_mine(row, column):
                self.place_mine(row, column)

    def get_random_cell(self) -> tuple:
        return (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
    
    def can_place_mine(self, row, column) -> bool:
        cell = self.board[row][column]
        cell.get_type == 'blank'

        return cell.get_type() == 'blank' # cells that are 'blank', and not 'empty' can have mines placed in them
            
    def place_mine(self, row, column) -> None:
        cell = self.board[row][column]
        cell.set_type("mine")
        self.mine_coords.add((row,column))
        cell.is_mine = True   
            
    def fill_numbers_or_empty(self) -> None:
        """ fill remaining cells after mines placed """
        for row_num, row in enumerate(self.board):
            for col, cell in enumerate(row):
                self.check_number_or_empty(row, row_num ,col, cell)
                
    def check_number_or_empty(self, row, row_num, col, cell) -> None:
        if self.count_adjacent_mines(row_num, col) > 0 and cell.get_type() == 'blank':
            self.set_adjacent_type(row_num, col, cell)
        elif not cell.is_mine:
            cell.set_type("empty")

    def set_adjacent_type(self, row_num, col, cell) -> None:
        cell.adjacent_mines = self.count_adjacent_mines(row_num, col)
        cell.set_type(str(cell.adjacent_mines))

    def reveal_cell(self, row, column) -> str:
        cell = self.board[row][column]
        cell.is_revealed = True
        
        if self.num_moves == 0:
            cell.set_type('empty')
            self.fill_board()
            self.num_moves += 1
        elif cell.get_type != 'mine' and self.num_moves > 0:
            self.count_current_score()
            self.num_moves +=1
            
        return cell.get_type()

    def toggle_flag(self, row, column):
        cell = self.board[row][column]

        if (not cell.is_revealed) and not cell.is_flagged:
            cell.is_flagged = True
            return 'setflag'
        elif (not cell.is_revealed) and cell.is_flagged:
            cell.is_flagged = False
            return 'unset_flag'
        else:
            print('Unexpected error, please reload program and play again')
            exit(1)

    def clear_adjacent_cells(self, row, col): 
        """ function that checks if adjacent cells are empty, and if so it clears them"""
        to_reveal = set()       # this set is used keep track of if cells are found that need to be revealed locally
        to_reveal.add((row, col))

        revealed_cells = set()  # Set to keep track of all the cells that need to be revealed globally on all iterations 

        while to_reveal:
            current_row, current_col = to_reveal.pop()
            curr_cell = self.board[current_row][current_col]

            # If the cell is already revealed or is a mine, skip it
            if (current_row, current_col) in revealed_cells or self.board[current_row][current_col].get_type() == 'mine':
                continue

            revealed_cells.add((current_row, current_col))
            curr_cell.is_revealed = True

            # If the current cell is empty, add its neighbors to the set
            if curr_cell.get_type() == 'empty':

                for row_offset, col_offset in self.NEIGHBOR_POSITIONS:
                    neighbor_row, neighbor_col = current_row + row_offset, current_col + col_offset
                    # Check if the neighbor is within the bounds of the board
                    if 0 <= neighbor_row < len(self.board) and 0 <= neighbor_col < len(self.board[0]):
                        neighbor_cell = self.board[neighbor_row][neighbor_col]
                        # Add the cell to be revealed if it is not a mine and not already revealed
                        if not neighbor_cell.is_mine and not neighbor_cell.is_revealed:
                            to_reveal.add((neighbor_row, neighbor_col))
        self.count_current_score()
        return revealed_cells

    def count_adjacent_mines(self, row, col) -> None:
        count = 0
        for row_offset, col_offset in self.NEIGHBOR_POSITIONS:
            neighbor_row, neighbor_col = row + row_offset, col + col_offset
            # Check if the neighbor is within the bounds of the board
            if 0 <= neighbor_row < len(self.board) and 0 <= neighbor_col < len(self.board[0]):
                if self.board[neighbor_row][neighbor_col].get_type() == 'mine':
                    count += 1

        return count

    def count_current_score(self) -> None:
        score = 0
        
        for row in self.board:
            for cell in row:
                score += self.process_current_cell_score(cell)

        if self.check_for_win():
            if self.all_mines_flagged():
                self.user_score = self.calculate_maximum_score()
            else:
                # Update score with the temporary score calculated
                self.user_score = score + (sum(cell.is_flagged for row in self.board for cell in row)) * self.CORRECT_FLAG_POINTS
        else:
            self.user_score = score
    
    def process_current_cell_score(self, cell):
        if cell.get_type() != 'mine' and cell.is_revealed:
            return 1
        return 0

    def all_mines_flagged(self):
        return all(cell.get_type() == 'mine' and cell.is_flagged for row in self.board for cell in row)

    def calculate_maximum_score(self):
        """ Calculate the maximum possible score. """
        max_score = 0
        for row in self.board:
            for cell in row:
                if cell.get_type() != 'mine':
                    max_score += 1
        return max_score + (self.num_mines * self.CORRECT_FLAG_POINTS) 

    def check_for_win(self):
        """function to check if the player has won the game"""
        for row in self.board:
            for cell in row:
                # if we find a cell that is not a mine and is not revealed yet, then we need to keep going
                if not cell.type == 'mine' and not cell.is_revealed:
                    return False
        return True                    
    
    def get_score(self):
        return self.user_score