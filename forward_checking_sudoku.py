## Uses both forward checking in parallel to the MRV Heuristic to solve Sudoku
## Minimum Remaining Value heuristic reduces search space by choosing the cell with the fewest legal values
## Forward checking put simply checks ahead for conflicts in neighbouring cells 

##RESULT = 97.2% time reduction from MRV_sudoku.py

import time
from copy import deepcopy

def parse_sudoku(file_path):
    """
    Parse a Sudoku string into a 2D list
    """
    with open(file_path, 'r') as thisFile:
        sudoku_lst = []
        for line in thisFile:
            line = line.strip()
            row = []
            for char in line:
                if char != " ":
                    row.append(int(char))
            sudoku_lst.append(row)
    return sudoku_lst

def print_sudoku(lst):
    """
    Print the Sudoku grid in a readable format
    """
    for i in range(len(lst)):
        if i % 3 == 0 and i != 0:
            print("-" * 21)

        for j in range(len(lst[i])):
            if j % 3 == 0 and j != 0:
                print("|", end="")

            if j == 8:
                print(lst[i][j])
            else:
                print(str(lst[i][j]) + " ", end="")

def eval_legal(lst, row, col):
    """
    Return a list of all legal values for a single cell
    """
    legal_lst = []
    for z in range(1,10):
        if valid(lst,z,(row,col)) == True:
            legal_lst.append(z)
    return legal_lst


def scan_empty(lst):
    """
    Find all empty cell in the Sudoku grid and its respective list containing all possible legal values for that cell
    """
    cell_map = {}
    for i in range(0,9):
        for j in range(0,9):
            if lst[i][j] == 0:
                cell_map[(i,j)] = eval_legal(lst, i, j)
    return cell_map


def valid(lst, new_num, pos:tuple): #pos = (i,j)
    """
    Return whether or not the filling of a specific cell with a particular number is valid
    """
    for i in range(len(lst[pos[0]])):
        if new_num == lst[pos[0]][i] and pos[1] != i:
            return False
    for j in range(len(lst[pos[0]])):
        if new_num == lst[j][pos[1]] and pos[0] != j:
            return False
    this_row = pos[0] // 3
    this_col = pos[1] // 3
    for i in range(this_row*3,this_row*3+3):
        for j in range(this_col*3,this_col*3+3):
            if new_num == lst[i][j] and pos != (i,j):
                return False
    return True

def smallest_legal_count(thisdict):
    """
    Returns the cell with the fewest legal candidates, determined by the length of its candidate list
    """
    return min(thisdict, key=lambda cell: len(thisdict[cell]))

def affected(lst, row,col):
    """
    Returns a list of all the empty cells affected by the temporary filling of a particular cell
    """
    new_lst = []
    for i in range(0,9):
        if lst[row][i] == 0 and i != col:
            new_lst.append((row,i))
    for j in range(0,9):
        if lst[j][col] == 0 and j != row:
            new_lst.append((j,col))
    this_row = row // 3
    this_col = col // 3
    for x in range(this_row*3,this_row*3+3):
        for y in range(this_col*3,this_col*3+3):
            if lst[x][y] == 0 and (x,y) != (row,col):
                new_lst.append((x,y))
    return new_lst

def solve(lst, initial=True, domains={}):
    
    if initial:
        domains = scan_empty(lst)
        initial = False

    if domains == {}:
        return True


    row, col = smallest_legal_count(domains)
    candidates = domains[(row, col)]

    for candidate in candidates:
        local_changes = {} #record which candidate gets removed from which neighbour
        lst[row][col] = candidate
        del domains[(row, col)]
        valid_assignment = True

        for neighbour in affected(lst, row, col):
            if neighbour in domains and candidate in domains[neighbour]:
                # Record this change
                if neighbour not in local_changes:
                    local_changes[neighbour] = []
                local_changes[neighbour].append(candidate)
                domains[neighbour].remove(candidate)

                #Assignment is invalid if neighbour runs out of candidates
                if domains[neighbour] == {}:
                    valid_assignment = False
                    break

        if not valid_assignment:
            # Undo changes if the assignment is invalid.
            lst[row][col] = 0
            for neighbour, removed in local_changes.items():
                if neighbour in domains:
                    domains[neighbour].extend(removed)
            domains[(row, col)] = eval_legal(lst, row, col)
            continue  

        if solve(lst, initial=False, domains=domains):
            return lst

        lst[row][col] = 0
        for neighbour, removed in local_changes.items():
            if neighbour in domains:
                domains[neighbour].extend(removed)
        domains[(row, col)] = eval_legal(lst, row, col)

    return False

def solution_verifier(lst):
    # Check all rows
    for row in lst:
        if sorted(row) != list(range(1, 10)):
            return False

    # Check all columns
    for col in range(9):
        col_values = [lst[row][col] for row in range(9)]
        if sorted(col_values) != list(range(1, 10)):
            return False

    # Check all 3x3 subgrids
    for start_row in range(0, 9, 3):
        for start_col in range(0, 9, 3):
            block = []
            for i in range(3):
                for j in range(3):
                    block.append(lst[start_row + i][start_col + j])
            if sorted(block) != list(range(1, 10)):
                return False

    return True
##MAIN

print_sudoku(parse_sudoku("sudoku.txt"))
print("\n")
start = time.time()
print_sudoku(solve(parse_sudoku("sudoku.txt")))
end = time.time()
print("Time taken to solve the Sudoku: ", end - start)

solution = solve(parse_sudoku("sudoku.txt"))
if solution_verifier(solution):
    print("The solved Sudoku is valid!")
else:
    print("The solved Sudoku is invalid!")