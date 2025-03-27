import tkinter as tk  # Import tkinter for creating the GUI
from tkinter import messagebox  # Import messagebox for showing pop-up messages
import random  # Import random for generating random numbers and AI moves
import time  # Import time to measure move execution time (optional for now)

class NumberGame:
    def __init__(self, root):
        # Initialize the game with a tkinter window (root)
        self.root = root
        self.root.title("Number Game with AI")  # Set the window title

        # Game variables
        self.string_length = 0  # Length of the number string (set by user, 15-25)
        self.num_string = []  # List to store the current sequence of numbers
        self.player_score = 0  # Human player's score
        self.computer_score = 0  # Computer's score
        self.current_player = "Human"  # Tracks whose turn it is ("Human" or "Computer"), matching radio button values
        self.selected_index = None  # Tracks the first selected number's index during player's turn

        # AI-related variables
        self.algorithm = "Minimax"  # Default algorithm (will be set by user choice)
        self.max_depth = 2 # Depth for Minimax/Alpha-Beta (keep small for performance)

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
        score_diff = computer_score - player_score if is_maximizing else player_score - computer_score
        length_penalty = len(num_string) * 0.1
        return score_diff - length_penalty

    def generate_moves(self, num_string, player_score, computer_score, current_player):
        moves = []
        for i in range(len(num_string) - 1):
            new_num_string = num_string[:]
            first_num, second_num = new_num_string[i], new_num_string[i + 1]
            sum_nums = first_num + second_num

            if sum_nums > 7:
                replacement = 1
                new_player_score = player_score + (1 if current_player == "Human" else 0)
                new_computer_score = computer_score + (1 if current_player == "Computer" else 0)
            elif sum_nums < 7:
                replacement = 3
                new_player_score = player_score - (1 if current_player == "Computer" else 0)
                new_computer_score = computer_score - (1 if current_player == "Human" else 0)
            else:
                replacement = 2
                new_player_score = player_score - (1 if current_player == "Human" else 0)
                new_computer_score = computer_score - (1 if current_player == "Computer" else 0)

            new_num_string.pop(i)
            new_num_string.pop(i)
            new_num_string.insert(i, replacement)

            moves.append({
                'num_string': new_num_string,
                'player_score': new_player_score,
                'computer_score': new_computer_score,
                'move': (i, i + 1)
            })
        return moves

    def minimax(self, num_string, player_score, computer_score, depth, is_maximizing, current_player):
        if depth == 0 or len(num_string) <= 1:
            return self.evaluate_state(num_string, player_score, computer_score, is_maximizing)

        moves = self.generate_moves(num_string, player_score, computer_score, current_player)
        next_player = "Human" if current_player == "Computer" else "Computer"

        if is_maximizing:
            best_value = float('-inf')
            for move in moves:
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, False, next_player
                )
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('inf')
            for move in moves:
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, True, next_player
                )
                best_value = min(best_value, value)
            return best_value

    def alpha_beta(self, num_string, player_score, computer_score, depth, alpha, beta, is_maximizing, current_player):
        if depth == 0 or len(num_string) <= 1:
            return self.evaluate_state(num_string, player_score, computer_score, is_maximizing)

        moves = self.generate_moves(num_string, player_score, computer_score, current_player)
        next_player = "Human" if current_player == "Computer" else "Computer"

        if is_maximizing:
            value = float('-inf')
            for move in moves:
                value = max(value, self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, alpha, beta, False, next_player
                ))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = float('inf')
            for move in moves:
                value = min(value, self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, alpha, beta, True, next_player
                ))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def find_best_move(self):
        moves = self.generate_moves(self.num_string, self.player_score, self.computer_score, "Computer")
        best_value = float('-inf')
        best_move = None

        for move in moves:
            if self.algorithm == "Minimax":
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    self.max_depth - 1, False, "Human"
                )
            else:
                value = self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    self.max_depth - 1, float('-inf'), float('inf'), False, "Human"
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
        self.current_player = self.var_start.get()  # Set based on radio button selection
        print(f"Game started, initial current_player set to: {self.current_player}")  # Debug initial value
        self.algorithm = self.var_algorithm.get()

        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text=f"{'Human' if self.current_player == 'Human' else 'Computer'}'s turn: Select two adjacent numbers:")

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
        print(f"Click detected at index {index}, current_player = {self.current_player}")

        if self.current_player != "Human":
            print("Not player's turn, ignoring click. Expected 'Human', got: {self.current_player}")
            return

        if self.selected_index is None:
            self.selected_index = index
            self.number_buttons[index].config(bg="yellow")
            print(f"First number selected at index {index}, num_string at that index: {self.num_string[index]}")
        else:
            print(f"Second number selected at index {index}, first was {self.selected_index}, num_string: {self.num_string}")
            if index == self.selected_index:
                print("Error: Cannot select the same number twice")
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")
                self.selected_index = None
                return
            if abs(index - self.selected_index) != 1:
                print(f"Error: {index} and {self.selected_index} are not adjacent (difference = {abs(index - self.selected_index)})")
                messagebox.showerror("Error", "Please select adjacent numbers!")
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")
                self.selected_index = None
                return

            print(f"Processing move with indices {self.selected_index} and {index}")
            first_num = self.num_string[self.selected_index]
            second_num = self.num_string[index]
            sum_nums = first_num + second_num
            print(f"Numbers selected: {first_num} + {second_num} = {sum_nums}")

            if sum_nums > 7:
                replacement = 1
                self.player_score += 1
                print("Rule applied: Sum > 7, replacement = 1, player_score += 1")
            elif sum_nums < 7:
                replacement = 3
                self.computer_score -= 1
                print("Rule applied: Sum < 7, replacement = 3, computer_score -= 1")
            else:
                replacement = 2
                self.player_score -= 1
                print("Rule applied: Sum = 7, replacement = 2, player_score -= 1")

            min_idx = min(self.selected_index, index)
            self.num_string.pop(min_idx)
            self.num_string.pop(min_idx)
            self.num_string.insert(min_idx, replacement)
            print(f"Updated num_string: {self.num_string}")

            self.label_string.config(text=f"Number String: {self.num_string}")
            self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

            for button in self.number_buttons:
                button.destroy()
            self.number_buttons.clear()
            print("Old buttons cleared and recreated")

            if len(self.num_string) == 1:
                self.end_game()
                return

            for i in range(len(self.num_string)):
                button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
                button.grid(row=0, column=i)
                self.number_buttons.append(button)

            self.current_player = "Computer"
            print(f"Turn switched to {self.current_player} after move")  # Debug turn switch
            self.label_instruction.config(text=f"{'Human' if self.current_player == 'Human' else 'Computer'}'s turn: Select two adjacent numbers:")
            self.selected_index = None
            self.root.after(1000, self.computer_move)

    def computer_move(self):
        print(f"Computer move starting, current state: {self.num_string}")
        if len(self.num_string) <= 1:
            print("Game over, no computer move")
            return

        move = self.find_best_move()
        if move is None:
            print("No best move found, falling back to random")
            move_start = random.randint(0, len(self.num_string) - 2)
            move_end = move_start + 1
        else:
            move_start, move_end = move
            print(f"Best move found: indices {move_start}, {move_end}")

        first_num = self.num_string[move_start]
        second_num = self.num_string[move_end]
        sum_nums = first_num + second_num
        print(f"Computer move: {first_num} + {second_num} = {sum_nums}")

        if sum_nums > 7:
            replacement = 1
            self.computer_score += 1
            print("Rule applied: Sum > 7, replacement = 1, computer_score += 1")
        elif sum_nums < 7:
            replacement = 3
            self.player_score -= 1
            print("Rule applied: Sum < 7, replacement = 3, player_score -= 1")
        else:
            replacement = 2
            self.computer_score -= 1
            print("Rule applied: Sum = 7, replacement = 2, computer_score -= 1")

        min_idx = min(move_start, move_end)
        self.num_string.pop(min_idx)
        self.num_string.pop(min_idx)
        self.num_string.insert(min_idx, replacement)
        print(f"Updated num_string: {self.num_string}")

        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()
        print("Old buttons cleared and recreated")

        if len(self.num_string) == 1:
            self.end_game()
            return

        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        self.current_player = "Human"
        print(f"Turn switched to {self.current_player} after computer move")  # Debug turn switch
        self.label_instruction.config(text=f"{'Human' if self.current_player == 'Human' else 'Computer'}'s turn: Select two adjacent numbers:")

    def end_game(self):
        winner = "Player" if self.player_score > self.computer_score else "Computer" if self.computer_score > self.player_score else "Tie"
        print(f"Game over, winner: {winner}, Scores - Player: {self.player_score}, Computer: {self.computer_score}")
        messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text="Select two adjacent numbers:")
        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()