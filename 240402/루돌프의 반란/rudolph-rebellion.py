DEBUG = 0
from typing import List, Tuple
from collections import deque
def get_length(src, dst):
    return (src[0]-dst[0])**2 + (src[1]-dst[1])**2
def zero_based_map(x):
    return int(x)-1
class Santa:
    def __init__(self, santa_lst, board_size):
        self.N = len(santa_lst)
        self.lst = santa_lst[:]
        self.board = self.to_board(board_size)
        self.invalidated = [False for _ in range(self.N)]
        self.faint = [0 for i in range(self.N)]
        self.score = [0 for i in range(self.N)]

    def santa_is_valid(self, idx):
        assert not self.invalidated[idx] and self.faint[idx] == 0
    def to_board(self, board_size):
        _board = [[-1 for _ in range(board_size)] for _ in range(board_size)]
        for i, santa in enumerate(self.lst):
            x, y = santa
            _board[x][y] = i
        return _board
        
    def move_to_rodulph(self, santa_idx, rodulph_pos):
        directions = self._get_rodulph_directions(santa_idx, rodulph_pos)
        for direction in directions:
            if direction: # Do not Move
                if self._move(santa_idx, direction):
                    return direction
        return False

    def fly(self, santa_idx, direction, amount):
        x, y = self.lst[santa_idx]
        nx, ny = x+amount*direction[0], y+amount*direction[1]
        if not (0<=nx<len(self.board) and 0<=ny<len(self.board)):
            self.invalidated[santa_idx] = True
            self.board[x][y] = -1
            if DEBUG == 2:
                print(f"user {santa_idx} are invalidated, during {direction}, {amount}")
            return
        if self.board[nx][ny] != -1:
            next_idx = self.board[nx][ny]
            self.fly(next_idx, direction, 1)
        self.board[x][y] = -1
        self.board[nx][ny] =santa_idx
        self.lst[santa_idx] = (nx, ny)
        if DEBUG == 2:
            print(f" user {santa_idx} flied from {(x, y)} to {(nx, ny)}")
    def get_score(self):
        for i in range(len(self.score)):
            if not self.invalidated[i]:
                self.score[i] += 1
    def _get_rodulph_directions(self, santa_idx, rodulph_pos):
        self.santa_is_valid(santa_idx)
        santa_pos = self.lst[santa_idx]
        
        def clip(x):
            return min(max(-1, x), 1)
        ret_value = []
        scores = 0
        for dx, dy in zip([-1, 0, 1, 0], [0, 1, 0, -1]):
            if get_length((santa_pos[0]+dx, santa_pos[1]+dy), rodulph_pos) < get_length(santa_pos, rodulph_pos): 
                ret_value.append((get_length((santa_pos[0]+dx, santa_pos[1]+dy), rodulph_pos), scores, dx, dy))
                scores+=1
        ret_value.sort()        

        ret_value = [tuple(map(clip, (r[2], r[3]))) for r in ret_value]
        return ret_value
    def _move(self, santa_idx, direction) -> bool:
        dx, dy = direction
        x, y = self.lst[santa_idx]
        if not (0<=x+dx<len(self.board) and 0<=y+dy<len(self.board)):
            return False
        next_idx = self.board[x+dx][y+dy]
        if next_idx != -1:
            if DEBUG:
                print(f"Santa {next_idx} occupies from {santa_idx}, ({x+dx}, {y+dy}) ")
            return False
        self.board[x][y] = -1
        self.board[x+dx][y+dy] = santa_idx
        self.lst[santa_idx] = (x+dx, y+dy)
        if DEBUG == 2:
            print(f"Santa {santa_idx } moved {(x, y)} to {(x+dx, y+dy)}")
        return True
    def hit_rodulph(self, idx, rodulph_pos) ->bool:
        if self.lst[idx] == rodulph_pos:
            return True
        return False
    def decrease_faint(self):
        for i in range(self.N):
            self.faint[i] = max(self.faint[i]-1, 0)
class Rodulph:
    def __init__(self, pos):
        self.pos = pos

    def choose_santa(self, santa_obj): #FIXME: Performance Issue
        metadata = []
        for i, santa in enumerate(santa_obj.lst):
            if santa_obj.invalidated[i]:
                continue
            dist = get_length(self.pos, santa)
            metadata.append((dist, santa[0], santa[1], i))
        if not metadata:
            return False
        metadata.sort(key=lambda x: (x[0], -x[1], -x[2]))
        return metadata[0][3]

    def move_to_santa(self, santa) ->Tuple :
        relative_vector = (santa[0]-self.pos[0], santa[1]-self.pos[1])
        def clip(x):
            return min(max(-1, x), 1)
        dx, dy = map(clip, relative_vector)
        self.pos = (self.pos[0]+dx, self.pos[1]+dy)
        return (dx, dy)

    def hit_santa(self, santa) -> bool:
        if santa == self.pos:
            return True
        return False

N, M, P, C, D = map(int, input().split())
rx, ry = map(zero_based_map, input().split())
santa_lst = [0 for _ in range(P)]
for i in range(P):
    idx, x, y = map(zero_based_map, input().split())
    santa_lst[idx] = (x, y)

santa_obj = Santa(santa_lst, N)
rodulph_obj = Rodulph((rx, ry))

def print_board_status(santa, rodulph):
    for i in range(N):
        for j in range(N):
            if (i, j) == rodulph.pos:
                print("R", end="\t")
            else:
                print(santa.board[i][j], end="\t")
        print()
    print()
    print("=======================")
if DEBUG:
    print_board_status(santa_obj, rodulph_obj)
while M:
    if DEBUG:
        print("Rodulph Move!")
    santa_idx = rodulph_obj.choose_santa(santa_obj)
    if santa_idx is None:
        break
    chosen_santa = santa_obj.lst[santa_idx]
    direction = rodulph_obj.move_to_santa(chosen_santa)
    if rodulph_obj.hit_santa(chosen_santa):        
        santa_obj.score[santa_idx] +=C
        if DEBUG ==2:
            print(f"Rodulph Hit to santa {santa_idx} on {M}th Phase, by {direction}, and flied {C}")
        santa_obj.fly(santa_idx, direction, C)
        santa_obj.faint[santa_idx] = 2

    if DEBUG:
        print_board_status(santa_obj, rodulph_obj)
        print("Santa Move!")
    for i in range(P):
        if not santa_obj.invalidated[i] and santa_obj.faint[i] == 0:
            direction = santa_obj.move_to_rodulph(i, rodulph_obj.pos)
            if santa_obj.hit_rodulph(i, rodulph_obj.pos):
                santa_obj.score[i]+=D
                santa_obj.fly(i, (-direction[0], -direction[1]), D)
                santa_obj.faint[i] = 2
    santa_obj.decrease_faint()
    santa_obj.get_score()
    if DEBUG:
        print_board_status(santa_obj, rodulph_obj)

    M-=1
for i in range(P):
    print(santa_obj.score[i], end=" ")