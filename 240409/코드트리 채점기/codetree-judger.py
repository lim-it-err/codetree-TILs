DEBUG = False
import heapq


class Domain:
    def __init__(self, name):
        self.domain_id = {}
        self.heap = []
        heapq.heapify(self.heap)
        self.name = name

    def add(self, t, p, uid):
        if uid in self.domain_id.keys():
            return 0
        self.domain_id[uid] = t
        heapq.heappush(self.heap, (p, t, uid, self.name))
        return 1
    def delete(self, uid):
        _, _, _uid, _ = heapq.heappop(self.heap)
        del self.domain_id[uid]
    def peek(self):
        if self.heap:
            return self.heap[0]
        return False
class WaitingQueue:
    def __init__(self):
        self.data = {}
        self.N = 0

    def add(self, t, p, u):
        domain, uid = u.split("/")
        if not domain in self.data:
            self.data[domain] = Domain(domain)
        if self.data[domain].add(t, p, uid):
            self.N += 1


    def delete(self, task):
        # Delete, if task are allocated.
        _, _, uid, domain_name = task
        self.data[domain_name].delete(uid)
        self.N -= 1

    def get_candidate(self, exclude):
        gp, gt = 1e12, 1e12
        ret_task = None
        for domain in self.data:
            if domain in exclude:
                continue
            element = self.data[domain].peek()
            if not element:
                continue
            p, t, x, y = element
            if p<gp or (p == gp and t<gt):
                ret_task = (p, t, x, y)
                gp, gt = p, t
        return ret_task

    def get_waiting_N(self):
        return self.N


class Judger():
    def __init__(self, N, wq):
        self.lst = [() for _ in range(N)]
        self.available = [i for i in range(N)]
        self.coldtime = {}
        self.working_domain = {}
        heapq.heapify(self.available)
        self.N = N
        self.wq = wq

    def allocate_available(self, t, task):
        p, _, uid, domain_name = task
        if not self.available:
            return False
        _id = heapq.heappop(self.available)
        self.lst[_id] = (p, t, uid, domain_name) # Updated T
        self.working_domain[domain_name] = True
        self.wq.delete(task)
        return True

    def start(self, t):
        exclude =list(self.working_domain.keys())+[domain_name for domain_name in self.coldtime if t<self.coldtime[domain_name]]
        exclude = {k:0 for k in exclude}
        candidates = wq.get_candidate(exclude)
        if not candidates:
            return False
        if not self.allocate_available(t, candidates):
            return False
        return True

    def end(self, end_t, worker_id):
        if self.lst[worker_id] == ():

            return
        task = self.lst[worker_id]
        p, t, uid, domain_name = task
        self.coldtime[domain_name] = t + (end_t - t) * 3
        del self.working_domain[domain_name]
        heapq.heappush(self.available, worker_id)
        self.lst[worker_id] = ()
        return

# import sys
# sys.stdin = open("input.txt")
wq = WaitingQueue()
Q = int(input())
jd = None
answer = []
import time
s = time.perf_counter()
for i in range(Q):
    cmd = input().split()
    if cmd[0] == "100":
        wq.add(0, 1, cmd[2])
        jd = Judger(int(cmd[1]), wq)
        # print(0, time.perf_counter() - s)
        # s = time.perf_counter()
        # 
        # if DEBUG:
        #     print(cmd, wq.get_waiting_N())
    if cmd[0] == "200":
        wq.add(int(cmd[1]), int(cmd[2]), cmd[3])
        # print(1, time.perf_counter() - s)
        # s = time.perf_counter()
        # if DEBUG:
        #     print(cmd, wq.get_waiting_N())
    if cmd[0] == "300":
        jd.start(int(cmd[1]))
        # print(2, time.perf_counter() - s)
        # s = time.perf_counter()
        # if DEBUG:
        #     print(cmd, wq.get_waiting_N())
    if cmd[0] == "400":
        jd.end(int(cmd[1]), int(cmd[2]) - 1)
        # print(3, time.perf_counter() - s)
        # s = time.perf_counter()
        # if DEBUG:
        #     print(cmd, wq.get_waiting_N())
    if cmd[0] == "500":
        answer.append(wq.get_waiting_N())
        # print(4, time.perf_counter() - s)
        # s = time.perf_counter()
# print("RET", time.perf_counter()-s)
for i in answer:
    print(i)