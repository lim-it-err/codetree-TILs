# import sys
# sys.stdin = open("input.txt")
import heapq

class Rabbit:
    def __init__(self, pid, power):
        self.pid = pid
        self.power = power
        self.jump = 0
        self.pos = (1, 1)
    def change_power(self, x):
        self.power *= x

    def get_priority(self):
        return (self.jump, sum(self.pos), self.pos[0], self.pos[1], self.pid)


class RabbitManager:
    def __init__(self, pids, distances, N, M):
        self.N, self.M = N, M
        self.lst = [Rabbit(pid, distance) for pid, distance in zip(pids, distances)]
        self.map_pid_to_lst = {self.lst[i].pid:i for i in range(len(self.lst))}
        self.chosen = [False for _ in range(len(self.lst))]
        self.priorities =[rabbit.get_priority() for rabbit in self.lst]
        heapq.heapify(self.priorities)
        self.score = [0 for _ in range(len(self.lst))]
        self.priorities2 =[ (-sum(rabbit.pos), -rabbit.pos[1], -rabbit.pos[0],-rabbit.pid ) for rabbit in self.lst]
        heapq.heapify(self.priorities2)
    def get_idx(self, pid):
        return self.map_pid_to_lst[pid]

    def move(self, K, S):
        self.chosen = [False for _ in range(len(self.lst))]
        max_idx, max_dist = 1e9, (0, 0)
        sum_score = 0
        for _ in range(K):
            _, _, _, _, pid = heapq.heappop(self.priorities)
            idx = self.get_idx(pid)
            agent_pos = self._move(idx)
            _score = sum(agent_pos)
            sum_score += _score
            self.score[idx]-=_score
            self.chosen[idx]= True

            if agent_pos>max_dist:
                max_idx = idx
                max_dist = agent_pos
            elif agent_pos == max_dist:
                max_idx = max(max_idx, idx)
            heapq.heappush(self.priorities, self.lst[idx].get_priority())
        for i in range(len(self.lst)):
            self.score[i] += sum_score
        self.score[max_idx] += S
        return

    def _move(self, idx):
        agent = self.lst[idx]
        power = agent.power
        agent.jump += 1
        x, y = agent.pos
        dxs, dys = [-1, 0, 1, 0], [0,1, 0, -1] # 상하좌우
        candidates = []
        for dx, dy in zip(dxs, dys):
            candidates.append(self.algorithm(x, y, dx, dy, power, N, M))
        candidates.sort(key=lambda x: (-x[0]-x[1],-x[0], -x[1]))
        agent.pos = candidates[0]
        return agent.pos

    def algorithm(self, x, y, dx, dy, power, N, M):
        x-=1
        y-=1
        if dx:
            T = 2 * N - 2
            power %= T

            B = N
        else:
            T = 2 * M - 2
            power %= T
            B = M
        if dx:
            nx = x + dx * power
            if nx < 0:
                nx = -nx
            if nx >= B:
                nx = -nx % T
            return nx+1, y+1
        else:
            ny = y + dy * power
            if ny < 0:
                ny = -ny
            if ny >= B:
                ny = -ny % T
            return x+1, ny+1

    def change_power(self, pid, L):
        self.lst[self.get_idx(pid)].change_power(L)
Q = int(input())
rm = None
for i in range(Q):
    cmd = list(map(int, input().split()))
    if cmd[0] == 100:
        N, M, _ = cmd[1:4]
        pids = [v for i, v in enumerate(cmd[4:]) if i%2==0]
        distances = [v for i, v in enumerate(cmd[4:]) if i%2]
        rm = RabbitManager(pids, distances, N,M)
    if cmd[0] == 200:
        rm.move(cmd[1], cmd[2])
    if cmd[0] == 300:
        rm.change_power(cmd[1], cmd[2])
    if cmd[0] == 400:
        print(max(rm.score))