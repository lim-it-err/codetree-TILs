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
        if DEBUG:
            print("After Insertion", self.heap, self.domain_id)
        return 1
    def delete(self, uid):
        _, _, _uid, _ = heapq.heappop(self.heap)
        # print(uid, "deleted", self.name)
        assert _uid == uid, "Logic Wrong."
        del self.domain_id[uid]
        # print(self.domain_id)
    def peek(self):
        if self.heap:
            return self.heap[0]
        print("WARNING: Domain is Empty!")
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

    def get_candidate(self):
        candidates = []
        heapq.heapify(candidates)
        for domain in self.data:
            data = self.data[domain].peek()
            if not data:
                continue
            heapq.heappush(candidates, self.data[domain].peek())
        return candidates

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
        # task : (p, t, uid, domain_name)
        p, _, uid, domain_name = task
        if not self.available:
            return False
        _id = heapq.heappop(self.available)
        self.lst[_id] = (p, t, uid, domain_name) # Updated T
        self.working_domain[domain_name] = True
        self.wq.delete(task)
        return True

    def start(self, t):
        candidates = wq.get_candidate()
        while candidates:
            candidate = heapq.heappop(candidates)
            _, _, uid, domain_name = candidate
            if domain_name in self.working_domain:
                continue  # Still Working
            if domain_name in self.coldtime and t < self.coldtime[domain_name]:
                continue  # in coldtime
            if not self.allocate_available(t, candidate):
                if DEBUG:
                    print("300:No worker left")
                return False
            if DEBUG:
                print(f"300:{candidate} started working")
            return True

    def end(self, end_t, worker_id):
        if self.lst[worker_id] == ():
            if DEBUG:
                print(f"400: {worker_id} was not in work. ignoring")
            return
        task = self.lst[worker_id]
        p, t, uid, domain_name = task
        self.coldtime[domain_name] = t + (end_t - t) * 3
        del self.working_domain[domain_name]
        heapq.heappush(self.available, worker_id)
        self.lst[worker_id] = ()
        if DEBUG:
            print(f"400: {task} are deleted, coldtime:{self.coldtime}")
        return


wq = WaitingQueue()
N = int(input())
jd = Judger(N, wq)
for i in range(N):
    cmd = input().split()
    if cmd[0] == "100":
        wq.add(0, 1, cmd[2])
        if DEBUG:
            print(cmd, wq.get_waiting_N())
    if cmd[0] == "200":
        wq.add(int(cmd[1]), int(cmd[2]), cmd[3])
        if DEBUG:
            print(cmd, wq.get_waiting_N())
    if cmd[0] == "300":
        jd.start(int(cmd[1]))
        if DEBUG:
            print(cmd, wq.get_waiting_N())
    if cmd[0] == "400":
        jd.end(int(cmd[1]), int(cmd[2]) - 1)
        if DEBUG:
            print(cmd, wq.get_waiting_N())
    if cmd[0] == "500":
        print(wq.get_waiting_N())