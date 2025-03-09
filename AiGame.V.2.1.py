import tkinter as tk
from tkinter import messagebox
import random
import time

class NumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game with Simple AI")

        # Game variables
        self.string_length = 0
        self.num_string = []
        self.player_score = 0
        self.computer_score = 0
        self.current_player = "Player"  # Will be set by user choice
        self.selected_index = None

        # GUI elements
        self.label_length = tk.Label(root, text="Enter string length (15-25):")
        self.label_length.pack()

        self.entry_length = tk.Entry(root)
        self.entry_length.pack()

        # Start options: Human or Computer
        self.label_start = tk.Label(root, text="Who starts? (Human/Computer)")
        self.label_start.pack()
        self.var_start = tk.StringVar(value="Human")
        self.radio_human = tk.Radiobutton(root, text="Human", variable=self.var_start, value="Human")
        self.radio_computer = tk.Radiobutton(root, text="Computer", variable=self.var_start, value="Computer")
        self.radio_human.pack()
        self.radio_computer.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.new_game_button = tk.Button(root, text="New Game", command=self.start_game, state=tk.DISABLED)
        self.new_game_button.pack()

        self.label_string = tk.Label(root, text="Number String: ")
        self.label_string.pack()

        self.label_scores = tk.Label(root, text="Player: 0 | Computer: 0")
        self.label_scores.pack()

        self.label_instruction = tk.Label(root, text="Select two adjacent numbers:")
        self.label_instruction.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.number_buttons = []

    def start_game(self):
        # Validate string length
        try:
            length = int(self.entry_length.get())
            if length < 15 or length > 25:
                messagebox.showerror("Error", "Length must be between 15 and 25!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        self.string_length = length
        self.num_string = [random.randint(1, 9) for _ in range(self.string_length)]
        self.player_score = 0
        self.computer_score = 0
        self.current_player = self.var_start.get()  # Set starting player

        # Update GUI
        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

        # Clear previous buttons
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        # Create buttons for each number
        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        # If computer starts, make its move
        if self.current_player == "Computer":
            self.root.after(1000, self.computer_move)  # Delay for better UX

    def select_number(self, index):
        # Human player's turn
        if self.current_player != "Player":
            return  # Ignore clicks during computer's turn

        if not hasattr(self, 'selected_index'):
            self.selected_index = index
            self.number_buttons[index].config(bg="yellow")
        else:
            # Check if the second selection is adjacent to the first
            if abs(index - self.selected_index) != 1:
                messagebox.showerror("Error", "Please select adjacent numbers!")
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")
                del self.selected_index
                return

            # Process the player's move
            self.process_move(self.selected_index, index)
            del self.selected_index

    def process_move(self, index1, index2):
        # Ensure indices are in order
        min_idx = min(index1, index2)
        first_num = self.num_string[min_idx]
        second_num = self.num_string[min_idx + 1]
        sum_nums = first_num + second_num

        # Determine replacement and scoring
        if sum_nums > 7:
            replacement = 1
            if self.current_player == "Player":
                self.player_score += 1
            else:
                self.computer_score += 1
        elif sum_nums < 7:
            replacement = 3
            if self.current_player == "Player":
                self.computer_score -= 1
            else:
                self.player_score -= 1
        else:  # sum == 7
            replacement = 2
            if self.current_player == "Player":
                self.player_score -= 1
            else:
                self.computer_score -= 1

        # Replace the pair with the new number
        self.num_string.pop(min_idx)
        self.num_string.pop(min_idx)
        self.num_string.insert(min_idx, replacement)

        # Update GUI
        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

        # Clear buttons
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        # Check if game is over
        if len(self.num_string) == 1:
            winner = "Player" if self.player_score > self.computer_score else "Computer" if self.computer_score > self.player_score else "Tie"
            messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.player_score} | Computer: {self.computer_score}")
            self.label_instruction.config(text="Select two adjacent numbers:")
            self.new_game_button.config(state=tk.NORMAL)
            self.start_button.config(state=tk.NORMAL)
            return

        # Recreate buttons for the updated string
        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        # Switch player
        self.current_player = "Computer" if self.current_player == "Player" else "Player"
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

        # If it's now the computer's turn, make its move
        if self.current_player == "Computer":
            self.root.after(1000, self.computer_move)  # Delay for better UX

    def computer_move(self):
        if len(self.num_string) <= 1:
            return  # Game is over

        # Simple AI: Randomly select two adjacent numbers
        possible_moves = list(range(len(self.num_string) - 1))  # Indices where a move can start
        if not possible_moves:
            return  # No moves available (shouldn't happen if len > 1)

        move_start = random.choice(possible_moves)
        move_end = move_start + 1

        # Process the computer's move
        self.process_move(move_start, move_end)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()