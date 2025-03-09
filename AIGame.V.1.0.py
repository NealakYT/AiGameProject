import tkinter as tk
from tkinter import messagebox
import random

class NumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game")

        # Game variables
        self.string_length = 0
        self.num_string = []
        self.player_score = 0
        self.opponent_score = 0
        self.current_player = "Player"  # Alternates between "Player" and "Opponent"

        # GUI elements
        self.label_length = tk.Label(root, text="Enter string length (15-25):")
        self.label_length.pack()

        self.entry_length = tk.Entry(root)
        self.entry_length.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.label_string = tk.Label(root, text="Number String: ")
        self.label_string.pack()

        self.label_scores = tk.Label(root, text="Player: 0 | Opponent: 0")
        self.label_scores.pack()

        self.label_instruction = tk.Label(root, text="Select two adjacent numbers:")
        self.label_instruction.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.number_buttons = []

    def start_game(self):
        # Get and validate string length
        try:
            length = int(self.entry_length.get())
            if length < 15 or length > 25:
                messagebox.showerror("Error", "Length must be between 15 and 25!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        self.string_length = length
        # Generate random number string (1 to 9)
        self.num_string = [random.randint(1, 9) for _ in range(self.string_length)]
        self.player_score = 0
        self.opponent_score = 0
        self.current_player = "Player"

        # Update GUI
        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Opponent: {self.opponent_score}")
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

    def select_number(self, index):
        # Highlight selected number by changing its button color
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

            # Process the move
            first_num = self.num_string[self.selected_index]
            second_num = self.num_string[index]
            sum_nums = first_num + second_num

            # Determine replacement and scoring
            if sum_nums > 7:
                replacement = 1
                if self.current_player == "Player":
                    self.player_score += 1
                else:
                    self.opponent_score += 1
            elif sum_nums < 7:
                replacement = 3
                if self.current_player == "Player":
                    self.opponent_score -= 1
                else:
                    self.player_score -= 1
            else:  # sum == 7
                replacement = 2
                if self.current_player == "Player":
                    self.player_score -= 1
                else:
                    self.opponent_score -= 1

            # Replace the pair with the new number
            min_idx = min(self.selected_index, index)
            self.num_string.pop(min_idx)
            self.num_string.pop(min_idx)
            self.num_string.insert(min_idx, replacement)

            # Update GUI
            self.label_string.config(text=f"Number String: {self.num_string}")
            self.label_scores.config(text=f"Player: {self.player_score} | Opponent: {self.opponent_score}")

            # Clear buttons
            for button in self.number_buttons:
                button.destroy()
            self.number_buttons.clear()

            # Check if game is over
            if len(self.num_string) == 1:
                winner = "Player" if self.player_score > self.opponent_score else "Opponent" if self.opponent_score > self.player_score else "Tie"
                messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.player_score} | Opponent: {self.opponent_score}")
                self.label_instruction.config(text="Select two adjacent numbers:")
                return

            # Recreate buttons for the updated string
            for i in range(len(self.num_string)):
                button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
                button.grid(row=0, column=i)
                self.number_buttons.append(button)

            # Switch player
            self.current_player = "Opponent" if self.current_player == "Player" else "Player"
            self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

            # Clear selection
            del self.selected_index

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()