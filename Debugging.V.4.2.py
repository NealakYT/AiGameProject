import tkinter as tk  # Import tkinter for creating the GUI
from tkinter import messagebox  # Import messagebox for showing pop-up messages
import random  # Import random for generating random numbers and AI moves

class NumberGame:
    def __init__(self, root):
        # Initialize the game with a tkinter window (root)
        self.root = root
        self.root.title("Number Game with Simple AI")  # Set the window title

        # Game variables
        self.string_length = 0  # Length of the number string (set by user, 15-25)
        self.num_string = []  # List to store the current sequence of numbers
        self.player_score = 0  # Human player's score
        self.computer_score = 0  # Computer's score
        self.current_player = "Player"  # Tracks whose turn it is ("Player" or "Computer")

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
        self.radio_human = tk.Radiobutton(root, text="Human", variable=self.var_start, value="Player")
        self.radio_computer = tk.Radiobutton(root, text="Computer", variable=self.var_start, value="Computer")
        self.radio_human.pack()
        self.radio_computer.pack()

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

    def start_game(self):
        # Start a new game by initializing the game state and GUI
        # Validate the user input for string length
        try:
            length = int(self.entry_length.get())
            if length < 15 or length > 25:
                messagebox.showerror("Error", "Length must be between 15 and 25!")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
            return

        # Set up the game state
        self.string_length = length  # Store the length
        self.num_string = [random.randint(1, 9) for _ in range(self.string_length)]  # Generate random numbers (1-9)
        self.player_score = 0  # Reset player score
        self.computer_score = 0  # Reset computer score
        self.current_player = self.var_start.get()  # Set starting player (Human or Computer)

        # Update GUI labels with initial state
        self.label_string.config(text=f"Number String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

        # Clear any existing buttons from previous games
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        # Create new buttons for each number in the string
        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)  # Arrange buttons in a horizontal line
            self.number_buttons.append(button)

        # Enable/disable buttons for game flow
        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.DISABLED)

        # If the computer starts, trigger its move after a 1-second delay
        if self.current_player == "Computer":
            self.root.after(1000, self.computer_move)

    def select_number(self, index):
        # Handle the human player's selection of numbers
        # Ignore clicks if it's not the player's turn
        if self.current_player != "Player":
            return

        # First number selection: highlight the button
        if not hasattr(self, 'selected_index'):
            self.selected_index = index
            self.number_buttons[index].config(bg="yellow")  # Highlight the selected number
        else:
            # Second number selection: check if it's adjacent to the first
            if abs(index - self.selected_index) != 1:
                messagebox.showerror("Error", "Please select adjacent numbers!")
                self.number_buttons[self.selected_index].config(bg="SystemButtonFace")  # Reset highlight
                del self.selected_index
                return

            # Process the move: get the two numbers and their sum
            first_num = self.num_string[self.selected_index]
            second_num = self.num_string[index]
            sum_nums = first_num + second_num

            # Apply game rules based on the sum
            if sum_nums > 7:
                replacement = 1
                self.player_score += 1  # Player gains a point
            elif sum_nums < 7:
                replacement = 3
                self.computer_score -= 1  # Computer loses a point
            else:  # sum_nums == 7
                replacement = 2
                self.player_score -= 1  # Player loses a point

            # Update the number string: remove the pair and insert the replacement
            min_idx = min(self.selected_index, index)
            self.num_string.pop(min_idx)
            self.num_string.pop(min_idx)
            self.num_string.insert(min_idx, replacement)

            # Update GUI with new string and scores
            self.label_string.config(text=f"Number String: {self.num_string}")
            self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

            # Clear old buttons
            for button in self.number_buttons:
                button.destroy()
            self.number_buttons.clear()

            # Check if the game is over (only one number left)
            if len(self.num_string) == 1:
                self.end_game()
                return

            # Recreate buttons for the updated string
            for i in range(len(self.num_string)):
                button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
                button.grid(row=0, column=i)
                self.number_buttons.append(button)

            # Switch to computer's turn
            self.current_player = "Computer"
            self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")
            del self.selected_index
            self.root.after(1000, self.computer_move)  # Trigger computer move after delay

    def computer_move(self):
        # Handle the computer's turn with a simple AI (random move)
        # Exit if the game is over
        if len(self.num_string) <= 1:
            return

        # Randomly select two adjacent numbers
        move_start = random.randint(0, len(self.num_string) - 2)  # Ensure there's a next number
        move_end = move_start + 1

        # Process the move: get the two numbers and their sum
        first_num = self.num_string[move_start]
        second_num = self.num_string[move_end]
        sum_nums = first_num + second_num

        # Apply game rules based on the sum
        if sum_nums > 7:
            replacement = 1
            self.computer_score += 1  # Computer gains a point
        elif sum_nums < 7:
            replacement = 3
            self.player_score -= 1  # Player loses a point
        else:  # sum_nums == 7
            replacement = 2
            self.computer_score -= 1  # Computer loses a point

        # Update the number string
        min_idx = min(move_start, move_end)
        self.num_string.pop(min_idx)
        self.num_string.pop(min_idx)
        self.num_string.insert(min_idx, replacement)

        # Update GUI with new string and scores
        self.label_string.config(text=f" loteNumber String: {self.num_string}")
        self.label_scores.config(text=f"Player: {self.player_score} | Computer: {self.computer_score}")

        # Clear old buttons
        for button in self.number_buttons:
            button.destroy()
        self.number_buttons.clear()

        # Check if the game is over
        if len(self.num_string) == 1:
            self.end_game()
            return

        # Recreate buttons for the updated string
        for i in range(len(self.num_string)):
            button = tk.Button(self.buttons_frame, text=str(self.num_string[i]), command=lambda idx=i: self.select_number(idx))
            button.grid(row=0, column=i)
            self.number_buttons.append(button)

        # Switch to player's turn
        self.current_player = "Player"
        self.label_instruction.config(text=f"{self.current_player}'s turn: Select two adjacent numbers:")

    def end_game(self):
        # End the game and display the result
        # Determine the winner based on scores
        winner = "Player" if self.player_score > self.computer_score else "Computer" if self.computer_score > self.player_score else "Tie"
        messagebox.showinfo("Game Over", f"Game Over! {winner} wins!\nPlayer: {self.player_score} | Computer: {self.computer_score}")
        self.label_instruction.config(text="Select two adjacent numbers:")
        self.new_game_button.config(state=tk.NORMAL)
        self.start_button.config(state=tk.NORMAL)

# Main execution: Create the tkinter window and start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGame(root)
    root.mainloop()