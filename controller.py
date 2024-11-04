from model import SudokuModel
from view import SudokuView


class SudokuController:
    def __init__(self):
        self.model = SudokuModel()
        self.view = SudokuView(self)

    def run(self):
        self.view.start_menu()
        self.view.mainloop()

    def start_game(self, level):
        self.model.init_game(level)
        self.view.update_grid(self.model.get_grid())
        self.view.select_cell(0, 0)  # Select the first cell

    def handle_keypress(self, row_delta, col_delta):
        if self.view.ready_for_input:
            self.view.move_selection(row_delta, col_delta)
            self.view.ready_for_input = False
            self.view.root.after(1000, self.view.reset_input_flag)

    def handle_number_input(self, event):
        if self.view.selected_cell and self.view.ready_for_input:
            row, col = self.view.get_selected_cell()
            success, bg_color = self.model.set_cell_value(
                row, col, int(event.char))
            if success:
                self.view.update_cell(row, col, event.char, bg_color)
                if self.model.has_won():
                    self.view.display_win()
            self.view.ready_for_input = False
            self.view.root.after(1000, self.view.reset_input_flag)
