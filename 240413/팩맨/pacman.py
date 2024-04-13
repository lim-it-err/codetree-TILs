dxs, dys = [-1, -1, 0, 1, 1, 1, 0, -1], [0,-1, -1, -1, 0, 1, 1, 1]
M, T = map(int, input().split())
r, c = map(int, input().split())
monsters = []
board = [[{} for _ in range(4)] for _ in range(4)]
new_id = 0
is_valid = lambda x, y : 0<=x<4 and 0<=y<4
board_corpse = [[{} for _ in range(4)] for _ in range(4)]
board_corpse_prev = [[{} for _ in range(4)] for _ in range(4)]


class Monster:
    def __init__(self, pos, heading, id, power=0):
        self.pos = pos
        self.power = power
        self.status = 1  # Corpse = -1
        self.heading = heading # 상, 좌상 ....
        self.id = id
        if power==0:
            board[self.pos[0]][self.pos[1]][self.id] = True
        else:
            board[self.pos[0]][self.pos[1]][self.id] = False # Egg

    def validate(self):
        board[self.pos[0]][self.pos[1]][self.id] = True
        self.power=0
    def move(self, pacman_pos, board_corpse, board_corpse_prev):
        if self.power <0:
            return False
        x, y = self.pos
        _dir = self.heading
        for i in range(8):
            nx, ny = x+dxs[(_dir+i)%8], y+dys[(_dir+i)%8]
            if not is_valid(nx, ny):
                continue
            if (nx, ny) == pacman_pos:
                continue
            if board_corpse[nx][ny] != {}:
                continue
            if board_corpse_prev[nx][ny]!={}:
                continue
            self.pos = (nx, ny)
            del board[x][y][self.id]
            board[nx][ny][self.id] = True
            self.heading = (_dir+i)%8
            return True
        return False


    def copy(self, new_id):
        return Monster(self.pos, self.heading,new_id, power=-1)

    def make_corpse(self, board_corpse):
        self.status = -1
        x, y = self.pos
        del board[x][y][self.id]
        board_corpse[x][y][self.id] = True


class Pacman:
    def __init__(self, pos):
        self.pos = pos
        self.move_candidate = self.get_candidate()
        self.dxs, self.dys = [-1, 0, 1, 0], [0, -1, 0, 1]
    def get_candidate(self):
        lst = [[0], [1], [2], [3]]
        while True:
            if len(lst[0]) == 3:
                return lst
            nl, lst = list(lst[0]), lst[1:]

            for i in range(4):
                lst.append(nl + [i])
    def move(self):
        board_corpse = [[{} for _ in range(4)] for _ in range(4)]
        max_eat = 0
        max_idx = -1
        for i in range(64):
            visited = [[False for _ in range(4)] for _ in range(4)]

            directions = self.move_candidate[i]
            eat = 0
            x, y = self.pos
            for d in directions:
                x, y = x+self.dxs[d], y+self.dys[d]

                if not is_valid(x, y):
                    eat = -1
                    break
                if visited[x][y]:
                    continue

                visited[x][y] = True
                for key in board[x][y].keys():
                    if monsters[key].power == 0:
                        eat+=1
            if eat>max_eat:
                max_eat = eat
                max_idx = i

        directions = self.move_candidate[max_idx]
        x, y = self.pos
        for d in directions:
            x, y = x + self.dxs[d], y + self.dys[d]
            keys = list(board[x][y].keys())
            for key in keys:
                if monsters[key].power == 0:
                    monsters[key].make_corpse(board_corpse)
        self.pos = (x, y)
        return board_corpse


pacman = Pacman((r - 1, c - 1))

for i in range(M):
    r, c, d = map(int, input().split())
    monsters.append(Monster((r - 1, c - 1), d - 1, i))
    new_id = i
for i in range(T):
    monster_candidate = []
    for monster in monsters:
        if monster.power == -1:
            monster.validate()

        if monster.status>0:
            new_id +=1
            monster_candidate.append(monster.copy(new_id)) # 1단계


    monsters.extend(monster_candidate)
    for i, monster in enumerate(monsters):
        if monster.status>0:
            ret = monster.move(pacman.pos, board_corpse, board_corpse_prev) # 2단계, ret: monster moved

    board_corpse_prev = board_corpse # TODO
    board_corpse = pacman.move() # 3,4단계

sum = 0
for i in range(len(board)):
    for j in range(len(board)):
       sum+=len(board[i][j])
print(sum)