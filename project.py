import requests
import re
import sys
import random
import csv
from datetime import datetime
import ast


def main():

    # introduction to the game
    print('>>   \033[1;36mSUDOKU GAME\033[0m')
    print('>> \033[36mWelcome to the SUDOKU GAME. The rules are simple: choose your difficulty' \
          '\n   level and start guessing. Stuck on a number? Just type "hint" and the program will' \
          '\n   automatically fill an empty spot for you. Need a break? Type "exit" to save your' \
          '\n   progress and restart exactly from where you left off. Enjoy!!!'\
          '\n \033[0m')

    # choose new or saved sudoku
    while True:
        firstchoice = input('>> \033[1mStart new sudoku or open saved one\033[0m \033[3m("new", "saved")\033[0m? ').strip().lower()
        if re.search(r'^new$', firstchoice):
            # input level of difficulty and generate sudoku
            while True:
                try:
                    level = input('>> \033[1mChoose your level\033[0m \033[3m("easy", "medium", "hard")\033[0m: ')
                    if level not in ['easy', 'medium', 'hard']:
                        raise ValueError
                    data = generate_sudoku(level.lower().strip())
                    empty_sudoku = data['puzzle']
                    solution_sudoku = data['solution']
                    difficulty = data['difficulty']
                    break
                except (UnboundLocalError, ValueError):
                    print('\033[93mInput valid level\033[0m')
            break
        elif re.search(r'^saved$', firstchoice):
            # recover saved sudoku
            if show_saves():
                while True:
                    try:
                        id_choice = input('>> \033[1mChoose an ID:\033[0m ')
                            
                        with open('savings.csv', 'r') as file:
                            reader = csv.DictReader(file)
                            rows = list(reader)

                            selected_row = None
                            for row in rows:
                                if row['id'] == id_choice:
                                    selected_row = row
                                    break

                            if selected_row is None:
                                raise ValueError

                            empty_sudoku = ast.literal_eval(selected_row['sudoku'])
                            solution_sudoku = ast.literal_eval(selected_row['solution'])
                            difficulty = selected_row['difficulty']
                            break
                    except (ValueError, IndexError, TypeError):
                        print('\033[93mInput valid ID\033[0m')
                break
            else:
                print('\033[93mYou must start a new game\033[0m')
        else:
            print('\033[93mInput valid choice\033[0m')

    # store sudoku, solution and moves needed        
    zeros = count_moves(empty_sudoku)
    print_sudoku(empty_sudoku)

    # start guessing and completing
    new_sudoku = empty_sudoku
    moves = zeros
    while moves > 0:
        while True:
            try:
                print(f'\033[36m{moves} guesses left\033[0m')
                guess_input = get_input('>> \033[1mAdd your guess\033[0m \033[3m(row,column) - guess\033[0m: ')

                # ask for hint
                if re.search(r'^hint$', guess_input):
                    row_hint, col_hint = hint_generator(new_sudoku)
                    new_sudoku[row_hint][col_hint] = solution_sudoku[row_hint][col_hint]
                    print_sudoku(new_sudoku)
                    print(f'\033[93m({row_hint+1},{col_hint+1}) was {solution_sudoku[row_hint][col_hint]}\033[0m')
                    moves -= 1

                    if moves == 0:
                        print('>> \033[1;36mSUDOKU COMPLETED!!!\033[0m')
                        sys.exit()
                    continue

                # save your progress and exit
                if guess_input == 'exit_and_save':
                    save_progress(difficulty, new_sudoku, solution_sudoku)
                    sys.exit()


                row, column, guess = add_number(guess_input)
                break
            except (ValueError, UnboundLocalError):
                print('\033[93mInput valid coordinates and guess\033[0m')

            
        # check your guess and spot
        if new_sudoku[row-1][column-1] == '0':
            if solution_sudoku[row-1][column-1] == f'{guess}':
                moves -= 1
                if moves != 0:
                    new_sudoku[row-1][column-1] = f'{guess}'
                    print_sudoku(new_sudoku)
                    print('\033[32mCorrect!!\033[0m')
                elif moves == 0:
                    new_sudoku[row-1][column-1] = f'{guess}'
                    print_sudoku(new_sudoku)
                    print('>> \033[1;36mSUDOKU COMPLETED!!!\033[0m')
                    break
            else:
                print('\033[31mWrong guess\033[0m')
        else:
            print('\033[93mInput a valid spot\033[0m')
    

# FUNCTIONS

def generate_sudoku(level: str):
    APIkey = 'zcQCtl7pn0hCrttKBipxg_uYCyGMkF0pUhov1Vq-d2Y'

    body = {
        'difficulty': level, # 'easy', 'medium', or 'hard' (defaults to 'easy')
        'solution': True, # True or False (defaults to True)
        'array': True # True or False (defaults to False)
    }

    headers = {
        'Content-Type': 'application/json',
        'x-api-key': APIkey
    }

    try:
        response = requests.post('https://www.youdosudoku.com/api/', json = body, headers = headers)

        if response.status_code == 200:
            return response.json()
        else:
            sys.exit(f'\033[93mAPI Error: Impossibile to generate Sudoku (Status {response.status_code}). Try again later.\033[0m')

    except requests.RequestException:
        sys.exit(f'\033[93mConnection Error: Impossibile to generate Sudoku. Check your network or try again later.\033[0m')


def add_number(guess):
    match = re.search(r'^\D*(\d)\D*(\d)\D*(\d)\D*$', guess)
    if match:
        row = int(match.group(1))
        column = int(match.group(2))
        number = int(match.group(3))

        if not (1 <= row <= 9 and 1 <= column <= 9 and 1 <= number <= 9):
            raise ValueError

        return row, column, number
    else:
        raise ValueError

def print_sudoku(grid):
    print()
    for row in range(9):

        if row == 0:
            print('\033[36m    1 2 3   4 5 6   7 8 9\033[0m')
            print('  ┌───────┬───────┬───────┐')
    
        elif row % 3 == 0 and row != 0:
            print('  ├───────┼───────┼───────┤')
            
        full_row = ''

        for col in range(9):

            num = str(grid[row][col])
            if num != '0':
                num_f = f'{num}'
            else:
                num_f = ' '

            if col == 0:
                full_row += f'\033[36m{row+1}\033[0m | '
            elif col % 3 == 0 and col != 0:
                full_row += '| '
            elif col == 8:
                full_row += num_f + ' ' + '|'
                continue
                
            
            full_row += num_f + ' '
            
        print(full_row)
    print('  └───────┴───────┴───────┘')

def hint_generator(current_sudoku):
    empty_spots = []
    for row in range(9):
        for col in range(9):
            if current_sudoku[row][col] == '0':
                empty_spots.append((row, col))
    row_hint, col_hint = random.choice(empty_spots)
    return row_hint, col_hint

def get_input(text):
    while True:
        answer = input(text).lower().strip()

        if re.search(r'^exit$', answer):
            
            while True:
                exit_choice = input('>> \033[1mDo you want to EXIT?\033[0m \033[3m(yes/no)\033[0m ').lower().strip()
                if exit_choice in ['y', 'yes', 'n', 'no']:
                    break 
                else:
                    print('\033[93mInvalid input. Please type "yes/y" or "no/n".\033[0m')

            if exit_choice in ['y', 'yes']:
                
                while True:
                    saving = input('>> \033[1mDo you want to save your progress?\033[0m \033[3m(yes/no)\033[0m ').lower().strip()
                    if saving in ['y', 'yes']:
                        return 'exit_and_save'
                    elif saving in ['n', 'no']:
                        sys.exit()
                    else:
                        print('\033[93mInvalid input. Please type "yes/y" or "no/n".\033[0m')

            else:
                continue

        return answer

def save_progress(difficulty, current_sudoku, solution_sudoku):
    needs_header = False
    try:
        with open('savings.csv', 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            if reader.fieldnames is None:
                needs_header = True

            if len(rows) == 0:
                id = 1
            elif len(rows) > 0:
                id = int(rows[-1]['id']) + 1
    except FileNotFoundError:
        id = 1
        needs_header = True
        
    with open('savings.csv', 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'date', 'difficulty','sudoku', 'solution'])
        if needs_header:
            writer.writeheader()

        date = datetime.now().strftime('%m/%d/%Y, %H:%M:%S')
        writer.writerow({
            'id': id,
            'date': date,
            'difficulty': difficulty,
            'sudoku': current_sudoku,
            'solution': solution_sudoku
        })
    print(f'\033[32mSudoku saved successfully! ID: \033[1m{id}\033[0m\033[32m, Date: \033[1m{date}\033[0m')

def show_saves():
    try:
        with open('savings.csv', 'r') as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            if len(rows) == 0:
                print('\033[93mNo saved games available\033[0m')
                return False

            print('\033[1;36m┌────────────────────────────────────────┐\033[0m')
            print('\033[1;36m│               SAVED GAMES              │\033[0m')
            print('\033[1;36m├────────────────────────────────────────┤\033[0m')
            for row in rows:
                if row['difficulty'] == 'medium':
                    print(f'\033[1;36m│ ID: {row["id"]}\033[0m  \033[36m| {row["date"]} | {row["difficulty"]} │\033[0m')
                else:
                    print(f'\033[1;36m│ ID: {row["id"]}\033[0m  \033[36m| {row["date"]} |  {row["difficulty"]}  │\033[0m')
            print('\033[1;36m└────────────────────────────────────────┘\033[0m\n')
            return True
    except FileNotFoundError:
        print('\033[93mNo saved games available\033[0m')
        return False

def count_moves(sudoku):
    return sum(row.count('0') for row in sudoku)


if __name__ == "__main__":
    main()
