x = int(input())
init_data = list(map(int, input().split()))
n, m = init_data[1], init_data[2]
id_convey_dict = {}
conveyid_status_list = [True for i in range(m)]

def get_input(id_list, weight_list):
    convey = [[] for _ in range(m)]
    for i, data in enumerate(id_list):
        convey[i//(n//m)].append((data, weight_list[i]))
        id_convey_dict[data] = i//(n//m)
    return convey


class Santa:
    def __init__(self, init_data):
        self.convey = get_input(init_data[3:3+n], init_data[3+n:])
        self.cur = [0 for _ in range(m)]

    def pop(self, value):
        weight = 0
        for i, convey in enumerate(self.convey):
            if conveyid_status_list[i] == False:
                continue
            if len(convey) == 0:
                continue
            # print(convey)
            idx = self.cur[i] #pointer(현재 위치)
            if convey[idx][1]<=value:
                weight+=convey[idx][1]
                del id_convey_dict[convey[idx][0]]
                del self.convey[i][idx]
                if idx>len(self.convey[i])-1:
                    self.cur[i] = 0
            else:
                self.cur[i] = (self.cur[i]+1)%len(self.convey[i])
        print(weight)

    def remove(self, id):
        if id not in id_convey_dict.keys():
            print(-1)
            return
        convey_idx = id_convey_dict[id]
        for i in range(len(self.convey[convey_idx])):
            if self.convey[convey_idx][i][0] == id:
                del self.convey[convey_idx][i]
                del id_convey_dict[id]
                if i < self.cur[convey_idx]:
                    self.cur[convey_idx] -= 1
                if self.cur[convey_idx]>len(self.convey[convey_idx])-1:
                    self.cur[convey_idx] = 0
                print(id)
                break

    def lookup(self, id):
        if id not in id_convey_dict.keys():
            print(-1)
            return
        convey_idx = id_convey_dict[id]
        for i in range(len(self.convey[convey_idx])):
            if self.convey[convey_idx][i][0] == id:
                self.cur[convey_idx] = i
        print(convey_idx+1)


    def breakdown(self, convey_id):
        to_migrate_id = -1
        if conveyid_status_list[convey_id] == False:
            print(-1)
        else:
            conveyid_status_list[convey_id] = False
            print(convey_id+1)
        for i in range(m):
            if conveyid_status_list[(i+convey_id)%m] == True:
                to_migrate_id = (i+convey_id)%m
                break
        self.convey[to_migrate_id] = self.convey[to_migrate_id][0:self.cur[to_migrate_id]]+self.convey[convey_id]+self.convey[to_migrate_id][self.cur[to_migrate_id]:]
        self.cur[to_migrate_id]+=len(self.convey[convey_id])
        self.cur[to_migrate_id] = self.cur[to_migrate_id]%len(self.convey[to_migrate_id])
        self.convey[convey_id] = []

        for key in id_convey_dict.keys():
            if id_convey_dict[key] == convey_id:
                id_convey_dict[key] = to_migrate_id

    def debug(self, id, i):
        print("=============")
        print(id, i)
        print(self.convey)
        print(self.cur)
        print(id_convey_dict)
        print(conveyid_status_list)
        print("=============")


santa = Santa(init_data)
for i in range(x-1):
    command, value = map(int, input().split())
    if command == 200:
        santa.pop(value)
        # santa.debug(200, i)
    elif command == 300:
        santa.remove(value)
        # santa.debug(300, i)
    elif command == 400:
        santa.lookup(value)
        # santa.debug(400, i)
    elif command == 500:
        santa.breakdown(value-1)
        # santa.debug(500, i)