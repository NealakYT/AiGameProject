import tkinter as tk  # Import tkinter for creating the GUI
from tkinter import messagebox  # Import messagebox for showing pop-up messages
import random  # Import random for generating random numbers and AI moves
import time  # Import time to measure move execution time (optional for now)

class NumberGame:
    def __init__(self, root):
        # Initialize the game with a tkinter window (root)
        self.root = root
        self.root.title("Number Game with AI")

        # Game variables
        self.string_length = 0  # Length of the number string (set by user, 15-25)
        self.num_string = []  # List to store the current sequence of numbers
        self.player_score = 0  # Human player's score
        self.computer_score = 0  # Computer's score
        self.current_player = "Player"  # Tracks whose turn it is ("Player" or "Computer")
        self.selected_index = None  # Tracks the first selected number's index during player's turn

        # AI-related variables
        self.algorithm = "Minimax"  # Default algorithm (will be set by user choice)
        self.max_depth = 2  # Depth for Minimax/Alpha-Beta (keep small for performance)

        # GUI setup: Create and pack all widgets
        # Label and entry for user to input the string length
        self.label_length = tk.Label(root, text="Enter string length (15-25):")
        self.label_length.pack()

        self.entry_length = tk.Entry(root)
        self.entry_length.pack()

        # Radio buttons to choose who starts (Human or Computer)
        self.label_start = tk.Label(root, text="Who starts? (Human/Computer)")
        self.label_start.pack()
        self.var_start = tk.StringVar(value="Human")  # Default to Human starting
        self.radio_human = tk.Radiobutton(root, text="Human", variable=self.var_start, value="Human")
        self.radio_computer = tk.Radiobutton(root, text="Computer", variable=self.var_start, value="Computer")
        self.radio_human.pack()
        self.radio_computer.pack()

        # Radio buttons to choose AI algorithm (Minimax or Alpha-Beta)
        self.label_algorithm = tk.Label(root, text="Choose AI algorithm (Minimax/Alpha-Beta):")
        self.label_algorithm.pack()
        self.var_algorithm = tk.StringVar(value="Minimax")  # Default to Minimax
        self.radio_minimax = tk.Radiobutton(root, text="Minimax", variable=self.var_algorithm, value="Minimax")
        self.radio_alphabeta = tk.Radiobutton(root, text="Alpha-Beta", variable=self.var_algorithm, value="AlphaBeta")
        self.radio_minimax.pack()
        self.radio_alphabeta.pack()

        # Button to start the game
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        # Button to start a new game (disabled until the game ends)
        self.new_game_button = tk.Button(root, text="New Game", command=self.start_game, state=tk.DISABLED)
        self.new_game_button.pack()

        # Labels to display the number string, scores, and instructions
        self.label_string = tk.Label(root, text="Number String: ")
        self.label_string.pack()

        self.label_scores = tk.Label(root, text="Player: 0 | Computer: 0")
        self.label_scores.pack()

        self.label_instruction = tk.Label(root, text="Select two adjacent numbers:")
        self.label_instruction.pack()

        # Frame to hold the number buttons and list to store them
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.number_buttons = []  # List to store the buttons for each number

    def evaluate_state(self, num_string, player_score, computer_score, is_maximizing):
        # Heuristic function to evaluate a game state
        # Favor states where the computer has a higher score (maximizing)
        # or the player has a lower score (minimizing)
        score_diff = computer_score - player_score if is_maximizing else player_score - computer_score
        # Add a small penalty for longer strings to encourage ending the game
        length_penalty = len(num_string) * 0.1
        return score_diff - length_penalty

    def generate_moves(self, num_string, player_score, computer_score, current_player):
        # Generate all possible moves (states) from the current state
        moves = []
        for i in range(len(num_string) - 1):  # Iterate through adjacent pairs
            new_num_string = num_string[:]  # Copy the current string
            first_num, second_num = new_num_string[i], new_num_string[i + 1]
            sum_nums = first_num + second_num

            # Apply game rules for the move
            if sum_nums > 7:
                replacement = 1
                new_player_score = player_score + (1 if current_player == "Player" else 0)
                new_computer_score = computer_score + (1 if current_player == "Computer" else 0)
            elif sum_nums < 7:
                replacement = 3
                new_player_score = player_score - (1 if current_player == "Computer" else 0)
                new_computer_score = computer_score - (1 if current_player == "Player" else 0)
            else:  # sum == 7
                replacement = 2
                new_player_score = player_score - (1 if current_player == "Player" else 0)
                new_computer_score = computer_score - (1 if current_player == "Computer" else 0)

            # Create new number string after the move
            new_num_string.pop(i)
            new_num_string.pop(i)
            new_num_string.insert(i, replacement)

            # Store the new state and the move that led to it
            moves.append({
                'num_string': new_num_string,
                'player_score': new_player_score,
                'computer_score': new_computer_score,
                'move': (i, i + 1)  # The indices of the selected numbers
            })
        return moves

    def minimax(self, num_string, player_score, computer_score, depth, is_maximizing, current_player):
        # Minimax algorithm to evaluate the best move
        # Base case: stop at max depth or if game is over
        if depth == 0 or len(num_string) <= 1:
            return self.evaluate_state(num_string, player_score, computer_score, is_maximizing)

        # Generate all possible moves
        moves = self.generate_moves(num_string, player_score, computer_score, current_player)
        next_player = "Player" if current_player == "Computer" else "Computer"

        if is_maximizing:  # Computer's turn (maximize)
            best_value = float('-inf')
            for move in moves:
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, False, next_player
                )
                best_value = max(best_value, value)
            return best_value
        else:  # Player's turn (minimize)
            best_value = float('inf')
            for move in moves:
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, True, next_player
                )
                best_value = min(best_value, value)
            return best_value

    def alpha_beta(self, num_string, player_score, computer_score, depth, alpha, beta, is_maximizing, current_player):
        # Alpha-Beta pruning algorithm to evaluate the best move
        # Base case: stop at max depth or if game is over
        if depth == 0 or len(num_string) <= 1:
            return self.evaluate_state(num_string, player_score, computer_score, is_maximizing)

        # Generate all possible moves
        moves = self.generate_moves(num_string, player_score, computer_score, current_player)
        next_player = "Player" if current_player == "Computer" else "Computer"

        if is_maximizing:  # Computer's turn (maximize)
            value = float('-inf')
            for move in moves:
                value = max(value, self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, alpha, beta, False, next_player
                ))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cutoff
            return value
        else:  # Player's turn (minimize)
            value = float('inf')
            for move in moves:
                value = min(value, self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, alpha, beta, True, next_player
                ))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return value

    def find_best_move(self):
        # Find the best move using the selected algorithm
        moves = self.generate_moves(self.num_string, self.player_score, self.computer_score, "Computer")
        best_value = float('-inf')
        best_move = None

        for move in moves:
            if self.algorithm == "Minimax":
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    self.max_depth - 1, False, "Player"
                )
            else:  # Alpha-Beta
                value = self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    self.max_depth - 1, float('-inf'), float('inf'), False, "Player"
                )
            if value > best_value:
                best_value = value
                best_move = move['move']

        return best_move

    def start_game(self):
        # Start a new game by initializing the game state and GUI
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
        self.current_player = self.var_start.get()
        self.algorithm = self.var_algorithm.get()  # Set the chosen algorithm

        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        if self.current_player == "Computer":
            self.root.after(1000, self.computer_move)

    def select_number(self, index):
        # Handle the human player's selection of numbers
        if self.current_player != "Player":
            return

        if not hasattr(self, 'selected_index'):
            self.selected_index = index
            self.number_buttons[index].config(bg="yellow")
        else:
            if abs(index - self.selected_index) != 1:
                messagebox.showerror("Error", "Please select adjacent numbers!")
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")
                del self.selected_index
                return

            first_num = self.num_string[self.selected_index]
            second_num = self.num_string[index]
            sum_nums = first_num + second_num

            if sum_nums > 7:
                replacement = 1
                self.player_score += 1
            elif sum_nums < 7:
                replacement = 3
                self.computer_score -= 1
            else:
                replacement = 2
                self.player_score -= 1

            min_idx = min(self.selected_index, index)
            self.num_string.pop(min_idx)
            self.num_string.pop(min_idx)
            self.num_string.insert(min_idx, replacement)

            self.label_string.config(text=f"Number String: {self.num_string}")
            self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

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

            self.current_player = "Computer"
            self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")
            del self.selected_index
            self.root.after(1000, self.computer_move)

    def computer_move(self):
        # Handle the computer's turn using the selected AI algorithm
        if len(self.num_string) <= 1:
            return

        # Use the selected algorithm to find the best move
        move = self.find_best_move()
        if move is None:  # Fallback to random move if no move found (shouldn't happen)
            move_start = random.randint(0, len(self.num_string) - 2)
            move_end = move_start + 1
        else:
            move_start, move_end = move

        first_num = self.num_string[move_start]
        second_num = self.num_string[move_end]
        sum_nums = first_num + second_num

        if sum_nums > 7:
            replacement = 1
            self.computer_score += 1
        elif sum_nums < 7:
            replacement = 3
            self.player_score -= 1
        else:
            replacement = 2
            self.computer_score -= 1

        min_idx = min(move_start, move_end)
        self.num_string.pop(min_idx)
        self.num_string.pop(min_idx)
        self.num_string.insert(min_idx, replacement)

        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

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

        self.current_player = "Player"
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

    def end_game(self):
        # End the game and display the result
        winner = "Player" if self.player_score > self.computer_score else "Computer" if self.computer_score > self.player_score else "Tie"
        messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text="Select two adjacent numbers:")
        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()