import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.table import Table

def chessTab(data, base=['pink', 'grey']):
    fig, ax = plt.subplots()
    ax.set_axis_off()
    tb = Table(ax, bbox=[0,0,1,1])
    nrows, ncols = data.shape
    w, h = 1.0 / ncols, 1.0 / nrows
    for (i,j), val in np.ndenumerate(data):

        if val == "Q":
            tb.add_cell(i, j, w, h, text= val,
                        loc='center', facecolor='orange')
            continue
        idx = [j % 2, (j + 1) % 2][i % 2]
        color = base[idx]

        tb.add_cell(i, j, w, h, text=val,
                    loc='center', facecolor=color)
    for i, label in enumerate(data.index):
        tb.add_cell(i, -1, w, h, text=label, loc='right',
                    edgecolor='none', facecolor='none')
    for j, label in enumerate(data.columns):
        tb.add_cell(-1, j, w, h/2, text=label, loc='center',
                    edgecolor='none', facecolor='none')
    ax.add_table(tb)
    return fig


class Chess:
    def __init__(self):
        self.Chess = []
    def setup(self, u):
        self.Chess = u
    def initQueen(self):
        pos = []
        for row,value in enumerate(self.Chess):
            for col, item in enumerate(value):
                if self.Chess[int(row)][int(col)] == "Q":
                    pos.append((row+1,col+1))
        return (sorted(pos, key= lambda k: k[1]))
    def HCost(self):
        Qset = self.initQueen()
        HBoard = []
        for x in range(1, 9):
            HList = []
            for y in range(1,9):
                temp = Qset.copy()
                temp.remove(Qset[y-1])
                temp.append((x, y))
                temp = sorted(temp, key= lambda k: k[1])
                h = 0
                for c1, Qattack in enumerate(temp):
                    for c2 in range(0,8):
                        Qattacked = temp[c2]
                        (rStart, cStart) = Qattack
                        (rEnd, cEnd) = Qattacked
                        if c1 < c2:
                            if (rStart == rEnd or abs(int(rStart) - int(rEnd)) == abs(int(cStart) - int(cEnd))):
                                h += 1
                HList.append(h)
            HBoard.append(HList)
        for rIdx, row in enumerate(HBoard):
            rIdx += 1
            for iIdx, col in enumerate(row):
                iIdx += 1
                if (rIdx, iIdx) in Qset:
                    HBoard[rIdx-1][iIdx-1] = "Q"
        string = ""
        for i in HBoard:
            for j in i:
                string += str(j) + " "
            string += "\n"
        string = string.rstrip("\n")
        return(string)
g = Chess()
matrix = []
op = []
f = open("board.txt", "r")
for i in f:
    j = [it for it in i.strip().split(' ')]
    matrix.append(j)
f.close()
g.setup(matrix)
print(g.HCost())
f = open("result.txt", "w")
for item in g.HCost():
    f.write(str(item))
f = open("result.txt", "r")
for i in f:
    j = [it for it in i.strip().split(' ')]
    op.append(j)
op2 = np.reshape(op, (-1, 8))
frame = pd.DataFrame(op2, columns=['1', '2', '3', '4', '5' , '6', '7', '8'])
chessTab(frame)
plt.show()

