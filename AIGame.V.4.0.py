import tkinter as tk
from tkinter import messagebox
import random

class GameState:
    def __init__(self, num_string, player_score, computer_score, current_player):
        self.num_string = num_string[:]  # Copy of the number string
        self.player_score = player_score
        self.computer_score = computer_score
        self.current_player = current_player
        self.children = []  # Possible next states
        self.move = None  # (index1, index2) of the move

# Heuristic function: Favor the computer by maximizing score difference
def evaluate_state(state):
    score_diff = state.computer_score - state.player_score  # Maximize computer's score
    # Add a small penalty for longer strings to encourage ending the game
    length_penalty = len(state.num_string) * 0.1
    return score_diff - length_penalty

class NumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game with Minimax AI")

        # Game variables
        self.string_length = 0
        self.current_state = None
        self.max_depth = 3  # N-ply look-ahead for Minimax

        # GUI elements
        self.label_length = tk.Label(root, text="Enter string length (15-25):")
        self.label_length.pack()

        self.entry_length = tk.Entry(root)
        self.entry_length.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.label_string = tk.Label(root, text="Number String: ")
        self.label_string.pack()

        self.label_scores = tk.Label(root, text="Player: 0 | Computer: 0")
        self.label_scores.pack()

        self.label_instruction = tk.Label(root, text="Select two adjacent numbers:")
        self.label_instruction.pack()

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.number_buttons = []

    def generate_game_tree(self, state, depth, max_depth):
        if depth >= max_depth or len(state.num_string) <= 1:
            return
        for i in range(len(state.num_string) - 1):
            new_num_string = state.num_string[:]
            first_num, second_num = new_num_string[i], new_num_string[i + 1]
            sum_nums = first_num + second_num

            # Determine replacement and scoring
            if sum_nums > 7:
                replacement = 1
                new_player_score = state.player_score + (1 if state.current_player == "Player" else 0)
                new_computer_score = state.computer_score + (1 if state.current_player == "Computer" else 0)
            elif sum_nums < 7:
                replacement = 3
                new_player_score = state.player_score - (1 if state.current_player == "Computer" else 0)
                new_computer_score = state.computer_score - (1 if state.current_player == "Player" else 0)
            else:
                replacement = 2
                new_player_score = state.player_score - (1 if state.current_player == "Player" else 0)
                new_computer_score = state.computer_score - (1 if state.current_player == "Computer" else 0)

            new_num_string.pop(i)
            new_num_string.pop(i)
            new_num_string.insert(i, replacement)
            new_state = GameState(
                num_string=new_num_string,
                player_score=new_player_score,
                computer_score=new_computer_score,
                current_player="Computer" if state.current_player == "Player" else "Player"
            )
            new_state.move = (i, i + 1)
            state.children.append(new_state)
            self.generate_game_tree(new_state, depth + 1, max_depth)

    def minimax(self, state, depth, is_maximizing):
        if depth == 0 or len(state.num_string) <= 1:
            return evaluate_state(state)
        if is_maximizing:  # Computer's turn (maximizing)
            max_eval = float('-inf')
            for child in state.children:
                eval_value = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval_value)
            return max_eval
        else:  # Player's turn (minimizing)
            min_eval = float('inf')
            for child in state.children:
                eval_value = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval_value)
            return min_eval

    def find_best_move(self, state):
        best_value = float('-inf')
        best_move = None
        for child in state.children:
            value = self.minimax(child, self.max_depth - 1, False)  # Computer is maximizing
            if value > best_value:
                best_value = value
                best_move = child.move
        return best_move

    def start_game(self):
        try:
            length = int(self.entry_length.get())
            if length < 15 or length > 25:
                messagebox.showerror("Error", "Length must be between 15 and 25!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        self.string_length = length
        num_string = [random.randint(1, 9) for _ in range(self.string_length)]
        self.current_state = GameState(num_string, 0, 0, "Player")
        self.generate_game_tree(self.current_state, 0, self.max_depth)

        self.label_string.config(text=f"Number String: {self.current_state.num_string}")
        self.label_scores.config(text=f"Player: {self.current_state.player_score} | Computer: {self.current_state.computer_score}")
        self.label_instruction.config(text=f"{self.current_state.current_player}'s turn: Select two adjacent numbers:")

        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        for i in range(len(self.current_state.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.current_state.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

    def select_number(self, index):
        if not hasattr(self, 'selected_index'):
            self.selected_index = index
            self.number_buttons[index].config(bg="yellow")
        else:
            if abs(index - self.selected_index) != 1:
                messagebox.showerror("Error", "Please select adjacent numbers!")
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")
                del self.selected_index
                return

            move = (min(self.selected_index, index), max(self.selected_index, index))
            for child in self.current_state.children:
                if child.move == move:
                    self.current_state = child
                    break

            self.label_string.config(text=f"Number String: {self.current_state.num_string}")
            self.label_scores.config(text=f"Player: {self.current_state.player_score} | Computer: {self.current_state.computer_score}")

            for button in self.number_buttons:
                button.destroy()
            self.number_buttons.clear()

            if len(self.current_state.num_string) == 1:
                winner = "Player" if self.current_state.player_score > self.current_state.computer_score else "Computer" if self.current_state.computer_score > self.current_state.player_score else "Tie"
                messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.current_state.player_score} | Computer: {self.current_state.computer_score}")
                self.label_instruction.config(text="Select two adjacent numbers:")
                return

            for i in range(len(self.current_state.num_string)):
                button = tk.Button(self.buttons_frame, text=str(self.current_state.num_string[i]), command=lambda idx=i: self.select_number(idx))
                button.grid(row=0, column=i)
                self.number_buttons.append(button)

            self.current_state.current_player = "Computer"
            self.label_instruction.config(text=f"{self.current_state.current_player}'s turn: Select two adjacent numbers:")

            del self.selected_index
            if self.current_state.current_player == "Computer":
                self.root.after(1000, self.computer_move)

    def computer_move(self):
        if len(self.current_state.num_string) <= 1:
            return

        # Use Minimax to find the best move
        move = self.find_best_move(self.current_state)
        if move is None:
            return  # No valid moves (shouldn't happen)

        # Apply the best move by selecting the corresponding child state
        for child in self.current_state.children:
            if child.move == move:
                self.current_state = child
                break

        # Clear the game tree and regenerate for the new state
        self.current_state.children = []
        self.generate_game_tree(self.current_state, 0, self.max_depth)

        # Update GUI
        self.label_string.config(text=f"Number String: {self.current_state.num_string}")
        self.label_scores.config(text=f"Player: {self.current_state.player_score} | Computer: {self.current_state.computer_score}")

        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        if len(self.current_state.num_string) == 1:
            winner = "Player" if self.current_state.player_score > self.current_state.computer_score else "Computer" if self.current_state.computer_score > self.current_state.player_score else "Tie"
            messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.current_state.player_score} | Computer: {self.current_state.computer_score}")
            self.label_instruction.config(text="Select two adjacent numbers:")
            return

        for i in range(len(self.current_state.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.current_state.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        self.current_state.current_player = "Player"
        self.label_instruction.config(text=f"{self.current_state.current_player}'s turn: Select two adjacent numbers:")

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()