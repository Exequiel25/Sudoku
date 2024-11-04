import tkinter as tk
import threading

GRID_SIZE = 9   # Size of the Sudoku grid
CELL_SIZE = (5, 2)  # Size of each cell in the grid
FONT = ('Arial', 24)    # Font for the numbers in the grid
SELECTED_BG = "light blue"  # Background color for the selected cell
DEFAULT_BG = "white"  # Default background color for the cells
WRONG_BG = "red"   # Background color for the cells with wrong values
SELECTED_WRONG_BG = "pink"  # Background color for the selected cell with wrong value


class SudokuView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.cells = []
        self.selected_cell = None
        self.ready_for_input = True

        # Bind arrow keys to move the selection
        self.root.bind(
            "<Up>", lambda e: self.controller.handle_keypress(-1, 0))
        self.root.bind(
            "<Down>", lambda e: self.controller.handle_keypress(1, 0))
        self.root.bind(
            "<Left>", lambda e: self.controller.handle_keypress(0, -1))
        self.root.bind(
            "<Right>", lambda e: self.controller.handle_keypress(0, 1))

    def start_menu(self):
        start_label = tk.Label(self.frame, text="Sudoku", font=('Arial', 36))
        start_label.grid(row=0, columnspan=GRID_SIZE)

        for i in range(1, 4):
            level_button = tk.Button(self.frame, text=f"Level {i}", font=FONT,
                                     padx=10, pady=10,
                                     command=lambda i=i: self.controller.start_game(i))
            level_button.grid(row=i, columnspan=GRID_SIZE)

            # Bind keys 1, 2, and 3 to the corresponding button commands
            self.root.bind(str(i), lambda e,
                           i=i: self.controller.start_game(i))

    def reset_input_flag(self):
        self.ready_for_input = True

    def create_grid(self):
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                border_widths = self.get_border_widths(i, j)
                cell = tk.Label(self.frame, text=" ", width=CELL_SIZE[0],
                                height=CELL_SIZE[1], borderwidth=border_widths['borderwidth'],
                                relief="solid", font=FONT, bg=DEFAULT_BG)
                cell.grid(
                    row=i, column=j, padx=border_widths['padx'], pady=border_widths['pady'])
                row.append(cell)
            self.cells.append(row)

    def get_border_widths(self, row, col):
        borderwidth = 1
        padx = 0
        pady = 0
        if row % 3 == 0:
            pady = (2, 0)
        if row % 3 == 2:
            pady = (0, 2)
        if col % 3 == 0:
            padx = (2, 0)
        if col % 3 == 2:
            padx = (0, 2)
        return {'borderwidth': borderwidth, 'padx': padx, 'pady': pady}

    def update_grid(self, grid):
        if not self.cells:
            # Remove the start menu
            for widget in self.frame.winfo_children():
                widget.destroy()
            # Create the Sudoku grid
            self.create_grid()
            # Bind number keys to set the value in the selected cell
            for i in range(1, 10):
                self.root.bind(str(i), self.controller.handle_number_input)
                self.root.bind(
                    f"<KP_{i}>", self.controller.handle_number_input)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = grid[i][j]
                if value == 0:
                    self.cells[i][j].config(text=" ")
                else:
                    self.cells[i][j].config(text=str(value))

    def update_cell(self, row, col, value, bg_color):
        self.cells[row][col].config(text=value, bg=bg_color
                                    if bg_color else DEFAULT_BG)

    def move_selection(self, d_row, d_col):
        if self.selected_cell:
            row, col = self.selected_cell
            # Calculate the new row and column for the selected cell
            new_row = (row + d_row) % GRID_SIZE
            new_col = (col + d_col) % GRID_SIZE
            self.select_cell(new_row, new_col)

    def select_cell(self, row, col):
        if self.selected_cell:
            # Reset the background color of the previously selected cell
            prev_row, prev_col = self.selected_cell
            prev_color = self.cells[prev_row][prev_col].cget('bg')
            if prev_color == SELECTED_WRONG_BG:
                self.cells[prev_row][prev_col].config(bg=WRONG_BG)
            else:
                self.cells[prev_row][prev_col].config(bg=DEFAULT_BG)

        # Update the background color of the newly selected cell
        color_of_cell = self.cells[row][col].cget('bg')
        # Change for selected bg if not a wrong cell
        if color_of_cell != WRONG_BG:
            self.cells[row][col].config(bg=SELECTED_BG)
        else:
            self.cells[row][col].config(bg=SELECTED_WRONG_BG)
        self.selected_cell = (row, col)

    def get_selected_cell(self):
        return self.selected_cell

    def display_win(self):
        win_label = tk.Label(self.frame, text="¡FELICIDADES!", font=FONT)
        win_label.grid(row=GRID_SIZE, columnspan=GRID_SIZE)

    def mainloop(self):
        self.root.mainloop()
