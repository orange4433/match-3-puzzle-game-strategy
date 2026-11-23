import numpy as np
import random
import copy
from time import time
from math import sqrt, log

BOARD_SIZE = 6
N_ROWS = 1200
COLORS = {'R': '0', 'B': '1', 'G': '2', 'Y': '3', 'P': '4'}
action_space = [((i, j), (i, j + 1)) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE - 1)] + \
               [((i + 1, j), (i, j)) for i in range(BOARD_SIZE - 1) for j in range(BOARD_SIZE)]


class MyBoard:
    def __init__(self, board, colors, scores, player, steps, action_space):
        self.size = board.shape[0]
        self.board = board.copy()
        self.colors = colors
        self.scores = np.array(scores, dtype=np.float64)
        self.player = player
        self.steps = steps
        self.is_finished = False

    @staticmethod
    def check(arr):
        repeats = set()
        for i in range(0, BOARD_SIZE - 2):
            for j in range(BOARD_SIZE):
                if arr[i, j] != 'nan' and (arr[i + 1:i + 3, j]
                                           == arr[i, j]).all():
                    repeats.add((i + 1, j))
                if arr[j, i] != 'nan' and (arr[j, i + 1:i + 3]
                                           == arr[j, i]).all():
                    repeats.add((j, i + 1))
        return repeats

    def eliminate(self, func=lambda x: (x - 2)**2):
        arr = self.board
        to_eliminate = np.zeros((self.size, self.size), dtype=int)
        directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        to_visit = self.check(arr)
        score = 0

        for coord in to_visit:
            if to_eliminate[coord[0], coord[1]] == 1:
                continue
            head = 0
            connected = [
                coord,
            ]
            while head < len(connected):
                current = connected[head]
                to_eliminate[current[0], current[1]] = 1
                for d in directions:
                    neighbor = current + d
                    if (neighbor < 0).any() or (neighbor >= self.size).any():
                        continue
                    if (arr[neighbor[0], neighbor[1]] == arr[current[0],
                                                             current[1]]
                            and to_eliminate[neighbor[0], neighbor[1]] == 0):
                        connected.append(neighbor)
                head += 1
            score += func(len(connected))

        col_eliminated = np.sum(to_eliminate, axis=1)
        col_remained = self.size - col_eliminated
        for i in range(self.size):
            if col_eliminated[i] == 0:
                continue
            col = self.board[i]
            self.board[i, :col_remained[i]] = col[:self.size][to_eliminate[i]
                                                              == 0]
            self.board[i, col_remained[i]:N_ROWS -
                       col_eliminated[i]] = col[self.size:]
            self.board[i, N_ROWS - col_eliminated[i]:] = np.nan

        # Return the total score and the number of columns eliminated
        return score, col_eliminated

    def check_can_eliminate(self, loc):
        i, j = loc
        flag = False
        if i + 2 < BOARD_SIZE and (self.board[i, j] == self.board[i + 1:i + 3,
                                                                  j]).all():
            flag = True
            return flag
        if i - 2 >= 0 and (self.board[i, j] == self.board[i - 2:i, j]).all():
            flag = True
            return flag
        if i - 1 >= 0 and i + 1 < BOARD_SIZE and (self.board[i - 1, j]
                                                  == self.board[i:i + 2,
                                                                j]).all():
            flag = True
            return flag
        if j + 2 < BOARD_SIZE and (self.board[i, j]
                                   == self.board[i, j + 1:j + 3]).all():
            flag = True
            return flag
        if j - 2 >= 0 and (self.board[i, j] == self.board[i, j - 2:j]).all():
            flag = True
            return flag
        if j - 1 >= 0 and j + 1 < BOARD_SIZE and (
                self.board[i, j - 1] == self.board[i, j:j + 2]).all():
            flag = True
            return flag
        return False

    def eliminate_from_move(self, loc1, loc2, func=lambda x: (x - 2)**2):
        arr = self.board
        to_eliminate = np.zeros((self.size, self.size), dtype=int)
        directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        to_visit = []
        if self.check_can_eliminate(loc1) == True:
            to_visit.append(loc1)
        if self.check_can_eliminate(loc2) == True:
            to_visit.append(loc2)
        score = 0

        for coord in to_visit:
            if to_eliminate[coord[0], coord[1]] == 1:
                continue
            head = 0
            connected = [
                coord,
            ]
            while head < len(connected):
                current = connected[head]
                to_eliminate[current[0], current[1]] = 1
                for d in directions:
                    neighbor = current + d
                    if (neighbor < 0).any() or (neighbor >= self.size).any():
                        continue
                    if (arr[neighbor[0], neighbor[1]] == arr[current[0],
                                                             current[1]]
                            and to_eliminate[neighbor[0], neighbor[1]] == 0):
                        connected.append(neighbor)
                head += 1
            score += func(len(connected))

        col_eliminated = np.sum(to_eliminate, axis=1)
        col_remained = self.size - col_eliminated
        for i in range(self.size):
            if col_eliminated[i] == 0:
                continue
            col = self.board[i]
            self.board[i, :col_remained[i]] = col[:self.size][to_eliminate[i]
                                                              == 0]
            self.board[i, col_remained[i]:N_ROWS -
                       col_eliminated[i]] = col[self.size:]
            self.board[i, N_ROWS - col_eliminated[i]:] = np.nan

        # Return the total score and the number of columns eliminated
        return score, col_eliminated

    def check_can_erase(self):
        flag = False
        arr = self.board
        arrt = self.board.T
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arr[i, j] == arr[i + 2:i + 4,
                                                            j]).all():
                    flag = True
                    break
                if i >= 2 and (arr[i + 1, j] == arr[i - 2:i, j]).all():
                    flag = True
                    break
                if j >= 2 and ((arr[i, j] == arr[i + 1, j - 2:j]).all() |
                               (arr[i + 1, j] == arr[i, j - 2:j]).all()):
                    flag = True
                    break
                if j <= self.size - 3 and (
                    (arr[i, j] == arr[i + 1, j + 1:j + 3]).all() |
                    (arr[i + 1, j] == arr[i, j + 1:j + 3]).all()):
                    flag = True
                    break
                if j >= 1 and j <= self.size - 2 and (
                    (arr[i, j] == arr[i + 1, [j - 1, j + 1]]).all() |
                    (arr[i + 1, j] == arr[i, [j - 1, j + 1]]).all()):
                    flag = True
                    break
            if (flag == True):
                break
        if (flag == True):
            return flag
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arrt[i, j] == arrt[i + 2:i + 4,
                                                              j]).all():
                    flag = True
                    break
                if i >= 2 and (arrt[i + 1, j] == arrt[i - 2:i, j]).all():
                    flag = True
                    break
                if j >= 2 and ((arrt[i, j] == arrt[i + 1, j - 2:j]).all() |
                               (arrt[i + 1, j] == arrt[i, j - 2:j]).all()):
                    flag = True
                    break
                if j <= self.size - 3 and (
                    (arrt[i, j] == arrt[i + 1, j + 1:j + 3]).all() |
                    (arrt[i + 1, j] == arrt[i, j + 1:j + 3]).all()):
                    flag = True
                    break
                if j >= 1 and j <= self.size - 2 and (
                    (arrt[i, j] == arrt[i + 1, [j - 1, j + 1]]).all() |
                    (arrt[i + 1, j] == arrt[i, [j - 1, j + 1]]).all()):
                    flag = True
                    break
            if (flag == True):
                return flag
        return flag

    def get_action_space(self):
        operations = []
        arr = self.board
        arrt = arr.T
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arr[i, j] == arr[i + 2:i + 4,
                                                            j]).all():
                    operations.append(((i, j), (i + 1, j)))
                    continue
                if i >= 2 and (arr[i + 1, j] == arr[i - 2:i, j]).all():
                    operations.append(((i, j), (i + 1, j)))
                    continue
                if j >= 2 and ((arr[i, j] == arr[i + 1, j - 2:j]).all() |
                               (arr[i + 1, j] == arr[i, j - 2:j]).all()):
                    operations.append(((i, j), (i + 1, j)))
                    continue
                if j <= self.size - 3 and (
                    (arr[i, j] == arr[i + 1, j + 1:j + 3]).all() |
                    (arr[i + 1, j] == arr[i, j + 1:j + 3]).all()):
                    operations.append(((i, j), (i + 1, j)))
                    continue
                if j >= 1 and j <= self.size - 2 and (
                    (arr[i, j] == arr[i + 1, [j - 1, j + 1]]).all() |
                    (arr[i + 1, j] == arr[i, [j - 1, j + 1]]).all()):
                    operations.append(((i, j), (i + 1, j)))
                    continue
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arrt[i, j] == arrt[i + 2:i + 4,
                                                              j]).all():
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if i >= 2 and (arrt[i + 1, j] == arrt[i - 2:i, j]).all():
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j >= 2 and ((arrt[i, j] == arrt[i + 1, j - 2:j]).all() |
                               (arrt[i + 1, j] == arrt[i, j - 2:j]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j <= self.size - 3 and (
                    (arrt[i, j] == arrt[i + 1, j + 1:j + 3]).all() |
                    (arrt[i + 1, j] == arrt[i, j + 1:j + 3]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j >= 1 and j <= self.size - 2 and (
                    (arrt[i, j] == arrt[i + 1, [j - 1, j + 1]]).all() |
                    (arrt[i + 1, j] == arrt[i, [j - 1, j + 1]]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
        return operations

    def move(self, loc1, loc2):
        x1, y1 = loc1
        x2, y2 = loc2
        temp1 = self.board[x1, y1].copy()
        temp2 = self.board[x2, y2].copy()
        self.board[x1, y1], self.board[x2, y2] = temp2, temp1
        total_score, columns_eliminated = self.eliminate_from_move(loc1, loc2)
        while columns_eliminated.sum() and not (
                self.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
            score, columns_eliminated = self.eliminate()
            total_score += score
        if (self.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
            self.is_finished = True
        if (self.steps >= 200):
            self.is_finished = True
        if (self.check_can_erase() == False):
            self.is_finished = True
        self.scores[self.player] += total_score
        self.steps += 1
        self.player = 1 - self.player

    def simulate_move(self, loc1, loc2):
        new_board = copy.deepcopy(self)
        new_board.move(loc1, loc2)
        return new_board

    def greedy_simulate(self):
        if (self.is_finished == True):
            if (self.scores[0] > self.scores[1]):
                self.scores[0] += 600
            else:
                self.scores[1] += 600
        return copy.deepcopy(self.scores)


class SearchTreeNode:
    def __init__(self, index, act):
        self.child_num1 = 0
        self.child_num2 = 0
        self.children = list()
        self.father = None
        self.index = index
        self.from_act = act

    def add_child(self, child, type):
        if type == 1:
            self.child_num1 += 1
        else:
            self.child_num2 += 1
        self.children.append(child)
        child.father = self

    def child(self, index):
        return self.children[index]

    def __eq__(self, other):
        return self.index == other.index

    def __hash__(self):
        return self.index


class SearchTree:
    def __init__(self):
        self.root = SearchTreeNode(0, 0)
        self.unique_identifier = 1
        self.n_nodes = 1
        self.node_of = {0: self.root}

    def create_node(self, act) -> SearchTreeNode:
        new_node = SearchTreeNode(self.unique_identifier, act)
        self.node_of[self.unique_identifier] = new_node
        self.unique_identifier += 1
        return new_node

    def add_as_child(self, type, parent: SearchTreeNode,
                     child: SearchTreeNode) -> None:
        parent.add_child(child, type)
        self.n_nodes += 1


class MonteCarloTreeSearch:
    def __init__(self,
                 root_state: MyBoard,
                 begin_time,
                 operations1,
                 operations2,
                 iterations=5000,
                 exploration=0.6):
        self.exploration = exploration
        self.search_tree = SearchTree()
        self.root_state = copy.deepcopy(root_state)
        self.visit_count_of = {0: 0}
        self.visit_values = {0: np.zeros(2, dtype=np.float64)}
        self.index_to_state = {0: root_state}
        self.action_space1 = {0: operations1}
        self.action_space2 = {0: operations2}
        self.len1 = {0: len(operations1)}
        self.len2 = {0: len(operations2)}
        self.iterations = iterations
        self.begin_time = begin_time
        self.debug_log = ""
        self.debug_count = 0
        self.max_depth = 0

    def calc(self, a, b, c):
        return a / b + self.exploration * sqrt(log(c) / b)

    def create_new_node(self, state, now_node, move, type):
        new_state = state.simulate_move(move[0], move[1])
        child = self.search_tree.create_node(move)
        self.search_tree.add_as_child(type, now_node, child)
        self.visit_count_of[child.index] = 1
        self.index_to_state[child.index] = new_state
        this_values = new_state.greedy_simulate()
        # print(child.index, this_values)
        self.visit_values[child.index] = this_values
        return this_values

    def sample_path(self, index, depth):
        self.max_depth = max(self.max_depth, depth)
        self.visit_count_of[index] += 1
        state = self.index_to_state[index]
        now_node = self.search_tree.node_of[index]
        player = state.player
        this_values = np.array((0, 0), dtype=np.float64)
        dice = random.random()
        if index not in self.len1:
            self.action_space1[index] = state.get_action_space()
            self.action_space2[index] = []
            self.debug_count += 1
            for op in action_space:
                if op not in self.action_space1[index]:
                    self.action_space2[index].append(op)
            self.len1[index] = len(self.action_space1[index])
            self.len2[index] = len(self.action_space2[index])
        if (dice <= 0.8 and state.is_finished == False
                and now_node.child_num1 < self.len1[index]):
            move = self.action_space1[index][now_node.child_num1]
            this_values = self.create_new_node(state, now_node, move, 1)
        elif (dice > 0.8 and state.is_finished == False
              and now_node.child_num2 < self.len2[index]):
            move = self.action_space2[index][now_node.child_num2]
            this_values = self.create_new_node(state, now_node, move, 2)
        elif (now_node.child_num1 + now_node.child_num2 > 0):
            target_index = -1
            max_value = -100000
            for child in now_node.children:
                if (player == 1):
                    child_value = self.visit_values[
                        child.index][1] - self.visit_values[child.index][0]
                else:
                    child_value = self.visit_values[
                        child.index][0] - self.visit_values[child.index][1]
                child_uct = self.calc(child_value,
                                      self.visit_count_of[child.index],
                                      self.visit_count_of[index])
                if (child_uct > max_value or target_index == -1):
                    target_index = child.index
                    max_value = child_uct
            this_values = self.sample_path(target_index, depth + 1)
        else:
            this_values = state.greedy_simulate()
        # print(this_values.shape)
        # print(self.visit_values[index].shape)
        self.visit_values[index] += this_values
        return this_values

    def select_action(self):
        max_cnt = self.iterations
        player = self.root_state.player
        idx = 0
        self.max_depth = 0
        for i in range(max_cnt):
            self.sample_path(0, 0)
            if (time() - self.begin_time > 0.58):
                break
            idx = i
        print("iterations:", idx, " depth:", self.max_depth, " calc:",
              self.debug_count)
        target_index = -1
        max_values = -100000
        for child in self.search_tree.root.children:
            child_value = (self.visit_values[child.index][player] -
                           self.visit_values[child.index][1 - player]
                           ) / self.visit_count_of[child.index]
            if (child_value > max_values or target_index == -1):
                max_values = child_value
                target_index = child.index
        print(target_index, self.search_tree.n_nodes)
        target_move = self.search_tree.node_of[target_index].from_act
        print(max_values)
        return target_move, max_values


class Plaser:
    def __init__(self, is_First):
        self.move_history = []
        # print("player1:", is_First)
        if (is_First == True):
            self.player = 0
        else:
            self.player = 1

    def move(self, board, operations, scores, turn_number):
        steps = turn_number * 2
        new_scores = copy.deepcopy(scores)
        if (self.player == 1):
            temp = copy.deepcopy(new_scores[0])
            new_scores[0] = new_scores[1]
            new_scores[1] = temp
        # print("player1 move")
        # scores[0] = 20000
        scores = np.array(scores, dtype=np.float64)
        state = MyBoard(board, np.array(list(COLORS.keys())), new_scores,
                        self.player, steps, operations)
        operations2 = []
        for op in action_space:
            if op not in operations:
                operations2.append(op)
        t0 = time()
        mcts = MonteCarloTreeSearch(state, t0, operations, operations2)
        choice, value = mcts.select_action()
        value -= (scores[0] - scores[1])
        print(scores[0] - scores[1])
        print(value)
        if value < 3 and scores[0] > scores[1]:
            print("trick")
            tricklist = [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 5), (1, 5)),
                         ((0, 5), (0, 4)), ((5, 0), (4, 0)), ((5, 0), (5, 1))]
            found = False
            while not found:
                random_number = random.randint(0, 5)
                if not tricklist[random_number] in operations:
                    return tricklist[random_number]
        else:
            return choice
