"""
Program:        wordgames.py
Author:         Bill Jameson (jamesw2@rpi.edu)
Description:    Provides functions to:
                    - generate word find puzzles
                    - solve word find puzzles
                    - generate double word squares
"""
import random

# HELPER FUNCTIONS
def readDict(file = 'ospd.txt'):
    """Read in and return a list containing the full list of words in the Scrabble dictionary."""
    return [line.strip() for line in open(file)]

def getRowCol(grid, pos):
    """Convert a position to a row and column in the grid"""
    rows = len(grid)
    cols = len(grid[0])
    row = pos // cols
    col = pos % cols
    return row, col

def getValidOrientations(word, grid, pos):
    """Get a list of valid orientations for the word in the grid at position pos.
       There are 8 possible word orientations, represented numerically:
        - 0 is horizontal left-to-right
        - 1 is diagonal to the right and down
        - 2 is vertical downward
        - 3-7 continue clockwise"""
    orientations = []
    rows = len(grid)
    cols = len(grid[0])
    row, col = getRowCol(grid, pos)
    
    # add orientations based on whether the word will fit, and whether the spaces it would occupy are already blank or contain letters in the word
    if (len(word) <= (cols-col) and
        ''.join([word[i] for i in range(len(word)) if (grid[row][col+i] == '-' or grid[row][col+i] == word[i])]) == word):
        orientations += [0]
    if (len(word) <= (cols-col) and len(word) <= (rows - row) and
        ''.join([word[i] for i in range(len(word)) if (grid[row+i][col+i] == '-' or grid[row+i][col+i] == word[i])]) == word):
        orientations += [1]
    if (len(word) <= (rows-row) and
        ''.join([word[i] for i in range(len(word)) if (grid[row+i][col] == '-' or grid[row+i][col] == word[i])]) == word):
        orientations += [2]
    if (len(word) <= col+1 and len(word) <= (rows-row) and
        ''.join([word[i] for i in range(len(word)) if (grid[row+i][col-i] == '-' or grid[row+i][col-i] == word[i])]) == word):
        orientations += [3]
    if (len(word) <= col+1 and
        ''.join([word[i] for i in range(len(word)) if (grid[row][col-i] == '-' or grid[row][col-i] == word[i])]) == word):
        orientations += [4]
    if (len(word) <= col+1 and len(word) <= row+1 and
        ''.join([word[i] for i in range(len(word)) if (grid[row-i][col-i] == '-' or grid[row-i][col-i] == word[i])]) == word):
        orientations += [5]
    if (len(word) <= row+1 and
        ''.join([word[i] for i in range(len(word)) if (grid[row-i][col] == '-' or grid[row-i][col] == word[i])]) == word):
        orientations += [6]
    if (len(word) <= (cols-col) and len(word) <= row+1 and
        ''.join([word[i] for i in range(len(word)) if (grid[row-i][col+i] == '-' or grid[row-i][col+i] == word[i])]) == word):
        orientations += [7]
    
    return orientations
    
def findValidPosition(word, grid):
    """Find a valid position and orientation for the word and the grid.
       Return None if the word will not fit."""
    rows = len(grid)
    cols = len(grid[0])
    startPos = random.randint(0, rows*cols)
    positions = [i for i in range(startPos, rows*cols)] + [i for i in range(startPos)]
    
    # if the first, random choice fails, check all the positions to see if any are valid
    for pos in positions:
        orientations = getValidOrientations(word, grid, pos)
        if len(orientations) > 0:
            return pos, random.choice(orientations)
        
    return None, None
    
def placeWord(grid, w, pos, orientation):
    """Place word w in the grid at the specified position with the specified orientation."""
    row, col = getRowCol(grid, pos)
    
    if orientation == 0:
        for i in range(len(w)):
            grid[row][col+i] = w[i]
    if orientation == 1:
        for i in range(len(w)):
            grid[row+i][col+i] = w[i]
    if orientation == 2:
        for i in range(len(w)):
            grid[row+i][col] = w[i]
    if orientation == 3:
        for i in range(len(w)):
            grid[row+i][col-i] = w[i]
    if orientation == 4:
        for i in range(len(w)):
            grid[row][col-i] = w[i]
    if orientation == 5:
        for i in range(len(w)):
            grid[row-i][col-i] = w[i]
    if orientation == 6:
        for i in range(len(w)):
            grid[row-i][col] = w[i]
    if orientation == 7:
        for i in range(len(w)):
            grid[row-i][col+i] = w[i]
            
def checkWord(grid, word):
    """Check to see if the word is present in the grid, at any position or orientation."""
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows*cols):
        if len(getValidOrientations(word, grid, i)) > 0:
            # don't need to iterate through all orientations, since it also checks letter-by-letter
            #   in addition to blanks
            return True
    return False
    
# HOMEWORK FUNCTION DEFINITIONS
def generateWordFindPuzzle(dic, n, rows, cols):
    """Generate a word find puzzle with the specified number of rows and columns, picking
        n random words from dic.
       Assumes that certain edge cases will not occur (e.g., user asks for more words to be placed than possible)."""
    alpha = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    blank = '-'
    grid = [[blank for i in range(cols)] for j in range(rows)]
    # eliminate words that won't fit in the grid
    validwords = [word for word in dic if (len(word) <= rows or len(word) <= cols)]
    wordsplaced = []
    
    for i in range(n):
        # randomly choose a word not used yet, position, and orientation
        w = ''
        while True:
            w = random.choice(validwords).upper()
            if w in wordsplaced:
                continue
            pos, orientation = findValidPosition(w, grid)
            if pos is None:
                continue
            else:
                break
                
        placeWord(grid, w, pos, orientation)
        wordsplaced += [w]
        
    # replace all blanks in the grid with random letters
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '-':
                grid[r][c] = random.choice(alpha)
    
    return '\n'.join([''.join(grid[i]) for i in range(rows)]), tuple(sorted(wordsplaced))
    
def findWords(dic, puzzle):
    """Use dictionary dic to find words in the puzzle"""
    grid = [[x for x in row] for row in puzzle.split()]
    rows = len(grid)
    cols = len(grid[0])
    validwords = [word for word in dic if (len(word) <= rows or len(word) <= cols)]
    wordsfound = []

    for w in validwords:
        if checkWord(grid, w.upper()):
            wordsfound += [w.upper()]

    return tuple(sorted(set(wordsfound)))
