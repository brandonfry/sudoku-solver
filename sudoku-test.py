# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 11:16:42 2017

@author: brandon
"""

import sudoku2
import copy
import unittest


def build_puzzle(numpuzzle):
    """Create and return a fully functional instance of Puzzle to
    be tested."""

    puzz = sudoku2.Puzzle()
    puzz.select_puzzle(numpuzzle)
    puzz.create_nodes()
    puzz.prev_state.append(copy.deepcopy(puzz.values))

    return puzz


def update_puzzle(puzz, guess, x, y):
    """Given a Puzzle, a guess and x, y-pair, update Puzzle with the guess
    at (x, y) and remove guess from that spot's possibilities, making the
    appropriate modifications to Puzzle.values and Puzzle.prev_state."""

    # remove guess from possibilities.
    puzz.values[x][y].remove_possibility(guess)
    # save, now that this possibility has been removed.
    # if puzzle is restored to this state, the possibility was
    # incorrect and will not be accessible.
    puzz.prev_state.append(copy.deepcopy(puzz.values))
    # set guess after state has been saved.
    puzz.values[x][y].set_value(guess)

    return puzz


class Guess(unittest.TestCase):

    def test_guess_has_blank_first(self):
        orig_puzzle = build_puzzle(1)
        guess, loc = orig_puzzle.guess_value()
        
        self.assertEqual(guess, '1')
        self.assertEqual(loc, (0, 0))
        
    def test_has_blank_second(self):
        orig_puzzle = build_puzzle(2)
        guess, loc = orig_puzzle.guess_value()
        
        self.assertEqual(guess, '1')
        self.assertEqual(loc, (0, 1))
        
    def test_wrong_guess(self):
        orig_puzzle = build_puzzle(2)
        orig_puzzle.eliminate_possibilities()
        new_puzzle = update_puzzle(orig_puzzle, '1', 0, 1)

        self.assertEqual(new_puzzle.values[0][1].get_possibilities(True), '4')        
        
        new_puzzle.eliminate_possibilities()
        
        self.assertEqual(new_puzzle.values[0][5].get_possibilities(), [])
        guess, loc = new_puzzle.guess_value()   
        
        self.assertEqual(guess, '4')
        self.assertEqual(loc, (0,1))
        
    def test_wrong_guess2(self):
        puzzle = build_puzzle(2)
        for i in range(2):
            puzzle.eliminate_possibilities()            
            guess, loc = puzzle.guess_value()
            puzzle = update_puzzle(puzzle, guess, *loc)
            puzzle.eliminate_possibilities()
        guess, loc = puzzle.guess_value()
        
        print(puzzle)        
        
        self.assertEqual(guess, '5')
        self.assertEqual(loc, (0, 2))


class Restore(unittest.TestCase):

    def test_restore_1(self):
        orig_puzzle = build_puzzle(1)
        new_puzzle = update_puzzle(orig_puzzle, '1', 0, 0)
        new_puzzle.restore()

        self.assertEqual(orig_puzzle.values, new_puzzle.values)
        self.assertEqual(orig_puzzle.prev_state,
                         new_puzzle.prev_state)
        self.assertEqual(orig_puzzle.values[0][0].get_possibilities(),
                         new_puzzle.values[0][0].get_possibilities())

    def test_restore_2(self):
        orig_puzzle = build_puzzle(1)
        new_puzzle = update_puzzle(orig_puzzle, '1', 0, 0)
        new_puzzle = update_puzzle(new_puzzle, '2', 0, 1)
        new_puzzle.restore()
        new_puzzle.restore()

        self.assertEqual(orig_puzzle.values, new_puzzle.values)
        self.assertEqual(orig_puzzle.prev_state,
                         new_puzzle.prev_state)
        self.assertEqual(orig_puzzle.values[0][0].get_possibilities(),
                         new_puzzle.values[0][0].get_possibilities())

if __name__ == '__main__':
    unittest.main()
    