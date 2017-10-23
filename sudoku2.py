# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 08:00:10 2017

@author: brandon
"""

import pprint as pp
import re
import copy


class Node:
    """Node(x, y[, value= ' '])

    Instatiates a Node in a sudoku puzzle with a value and
    (x, y)-coordinates. Value defaults to a blank space should none be
    provided. x and y as integers, value as string."""

    def __init__(self, x, y, value=' '):
        self.value = value
        self.x = x
        self.y = y
        self.__set_possibilitites__()

    def remove_possibility(self, value):
        """Node.remove(value)

        Remvoe a single value from the Node with value as a string"""

        if value in self.possibilities:
            self.possibilities.remove(value)
        else:
            pass

    def get_pos(self):
        """Node.get_pos()

        Return (x, y) of Node."""

        return (self.x, self.y)

    def get_value(self):
        """Node.get_value()

        Return value of Node."""

        return self.value

    def set_value(self, value):
        """Node.set_value(value)

        Set value of Node."""

        self.value = value

    def get_possibilities(self, single=False):
        """Node.get_possibilities([single=False])

        Return either a list of possible values or an integer value if the
        list of possible values is a singleton. If called with True, only the
        first value is returned"""

        if len(self.possibilities) == 1 or single:
            try:
                return self.possibilities[0]
            except:  # if list is empty, return empty list
                return self.possibilities
        else:  # return all values
            return self.possibilities

    def nul_possibilities(self):
        """Node.nul_possibilities()

        Remove all possibilities from a Node."""

        self.possibilities = []

    def __set_possibilitites__(self):
        """Node.__set_possibilities__()

        Initialize possible values for Node."""

        if self.value == ' ':  # establish possible fill-in values
            self.possibilities = ['1', '2', '3', '4', '5',
                                  '6', '7', '8', '9']
        else:  # no values needed if Node is populated
            self.possibilities = []

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "{}".format(str(self.value))


class Puzzle:
    """Instatiates a sudoku Puzzle and solves it."""

    def __init__(self):
        self.values = []
        self.prev_state = []
        self.iterations = 0  # prevent excess calculations if guessing needed
        # establish starting corners of sub-grids
        self.squares = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3),
                        (3, 6), (6, 0), (6, 3), (6, 6)]
        self.read_from_file()  # grab collection of puzzles

    def generate_puzzle(self):
        """Generates a single Puzzle selected from a list of puzzles."""

        self.select_puzzle()
        self.create_nodes()
        self.prev_state.append(copy.deepcopy(self.values))

    def read_from_file(self):
        """Read from a list of puzzles in a text file with format:
            Grid ##
            003020600
            900305001
            001806400
            008102900
            700000008
            006708200
            002609500
            800203009
            005010300
            Grid ##
            ..."""

        with open('puzzles.txt', 'r') as f:
            puzzles = [item.strip().split(sep='\n') for item in
                       re.split(r'(Grid [0-9]+\n)', f.read())[2:-1:2]]
        f.close()
        self.puzzles = puzzles

    def select_puzzle(self, numpuzzle=0):
        """"Get puzzle number from user or test input"""

        if numpuzzle == 0:  # get value from user if not provided
            numpuzzle = int(input("Please enter puzzle number in range %i: "
                              % (len(self.puzzles) + 1)).strip())
        self.values = [list(row) for row in self.puzzles[numpuzzle - 1]]

    def create_nodes(self):
        """Instantiate all nodes in a puzzle and replace their plaintext
        values in self.values with their instances."""

        for i in range(9):
            for j in range(9):
                if self.values[i][j] == '0':
                    self.values[i][j] = Node(i, j)
                else:
                    self.values[i][j] = Node(i, j, self.values[i][j])
#        self.print_puzzle()

    def print_puzzle(self):
        print("Current puzzle state:")
        pp.pprint(self.values)

    def print_original_puzzle(self):
        print("Original puzzle state:")
        pp.pprint(self.prev_state[0])

    def do_checks(self):
        """Run through all check methods for a Puzzle."""

        for i in range(9):
            self.check_square(*self.squares[i])
            self.check_row(i)
            self.check_column(i)

    def check_square(self, m, n):
        """Eliminates node possibilities inside a single sub-grid of puzzle."""

        # create a list of nodes from 3x3 square, given top-left start point
        nodelist = []
        for i in range(m, (m)+3):
            for j in range(n, (n)+3):
                nodelist.append(self.values[i][j])

        # find values present in square and remove them from possibilities
        toremove = [node.get_value() for node in nodelist if node != ' ']
        for node in nodelist:
            if node.get_value() == ' ':
                for value in toremove:
                    node.remove_possibility(value)

    def check_row(self, m):
        """Eliminates node possibilities inside a single row of puzzle."""

        # create a list of nodes in the given row
        nodelist = []
        for j in range(9):
            nodelist.append(self.values[m][j])

        # find values present in row and remove them from possibilites
        toremove = [node.get_value() for node in nodelist if node != ' ']
        for node in nodelist:
            if node.get_value() == ' ':
                for value in toremove:
                    node.remove_possibility(value)

    def check_column(self, n):
        """Eliminates node possibilities inside a single column of puzzle."""

        # create a list of nodes in the given row
        nodelist = []
        for i in range(9):
            nodelist.append(self.values[i][n])

        # find values present in row and remove them from possibilites
        toremove = [node.get_value() for node in nodelist if node != ' ']
        for node in nodelist:
            if node.get_value() == ' ':
                for value in toremove:
                    node.remove_possibility(value)

    def has_empties(self):
        """Check if there are any empty values left in the puzzle."""

        for row in self.values:
            for node in row:
                if node.get_value() == ' ':
                    return True
        return False

    def is_valid_solution(self):
        """Check if a completed puzzle is permitted."""

        for i in range(9):
            row = self.values[i][:]
            row = [node.get_value() for node in row]
            col = self.values[:][i]
            col = [node.get_value() for node in col]
            grid = self.values[0][0:3] + self.values[1][0:3] + \
                self.values[2][0:3]
            grid = [node.get_value() for node in grid]

            # if not 9 unique values in each, not a solution
            if len(set(row)) == len(set(col)) == len(set(grid)) != 9:
                return False
        # if not false by now, all values unique
        return True

    def check_puzzle(self):
        """Check to see if puzzle is both complete and correct."""

        if self.has_empties() is False:
            if self.is_valid_solution() is True:
                return True
        return False

    def eliminate_possibilities(self):
        """Recursive solver for straightforward sudoku puzzles, i.e. those
        which do not require a guess-and-check approach but can be solved
        through simple elimination."""

        self.do_checks()

        repeat = False
        # if one possibility remains, assign it to Node.value
        # then redo checks to eliminate other possibilities
        for row in self.values:
            for node in row:
                if len(node.get_possibilities()) == 1:
                    repeat = True
                    node.set_value(node.get_possibilities(True))
                    node.remove_possibility(node.get_value())
                    self.do_checks()

        # recurse if a value was just eliminated
        if repeat is True:
            self.eliminate_possibilities()

    def restore(self):
        """Restore Puzzle.prev_state and Puzzle.values to the state before the
        last incorrect guess."""

        # copy up to the last choice.
        self.prev_state = copy.deepcopy(self.prev_state[:-1])
        # values set to before last guess was implimented,
        # but after the guess was removed from the Node's
        # possibilities.
        self.values = copy.deepcopy(self.prev_state[-1])

    def guess_value(self):
        """Return a possible guess for the first blank Node and the Node's
        location. If the first blank node does not have any possibilities,
        then the puzzle cannot be solved based on an error in a previous guess.
        In this case the previous state of the puzzle is restored and a new
        guess is returned, different from the previous and incorrect guess."""

        # find the first blank Node.
        for i in range(9):
                for j in range(9):
                    node = self.values[i][j]
                    if node.get_value() == ' ':
                        # does this blank Node have any possibilities?
                        if node.get_possibilities():
                            guess = node.get_possibilities(True)
                            loc = node.get_pos()
                            return guess, loc
                        else:  # if not, go back a guess and try differently.
                            self.restore()
                            # restart method and see if a possibility
                            # can be found.
                            return self.guess_value()
        # there are no unsolved Nodes. shouldn't be used?
        print("what the hell?")
        return None, (None, None)

    def while_solve(self):
        self.eliminate_possibilities()

        while self.check_puzzle() is False:
            self.iterations += 1
            # make guess.
            guess, (i, j) = self.guess_value()
            # remove guess from possibilities.
            self.values[i][j].remove_possibility(guess)
            # save, now that this possibility has been removed.
            # if puzzle is restored to this state, the possibility was
            # incorrect and will not be accessible.
            self.prev_state.append(copy.deepcopy(self.values))
            # set guess after state has been saved.
            self.values[i][j].set_value(guess)
            # try for simple elimination.
            self.eliminate_possibilities()
            self.print_puzzle()
            # if it's not solved by now...
            if self.iterations == 500:
                break

    def solve(self):
        """Puzzle.solve()

        Solves a sudoku puzzle (provided by user in plaintext format) by
        simple elimination and guessing."""

        self.while_solve()
        self.print_original_puzzle()
        self.print_puzzle()

if __name__ == '__main__':
    puzz = Puzzle()
    puzz.generate_puzzle()
    puzz.solve()