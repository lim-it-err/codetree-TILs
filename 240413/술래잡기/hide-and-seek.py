N, M, H, K = map(int, input().split())

board = [[{} for _ in range(N)] for _ in range(N)]
tree_board = [[False for _ in range(N)] for _ in range(N)]
runners = []


def get_distance(a, b):
    value = abs(a[0] - b[0]) + abs(a[1] - b[1])
    return value


class Runner:
    def __init__(self, x, y, direction, N, i):
        self.is_disabled = False
        self.pos = (x, y)
        self.direction = direction - 1  # 1: 좌(1)우(0), 2: 상(1)하(0)
        self.view = 0
        self.dxs, self.dys = [[0, 0], [1, -1]], [[1, -1], [0, 0]]
        self.N = N
        self.id = i
        board[x][y][self.id] = True

    def disable(self):
        x, y = self.pos
        del board[x][y][self.id]
        self.is_disabled = True

    def is_valid(self, next_pos, catcher_pos):
        x, y = next_pos
        if not (0 <= x < self.N and 0 <= y < self.N):
            return -1
        if next_pos == catcher_pos:
            return -2
        return 1

    def move(self, catcher_pos):
        if get_distance(self.pos, catcher_pos) > 3:
            return False
        x, y = self.pos
        nx, ny = self.dxs[self.direction][self.view] + x, self.dys[self.direction][self.view] + y

        validity = self.is_valid((nx, ny), catcher_pos)
        if validity > 0:
            self.pos = (nx, ny)
            del board[x][y][self.id]
            board[nx][ny][self.id]=True
            return True
        elif validity == -2:
            return False

        self.view = (self.view + 1) % 2
        nx, ny = self.dxs[self.direction][self.view] + x, self.dys[self.direction][self.view] + y
        if self.is_valid((nx, ny), catcher_pos) > 0:
            self.pos = (nx, ny)
            del board[x][y][self.id]
            board[nx][ny][self.id]=True
            return True
        return False

class Catcher:
    def __init__(self, N):
        self.pos = (N // 2, N // 2)
        self.dxs, self.dys = [-1, 0, 1, 0], [0, 1, 0, -1]
        self.direction = 0
        self.N = N
        self.candidate = self.make_candidate()
        self.idx = 0
        self.reverse = 1
    def make_candidate(self):
        nx, ny = self.pos[0], self.pos[1]
        candidate = [(nx, ny, 0)]
        while not (nx==0 and ny ==0):
            degree = 1
            di = 0
            for i in range(self.N):
                for _ in range(2):
                    for j in range(int(degree)):
                        nx, ny = nx+self.dxs[di], ny+self.dys[di]
                        if nx == -1:
                            return candidate
                        candidate.append((nx, ny, di))
                    if (nx, ny) in [(0, 0), self.pos]:
                        di = (di+2)%4
                    else:
                        di = (di+1)%4
                    candidate[-1] = (candidate[-1][0], candidate[-1][1], di)
                degree+=1

    def clip(self, value, min_v, max_v):
        return min(max(min_v, value), max_v)

    def move(self):
        self.idx+=self.reverse
        if self.idx == self.N*self.N-1 or self.idx == 0:
            self.reverse*=-1
        self.pos = self.candidate[self.idx][0], self.candidate[self.idx][1]
        if self.reverse<0:
            self.direction = (self.candidate[self.idx][2]+2)%4
        else:
            self.direction = self.candidate[self.idx][2]
    def look_at(self, tree_board):
        ret_value = []
        x, y = self.pos
        for i in range(3):
            nx, ny = x + self.dxs[self.direction]*(i), y + self.dys[self.direction]*(i)
            if 0 <= nx < self.N and 0 <= ny < self.N and not tree_board[nx][ny]:
                ret_value.append((nx, ny))
        return ret_value


catcher = Catcher(N)
for i in range(M):
    x, y, z = map(int, input().split())
    runners.append(Runner(x - 1, y - 1, z, N, i + 1))

for i in range(H):
    x, y = map(int, input().split())
    tree_board[x - 1][y - 1] = True
score = 0
for i in range(K):
    for runner in runners:
        if runner.is_disabled:
            continue
        runner.move(catcher.pos)
    catcher.move()

    for value in catcher.look_at(tree_board):
        x, y = value
        keys = list(board[x][y].keys())
        for key in keys:
            runner = runners[key-1]
            runner.disable()
            score+=(i+1)
    


print(score)