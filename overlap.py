import io
f = io.open('test1.json', 'r')
lines = f.readlines()
for i in range(0, len(lines) - 1):
    for j in range(i + 1, len(lines)):
        if lines[i] == lines[j]:
            print('overlaped')