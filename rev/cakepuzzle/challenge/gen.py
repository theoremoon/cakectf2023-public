import random
import os

puzzle = list(range(16))

puzzle = [
    [ puzzle[0],  puzzle[1], puzzle[2], puzzle[3]],
    [ puzzle[4],  puzzle[5], puzzle[6], puzzle[7]],
    [ puzzle[8],  puzzle[9], puzzle[10], puzzle[11]],
    [ puzzle[12],  puzzle[13], puzzle[14], puzzle[15]],
]

colors = [ 40, 41, 42, 43, 44, 45, 46, 47, 100, 101, 102, 103, 104, 105, 106, 107]

def show():
    for i in range(4):
        for j in range(4):
            print("\x1b[0;{}m{:2d}\x1b[0m".format(colors[puzzle[i][j]], puzzle[i][j]), end="")
        print("")
    print("")




def do(q):
    x, y = None, None
    for i in range(4):
        for j in range(4):
            if puzzle[i][j] == 0:
                x, y = j, i

    if q == "U":
        if y == 0:
            return False
        puzzle[y][x], puzzle[y-1][x] = puzzle[y-1][x], puzzle[y][x]

    elif q == "D":
        if y == 3:
            return False
        puzzle[y][x], puzzle[y+1][x] = puzzle[y+1][x], puzzle[y][x]

    elif q == "L":
        if x == 0:
            return False
        puzzle[y][x], puzzle[y][x-1] = puzzle[y][x-1], puzzle[y][x]

    elif q == "R":
        if x == 3:
            return False

        puzzle[y][x], puzzle[y][x+1] = puzzle[y][x+1], puzzle[y][x]
    else:
        assert False

    return True

queries = []

while len(queries) != 100000:
    q = random.choice("UDLR")
    ok = do(q)
    if ok:
        queries.append(q)

rev = {"U": "D", "D": "U", "L": "R", "R": "L"}
ans = []
for q in queries[::-1]:
    # do(rev[q])
    ans.append(rev[q])


seq = [0] + list(sorted(random.randrange(1, 2**31) for _ in range(15)))
# seq = list(range(16))

s = "{"
for i in range(4):
    s += "{"
    for j in range(4):
        s += str(seq[puzzle[i][j]])
        s += ","

    s += "},"
s += "}"

with open("main.c.template", "r") as f:
    template = f.read()

with open("main.c", "w") as f:
    f.write(template.replace("__TEMPLATE__", s))

os.system("gcc main.c -o chal")

with open("ans.txt", "w") as f:
    f.write("\n".join(ans) +"\n")
