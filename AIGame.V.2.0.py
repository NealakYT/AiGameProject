import tkinter as tk
from tkinter import messagebox
import random
import time

class GameState:
    def __init__(self, num_string, player_score, opponent_score, current_player):
        self.num_string = num_string[:]  # Copy of the number string
        self.player_score = player_score
        self.opponent_score = opponent_score
        self.current_player = current_player
        self.children = []  # Possible next states
        self.parent = None
        self.move = None  # (index1, index2) of the move
        self.value = 0  # For Minimax/Alpha-Beta evaluation

# Heuristic function: higher score difference favors the computer
def evaluate_state(state, is_maximizing_player):
    score_diff = state.opponent_score - state.player_score if is_maximizing_player else state.player_score - state.opponent_score
    # Penalize longer strings (encourages reducing the string)
    length_penalty = len(state.num_string) * 0.1
    return score_diff - length_penalty

class NumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Game with AI")

        # Game variables
        self.string_length = 0
        self.current_state = None
        self.player_score = 0
        self.opponent_score = 0
        self.current_player = "Player"
        self.selected_index = None
        self.algorithm = "Minimax"  # Default algorithm
        self.start_player = "Human"  # Default starting player
        self.experiments = {"Minimax": {"wins_computer": 0, "wins_human": 0, "nodes": [], "times": []},
                           "AlphaBeta": {"wins_computer": 0, "wins_human": 0, "nodes": [], "times": []}}
        self.experiment_count = 0
        self.max_depth = 3  # N-ply look-ahead depth

        # GUI elements
        self.label_length = tk.Label(root, text="Enter string length (15-25):")
        self.label_length.pack()

        self.entry_length = tk.Entry(root)
        self.entry_length.pack()

        # Start options
        self.label_start = tk.Label(root, text="Who starts? (Human/Computer)")
        self.label_start.pack()
        self.var_start = tk.StringVar(value="Human")
        self.radio_human = tk.Radiobutton(root, text="Human", variable=self.var_start, value="Human")
        self.radio_computer = tk.Radiobutton(root, text="Computer", variable=self.var_start, value="Computer")
        self.radio_human.pack()
        self.radio_computer.pack()

        # Algorithm options
        self.label_algo = tk.Label(root, text="Choose algorithm: (Minimax/AlphaBeta)")
        self.label_algo.pack()
        self.var_algo = tk.StringVar(value="Minimax")
        self.radio_minimax = tk.Radiobutton(root, text="Minimax", variable=self.var_algo, value="Minimax")
        self.radio_alphabeta = tk.Radiobutton(root, text="AlphaBeta", variable=self.var_algo, value="AlphaBeta")
        self.radio_minimax.pack()
        self.radio_alphabeta.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.new_game_button = tk.Button(root, text="New Game", command=self.start_game, state=tk.DISABLED)
        self.new_game_button.pack()

        self.label_string = tk.Label(root, text="Number String: ")
        self.label_string.pack()

        self.label_scores = tk.Label(root, text="Player: 0 | Opponent: 0")
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

            if sum_nums > 7:
                replacement = 1
                new_player_score = state.player_score + (1 if state.current_player == "Player" else 0)
                new_opponent_score = state.opponent_score + (1 if state.current_player == "Opponent" else 0)
            elif sum_nums < 7:
                replacement = 3
                new_player_score = state.player_score - (1 if state.current_player == "Opponent" else 0)
                new_opponent_score = state.opponent_score - (1 if state.current_player == "Player" else 0)
            else:
                replacement = 2
                new_player_score = state.player_score - (1 if state.current_player == "Player" else 0)
                new_opponent_score = state.opponent_score - (1 if state.current_player == "Opponent" else 0)

            new_num_string.pop(i)
            new_num_string.pop(i)
            new_num_string.insert(i, replacement)
            new_state = GameState(
                num_string=new_num_string,
                player_score=new_player_score,
                opponent_score=new_opponent_score,
                current_player="Opponent" if state.current_player == "Player" else "Player"
            )
            new_state.parent = state
            new_state.move = (i, i + 1)
            state.children.append(new_state)
            self.generate_game_tree(new_state, depth + 1, max_depth)

    def minimax(self, state, depth, is_maximizing):
        if depth == 0 or len(state.num_string) <= 1:
            return evaluate_state(state, is_maximizing)

        if is_maximizing:
            max_eval = float('-inf')
            for child in state.children:
                eval_value = self.minimax(child, depth - 1, False)
                max_eval = max(max_eval, eval_value)
            return max_eval
        else:
            min_eval = float('inf')
            for child in state.children:
                eval_value = self.minimax(child, depth - 1, True)
                min_eval = min(min_eval, eval_value)
            return min_eval

    def alpha_beta(self, state, depth, alpha, beta, is_maximizing):
        if depth == 0 or len(state.num_string) <= 1:
            return evaluate_state(state, is_maximizing)

        if is_maximizing:
            value = float('-inf')
            for child in state.children:
                value = max(value, self.alpha_beta(child, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cutoff
            return value
        else:
            value = float('inf')
            for child in state.children:
                value = min(value, self.alpha_beta(child, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return value

    def find_best_move(self, state):
        start_time = time.time()
        nodes_visited = 0
        best_value = float('-inf') if state.current_player == "Opponent" else float('inf')
        best_move = None

        for child in state.children:
            nodes_visited += 1
            if self.algorithm == "Minimax":
                value = self.minimax(child, self.max_depth - 1, state.current_player == "Opponent")
            else:  # Alpha-Beta
                value = self.alpha_beta(child, self.max_depth - 1, float('-inf'), float('inf'), state.current_player == "Opponent")
            is_better = value > best_value if state.current_player == "Opponent" else value < best_value
            if is_better:
                best_value = value
                best_move = child.move

        end_time = time.time()
        return best_move, nodes_visited, end_time - start_time

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
        self.num_string = [random.randint(1, 9) for _ in range(self.string_length)]
        self.player_score = 0
        self.opponent_score = 0
        self.current_player = self.var_start.get()
        self.algorithm = self.var_algo.get()
        self.current_state = GameState(self.num_string, self.player_score, self.opponent_score, self.current_player)
        self.generate_game_tree(self.current_state, 0, self.max_depth)
        self.experiment_count += 1

        self.label_string.config(text=f"Number String: {self.current_state.num_string}")
        self.label_scores.config(text=f"Player: {self.current_state.player_score} | Opponent: {self.current_state.opponent_score}")
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")
        self.update_buttons()
        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        if self.current_player == "Computer":
            self.computer_move()

    def update_buttons(self):
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
            self.label_scores.config(text=f"Player: {self.current_state.player_score} | Opponent: {self.current_state.opponent_score}")
            self.update_buttons()

            if len(self.current_state.num_string) == 1:
                winner = "Computer" if self.current_state.opponent_score > self.current_state.player_score else "Player" if self.current_state.player_score > self.current_state.opponent_score else "Tie"
                self.experiments[self.algorithm]["wins_computer" if winner == "Computer" else "wins_human"] += 1
                messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.current_state.player_score} | Opponent: {self.current_state.opponent_score}")
                self.log_experiment_results()
                return

            self.current_player = "Opponent" if self.current_player == "Player" else "Player"
            self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")
            del self.selected_index

            if self.current_player == "Computer":
                self.computer_move()

    def computer_move(self):
        if len(self.current_state.num_string) > 1:
            move, nodes, time_taken = self.find_best_move(self.current_state)
            self.experiments[self.algorithm]["nodes"].append(nodes)
            self.experiments[self.algorithm]["times"].append(time_taken)

            for child in self.current_state.children:
                if child.move == move:
                    self.current_state = child
                    break

            self.label_string.config(text=f"Number String: {self.current_state.num_string}")
            self.label_scores.config(text=f"Player: {self.current_state.player_score} | Opponent: {self.current_state.opponent_score}")
            self.update_buttons()

            if len(self.current_state.num_string) == 1:
                winner = "Computer" if self.current_state.opponent_score > self.current_state.player_score else "Player" if self.current_state.player_score > self.current_state.opponent_score else "Tie"
                self.experiments[self.algorithm]["wins_computer" if winner == "Computer" else "wins_human"] += 1
                messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.current_state.player_score} | Opponent: {self.current_state.opponent_score}")
                self.log_experiment_results()
                return

            self.current_player = "Player"
            self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

    def log_experiment_results(self):
        if self.experiment_count < 10:
            return
        algo_data = self.experiments[self.algorithm]
        avg_nodes = sum(algo_data["nodes"]) / len(algo_data["nodes"]) if algo_data["nodes"] else 0
        avg_time = sum(algo_data["times"]) / len(algo_data["times"]) if algo_data["times"] else 0
        messagebox.showinfo("Experiment Results", f"{self.algorithm} Results (10 games):\n"
                                                  f"Computer Wins: {algo_data['wins_computer']}\n"
                                                  f"Human Wins: {algo_data['wins_human']}\n"
                                                  f"Avg Nodes Visited: {avg_nodes}\n"
                                                  f"Avg Time per Move: {avg_time:.4f}s")
        self.experiments[self.algorithm] = {"wins_computer": 0, "wins_human": 0, "nodes": [], "times": []}
        self.experiment_count = 0

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()