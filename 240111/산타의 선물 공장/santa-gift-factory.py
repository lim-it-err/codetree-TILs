### 문제 분석
#10억개의 상자 및 무게 범위를 다루어야 하기 때문에, O(1) 내지 O(logn) 수준으로 Time Complexity를 다루어야 함.

# 1. 번호는 상자마다 다르지만, 무게는 동일할 수 있다. -> id를 기반으로 자료 구조 구성
# 2. 물건 하차 -> seek 함수 구현하라 : O(1))
# 3. 물건 제거 -> remove 함수 구현하라, 리스트로 구현 시 O(n)
# 키 값을 들고 있는 dictionary를 다루자. hash[id] = (belt)
# 4. 물건 확인 -> lseek 함수 구현하라: O(n)
# 위치 또한 알아야 하기 때문에, hash[id] = (belt, cur)로 사전 구조를 변형.
# 5. 벨트 고장 -> 재배치. 기존에 구현한 add 함수를 재활용한다 (최대 호출 10회)
# 벨트의 위치 및 cur가 변형됨. 순서가 보장되기 때문에, 링크드 리스트로 구현하자.
# Dictionary 참조를 위해, belt의 리디렉션을 표기할 table 하나 필요.
# Circular Linked List로 구현.
DEBUG = False # Debug Mode
from typing import List
class Node:
    def __init__(self, iid, weight, prv = None,  nxt = None):
        self.iid = iid
        self.weight = weight
        self.nxt = nxt
        self.prv = prv

class Pipeline:
    def __init__(self, pipeline_iid):
        self.len = 0
        self.iid = pipeline_iid
        self.head_node = None

    def add(self, presents_id:List, weights:List):
        """
        Do not need to be worried about Time Complexity. Will be called in 11 times.
        """
        if not self.head_node:
            self.head_node = Node(presents_id[0], weights[0], None,None)
            presents_id, weights = presents_id[1:], weights[1:]
            self.len +=1
            self.head_node.prv = self.head_node
            self.head_node.nxt = self.head_node

        lst_node = self.head_node.prv
        for present_id, weight in zip(presents_id, weights):
            new_node = Node(present_id, weight, lst_node, None)
            lst_node.nxt = new_node

            lst_node = lst_node.nxt
            self.len+=1
        lst_node.nxt = self.head_node
        self.head_node.prv = lst_node

    def lseek(self):
        self.head_node = self.head_node.nxt


    def pop(self):
        """
        delete it's element
        """
        prv_node = self.head_node.prv
        nxt_node = self.head_node.nxt
        prv_node.nxt = nxt_node
        nxt_node.prv = prv_node
        self.head_node = nxt_node
        self.len-=1

    def lseek_by_value(self, iid):
        cur = self.head_node
        while True:
            if cur.iid == iid:
                break
            cur = cur.nxt
            if cur == self.head_node:
                raise Exception("Unexpected--4")
        self.head_node = cur

    def peek(self):
        return self.head_node.iid, self.head_node.weight

    def peek_all(self):
        ids, weights = [], []
        cur = self.head_node
        while self.len!=0:
            ids.append(cur.iid)
            weights.append(cur.weight)
            cur = cur.nxt
            self.len-=1
        return ids, weights

    def delete(self, present_iid):
        cur = self.head_node
        while True:
            if cur.iid == present_iid:
                prv_node = cur.prv
                nxt_node = cur.nxt
                prv_node.nxt = nxt_node
                nxt_node.prv = prv_node
                self.len-=1
                return True
            cur = cur.nxt
            if cur == self.head_node:
                raise Exception("Unexpected-5")


    def debug(self):
        if DEBUG:
            print(f"pipeline {self.iid} has following. with len {self.len}")
            cur_node = self.head_node
            for i in range(self.len):
                print(f"{i}'s item : {cur_node.iid}, {cur_node.weight}")
                cur_node = cur_node.nxt
            print("====================")

class Worker:
    def __init__(self, present_num, belt_num):
        self.pipelines = self._construct_pipeline(belt_num)
        self.present_dict = {}
        self.pipelines_status = [i for i in range(belt_num)]
        self.pipeline_num = len(self.pipelines)


    def _construct_pipeline(self, n) ->List[Pipeline]:
        return [Pipeline(i) for i in range(n)]

    def allocate(self, present):
        id_list, weight_list = present[:len(present)//2], present[len(present)//2:]
        present_per_belt = len(id_list) // len(self.pipelines)
        for i in range(self.pipeline_num):
            self.pipelines[i].add(
                id_list[i*present_per_belt:(i+1)*(present_per_belt)],
                weight_list[i*present_per_belt:(i+1)*(present_per_belt)]
            )
            for k in range(i*present_per_belt, (i+1)*(present_per_belt)):
                self.present_dict[id_list[k]] = i

    def seek(self, w_max):
        weight_sum= 0
        for i in range(self.pipeline_num):
            if self.pipelines_status[i] != i: # Broken
                continue

            cur_iid, cur_weight =  self.pipelines[i].peek()
            if cur_weight <= w_max:
                self.pipelines[i].pop()
                del self.present_dict[cur_iid]
                weight_sum += cur_weight
            else:
                self.pipelines[i].lseek()

        return weight_sum

    def delete(self, iid):
        try:
            pipeline_id = self.present_dict[iid]
            self.pipelines[pipeline_id].delete(iid)
            del self.present_dict[iid]
            return iid
        except KeyError:
            return -1
        except:
            raise Exception("Unexpected")

    def lookup(self, iid):
        try:
            pipeline_id = self.present_dict[iid]
            self.pipelines[pipeline_id].lseek_by_value(iid)

            return self.pipelines_status[pipeline_id] + 1
        except KeyError:
            return -1
        except:
            raise Exception("Unexpected-3")

    def breakdown(self, pipeline_iid):
        pipeline_iid-=1
        target_iid = -1
        if self.pipelines_status[pipeline_iid] != pipeline_iid:
            return -1
        for i in range(1, self.pipeline_num):
            if self.pipelines_status[(pipeline_iid +i)%self.pipeline_num] == (pipeline_iid +i)%self.pipeline_num:
                target_iid = (pipeline_iid +i)%self.pipeline_num
                break
        for i in range(self.pipeline_num):
            if self.pipelines_status[i] == pipeline_iid:
                self.pipelines_status[i] = target_iid
        ids, weights = self.pipelines[pipeline_iid].peek_all()
        self.pipelines[target_iid].add(ids, weights)
        return pipeline_iid+1

class Master:
    def __init__(self, present_num, belt_num, ):
        self.worker = Worker(present_num, belt_num)
        self.belt_num = belt_num
    def add(self, present):
        self.worker.allocate(present)

    def parse_command(self, command: List):
        typ, info = command[0], command[1:]
        if typ == 200:
            print(self.worker.seek(info[0]))
        elif typ == 300:
            print(self.worker.delete(info[0]))
        elif typ == 400:
            print(self.worker.lookup(info[0]))
        elif typ == 500:
            print(self.worker.breakdown(info[0]))
        if DEBUG:
            for i in range(self.belt_num):
                self.worker.pipelines[i].debug()
            print(f"{command} has been finished.[======")

n = int(input())
init_info = list(map(int, input().split()))
m, k, present = init_info[1], init_info[2], init_info[3:]
master= Master(m, k)
master.add(present)
for i in range(n-1):
    master.parse_command(list(map(int, input().split())))