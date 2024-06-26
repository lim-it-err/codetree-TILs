# 7:20
# import sys
# sys.stdin = open("input2.txt")
DEBUG = False
class Box:
    def __init__(self, _id, _w):
        self.nxt = None
        self.prv = None
        self.id = _id
        self.w = _w

    def link_nxt(self, target_box=None):
        self.nxt = target_box

    def link_prv(self, target_box=None):
        self.prv = target_box


class CircularLinkedList():
    def __init__(self, id, N, ids, weights):
        self.id = id
        self.available = True
        self.head = None
        self.make_linked_list(ids, weights)
        self.N = len(ids)
        self.valid = {_id: True for _id in ids}  # ID, True, if needs deletion-> False
    def make_linked_list(self, ids, weights):
        prev_box = None
        for id, weight in zip(ids, weights):
            new_box = Box(id, weight)
            if prev_box:
                new_box.link_prv(prev_box)
                prev_box.link_nxt(new_box)
            else:
                self.head = new_box
            prev_box = new_box
        prev_box.link_nxt(self.head)
        self.head.link_prv(prev_box)

    def pop(self, criteria):
        if self.N < 0:
            if DEBUG:
                print("LinkedList Empty")
            return 0
        self._check_deletion()
        if self.head.w <= criteria:
            self.valid[self.head.id] = False
            ret = self.head.w
            self.head = self.head.nxt
            self.N-=1
            return ret
        self.head = self.head.nxt
        return 0 # Nothing to pop

    def remove(self, r_id):
        if not r_id in self.valid or self.valid[r_id] == False:
            return -1
        self.N -=1
        self.valid[r_id] = False
        self._check_deletion()

        return r_id

    def declare_breakdown(self):
        self.available = False

    def get_element(self, other_linkedlist):
        last_head = self.head.prv
        other_head = other_linkedlist.head
        other_last_head = other_linkedlist.head.prv

        last_head.link_nxt(other_linkedlist.head)
        other_head.link_prv(last_head)

        self.head.link_prv(other_last_head)
        other_last_head.link_nxt(self.head)
        for key in other_linkedlist.valid:
            self.valid[key] = other_linkedlist.valid[key]
        self.N += other_linkedlist.N




    def is_element(self, f_id):
        if f_id in self.valid and self.valid[f_id] == True:
            self._check_deletion()
            while self.head.id != f_id:
                self.head = self.head.nxt
            return True
        return False

    def _check_deletion(self):
        while True:
            if self.N <= 0:
                return False  # No element Left
            if self.valid[self.head.id] == False:
                prv_node = self.head.prv
                nxt_node = self.head.nxt
                prv_node.link_nxt(nxt_node)
                nxt_node.link_prv(prv_node)
                head = self.head.nxt
                self.head = head
                continue
            return False
    def debug(self):
        if DEBUG:
            head = self.head
            print(head.id, end="->")
            cur = head.nxt
            while cur != head:
                print(cur.id, end="->")
                cur= cur.nxt
            print("E")


Q = int(input())
line = []
import time
for _ in range(Q):
    cmd = list(map(int, input().split()))
    if cmd[0] == 100:
        N, M = cmd[1], cmd[2]
        cmd_n = cmd[3:]
        cmd_n, cmd_m = cmd_n[:len(cmd_n)//2], cmd_n[len(cmd_n)//2:]
        for j in range(0, N, N//M):
            line.append(CircularLinkedList(j//(N//M), N, cmd_n[j:j+N//M], cmd_m[j:j+N//M]))
        s = time.perf_counter()
    elif cmd[0] == 200:
        summation = 0
        for l in line:
            if not l.available:
                continue
            this = l.pop(cmd[1])
            summation+=this
        print(summation)
    elif cmd[0] == 300:
        summation = -1
        for l in line:
            if not l.available:
                continue
            this = l.remove(cmd[1])
            summation = max(summation, this)
        print(summation)
    elif cmd[0] == 400:
        summation = -1
        for i, l in enumerate(line):
            if not l.available:
                continue
            if l.is_element(cmd[1]):
                summation = i+1
        print(summation)
        # s=time.perf_counter()
    elif cmd[0] == 500:
        if line[cmd[1]-1].available == False:
            print(-1)
        else:
            line[cmd[1]-1].declare_breakdown()
            i = cmd[1]%len(line)
            while i != cmd[1]-1:
                l = line[i]
                if l.available:
                    l.get_element(line[cmd[1]-1])
                    break
                i = (i+1)%len(line)
            print(cmd[1])
        # print(time.perf_counter()-s)
        # s = time.perf_counter()
    # if DEBUG:
    #     for i in line:
    #         print(f"{i.id}-, activated:{i.available}-, cmd:{cmd}")
    #         i.debug()
    #         print(i.valid, i.N)
    #     print("================")