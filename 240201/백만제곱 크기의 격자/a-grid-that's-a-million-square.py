N = int(input())
is_valid = lambda x, y: 0<=x<N and 0<=y<N
history_dict = {}
input_dict = {}
dxs, dys = [0, 0, 1, -1], [1, -1, 0, 0]
MIN_x, MIN_y, MAX_x, MAX_y = 1e9, 1e9, -1, -1
for i in range(N):
    x, y = map(int, input().split())
    input_dict[(x, y)] = True
    MIN_x, MIN_y = min(x, MIN_x), min(y, MIN_y)
    MAX_x, MAX_y = max(x, MAX_x), max(y, MAX_y)
    for dx, dy in zip(dxs, dys):
        try:
            history_dict[(x+dx, y+dy)]+=1
        except KeyError:
            history_dict[(x+dx, y+dy)] = 1
def three():
    return list(history_dict.values()).count(3)*3

def four_with_no_area():
    ret = 0
    for key in history_dict.keys():
        try:
            if (history_dict[key] == 4 and input_dict[key] == True):
                pass
        except KeyError:
            ret +=1

    return ret*4
# print(four_with_no_area() + three()+2*(MAX_x-MIN_x+1)+2*(MAX_y-MIN_y+1))
# print(four_with_no_area())
# print(three())
print(2*(MAX_x-MIN_x+1)+2*(MAX_y-MIN_y+1))