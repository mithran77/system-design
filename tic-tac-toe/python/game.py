from board import Board

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

    def play(self):
        while not self.board.is_full() or not self.board.has_winner():
            # Curernt player play
            print(f"{self.current_player.get_name()}'s turn.")
            row = self.get_valid_input("Enter row (0-2): ")
            col = self.get_valid_input("Enter column (0-2): ")
            try:
                self.board.make_move(row, col, self.current_player.get_symbol())
                self.board.print_board()
                self.switch_player()
            except ValueError as e:
                print(str(e))

        if self.board.has_winner():
            self.switch_player()
            print(f"{self.current_player.get_name()} has won!!")
        else:
            print("It is a draw!")

    def switch_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def get_valid_input(self, message):
        while True:
            try:
                idx = int(input(message))
                if idx in range(3):
                    return idx
                else:
                    print("Invalid input! Please enter a number between 0 and 2.")
            except ValueError:
                print("Invalid input! Please enter a number between 0 and 2.")
