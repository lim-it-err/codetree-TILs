dxs, dys = [-1, 0, 1, 0], [0, 1, 0, -1]
from collections import deque, defaultdict
class Fighter:
    def __init__(self, board, fighters):
        self.board = board
        self.fighter_lst = fighters
        self.fighter_arr = [[-3 for _ in range(len(self.board))] for _ in range(len(self.board))]
        self._fighter_to_arr()
        self.is_valid = lambda x, y: 0 <= x < len(board) and 0 <= y < len(board[0])
        self.answer = defaultdict(int)
    def _set_fighter(self,fighter, delta, value):
        r, c, h, w, k = fighter
        dx, dy = delta
        for x in range(h):
            for y in range(w):
                self.fighter_arr[r + x+dx][c + y+dy] = value
    def _fighter_to_arr(self):
        for i, fighter in enumerate(self.fighter_lst):
            self._set_fighter(fighter, (0, 0), i)

    def move(self, agent_id, direction):
        if not self.fighter_lst[agent_id]:
            return
        stack = deque([agent_id])
        while stack:
            cur_id = stack[-1]
            flag = False
            dx, dy = dxs[direction], dys[direction]

            r, c, h, w, k = self.fighter_lst[cur_id]
            for x in range(h):
                for y in range(w):
                    if self.is_valid(r+x+dx, c+y+dy):
                        if self.fighter_arr[r+x+dx][c+y+dy] not in [-3, cur_id]:
                            stack.append(self.fighter_arr[r+x+dx][c+y+dy])
                            flag = True
            if not flag:
                break
        cur_id = stack[-1]
        r, c, h, w, k = self.fighter_lst[cur_id]
        dx, dy = dxs[direction], dys[direction]
        for x in range(h):
            for y in range(w):
                if not self.is_valid(r+x+dx, c+y+dy) or self.board[r+x+dx][c+y+dy]==2:
                    # print(cur_id, r+x+dx, c+y+dy)

                    stack = deque([])
                    break
        stack = deque(set(list(stack)))
        moved = stack.copy()
        while stack:
            cur_id = stack.pop()
            dx, dy = dxs[direction], dys[direction]
            self._set_fighter(self.fighter_lst[cur_id], (0, 0), -3)
            self._set_fighter(self.fighter_lst[cur_id], (dx, dy), cur_id)
            r, c, h, w, k = self.fighter_lst[cur_id]
            self.fighter_lst[cur_id] = (r+dx, c+dy, h, w, k)
        while moved:
            fighter_idx = moved.pop()
            if fighter_idx == agent_id:
                continue

            r, c, h, w, k = self.fighter_lst[fighter_idx]
            damage = 0
            for x in range(h):
                for y in range(w):
                    if self.board[r+x][c+y]==1:
                        damage += 1
                        self.answer[fighter_idx]+=1
            if k-damage>0:
                self.fighter_lst[fighter_idx] = (r, c, h, w, k-damage)
            else:
                self._set_fighter(self.fighter_lst[fighter_idx], (0, 0), -3)
                self.fighter_lst[fighter_idx] = None
                del self.answer[fighter_idx]

    def print(self):
        for i in range(len(self.fighter_lst)):
            print(self.fighter_lst[i])
        for i in range(len(self.fighter_arr)):
            print(self.fighter_arr[i])

import sys
L, N, Q = map(int, input().split())
board = [0 for _ in range(L)]
fighters = []
def zero_based_int(data):
    return int(data)-1
for i in range(L):
    board[i] = list(map(int, input().split()))

for i in range(N):
    r, c, h, w, k = map(int, input().split())
    fighters.append((r-1, c-1, h, w, k))

agent = Fighter(board, fighters)
for i in range(Q):
    id,dir = map(int, input().split())
    # print(f"id: {id}, dir: {dir}")
    agent.move(id-1, dir)
    # agent.print()
answer = 0
for key in agent.answer:
    answer += agent.answer[key]
print(answer)