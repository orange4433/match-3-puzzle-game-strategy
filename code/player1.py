import numpy as np
import random

BOARD_SIZE = 6
N_ROWS = 1200
COLORS = {'R': '0', 'B': '1', 'G': '2', 'Y': '3', 'P': '4'}
action_space = [((i, j), (i, j + 1)) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE - 1)] + \
               [((i + 1, j), (i, j)) for i in range(BOARD_SIZE - 1) for j in range(BOARD_SIZE)]
action_board_dict={}
class MyBoard:
    def __init__(self, board, colors,score=0,movement=None,valid_movements=None):
        self.size = board.shape[0]
        self.board = board.copy()
        self.colors = colors
        # These MyBoard attributes support the alpha-beta search tree.
        self.score=score
        self.movement=movement
        self.valid_movements=valid_movements

    def change(self, loc1, loc2):
        x1, y1 = loc1
        x2, y2 = loc2
        temp1 = self.board[x1, y1].copy()
        temp2 = self.board[x2, y2].copy()
        self.board[x1, y1], self.board[x2, y2] = temp2, temp1

    @staticmethod
    def check(arr):
        repeats = set()
        for i in range(0, BOARD_SIZE - 2):
            for j in range(BOARD_SIZE):
                if arr[i, j] != 'nan' and (arr[i+1:i+3, j] == arr[i, j]).all():
                    repeats.add((i+1, j))
                if arr[j, i] != 'nan' and (arr[j, i+1:i+3] == arr[j, i]).all():
                    repeats.add((j, i+1))
        return repeats

    def eliminate(self, func=lambda x: (x - 2) ** 2):
        arr = self.board
        to_eliminate = np.zeros((self.size, self.size), dtype=int)
        directions = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
        to_visit = self.check(arr)
        score = 0

        for coord in to_visit:
            if to_eliminate[coord[0], coord[1]] == 1:
                continue
            head = 0
            connected = [coord, ]
            while head < len(connected):
                current = connected[head]
                to_eliminate[current[0], current[1]] = 1
                for d in directions:
                    neighbor = current + d
                    if (neighbor < 0).any() or (neighbor >= self.size).any():
                        continue
                    if (arr[neighbor[0], neighbor[1]] == arr[current[0], current[1]]
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
            self.board[i, :col_remained[i]] = col[:self.size][to_eliminate[i] == 0]
            self.board[i, col_remained[i]:N_ROWS - col_eliminated[i]] = col[self.size:]
            self.board[i, N_ROWS - col_eliminated[i]:] = np.nan

        # Return the total score and the number of columns eliminated
        return score, col_eliminated
    def get_next_state(self, action):# Board state after an action: score and the movement's new_board.
        (x1, y1), (x2, y2) = action
        new_board = MyBoard(board=self.board,colors=np.array(list(COLORS.keys())))
        new_board.change((x1, y1), (x2, y2))
        total_score, columns_eliminated = new_board.eliminate()
        while columns_eliminated.sum() and not (new_board.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
            score, columns_eliminated = new_board.eliminate()
            total_score += score
        new_board.score = total_score
        new_board.movement = action
        return new_board
    def get_info(self):
        if self.valid_movements is not None:
            return self.valid_movements
        operations = []
        arr = self.board
        arrt = self.board.T
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arr[i, j] == arr[i+2:i+4, j]).all():
                    operations.append(((i, j), (i+1, j)))
                    continue
                if i >= 2 and (arr[i+1, j] == arr[i-2:i, j]).all():
                    operations.append(((i, j), (i+1, j)))
                    continue
                if j >= 2 and ((arr[i, j] == arr[i+1, j-2:j]).all() |
                        (arr[i+1, j] == arr[i, j-2:j]).all()):
                    operations.append(((i, j), (i+1, j)))
                    continue
                if j <= self.size - 3 and ((arr[i, j] == arr[i+1, j+1:j+3]).all() |
                        (arr[i+1, j] == arr[i, j+1:j+3]).all()):
                    operations.append(((i, j), (i+1, j)))
                    continue
                if j >= 1 and j <= self.size - 2 and ((arr[i, j] == arr[i+1, [j-1, j+1]]).all() |
                        (arr[i+1, j] == arr[i, [j-1, j+1]]).all()):
                    operations.append(((i, j), (i+1, j)))
                    continue
        for i in range(self.size - 1):
            for j in range(self.size):
                if i <= self.size - 4 and (arrt[i, j] == arrt[i+2:i+4, j]).all():
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if i >= 2 and (arrt[i+1, j] == arrt[i-2:i, j]).all():
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j >= 2 and ((arrt[i, j] == arrt[i+1, j-2:j]).all() |
                        (arrt[i+1, j] == arrt[i, j-2:j]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j <= self.size - 3 and ((arrt[i, j] == arrt[i+1, j+1:j+3]).all() |
                        (arrt[i+1, j] == arrt[i, j+1:j+3]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
                if j >= 1 and j <= self.size - 2 and ((arrt[i, j] == arrt[i+1, [j-1, j+1]]).all() |
                        (arrt[i+1, j] == arrt[i, [j-1, j+1]]).all()):
                    operations.append(((j, i), (j, i + 1)))
                    continue
        return operations
    def get_children(self): # Children are boards obtained from every action in valid_movements.
        children = []
        for action in self.get_info():
            new_board = self.get_next_state(action)
            action_board_dict[action]=new_board
            children.append(new_board)
        children.sort(key=lambda x: x.score, reverse=True)
        return children
def finder(Board):# Find connected same-color blocks on the current main board.
    board=Board.board
    found=0
    for i in range(5):
        for j in range(5):
            if board[j][i]==board[j][i+1]:
                trick_action=((j,i),(j,i+1))
                found=1
                return trick_action,found
            if board[j][i]==board[j+1][i]:
                trick_action=((j,i),(j+1,i))
                found=1
                return trick_action,found
    return ((0,0),(0,1)),found
    
def alpha_beta_pruning(Board, depth, alpha, beta, maximizing_player, total_score): # Alpha-beta pruning returns the best action.
    # Recursion stopping condition:
    if depth == 0:
        return total_score, None

    if maximizing_player:# Maximizing player
        max_eval = float("-inf")
        best_move = None
        for child in Board.get_children()[:5]:
            child_eval, _ = alpha_beta_pruning(child, depth - 1, alpha, beta, False, total_score + child.score)
            if child_eval > max_eval:
                max_eval = child_eval
                best_move = child.movement
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:# Minimizing player
        min_eval = float("inf")
        best_move = None
        for child in Board.get_children()[:3]:
            child_eval, _ = alpha_beta_pruning(child, depth - 1, alpha, beta, True, total_score - child.score)
            if child_eval < min_eval:
                min_eval = child_eval
                best_move = child.movement
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move
def greedy_1(board,valid_movements):
    value = 0
    choice = None
    for action in valid_movements:
        (x1, y1), (x2, y2) = action
        new_board = MyBoard(board=board.board,colors=np.array(list(COLORS.keys())))
        new_board.change((x1, y1), (x2, y2))
        total_score, columns_eliminated = new_board.eliminate()
        while columns_eliminated.sum() and not (new_board.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
            score, columns_eliminated = new_board.eliminate()
            total_score += score
        if total_score > value:
            value = total_score
            choice = action
    if choice is not None:
        return choice,value
    return random.choice(action_space),value
def greedy_2(board,valid_movements):
    value = -99999
    choice = None
    for action in valid_movements:
        (x1, y1), (x2, y2) = action
        new_board = MyBoard(board=board.board,colors=np.array(list(COLORS.keys())))
        new_board.change((x1, y1), (x2, y2))
        total_score, columns_eliminated = new_board.eliminate()
        while columns_eliminated.sum() and not (new_board.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
            score, columns_eliminated = new_board.eliminate()
            total_score += score
        operations0=new_board.get_info()
        value0=-99999
        for action0 in operations0:
            (x1, y1), (x2, y2) = action0
            new_board0 = MyBoard(board=new_board.board, colors=board.colors)
            new_board0.change((x1, y1), (x2, y2))
            total_score0, columns_eliminated0 = new_board0.eliminate()
            while columns_eliminated0.sum() and not (new_board0.board[:BOARD_SIZE, :BOARD_SIZE] == 'nan').any():
                score0, columns_eliminated0 = new_board0.eliminate()
                total_score0 += score0
            if total_score0>value0:
                value0=total_score0
        total_score-=value0
        if total_score > value:
            value = total_score
            choice = action
    if choice is not None:
        return choice,value
    return random.choice(action_space),value
def select(board,time,is_First,move_history,turn_number,scores,opponent_score_list,my_score_list,is_ahead):
    valid_movements=board.valid_movements
    if turn_number<100:
        if time>58.5:
            choice,value=greedy_1(board,valid_movements)
            return choice
        else:
            if turn_number>=3:
                if is_ahead and opponent_score_list[len(opponent_score_list)-1]==opponent_score_list[len(opponent_score_list)-2]:
                    # Defend against setup moves while ahead.
                    if is_First:
                        action=move_history[2*(turn_number-1)-1]
                    else:
                        action = move_history[2*turn_number-2]
                    return action
                if not is_ahead and opponent_score_list[len(opponent_score_list)-1]==opponent_score_list[len(opponent_score_list)-2] and my_score_list[len(my_score_list)-1]==my_score_list[len(my_score_list)-2]:
                    # Avoid getting trapped when an opponent interrupts a setup while behind.
                    _, choice=alpha_beta_pruning(board, 3, float("-inf"),float("inf"),True, 0)
                    if choice is not None:
                        return choice
                    else:
                        return random.choice(valid_movements)
            # Search for the best value regardless of the lead; depth 3 could be reduced while ahead or increased while behind.
            value,best_move=alpha_beta_pruning(board, 3, float("-inf"),float("inf"),True, 0)
            if best_move is not None:
                if not is_ahead:
                    next_board=action_board_dict[best_move]
                    add_value=next_board.score
                    if scores[0]+add_value>scores[1]:
                        return best_move
                    else:
                        if not next_board.get_info():
                            return random.choice(valid_movements)
                if value>=6:
                    return best_move
                elif value<6:
                    trick_action,found=finder(board)
                    if found:
                        return trick_action
                    else:
                        if trick_action not in valid_movements:
                            return trick_action
                        else:
                            for movement in [((0,0),(1,0)),((0,5),(1,5)),((0,5),(0,4)),((5,0),(4,0)),((5,0),(5,1))]:
                                if not movement in valid_movements:
                                    return movement
                            return random.choice(action_space)
            else:
                return random.choice(valid_movements)
            
    else:# Take a final-turn risk.
        if not is_ahead:# While behind
            if is_First:# First player
                choice,value=greedy_2(board,valid_movements)
                if choice is not None:# What if the score margin is negative?
                    return choice
            elif not is_First:
                choice,value=greedy_1(board,valid_movements)
                if choice is not None:
                    return choice
        else:
            if is_First:
                fen_cha=scores[0]-scores[1]
                choice,value=greedy_2(board,valid_movements)
                if choice is not None and value>=-fen_cha:
                    return choice
                else:# Retain this choice for now; finder() may not be appropriate here.
                    trick_action,found=finder(board)
                    if found:
                        return trick_action
                    else:
                        if not trick_action in valid_movements:
                            return trick_action
                        else:
                            for movement in [((0,0),(1,0)),((0,5),(1,5)),((0,5),(0,4)),((5,0),(4,0)),((5,0),(5,1))]:
                                if not movement in valid_movements:
                                    return movement
                            return random.choice(action_space)
            elif not is_First:
                choice,value=greedy_1(board,valid_movements)
                if choice is not None:
                    return choice
def Chebyshev_distance(x1,y1,x2,y2):
    return abs(x1-x2)+abs(y1-y2)
def killer_search(board, valid_movements,length):
    if length == 1:
        return killer_search_length_1(board, valid_movements[0])
    else:
        return killer_search_length_2(board, valid_movements)

def killer_search_length_1(board, movement):
    (x1, y1), (x2, y2) = movement
    for action in action_space:
        (x3, y3), (x4, y4) = action
        if Chebyshev_distance(x1, y1, x3, y3) <= 3 \
           or Chebyshev_distance(x1, y1, x4, y4) <= 3 \
                or Chebyshev_distance(x2, y2, x3, y3) <= 3 \
                or Chebyshev_distance(x2, y2, x4, y4) <= 3:
            new_board = MyBoard(board=board.board, colors=np.array(list(COLORS.keys())))
            new_board.change((x3, y3), (x4, y4))
            new_board.eliminate()
            operations = new_board.get_info()
            if not operations:
                return action

def killer_search_length_2(board, movements):
    candidates = []
    (x1, y1), (x2, y2) = movements[0]
    (x3, y3), (x4, y4) = movements[1]
    Original_dicts=[
            Chebyshev_distance(x1, y1, x3, y3),
            Chebyshev_distance(x1, y1, x4, y4),
            Chebyshev_distance(x2, y2, x3, y3),
            Chebyshev_distance(x2, y2, x4, y4),
        ]
    if np.any(np.array(Original_dicts)<=4):
        for action in action_space:
            (x5, y5), (x6, y6) = action
            dists = [
                Chebyshev_distance(x1, y1, x5, y5),
                Chebyshev_distance(x1, y1, x6, y6),
                Chebyshev_distance(x2, y2, x5, y5),
                Chebyshev_distance(x2, y2, x6, y6),
                Chebyshev_distance(x3, y3, x5, y5),
                Chebyshev_distance(x3, y3, x6, y6),
                Chebyshev_distance(x4, y4, x5, y5),
                Chebyshev_distance(x4, y4, x6, y6)
            ]
            if np.any(np.array(dists) <= 2):
                new_board = MyBoard(board=board.board, colors=np.array(list(COLORS.keys())))
                new_board.change((x5, y5), (x6, y6))
                new_board.eliminate()
                operations = new_board.get_info()
                if not operations:
                    return (x5, y5), (x6, y6)
    return None
         
        
    
class Plaser:
    def __init__(self, is_First):
        # Plaser stores turn order, both score histories, used times (used_time[0] is ours), and both action histories.
        self.is_First=is_First
        self.my_score_list=[]
        self.opponent_score_list=[]
        self.move_history=[]

    def move(self, current_board, valid_movements, scores, turn_number):
        self.my_score_list.append(scores[0])
        self.opponent_score_list.append(scores[1])
        my_score_list=self.my_score_list
        opponent_score_list=self.opponent_score_list
        is_First=self.is_First
        move_history=self.move_history 
        board=MyBoard(board=current_board, colors=np.array(list(COLORS.keys())), valid_movements=valid_movements)
        length=len(valid_movements)
        my_time=self.used_time[0]
        opponent_time=self.used_time[1]
        is_ahead=0
        if scores[0]>scores[1] or (scores[0]==scores[1] and my_time<opponent_time):
            is_ahead=1
        if length<=2 and is_ahead:
            kill_move=killer_search(board,valid_movements,length)
            if kill_move is not None:
                return kill_move
        return select(board,my_time,is_First,move_history,turn_number,scores,opponent_score_list,my_score_list,is_ahead)
        

