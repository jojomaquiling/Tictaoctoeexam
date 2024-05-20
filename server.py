import zerorpc
import itertools

class TicTacToeServer:
    def __init__(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.current_player = "X"
        self.connected_users = []

    def make_move(self, row, col):
        if self.board[row][col] == 0:
            player = self.current_player
            self.board[row][col] = player
            return True
        else:
            return False

    def get_state(self):
        winner = self.check_for_winner()
        if winner:
            self.reset_game()
            return self.board, None, winner
        return self.board, self.current_player, None

    def reset_game(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.current_player = 'X'

    def check_for_winner(self):
        # Check rows
        for row in self.board:
            if row.count(row[0]) == len(row) and row[0] != 0:
                return row[0]

        # Check columns
        for col in range(len(self.board)):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != 0:
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != 0:
            return self.board[0][0]
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != 0:
            return self.board[0][2]

        # Check for a tie
        if all(all(row) for row in self.board):
            return "tie"

        return None

    def connect_user(self, user_id='X'):
        if (len(self.connected_users) == 0):    
           self.connected_users.append('X')
           return 'X'
        elif (len(self.connected_users) == 1):
           self.connected_users.append('O')
           return 'O'
        else:
           return None 


    def disconnect_user(self, user_id):
        if user_id in self.connected_users:
            del self.connected_users[user_id]


def main():
    server = zerorpc.Server(TicTacToeServer())
    server.bind("tcp://0.0.0.0:4242")
    print ("TicTacToe server running in port 4242")
    server.run()

if __name__ == "__main__":
    main()

