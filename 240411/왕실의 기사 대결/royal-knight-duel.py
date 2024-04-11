L, N, Q = map(int, input().split())
board = []
agent_board = [[0 for _ in range(L)] for _ in range(L)]
agent = []
for i in range(L):
    board.append(list(map(int, input().split())))




class Agent:
    def __init__(self, init_data, _id, N):
        r, c, h, w, k = init_data
        self.activate = True
        self.pos = (r-1, c-1)
        self.area = (h, w)
        self.power = k
        self.initial = k
        self.id = _id
        self.N = N
        self._record_pos(self.id)

    def _record_pos(self, degree, dx=0, dy=0):
        r, c = self.pos
        h, w = self.area
        for i in range(r+dx, r+h+dx):
            for j in range(c+dy, c+w+dy):
                agent_board[i][j] = degree
    def manage_health(self):
        r, c = self.pos
        h, w = self.area
        for i in range(r, r + h):
            for j in range(c, c + w):
                if board[i][j] == 1:
                    self.power-=1
        if self.power <= 0:
            self.activate = False
            self._record_pos(0)
    def is_available(self, dx, dy):
        r, c = self.pos
        h, w = self.area
        if r+dx<0 or c+dy<0 or r+h+dx>self.N or c+w+dy>self.N:
            return False

        ret = {}
        if dx>0:
            for i in range(c, c+w):
                if board[r+h][i] == 2:
                    return False
                if agent_board[r+h][i] > 0:
                    ret[agent_board[r+h][i]] = True
        elif dx < 0:
            for i in range(c, c+w):
                if board[r-1][i] == 2:
                    return False
                if agent_board[r-1][i] > 0:
                    ret[agent_board[r-1][i]] = True
        if dy > 0:
            for i in range(r, r+h):
                if board[i][c+w] == 2:
                    return False
                if agent_board[i][c+w] > 0:
                    ret[agent_board[i][c+w]] = True
        elif dy < 0:
            for i in range(r, r+h):
                if board[i][c-1]==2:
                    return False
                if agent_board[i][c-1] > 0:
                    ret[agent_board[i][c-1]] = True
        return ret

    def move(self, dx, dy):
        if self.is_available(dx, dy) == False:
            return False
        r, c= self.pos
        self._record_pos(0)
        self._record_pos(self.id, dx, dy)
        self.pos = (r+dx, c+dy)
        return True
    def debug(self):
        for i in range(len(board)):
            print(board[i])

for i in range(N):
    r, c, h, w, k = tuple(map(int, input().split()))
    agent.append(Agent((r, c, h, w, k), i+1, L))

from collections import deque


for i in range(Q):
    flag = True
    x, y = map(int, input().split())
    if not agent[x-1].activate:
        continue
    dxs, dys = [-1, 0, 1, 0], [0, 1, 0, -1]
    s = deque([x])
    _s = deque([x])
    while _s:
        cur = _s.pop()
        next_node= agent[cur-1].is_available(dxs[y], dys[y])
        if next_node == False:
            flag = False
            break
        for key in next_node.keys():
            s.append(key)
            _s.append(key) # 1~

    if flag:
        while s:
            cur = s.pop()
            ret = agent[cur-1].move(dxs[y], dys[y])
            if ret and cur!=x:
                agent[cur-1].manage_health()

sum = 0
for a in agent:
    if a.activate:
        sum+=(a.initial-a.power)
print(sum)