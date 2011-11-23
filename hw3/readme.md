### HOMEWORK #3 - WORD GAMES  
*Due Tuesday 11/22*

Our third (and final!) homework assignment is to be completed individually. Do not share code or review anyone else's code. Work on this homework assignment is to be your own.

Submit your homework [via RPI LMS](https://rpilms.rpi.edu/webct/logon/200146816001). Put all your code into exactly one Python file and name it your RCS userid. For example, if your RCS userid is `goldsd3`, then your Python file name for this assignment must be `goldsd3.py`.

*Be sure to comment your code and include your name at the top of each file submitted.*

**Valid Words:**  
First download the [ospd.txt](http://cs.strose.edu/goldschd/docs/ospd.txt) (Official Scrabble® Player's Dictionary) file. This will be your only source of valid words for this assignment.

**Word Find:**  
Write a Python function called `generateWordFindPuzzle()` that takes exactly four arguments (in this order): the dictionary of valid words (as a list); the number of words to hide in the puzzle; the number of rows in the puzzle; and the number of columns in the puzzle. This function generates a word-find puzzle (ALL UPPERCASE) and return the puzzle as a string (see below for the additional return value). Note that the string must contain newline characters (`'\n'`) at the end of each line (except for the last line). An example puzzle (with words PYTHON and PERL) is:

    QOFJEFUEJQ
    SWEOPYTHON
    WEJDEJWVJE
    WEFORWOEFF
    WJEELVNMZM
    PFEPEPDDAE

Randomly select words from the dictionary of valid words, then hide these words in the puzzle by placing them in random locations and in random directions. Words may appear in the horizontal, vertical, and diagonal directions and may be either forwards or backwards. Fill in all empty spaces with random letters.

In addition to returning the puzzle as a string, the `generateWordFindPuzzle()` function must return a tuple of the hidden words (which must be in sorted order). Therefore, this function has exactly two return values (a string and a tuple), as in:

    puzzle = 'QOFJEFUEJQ\nSWEOPYTHON\nWEJDEJWVJE\nWEFORWOEFF\nWJEELVNMZM\nPFEPEPDDAE'
    wordlist = ( 'PERL', 'PYTHON' )
    return puzzle, wordlist
	
Next, write a Python function called `findWords()` that takes exactly two arguments (in this order): the dictionary of valid words (as a list); and the puzzle (as a string). The function must return a tuple of all valid words found.

In general, if a puzzle generated using the `generateWordFindPuzzle()` function above with `N` hidden words is given as input to the `findWords()` function, a tuple of at least size `N` should be returned from `findWords()`. Be sure that this tuple is sorted and contains no duplicate words.

**Double Word Square:**  
A double word square is a grid of letters with the same number of rows and columns in which all words across and down are valid. For example, a valid 5x5 double word square is:

    SCENT
    CANOE
    ARSON
    ROUSE
    FLEET

Write a Python function called `generateDoubleWordSquare()` that takes exactly two arguments (in this order): the dictionary of valid words (as a list); and the size of the double word square (e.g. 5). Using random words from the list, this function must generate a valid double word square (ALL UPPERCASE) and return it as a string. Note that the string must contain newline characters (`'\n'`) at the end of each line (except for the last line).

Use whatever approach you like (e.g. recursion, brute force, genetic algorithm, etc.). To improve performance, consider paring down the given dictionary of valid words to sets of valid 2-letter words, 3-letter words, 4-letter words, etc.