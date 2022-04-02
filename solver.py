from audioop import tostereo
from platform import node
from queue import PriorityQueue
import numpy as np
import copy
import time

'''
get starting puzzle matrix from input
'''
def matrixInput():
    blank = -1
    checkPos = 1
    lowerbound = 0
    puzzle = [[0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            num = int(input("Enter element (" + str(i) + "," + str(j) + "): "))
            if (num < 1 or num > 15):
                blank = num
            else:
                if (num != checkPos):
                    lowerbound += 1
            checkPos += 1
            puzzle[i][j] = num
    return puzzle, blank, lowerbound


'''
get starting puzzle matrix from file
'''
def matrixFile(filename):
    puzzle = []
    blank = -1
    checkPos = 1
    lowerbound = 0
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            temp = []
            for num in line.split():
                num = int(num)
                if (num < 1 or num > 15):
                    blank = num
                else:
                    if (num != checkPos):
                        lowerbound += 1
                temp.append(num)
                checkPos += 1
            puzzle.append(temp)
        f.close()
    return puzzle, blank, lowerbound


'''
get element index
'''
def getIdx(puzzle, val):
    temp = np.array(puzzle)
    res = np.where(temp == val)
    return (res[0][0]), (res[1][0])


'''
check reachability using kurang(i) function
'''
def reachable(puzzle, blank, x, y):
    if (((x % 2 == 1) and (y % 2 == 0)) or ((x % 2 == 0) and (y % 2 == 1))):
        kurangx = 1
    else:
        kurangx = 0
    temp = sum(puzzle, [])
    temp.remove(blank)
    total = 0
    kurangi = {}
    for row in range(4):
        for col in range(4):
            i = puzzle[row][col]
            if (i == blank):
                i = 16
            else:
                temp.remove(i)
            kurangsum = sum(j < i for j in temp)
            kurangi[i] = kurangsum
            total += kurangsum
    for i in range(16):
        print("KURANG(%02d): " % (i+1) + str(kurangi[i+1]))
    res = kurangx + total
    print("SUM KURANG(i) + X: " + str(res))
    if (res % 2 == 0):
        return True
    else:
        return False


'''
count non-blank tiles not in expected position
'''
def notInPos(node, blank):
    count = 0
    check = 1
    for i in range(4):
        for j in range(4):
            if (node[i][j] != check and node[i][j] != blank):
                count += 1
            check += 1
    return count


def swap(currnode, dirX, dirY, blank, visited):
    node = copy.deepcopy(currnode)
    x, y = getIdx(node, blank)
    swapX = x + dirX
    swapY = y + dirY
    if (swapX > 3 or swapX < 0 or swapY > 3 or swapY < 0):
        return -1, -1
    pos = inPos[(node[swapX][swapY])]
    if (pos[0] == swapX and pos[1] == swapY):
        addCost = 1
    elif (pos[0] == x and pos[1] == y):
        addCost = -1
    else:
        addCost = 0

    temp = node[x][y]
    node[x][y] = node[swapX][swapY]
    node[swapX][swapY] = temp
    
    if node in visited:
        return -1, -1

    return node, addCost
    

inPos = {
    1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [1, 0], 6: [1, 1], 7: [1, 2], 8: [1, 3],
    9: [2, 0], 10: [2, 1], 11: [2, 2], 12: [2, 3], 13: [3, 0], 14: [3, 1], 15: [3, 2]
}

def displayMatrix(nodes, blank):
    count = 0
    for node in nodes:
        array = node[0]
        if (count == 0):
            print("INITIAL STATE")
        elif (count == 1):
            print("MOVES TAKEN")
        elif (count == len(nodes) - 1):
            print("FINAL STATE")
        print ("DIRECTION: " + node[1])
        print("╔═══╦═══╦═══╦═══╗")
        for i in range(4):
            for j in range(4):
                print("║",end="")
                if (array[i][j] == blank):
                    print("  ", end=" ")
                else:
                    print("%02d" % (array[i][j]), end=" ")
            print("║")
            if(i != 3):
                print("╠═══╬═══╬═══╬═══╣")
        print("╚═══╩═══╩═══╩═══╝\n")
        count += 1

'''
branch and bound search
'''
def search(puzzle, blank, lowerbound):
    dir = { 0: [-1, 0, "UP"], 1: [1, 0, "DOWN"], 2: [0, -1, "LEFT"], 3: [0, 1, "RIGHT"] }
    countnode = 0
    visited = []
    curpath = [[puzzle, "-"]]
    livenode = PriorityQueue()
    livenode.put([lowerbound, puzzle, lowerbound, 0, curpath])

    start = time.time()
    while (True):
        toSearch = livenode.get()
        currcost = toSearch[0]
        currnode = toSearch[1]
        currleft = toSearch[2]
        currdepth = toSearch[3]
        curpath = toSearch[4]
        visited.append(currnode)

        if (currleft == 0):
            end = time.time()
            displayMatrix(curpath, blank)
            print("Elapsed time: " + str(end - start))
            print("Total step: " + str(currdepth))
            print("Visited nodes: " + str(countnode))
            break

        # get available moves
        for i in range(4):
            pos = dir[i]
            nodeDir, addCost = swap(currnode, pos[0], pos[1], blank, visited)
            if (nodeDir != -1):
                costDir = currcost + 1 + addCost
                temp = copy.deepcopy(curpath)
                temp.append([nodeDir, (dir[i])[2]])
                livenode.put([costDir, nodeDir, currleft + addCost, currdepth + 1, temp])
        
        countnode += 1

