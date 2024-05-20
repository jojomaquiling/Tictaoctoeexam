import tkinter as tk
from tkinter import messagebox
import zerorpc
import datetime 
import time
import pdb

# Connect to the ZeroRPC server
c = zerorpc.Client()
c.connect("tcp://127.0.0.1:4242")
c.connect_user()

window = tk.Tk()
window.title("Tic Tac Toe")

# Create board
buttons = [[None for _ in range(3)] for _ in range(3)]

def create_board():
    for i in range(3):
        for j in range(3):
            button = tk.Button(window, text="", font=("Arial", 50), height=2, width=6, bg="lightblue", command=lambda row=i, col=j: handle_click(row, col))
            button.grid(row=i, column=j, sticky="nsew")
            buttons[i][j] = button

create_board()


# Function to disable all buttons
def disable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)

# Function to enable all buttons
def enable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.NORMAL)


# Handle button clicks
def handle_click(row, col):
    # Make the move and update the board
    success = c.make_move(row, col)
    if not success:
        return

    # Get the updated state from the server
    board, current_player, winner = c.get_state()

    # Update the board
    update_board(board)

    # Check if there is a winner
    if winner:
        declare_winner(winner)
    else:
        window.title(f"Tic Tac Toe - Player {current_player}'s turn")
        if current_player == "X":
            enable_buttons()
        else:
            disable_buttons()

# Update the board with the latest state
def update_board(board):    
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=board[i][j] if board[i][j] != 0 else "")

# Declare the winner and ask to restart the game
def declare_winner(winner):
    if winner == "tie":
        message = "It's a tie!"
    else:
        message = f"Player {winner} wins!"

    answer = messagebox.askyesno("Game Over", message + " Do you want to restart the game?")
    if answer:
        c.reset_game()
        board, current_player, _ = c.get_state()
        update_board(board)
        window.title(f"Tic Tac Toe - Player {current_player}'s turn")
    else:
        window.quit()


def check_for_updates():
   # Get the updated state from the server
   board, current_player, winner = c.get_state()
   
   
   # Update the board
   update_board(board)

   # Check if there is a winner
   if winner:
        declare_winner(winner)

   window.title(f"Tic Tac Toe - Player {current_player}'s turn")
   window.after(500, check_for_updates)



def stop_game():
    answer = messagebox.askyesno("Stop Game", "Are you sure you want to stop the game?")
    if answer:
        window.quit()

# Add a "Stop" button
stop_button = tk.Button(window, text="Stop", font=("Arial", 14), command=stop_game)
stop_button.grid(row=3, column=1, columnspan=3, padx=10, pady=10)
window.after(0, check_for_updates)
window.mainloop()

