import copy
import time
import numpy as np
from queue import PriorityQueue

'''
get starting puzzle matrix from input
'''
def matrixInput():
    blank = -1
    checkPos = 1
    lowerbound = 0
    puzzle = [[0 for i in range(4)] for j in range(4)]
    # fill puzzle matrix
    for i in range(4):
        for j in range(4):
            num = int(input("Enter element (" + str(i) + "," + str(j) + "): "))
            # check for blank tile
            if (num < 1 or num > 15):
                blank = num
            else:
                # check if already in solved position
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
            # fill puzzle matrix
            for num in line.split():
                num = int(num)
                # check for blank tile
                if (num < 1 or num > 15):
                    blank = num
                else:
                    # check if already in solved position
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
    return (res[0][0]), (res[1][0]) # returns x and y position


'''
check reachability using kurang(i) function
'''
def reachable(puzzle, blank, x, y):
    # check if blank tile is in shaded area
    if (((x % 2 == 1) and (y % 2 == 0)) or ((x % 2 == 0) and (y % 2 == 1))):
        kurangx = 1
    else:
        kurangx = 0
    # initialize 1D array of puzzle elements in order
    check = sum(puzzle, [])
    check.remove(blank)
    total = 0
    kurangi = {}
    for row in range(4):
        for col in range(4):
            i = puzzle[row][col]
            if (i == blank):
                i = 16 # convert blank tile value to 16
            else:
                check.remove(i) # remove value from checked
            # get kurang(i)
            kurangsum = sum(j < i for j in check) 
            kurangi[i] = kurangsum
            total += kurangsum
    for i in range(16):
        print("KURANG(%02d): " % (i+1) + str(kurangi[i+1]))
    res = kurangx + total
    print("SUM KURANG(i) + X: " + str(res))
    # check if reachable
    if (res % 2 == 0):
        return True
    else:
        return False


'''
move blank tile in a certain direction by swapping with a target tile
'''
def swap(currnode, dirX, dirY, blank, visited):
    # initialize solved position
    inPos = { 
        1: [0, 0], 2: [0, 1], 3: [0, 2], 4: [0, 3], 5: [1, 0], 
        6: [1, 1], 7: [1, 2], 8: [1, 3], 9: [2, 0], 10: [2, 1], 
        11: [2, 2], 12: [2, 3], 13: [3, 0], 14: [3, 1], 15: [3, 2] 
    }
    node = copy.deepcopy(currnode)
    x, y = getIdx(node, blank)
    swapX = x + dirX
    swapY = y + dirY
    # check if movement is invalid (out of range)
    if (swapX > 3 or swapX < 0 or swapY > 3 or swapY < 0):
        return -1, -1
    pos = inPos[(node[swapX][swapY])]
    # case when target tile is already in solved position
    if (pos[0] == swapX and pos[1] == swapY):
        addCost = 1
    # case when target tile is not in solved position and will be in solved position
    elif (pos[0] == x and pos[1] == y):
        addCost = -1
    # case when target tile is and will not be in solved position
    else:
        addCost = 0

    # swap blank tile with target tile
    temp = node[x][y]
    node[x][y] = node[swapX][swapY]
    node[swapX][swapY] = temp
    
    # ignore node if redundant (already visited)
    if node in visited:
        return -1, -1
    return node, addCost
    

'''
display puzzle matrix
'''
def displayMatrix(nodes, blank):
    count = 0
    for node in nodes:
        # print puzzle state description
        if (count == 0):
            print("INITIAL STATE")
        elif (count == 1):
            print("MOVES TAKEN")
        elif (count == len(nodes) - 1):
            print("FINAL STATE")
        # print movement direction
        print ("DIRECTION: " + node[1])
        # print puzzle
        print("╔═══╦═══╦═══╦═══╗")
        array = node[0] # initialize array
        for i in range(4):
            for j in range(4):
                print("║",end="")
                if (array[i][j] == blank):
                    print("  ", end=" ") # print blank tile as blank (no number)
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
    # initialize movement direction
    dir = { 0: [-1, 0, "UP"], 1: [1, 0, "DOWN"], 2: [0, -1, "LEFT"], 3: [0, 1, "RIGHT"] }

    visited = []
    currpath = [[puzzle, "-"]]
    livenode = PriorityQueue()
    livenode.put([lowerbound, puzzle, lowerbound, 0, currpath]) # add initial puzzle state

    start = time.time()
    while (True):
        # get lowest cost node
        toSearch = livenode.get()
        # initialize node info
        currcost = toSearch[0]
        currnode = toSearch[1]
        currleft = toSearch[2]
        currdepth = toSearch[3]
        currpath = toSearch[4]
        visited.append(currnode)

        # case when all tiles are in solved position
        if (currleft == 0):
            end = time.time()
            displayMatrix(currpath, blank)
            print("Elapsed time: " + str(end - start))
            print("Total step: " + str(currdepth))
            print("Visited nodes: " + str(len(visited) - 1))
            break

        # get nodes for all movement directions
        for i in range(4):
            pos = dir[i]
            nodeDir, addCost = swap(currnode, pos[0], pos[1], blank, visited)
            # case when node is valid (not out of range or visited)
            if (nodeDir != -1):
                costDir = currcost + 1 + addCost # initialize cost
                path = currpath + [[nodeDir, (dir[i])[2]]] # initialize path and movement
                livenode.put([costDir, nodeDir, currleft + addCost, currdepth + 1, path])
