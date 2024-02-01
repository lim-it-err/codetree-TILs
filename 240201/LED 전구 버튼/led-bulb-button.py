N, B = map(int, input().split())
data = []
for i in range(N):
    data.append(int(input()))
history = {}
old_data = data.copy()
iterate_idx = 0
T = 0

while iterate_idx != B:
    iterate_idx+=1
    new_data = []
    for i in range(len(old_data)):
        if old_data[(i-1)%len(data)] == 1:
            new_data.append((old_data[i]-1)%2)
        else:
            new_data.append(old_data[i])
    summation = 0
    for i in range(len(old_data)):
        summation += (2**i)*old_data[i]
    try:
        T = iterate_idx - history[summation]
        iterate_idx = (B-iterate_idx)//T * T + iterate_idx
        old_data = new_data[:]
    except KeyError:
        history[summation] = iterate_idx
        old_data = new_data[:]
for i in old_data:
    print(i)