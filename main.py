with open("00-example.txt") as f:
    lines = f.read().splitlines()

C, R, S = map(int,lines[0].split())
sneake_len = list(map(int,lines[1].split()))

matrix = [[0 for _ in range(C)] for _ in range(R)]

for i in range(R):
    matrix[i] = list(lines[i+2].split())

print(matrix)


output = ""
with open("output.txt","w") as f:
    f.write(output)
