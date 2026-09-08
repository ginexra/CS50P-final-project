# SUDOKU GAME
### Video Demo:  <https://youtu.be/jQOMqzUUXYk>

## Description:
My project is an interactive Sudoku game. The grid is generated using the [https://www.youdosudoku.com](https://www.youdosudoku.com) API, which also provides the correct solution for the code to compare with the user's guesses. The website offers three levels of difficulty. The code allows the user to save the game once it has been generated and displayed or to exit without saving any progress.

At the beginning of the program, the user is prompted to choose between starting a new Sudoku or recovering a saved one. If saved games are present, the program displays the available ones and the user can input the associated ID. Each saved game is stored together with the date and time of saving and the corresponding difficulty. Once the user has made a choice, the game begins.

The user is asked to input guesses to fill all empty spots. At each move, the program displays the number of guesses left. If the selected spot is already full, the input is invalid or the inserted number is wrong, the program indicates the problem and asks again for a guess without decreasing the number of remaining spots. If instead, the user gives a correct answer, the Sudoku grid is updated, displayed again and the game continues.

If the user is stuck, they can ask for a hint and the program will automatically fill a random spot. During the game, the user can decide to quit at any time by typing `exit` with the possibility to save the game for later. The game is saved in the `savings.csv` file together with the date, time, difficulty and the related solution.

## Project Structure:
- `project.py`: Main script containing the core logic of the game.
- `test_project.py`: File containing unit tests for three functions of project.py, designed to be executed via _pytest_.
- `requirements.txt`: A list of pip-installable external libraries required to run the project.
- `savings.csv`: File for storing saved games. It's automatically created the first time the user saves their progress. Should not be opened nor modified.

### Libraries used:
- **External:** `requests`, `pytest`
- **Standard:** `re`, `sys`, `random`, `csv`, `datetime`, `ast`

### Functions developed:
- `main()`: Main function where the body of the program is developed.
- `generate_sudoku(level)`: Takes the difficulty _level_ (str) chosen by the user and fetches data from the API. It returns a dictionary containing the puzzle, solution and difficulty.
- `add_number(guess)`: Function to process the user guess. It returns a tuple of three numbers indicating row, column and guess. It expects three numbers in the input _guess_ (str), which must start and end with a number. In order to detect the correct input RegEx is used together with try/except blocks.
- `print_sudoku(grid)`: Takes as input a list of lists (the sudoku grid) and prints it to the terminal with proper formatting. It does not return anything.
- `hint_generator(current_sudoku)`: Function activated when the user asks for a hint. It takes as input the current sudoku grid, find a random empty spot and returns the corresponding row and column coordinates.
- `get_input(text)`: Alternative function to _input()_. It continually monitors for the _"exit"_ command and manages the save prompt during the game. It simply returns the text given by the user if no _"exit"_ command is typed.
- `save_progress(difficulty, current_sudoku, solution_sudoku)`: Function called when the user decides to save their progress. It creates or appends to the _.csv_ file, writing the current sudoku grid, solution and difficulty level. It does not return anything.
- `show_saves()`: Called when the user chooses to resume a saved game. It reads the _.csv_ file and displays a formatted table of all available saves. If the file is empty, it notifies the user that no saved games exist. It returns _True_ or _False_ depending on the existence of at least one saved game.
- `count_moves(sudoku)`: Function that calculates and returns the total number of empty spots (zeros) remaining in the puzzle.

### Considerations and possible improvements:
The program features robust error handling. Anytime the user is asked to input anything, if the answer is not what the code expects, the program prompts again for a valid answer without crashing or throwing any Python errors. This is achieved utilizing _while True_ loops and try/except blocks where needed.   
When developing this challenging project, I identified several potential improvements, but I chose to keep the core structure simple. However, the code could be improved by avoiding saving a game under a new ID, when it's already loaded from the _savings.csv_ file and instead overwriting the previous save.  
Another improvement would be to automatically delete a saved Sudoku once it has been completed by the user.  
The project was developed with the user in mind, trying to reproduce a typical Sudoku game with all its features, while keeping the code structure simple and understandable. Building this game proved to be a highly enjoyable and rewarding experience as it is to play.