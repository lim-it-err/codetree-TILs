N, B = map(int, input().split())
data = []
for i in range(N):
    data.append(int(input()))
history = {}
def iterate():
    old_data = data.copy()
    iterate_idx = -1
    T = 0
    while True:
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
            return T
        except KeyError:
            history[summation] = iterate_idx
            old_data = new_data[:]


jugi = iterate()
B %= jugi
answer_data = []
old_data = data.copy()
for i in range(B):
    answer_data = []

    for i in range(len(old_data)):
        if old_data[(i-1)%len(old_data)] == 1:
            answer_data.append((old_data[i]-1)%2)
        else:
            answer_data.append(old_data[i])
    old_data = answer_data[:]

for i in answer_data:
    print(i)