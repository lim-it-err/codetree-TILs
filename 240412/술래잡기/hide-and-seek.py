N, M, H, K = map(int, input().split())

board = [[False for _ in range(N)] for _ in range(N)]
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
        self.dxs, self.dys = [[0, 0], [-1, 1]], [[1, -1], [0, 0]]
        self.N = N
        self.id = i

    def disable(self):
        x, y = self.pos
        board[x][y] = 0
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
            board[x][y] = 0
            board[nx][ny] = self.id
            return True
        elif validity == -2:
            return False

        self.view = (self.view + 1) % 2
        nx, ny = self.dxs[self.direction][self.view] + x, self.dys[self.direction][self.view] + y
        if self.is_valid((nx, ny), catcher_pos) > 0:
            self.pos = (nx, ny)
            board[x][y] = 0
            board[nx][ny] = self.id
            return True
        return False


class Catcher:
    def __init__(self, N):
        self.pos = (N // 2, N // 2)
        self.dxs, self.dys = [-1, 0, 1, 0], [0, 1, 0, -1]
        self.cur = 2
        self.direction = 0
        self.reverse = 1
        self.N = N

    def clip(self, value, min_v, max_v):
        return min(max(min_v, value), max_v)

    def move(self):
        amount = self.cur // 2
        x, y = self.pos
        self.pos = (self.clip(x + self.dxs[self.direction] * amount, 0, self.N - 1),
                    self.clip(y + self.dys[self.direction] * amount, 0, self.N - 1))

        if self.pos == (0, 0) or self.pos == (self.N // 2, self.N // 2):
            self.cur += self.reverse
            self.direction = (self.direction + 2 + self.reverse) % 4
            self.reverse *= -1
        self.cur += self.reverse
        self.direction = (self.direction + self.reverse) % 4

    def look_at(self, tree_board):
        ret_value = []
        x, y = self.pos
        for i in range(3):
            nx, ny = x + self.dxs[self.direction]*(i+1), y + self.dys[self.direction]*(i+1)
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
        if board[x][y]!= 0:
            runner = runners[board[x][y]-1]
            if not runner.is_disabled:
                runner.disable()
                score+=(i+1)

print(score)