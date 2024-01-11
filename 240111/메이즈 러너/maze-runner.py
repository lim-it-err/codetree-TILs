DEBUG = False
dxs, dys= [1, -1, 0, 0], [0, 0, 1, -1] #S, N, E, W
n, m, k = map(int, input().split())

field = [list(map(int, input().split())) for _ in range(n)]
users = []
for i in range(m):
    x, y = map(int, input().split())
    users.append((x-1, y-1))
    # field[x-1][y-1] = -1
dst = tuple(map(int, input().split()))
dst = (dst[0]-1, dst[1]-1)
is_valid = lambda x, y : 0 <=x < n and 0<=y<n and field[x][y]==0 if True else False
is_seg_valid = lambda x, y : 0 <= x < n and 0<=y < n if True else False
demask = [False for i in range(m)]
answer = 0

def get_direction(src, dst):
    ret = []
    x, y = src
    nx, ny = dst
    if nx > x:
        ret.append(0) #S
    elif nx < x:
        ret.append(1) #N
    if ny > y:
        ret.append(2) #E
    elif ny < y:
        ret.append(3)
    return ret


def get_smallest_rectangle(srcs, dst):
    x, y = dst
    min_src = []
    dist = 99999
    for i, src in enumerate(srcs):
        if demask[i]:
            continue
        sx, sy = src
        if max(abs(sx-x), abs(sy-y)) < dist:
            min_src = [src]
            dist = max(abs(sx-x), abs(sy-y))
        elif max(abs(sx-x), abs(sy-y)) == dist:
            min_src.append(src)
    for i in range(max(x-dist, 0), x+1):
        for j in range(max(y-dist, 0), y+1):
            if not is_seg_valid(i, j):
                continue
            if not is_seg_valid(i+dist, j+dist):
                continue
            for minsrc in min_src:
                if is_in_rectangle((i, j), minsrc, dist):
                    return (i, j), dist
    print("Unexpected")
    exit()


def is_in_rectangle(rect, src, i):
    x, y = rect
    nx, ny = x+i, y+i
    a, b = src
    if x<=a<=nx and y<=b<=ny:
        return True
    return False

def rotate_field(rect_pos, size):
    new_field = [[0 for _ in range(size+1)] for _ in range(size+1)]
    for i in range(size+1):
        for j in range(size+1):
            # print(i, j, size-j+rect_pos[0], i+rect_pos[1])
            new_field[i][j] = max(field[size-j+rect_pos[0]][i+rect_pos[1]]-1, 0)
    # print("==")
    return new_field



def rotate_pos(rect_pos, pos, size):
    x, y = pos
    x-=rect_pos[0]
    y-= rect_pos[1]
    return (y+rect_pos[0], size-x+rect_pos[1])

for _ in range(k):
    for i, user_pos in enumerate(users):
        if demask[i]:
            continue
        x, y = user_pos
        dir_lst = get_direction(user_pos, dst)
        for _dir in dir_lst:
            nx, ny = x + dxs[_dir], y + dys[_dir]
            if is_valid(nx, ny):
                users[i] = (nx, ny)
                answer+=1
                break
    if DEBUG:
        print("users moved", users, dst)
    for i, user in enumerate(users):
        if demask[i]:
            continue
        if user == dst:
            demask[i] = True
    if DEBUG:
        print("users demasked", demask)
    if all(demask):
        break
    rect_pos, size = get_smallest_rectangle(users, dst)
    if DEBUG:
        print("rectangle are", rect_pos, size)
    new_field = rotate_field(rect_pos, size)
    for i in range(rect_pos[0], rect_pos[0]+size+1):
        for j in range(rect_pos[1], rect_pos[1]+size+1):
            field[i][j] = new_field[i-rect_pos[0]][j-rect_pos[1]]
    if DEBUG:
        print("rotated", field)
    dst = rotate_pos(rect_pos, dst, size)
    for i, user in enumerate(users):
        if demask[i]:
            continue
        if is_in_rectangle(rect_pos, user, size):
            users[i] = rotate_pos(rect_pos, user, size)
    if DEBUG:
        __board = [[0 for _ in range(n)] for _ in range(n)]
        for i, user in enumerate(users):
            if demask[i]:
                continue
            __board[user[0]][user[1]] = i
            __board[dst[0]][dst[1]] = -1

        for i in range(n):
            print("rotated", __board[i])
        print(answer)
        print("===")

print(answer)
print(dst[0]+1, dst[1]+1)