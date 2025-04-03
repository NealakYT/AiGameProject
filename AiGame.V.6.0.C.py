import tkinter as tk  # Import tkinter for GUI creation
from tkinter import messagebox  # Import messagebox for displaying pop-up messages
import random  # Import random for generating random numbers and AI moves
import time  # Import time for potential move timing (not currently used)

class NumberGame:
    def __init__(self, root):
        # Initialize the game with a tkinter window
        self.root = root
        self.root.title("Number Game with AI")  # Set window title

        # Initialize game state variables
        self.string_length = 0  # Length of the number string (user-defined, 15-25)
        self.num_string = []  # List to store the sequence of numbers
        self.player_score = 0  # Human player's score
        self.computer_score = 0  # Computer's score
        self.current_player = "Human"  # Track current player ("Human" or "Computer")
        self.selected_index = None  # Track the first selected number's index

        # Initialize AI settings
        self.algorithm = "Minimax"  # Default AI algorithm (user can choose Minimax or Alpha-Beta)
        self.max_depth = 2 # Maximum depth for AI search algorithms

        # Set up GUI elements
        self.label_length = tk.Label(root, text="Enter string length (15-25):")  # Label for string length input
        self.label_length.pack()
        self.entry_length = tk.Entry(root)  # Entry field for string length
        self.entry_length.pack()

        # Radio buttons for selecting starting player
        self.label_start = tk.Label(root, text="Who starts? (Human/Computer)")  # Label for starting player selection
        self.label_start.pack()
        self.var_start = tk.StringVar(value="Human")  # Default starting player is Human
        self.radio_human = tk.Radiobutton(root, text="Human", variable=self.var_start, value="Human")  # Human option
        self.radio_computer = tk.Radiobutton(root, text="Computer", variable=self.var_start, value="Computer")  # Computer option
        self.radio_human.pack()
        self.radio_computer.pack()

        # Radio buttons for selecting AI algorithm
        self.label_algorithm = tk.Label(root, text="Choose AI algorithm (Minimax/Alpha-Beta):")  # Label for algorithm selection
        self.label_algorithm.pack()
        self.var_algorithm = tk.StringVar(value="Minimax")  # Default algorithm is Minimax
        self.radio_minimax = tk.Radiobutton(root, text="Minimax", variable=self.var_algorithm, value="Minimax")  # Minimax option
        self.radio_alphabeta = tk.Radiobutton(root, text="Alpha-Beta", variable=self.var_algorithm, value="AlphaBeta")  # Alpha-Beta option
        self.radio_minimax.pack()
        self.radio_alphabeta.pack()

        # Buttons for game control
        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)  # Button to start the game
        self.start_button.pack()
        self.new_game_button = tk.Button(root, text="New Game", command=self.start_game, state=tk.DISABLED)  # Button to start a new game (initially disabled)
        self.new_game_button.pack()

        # Labels for game information
        self.label_string = tk.Label(root, text="Number String: ")  # Label to display the number string
        self.label_string.pack()
        self.label_scores = tk.Label(root, text="Player: 0 | Computer: 0")  # Label to display scores
        self.label_scores.pack()
        self.label_instruction = tk.Label(root, text="Select two adjacent numbers:")  # Label for game instructions
        self.label_instruction.pack()

        # Frame and list for number buttons
        self.buttons_frame = tk.Frame(root)  # Frame to hold number buttons
        self.buttons_frame.pack()
        self.number_buttons = []  # List to store number buttons

    def evaluate_state(self, num_string, player_score, computer_score, is_maximizing):
        # Heuristic function to evaluate a game state for AI decision-making
        # Calculate score difference based on perspective (maximizing for computer, minimizing for human)
        score_diff = computer_score - player_score if is_maximizing else player_score - computer_score
        return score_diff

    def generate_moves(self, num_string, player_score, computer_score, current_player):
        # Generate all possible moves from the current game state
        moves = []  # List to store possible moves
        for i in range(len(num_string) - 1):  # Iterate through adjacent pairs
            new_num_string = num_string[:]  # Create a copy of the current number string
            first_num, second_num = new_num_string[i], new_num_string[i + 1]  # Get the two adjacent numbers
            sum_nums = first_num + second_num  # Calculate their sum

            # Apply game rules based on the sum
            if sum_nums > 7:
                replacement = 1  # Replace with 1 if sum > 7
                new_player_score = player_score + (1 if current_player == "Human" else 0)  # Update human score
                new_computer_score = computer_score + (1 if current_player == "Computer" else 0)  # Update computer score
            elif sum_nums < 7:
                replacement = 3  # Replace with 3 if sum < 7
                new_player_score = player_score - (1 if current_player == "Computer" else 0)  # Update human score
                new_computer_score = computer_score - (1 if current_player == "Human" else 0)  # Update computer score
            else:  # Sum equals 7
                replacement = 2  # Replace with 2 if sum = 7
                new_player_score = player_score - (1 if current_player == "Human" else 0)  # Update human score
                new_computer_score = computer_score - (1 if current_player == "Computer" else 0)  # Update computer score

            # Update the number string by removing the pair and inserting the replacement
            new_num_string.pop(i)
            new_num_string.pop(i)
            new_num_string.insert(i, replacement)

            # Store the new game state as a dictionary
            moves.append({
                'num_string': new_num_string,  # Updated number string
                'player_score': new_player_score,  # Updated human score
                'computer_score': new_computer_score,  # Updated computer score
                'move': (i, i + 1)  # Indices of the selected numbers
            })
        return moves  # Return the list of possible moves

    def minimax(self, num_string, player_score, computer_score, depth, is_maximizing, current_player):
        # Minimax algorithm for evaluating the best move
        # Base case: stop if maximum depth is reached or game is over
        if depth == 0 or len(num_string) <= 1:
            return self.evaluate_state(num_string, player_score, computer_score, is_maximizing)

        # Generate all possible moves
        moves = self.generate_moves(num_string, player_score, computer_score, current_player)
        next_player = "Human" if current_player == "Computer" else "Computer"  # Switch player for next turn

        # Maximizing player's turn (computer)
        if is_maximizing:
            best_value = float('-inf')  # Initialize best value to negative infinity
            for move in moves:
                # Recursively evaluate the move
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, False, next_player
                )
                best_value = max(best_value, value)  # Update best value if current value is higher
            return best_value  # Return the best value for maximizing player
        # Minimizing player's turn (human)
        else:
            best_value = float('inf')  # Initialize best value to positive infinity
            for move in moves:
                # Recursively evaluate the move
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, True, next_player
                )
                best_value = min(best_value, value)  # Update best value if current value is lower
            return best_value  # Return the best value for minimizing player

    def alpha_beta(self, num_string, player_score, computer_score, depth, alpha, beta, is_maximizing, current_player):
        # Alpha-Beta pruning algorithm for evaluating the best move
        # Base case: stop if maximum depth is reached or game is over
        if depth == 0 or len(num_string) <= 1:
            return self.evaluate_state(num_string, player_score, computer_score, is_maximizing)

        # Generate all possible moves
        moves = self.generate_moves(num_string, player_score, computer_score, current_player)
        next_player = "Human" if current_player == "Computer" else "Computer"  # Switch player for next turn

        # Maximizing player's turn (computer)
        if is_maximizing:
            value = float('-inf')  # Initialize value to negative infinity
            for move in moves:
                # Recursively evaluate the move
                value = max(value, self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, alpha, beta, False, next_player
                ))
                alpha = max(alpha, value)  # Update alpha with the best value found
                if beta <= alpha:  # Prune if beta is less than or equal to alpha
                    break
            return value  # Return the best value for maximizing player
        # Minimizing player's turn (human)
        else:
            value = float('inf')  # Initialize value to positive infinity
            for move in moves:
                # Recursively evaluate the move
                value = min(value, self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    depth - 1, alpha, beta, True, next_player
                ))
                beta = min(beta, value)  # Update beta with the best value found
                if beta <= alpha:  # Prune if beta is less than or equal to alpha
                    break
            return value  # Return the best value for minimizing player

    def find_best_move(self):
        # Find the best move for the computer using the selected algorithm
        # Generate all possible moves for the computer
        moves = self.generate_moves(self.num_string, self.player_score, self.computer_score, "Computer")
        best_value = float('-inf')  # Initialize best value to negative infinity
        best_move = None  # Initialize best move as None

        # Evaluate each move using the selected algorithm
        for move in moves:
            if self.algorithm == "Minimax":
                value = self.minimax(
                    move['num_string'], move['player_score'], move['computer_score'],
                    self.max_depth - 1, False, "Human"
                )
            else:  # Use Alpha-Beta if selected
                value = self.alpha_beta(
                    move['num_string'], move['player_score'], move['computer_score'],
                    self.max_depth - 1, float('-inf'), float('inf'), False, "Human"
                )
            # Update best move if the current value is better
            if value > best_value:
                best_value = value
                best_move = move['move']

        return best_move  # Return the indices of the best move

    def start_game(self):
        # Initialize a new game with user-defined settings
        # Validate the input string length
        try:
            length = int(self.entry_length.get())
            if length < 15 or length > 25:
                messagebox.showerror("Error", "Length must be between 15 and 25!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        # Set up the game state
        self.string_length = length
        self.num_string = [random.randint(1, 9) for _ in range(self.string_length)]  # Generate random number string
        self.player_score = 0  # Reset human score
        self.computer_score = 0  # Reset computer score
        self.current_player = self.var_start.get()  # Set starting player based on user selection
        print(f"Game started, initial current_player set to: {self.current_player}")  # Log starting player
        self.algorithm = self.var_algorithm.get()  # Set AI algorithm based on user selection

        # Update GUI labels
        self.label_string.config(text=f"Number String: {self.num_string}")  # Display number string
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")  # Display scores
        self.label_instruction.config(text=f"{'Human' if self.current_player == 'Human' else 'Computer'}'s turn: Select two adjacent numbers:")  # Display turn instruction

        # Clear existing buttons
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        # Create new buttons for each number in the string
        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        # Enable/disable game control buttons
        self.new_game_button.config(state=tk.NORMAL)  # Enable new game button
        self.start_button.config(state=tk.DISABLED)  # Disable start button

        # If computer starts, schedule its move
        if self.current_player == "Computer":
            self.root.after(1000, self.computer_move)

    def select_number(self, index):
        # Handle human player's number selection
        print(f"Click detected at index {index}, current_player = {self.current_player}")  # Log click event

        # Ensure it's the human's turn
        if self.current_player != "Human":
            print("Not player's turn, ignoring click. Expected 'Human', got: {self.current_player}")  # Log turn error
            return

        # First selection: highlight the number
        if self.selected_index is None:
            self.selected_index = index
            self.number_buttons[index].config(bg="yellow")  # Highlight selected number
            print(f"First number selected at index {index}, num_string at that index: {self.num_string[index]}")  # Log first selection
        else:
            # Second selection: validate and process the move
            print(f"Second number selected at index {index}, first was {self.selected_index}, num_string: {self.num_string}")  # Log second selection
            # Check if the same number was selected twice
            if index == self.selected_index:
                print("Error: Cannot select the same number twice")  # Log error
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")  # Reset highlight
                self.selected_index = None  # Reset selection
                return
            # Check if the selected numbers are adjacent
            if abs(index - self.selected_index) != 1:
                print(f"Error: {index} and {self.selected_index} are not adjacent (difference = {abs(index - self.selected_index)})")  # Log error
                messagebox.showerror("Error", "Please select adjacent numbers!")  # Show error message
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")  # Reset highlight
                self.selected_index = None  # Reset selection
                return

            # Process the move
            print(f"Processing move with indices {self.selected_index} and {index}")  # Log move processing
            first_num = self.num_string[self.selected_index]  # Get first number
            second_num = self.num_string[index]  # Get second number
            sum_nums = first_num + second_num  # Calculate sum
            print(f"Numbers selected: {first_num} + {second_num} = {sum_nums}")  # Log numbers and sum

            # Apply game rules based on the sum
            if sum_nums > 7:
                replacement = 1  # Replace with 1 if sum > 7
                self.player_score += 1  # Increase human score
                print("Rule applied: Sum > 7, replacement = 1, player_score += 1")  # Log rule application
            elif sum_nums < 7:
                replacement = 3  # Replace with 3 if sum < 7
                self.computer_score -= 1  # Decrease computer score
                print("Rule applied: Sum < 7, replacement = 3, computer_score -= 1")  # Log rule application
            else:
                replacement = 2  # Replace with 2 if sum = 7
                self.player_score -= 1  # Decrease human score
                print("Rule applied: Sum = 7, replacement = 2, player_score -= 1")  # Log rule application

            # Update the number string
            min_idx = min(self.selected_index, index)  # Determine the lower index
            self.num_string.pop(min_idx)  # Remove first number
            self.num_string.pop(min_idx)  # Remove second number
            self.num_string.insert(min_idx, replacement)  # Insert replacement
            print(f"Updated num_string: {self.num_string}")  # Log updated string

            # Update GUI labels
            self.label_string.config(text=f"Number String: {self.num_string}")  # Display updated string
            self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")  # Display updated scores

            # Clear existing buttons
            for button in self.number_buttons:
                button.destroy()
            self.number_buttons.clear()
            print("Old buttons cleared and recreated")  # Log button recreation

            # Check if game is over
            if len(self.num_string) == 1:
                self.end_game()  # End the game if only one number remains
                return

            # Create new buttons for the updated string
            for i in range(len(self.num_string)):
                button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
                button.grid(row=0, column=i)
                self.number_buttons.append(button)

            # Switch turn to computer
            self.current_player = "Computer"
            print(f"Turn switched to {self.current_player} after move")  # Log turn switch
            self.label_instruction.config(text=f"{'Human' if self.current_player == 'Human' else 'Computer'}'s turn: Select two adjacent numbers:")  # Update instruction
            self.selected_index = None  # Reset selection
            self.root.after(1000, self.computer_move)  # Schedule computer's move

    def computer_move(self):
        # Handle the computer's turn
        print(f"Computer move starting, current state: {self.num_string}")  # Log computer move start
        # Check if game is over
        if len(self.num_string) <= 1:
            print("Game over, no computer move")  # Log game over
            return

        # Find the best move using the selected algorithm
        move = self.find_best_move()
        if move is None:
            print("No best move found, falling back to random")  # Log fallback to random move
            move_start = random.randint(0, len(self.num_string) - 2)  # Randomly select a starting index
            move_end = move_start + 1  # Select the adjacent index
        else:
            move_start, move_end = move  # Use the best move
            print(f"Best move found: indices {move_start}, {move_end}")  # Log best move

        # Process the move
        first_num = self.num_string[move_start]  # Get first number
        second_num = self.num_string[move_end]  # Get second number
        sum_nums = first_num + second_num  # Calculate sum
        print(f"Computer move: {first_num} + {second_num} = {sum_nums}")  # Log numbers and sum

        # Apply game rules based on the sum
        if sum_nums > 7:
            replacement = 1  # Replace with 1 if sum > 7
            self.computer_score += 1  # Increase computer score
            print("Rule applied: Sum > 7, replacement = 1, computer_score += 1")  # Log rule application
        elif sum_nums < 7:
            replacement = 3  # Replace with 3 if sum < 7
            self.player_score -= 1  # Decrease human score
            print("Rule applied: Sum < 7, replacement = 3, player_score -= 1")  # Log rule application
        else:
            replacement = 2  # Replace with 2 if sum = 7
            self.computer_score -= 1  # Decrease computer score
            print("Rule applied: Sum = 7, replacement = 2, computer_score -= 1")  # Log rule application

        # Update the number string
        min_idx = min(move_start, move_end)  # Determine the lower index
        self.num_string.pop(min_idx)  # Remove first number
        self.num_string.pop(min_idx)  # Remove second number
        self.num_string.insert(min_idx, replacement)  # Insert replacement
        print(f"Updated num_string: {self.num_string}")  # Log updated string

        # Update GUI labels
        self.label_string.config(text=f"Number String: {self.num_string}")  # Display updated string
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")  # Display updated scores

        # Clear existing buttons
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()
        print("Old buttons cleared and recreated")  # Log button recreation

        # Check if game is over
        if len(self.num_string) == 1:
            self.end_game()  # End the game if only one number remains
            return

        # Create new buttons for the updated string
        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        # Switch turn to human
        self.current_player = "Human"
        print(f"Turn switched to {self.current_player} after computer move")  # Log turn switch
        self.label_instruction.config(text=f"{'Human' if self.current_player == 'Human' else 'Computer'}'s turn: Select two adjacent numbers:")  # Update instruction

    def end_game(self):
        # End the game and display the result
        # Determine the winner based on scores
        winner = "Player" if self.player_score > self.computer_score else "Computer" if self.computer_score > self.player_score else "Tie"
        print(f"Game over, winner: {winner}, Scores - Player: {self.player_score}, Computer: {self.computer_score}")  # Log game result
        messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.player_score} | Computer: {self.computer_score}")  # Display result
        self.label_instruction.config(text="Select two adjacent numbers:")  # Reset instruction label
        self.new_game_button.config(state=tk.NORMAL)  # Enable new game button
        self.start_button.config(state=tk.NORMAL)  # Enable start button

if __name__ == "__main__":
    # Entry point of the program
    root = tk.Tk()  # Create the main tkinter window
    game = NumberGame(root)  # Instantiate the game
    root.mainloop()  # Start the GUI event loop