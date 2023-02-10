# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


from random import shuffle, randrange
import sys

#code from https://rosettacode.org/wiki/Maze_generation#Python
def make_maze(w = 10, h = 10):
    sys.setrecursionlimit(5000)
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)
    walk(randrange(w), randrange(h))


    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    f = lambda list: [sublist.split(' ') for sublist in list.split('\n')]
    maze = f(s)
    return s, maze


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    output, maze1 = make_maze()
    print(output)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
