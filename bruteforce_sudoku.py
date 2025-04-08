import time

def parse_sudoku(file_path):
    """
    Parse a Sudoku string into a 2D list.
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
    Print the Sudoku grid in a readable format.
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

def find_empty(lst):
    """
    Find an empty cell in the Sudoku grid.
    """
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == 0:
                return (i, j)  # row, column
    return None

def valid(lst, new_num, pos:tuple): #pos = (i,j)
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

def solve(lst):
    if find_empty(lst) == None:
        return True
    
    row, col = find_empty(lst)

    for i in range(1,10):
        if valid(lst, i, (row,col)):
            lst[row][col] = i

            if solve(lst):
                return lst

            lst[row][col] = 0
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