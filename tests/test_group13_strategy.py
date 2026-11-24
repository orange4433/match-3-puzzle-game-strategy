"""Check the recovered agent's score-difference and board-preserving policies."""
from pathlib import Path
import copy
import sys
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
import board
import group13_agent as agent
from exception_manager import Player_safe


def advance(position, action):
    """Score an exchange using the independent course game engine."""
    result = copy.deepcopy(position)
    result.change(*action)
    total = 0
    while True:
        points, removed = result.eliminate()
        total += points
        if not removed.any() or (result.mainboard == 'nan').any():
            return result, total


class StrategyTests(unittest.TestCase):
    def setUp(self):
        self.position = board.Board(seed=42)
        current, self.moves = self.position.get_info()
        self.current = current
        self.model = agent.MyBoard(current, np.array(list(agent.COLORS)),
                                   valid_movements=self.moves)

    def test_two_ply_matches_course_engine_score_difference(self):
        values = []
        for move in self.moves:
            successor, ours = advance(self.position, move)
            replies = successor.get_info()[1]
            self.assertTrue(replies, "Fixture must have an opponent reply.")
            opponent = max(advance(successor, reply)[1] for reply in replies)
            values.append((ours - opponent, move))
        expected_value = max(value for value, _ in values)
        move, value = agent.greedy_2(self.model, self.moves)
        self.assertEqual(value, expected_value)
        self.assertIn((value, move), values)

    def test_unfavorable_search_can_leave_board_unchanged(self):
        with patch.object(agent, 'alpha_beta_pruning', return_value=(-10, self.moves[0])):
            move = agent.select(self.model, 0, True, [], 1, [0, 0], [0], [0], False, False)
        Player_safe.check_for_invalid_move(None, move)
        before = self.model.board.copy()
        self.model.change(*move)
        np.testing.assert_array_equal(self.model.board, before)

    def test_sparse_position_override_accepts_search_move(self):
        with patch.object(agent, 'alpha_beta_pruning', return_value=(-10, self.moves[0])):
            move = agent.select(self.model, 0, True, [], 1, [0, 0], [0], [0], False, True)
        self.assertEqual(move, self.moves[0])

    def test_three_ply_adds_ours_subtracts_reply_adds_ours(self):
        class Node:
            def __init__(self, score=0, move=None, children=()):
                self.score, self.movement, self.children = score, move, list(children)

            def get_children(self, depth, cache):
                return self.children

        # Immediate score 7 loses to the continuation 4 - 1 + 5 = 8.
        a = ((0, 0), (0, 1))
        b = ((1, 0), (1, 1))
        root = Node(children=[Node(7, a, [Node(8, children=[Node(1)])]),
                              Node(4, b, [Node(1, children=[Node(5)])])])
        value, move = agent.alpha_beta_pruning(root, 3, float('-inf'),
                                               float('inf'), True, 0, True, {}, [0, 0])
        self.assertEqual((value, move), (8, b))


if __name__ == '__main__':
    unittest.main()
