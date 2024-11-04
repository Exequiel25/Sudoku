import random


SELECTED_WRONG_BG = "pink"   # Background color for the cells with wrong values
# Background color for the cells with right values
SELECTED_RIGHT_BG = "light green"


class SudokuModel:
    def __init__(self):
        self.solution_grid = []
        self.sudoku_grid = []
        self.win = False
        # self.init_game()

    def init_game(self, level=1):
        # Initialize a 9x9 grid for the Sudoku puzzle
        self.solution_grid = self.create_solution_grid()
        # Get the Sudoku grid with some cells removed (depending on level)
        self.sudoku_grid = self.create_sudoku_grid(level)

    def create_solution_grid(self):
        # Create a Sudoku solution grid
        def pattern(r, c): return (3*(r % 3) + r//3 + c) % 9
        def shuffle(s): return random.sample(s, len(s))
        rBase = range(3)
        rows = [g*3 + r for g in shuffle(rBase) for r in shuffle(rBase)]
        cols = [g*3 + c for g in shuffle(rBase) for c in shuffle(rBase)]
        nums = shuffle(range(1, 10))

        grid = [[nums[pattern(r, c)] for c in cols] for r in rows]
        return grid

    def create_sudoku_grid(self, level):
        # Create a Sudoku grid by removing some cells from the solution grid
        grid = [row[:] for row in self.solution_grid]
        # Remove cells based on the level
        if level == 1:
            # Easy level: Remove 40 cells
            self.remove_cells(grid, 40)
        elif level == 2:
            # Medium level: Remove 50 cells
            self.remove_cells(grid, 50)
        elif level == 3:
            # Hard level: Remove 60 cells
            self.remove_cells(grid, 60)
        return grid

    def remove_cells(self, grid, num_cells):
        # Remove num_cells from the grid
        for _ in range(num_cells):
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            grid[row][col] = 0

    def get_grid(self):
        return self.sudoku_grid

    def set_cell_value(self, row, col, value):
        # Check if the value is not between 1 and 9
        if value < 1 or value > 9:
            return False, None

        # Check if the cell is not empty or already a right value
        if self.sudoku_grid[row][col] == self.solution_grid[row][col]:
            return False, None

        # Set the cell value
        self.sudoku_grid[row][col] = value

        # Check if the grid is complete
        self.win = self.sudoku_grid == self.solution_grid

        # If the value is not the same as the solution, return True with red bg color
        if self.sudoku_grid[row][col] != self.solution_grid[row][col]:
            return True, SELECTED_WRONG_BG
        return True, SELECTED_RIGHT_BG

    def has_won(self):
        return self.win
