import math
import random


def group(values, n):
    answer = []
    helper = []
    counter = 0
    for i in range(0,n):
        if counter >= len(values):
            break
        for j in range(0,n):
            if counter >= len(values):
                break
            helper.append(values[counter])
            counter = counter + 1
        answer.append(helper)
        helper = []
    return answer


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    
    grid = group(digits, 9)
    return grid


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return(values[pos[0]])


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    i = pos[1]
    answer = []  
    for j in range(0,len(values)):
        answer.append(values[j][i])
    return answer


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos """
    
    blockRowStart = 3 * (pos[0] // 3)
    blockColumnStart = 3 * (pos[1] // 3)
    answer = []
    for i in range(3):
        for j in range(3):
             answer.append(values[blockRowStart + i][blockColumnStart + j])
    return answer

def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        
    


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i in range(len(grid)):
        if (grid[i].count(".") != 0):
            return (i, grid[i].index("."))
    return ()


def find_possible_values(grid, pos):
    numb = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    for i in range(1, 10):
        if str(i) in row:
            numb.remove(i)
            continue
        if str(i) in col:
            numb.remove(i)
            continue
        for k in range(3):
            if str(i) in block[k]:
                numb.remove(i)
    return numb


flag = False


def solve(grid):
    gr = find_empty_positions(grid)
    if gr == ():
        return grid
    else:
        ss = find_possible_values(grid, gr)
        if ss == []:
            return None
        for i in ss:
            grid[gr[0]][gr[1]] = str(i)
            s = solve(grid)
            if s is not None:
                return grid
    grid[gr[0]][gr[1]] = "."


def check_solution(grid):
    got = False
    for i in range(9):
        for j in range(9):
            row = get_row(grid, [i,j])
            col = get_col(grid, [i,j])
            block = get_block(grid, [i,j])
            row = sorted(row)
            col = sorted(col)
            block = sorted(block)
            for jj in range(9):
                if (row[jj] == col[jj]) and (col[jj] == block[jj]):
                    pass
                else:
                    
                    
                    return [i, j], got
    got = True
    return got


def generate_sudoku(grid,n):
    cou = 0
    check = []
    
    while cou < n:
        ss1 = random.randrange(0,9)
        ss2 = random.randrange(0,9)
        if [ss1,ss2] not in check:
            
            check.append([ss1, ss2])
            
            row = get_row(grid, [ss1,ss2])
            col = get_col(grid, [ss1,ss2])
            block = get_block(grid, [ss1,ss2])
  
            for i in range(9):
                if ((str(i+1) not in row) and (str(i+1) not in col) and (str(i+1) not in block)):
                    grid[ss1][ss2] = str(i+1)
                    cou += 1 
                    break       
    return grid



if __name__ == '__main__':
    for fname in ['gen.txt']:
        grid = read_sudoku(fname)
        grid = generate_sudoku(grid,50)
        
    for fname in ['puzzle3.txt']:

        
        grid = read_sudoku(fname)
        display(grid)
        print("_______")

        solution = solve(grid)
        display(solution)
               