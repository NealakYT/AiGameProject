import tkinter as tk
from tkinter import messagebox
import random

class NumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game with Simple AI")

        # Game variables
        self.string_length = 0
        self.num_string = []
        self.player_score = 0
        self.computer_score = 0
        self.current_player = "Player"

        # GUI setup
        self.label_length = tk.Label(root, text="Enter string length (15-25):")
        self.label_length.pack()

        self.entry_length = tk.Entry(root)
        self.entry_length.pack()

        # Start options
        self.label_start = tk.Label(root, text="Who starts? (Human/Computer)")
        self.label_start.pack()
        self.var_start = tk.StringVar(value="Player")
        self.radio_human = tk.Radiobutton(root, text="Human", variable=self.var_start, value="Player")
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

        self.number_buttons = []  # To store number buttons

    def start_game(self):
        # Validate input length
        try:
            length = int(self.entry_length.get())
            if length < 15 or length > 25:
                messagebox.showerror("Error", "Length must be between 15 and 25!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        # Initialize game state
        self.string_length = length
        self.num_string = [random.randint(1, 9) for _ in range(self.string_length)]
        self.player_score = 0
        self.computer_score = 0
        self.current_player = self.var_start.get()

        # Update GUI
        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

        # Clear old buttons
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        # Create new number buttons
        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        # Enable/disable buttons
        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        # If computer starts, trigger its move
        if self.current_player == "Computer":
            self.root.after(1000, self.computer_move)  # Delay for visibility

    def select_number(self, index):
        if self.current_player != "Player":
            return  # Ignore clicks during computer's turn

        # First number selection
        if not hasattr(self, 'selected_index'):
            self.selected_index = index
            self.number_buttons[index].config(bg="yellow")  # Highlight selection
        else:
            # Check if adjacent
            if abs(index - self.selected_index) != 1:
                messagebox.showerror("Error", "Please select adjacent numbers!")
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")
                del self.selected_index
                return

            # Process the move
            first_num = self.num_string[self.selected_index]
            second_num = self.num_string[index]
            sum_nums = first_num + second_num

            if sum_nums > 7:
                replacement = 1
                self.player_score += 1
            elif sum_nums < 7:
                replacement = 3
                self.computer_score -= 1
            else:  # sum_nums == 7
                replacement = 2
                self.player_score -= 1

            # Update number string
            min_idx = min(self.selected_index, index)
            self.num_string.pop(min_idx)
            self.num_string.pop(min_idx)
            self.num_string.insert(min_idx, replacement)

            # Update GUI
            self.label_string.config(text=f"Number String: {self.num_string}")
            self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

            # Recreate buttons
            for button in self.number_buttons:
                button.destroy()
            self.number_buttons.clear()

            if len(self.num_string) == 1:
                self.end_game()
                return

            for i in range(len(self.num_string)):
                button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
                button.grid(row=0, column=i)
                self.number_buttons.append(button)

            # Switch to computer
            self.current_player = "Computer"
            self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")
            del self.selected_index
            self.root.after(1000, self.computer_move)

    def computer_move(self):
        if len(self.num_string) <= 1:
            return

        # Randomly pick two adjacent numbers
        move_start = random.randint(0, len(self.num_string) - 2)  # Ensure there's a next number
        move_end = move_start + 1

        # Process the move
        first_num = self.num_string[move_start]
        second_num = self.num_string[move_end]
        sum_nums = first_num + second_num

        if sum_nums > 7:
            replacement = 1
            self.computer_score += 1
        elif sum_nums < 7:
            replacement = 3
            self.player_score -= 1
        else:  # sum_nums == 7
            replacement = 2
            self.computer_score -= 1

        # Update number string
        min_idx = min(move_start, move_end)
        self.num_string.pop(min_idx)
        self.num_string.pop(min_idx)
        self.num_string.insert(min_idx, replacement)

        # Update GUI
        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

        # Recreate buttons
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        if len(self.num_string) == 1:
            self.end_game()
            return

        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        # Switch to player
        self.current_player = "Player"
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

    def end_game(self):
        # Determine winner
        winner = "Player" if self.player_score > self.computer_score else "Computer" if self.computer_score > self.player_score else "Tie"
        messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text="Select two adjacent numbers:")
        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()