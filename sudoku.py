"""This module contains a fitness function for sudoku puzzles.

It is specialized for 9x9 puzzles, but could be extended to 4x4, 16x16, 25x25,
etc, by making DIM a parameter and fixing one_box and boxes.

To use this module, you want to call either sudoku_fitness or ga_sudoku.

An example puzzle and solution is provided in PUZZLE and SOLUTION.
"""

#The dimension of the puzzle.
DIM = 9

#A sudoku puzzle, that I found somewhere. I guess it is of average difficulty.
PUZZLE = [[0, 0, 4, 8, 0, 0, 0, 1, 9],
          [6, 7, 0, 9, 0, 0, 0, 0, 0],
          [5, 0, 8, 0, 3, 0, 0, 0, 4],
          [3, 0, 0, 7, 4, 0, 1, 0, 0],
          [0, 6, 9, 0, 0, 0, 7, 8, 0],
          [0, 0, 1, 0, 6, 9, 0, 0, 5],
          [1, 0, 0, 0, 8, 0, 3, 0, 6],
          [0, 0, 0, 0, 0, 6, 0, 9, 1],
          [2, 4, 0, 0, 0, 1, 5, 0, 0]]


#The correct solution.
SOLUTION = [[9, 3, 4, 8, 2, 5, 6, 1, 9],
            [6, 7, 2, 9, 1, 4, 8, 5, 3],
            [5, 1, 8, 6, 3, 7, 9, 2, 4],
            [3, 2, 5, 7, 4, 8, 1, 6, 9],
            [4, 6, 9, 1, 5, 3, 7, 8, 2],
            [7, 8, 1, 2, 6, 9, 4, 3, 5],
            [1, 9, 7, 5, 8, 2, 3, 4, 6],
            [8, 5, 3, 4, 7, 6, 2, 9, 1],
            [2, 4, 6, 3, 9, 1, 5, 7, 8]]

def set_puzzle(puzzle):
	PUZZLE = list(puzzle)

def set_solution(sol):
	SOLUTION = list(sol)

def one_box(solution, i):
    """Extract the 9 elements of a 3 x 3 box in a 9 x 9 sudoku solution.

    @param solution: The sudoku solution as a flat vector with 81 elements.

    @param i: The upper left corner

    @return: A vector with 9 elements, representing a sudoku box.
    """
    return solution[i:i+3] + solution[i+9:i+12] + solution[i+18:i+21]

def boxes(solution):
    """Divide a flat vector into vectors with 9 elements, representing 3 x 3
    boxes in the corresponding 9 x 9 2D vector. These are the standard
    sudoku boxes.

    @param solution: A flat vector, containing a sudoku solution.

    @return: A vector of vectors with 9 elements, representing sudoku boxes.
    """
    return [one_box(solution, i) for i in [0, 3, 6, 27, 30, 33, 54, 57, 60]]

def splitup(solution):
    """Take a flat vector and make it 2D

    @param solution: A flat vector with DIM * DIM elements

    @return: A 2D vector with DIM rows with DIM elements each.
    """
    return [solution[i * DIM:(i + 1) * DIM] for i in xrange(DIM)]

def consistent(solution):
    """Check how many different elements there are in each row.

    Ideally there should be DIM different elements, if there are no duplicates.

    @param solution: A 9 x 9 2D vector with a puzzle

    @return: The sum of duplicates in each row
    """
    return sum(DIM - len(set(row)) for row in solution)

def compare(xs1, xs2):
    """Compare two flat vectors and return how much they differ

    @param xs1: The puzzle as a flat vector. Zeroes are not compared.

    @param xs2: The solution as a flat vector.

    @return: The number of elements that differ and where xs1 is not 0.
    """
    return sum(1 if x1 and x1 != x2 else 0 for x1, x2 in zip(xs1, xs2))

def sudoku_fitness(flatsolution, puzzle, flatpuzzle=None):
    """Evaluate the fitness of flatsolution.

    @param flatsolution: A flat vector with 81 integer elements between 1 and 9.

    @param puzzle: A 9 x 9 2D vector with a sudoku puzzle. Zero means unknown.
    
    @param flatpuzzle: A 1D flattened version of puzzle. If it is not supplied
    it is calculated from puzzle. If you want to run this fitness function
    millions of times, it might be a good idea to precalculate this.

    @return: A fitness value. Higher is worse and 0 is perfect.
    """
    if not flatpuzzle:
        flatpuzzle = sum(puzzle, [])
    solution = splitup(flatsolution)
    fitness = consistent(solution)
    fitness += consistent(zip(*solution))
    fitness += consistent(boxes(flatsolution))
    fitness += compare(flatpuzzle, flatsolution) * 10
    return fitness

def ga_sudoku(puzzle):
    """Return a fitness function wrapper that extracts the .genes attribute from
    an individual and sends it to sudoku_fitness.

    @param puzzle: A 9 x 9 2D vector with a sudoku puzzle. Zero means unknown.

    @return: A fitness function that takes a linear genome class and returns a
    fitness value, where higher is worse and 0 is perfect.
    """
    flatpuzzle = sum(puzzle, [])
    def fit(guy):
        """A GA wrapper for sudoku_fitness"""
        return sudoku_fitness(guy.genes, puzzle, flatpuzzle)

    return fit
