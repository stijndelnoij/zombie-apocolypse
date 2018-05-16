import random
import matplotlib.pyplot as plt
from matplotlib import colors
import math
import numpy as np
import time

def coordinates(direct, xy):
    x = xy[0] 
    y = xy[1]
    if direct == 'u':
        x = x
        y = y + 1

    elif direct == 'd':
        x = x
        y = y - 1

    elif direct == 'l':
        x = x - 1
        y = y

    elif direct == 'r':
        x = x + 1
        y = y
    
    return x, y
    
def zombies(n, p_thres):
    count = 0
    start1 = time.time()
    x0 = random.randint(0, n - 1)
    y0 = random.randint(0, n - 1)
    L_pos = [[0] * (n + 1) for i in range(n + 1)] 
    L_pos[x0][y0] = 1
    xy = tuple([x0, y0])
    L_zomb = [xy]
    for i in range(n):
        L_pos[i][n] = 3

    for i in range(n):
        for j in range(n):
            p = random.random()
            if p < p_thres and L_pos[i][j] == 0:
                L_pos[i][j] = 2
                count = count + 1
        
    end1 = time.time()
    print "Runtime is %f" % (end1 - start1)
    print "Factor mensen is %f" % (count / float(n ** 2))
    return L_pos, L_zomb

def interactie(L_pos, L_zomb, b, k):
    L_add, L_remove = [], []
    events = 0
    for xy in L_zomb:
        x, y = xy
        count = 0
        L_bonds = ['u', 'r', 'd', 'l']
        event = 0
        for direct in L_bonds:
            xnew, ynew = coordinates(direct, xy)
            if L_pos[xnew][ynew] == 2:
                count = count + 1
                
        if count > 0:
            if count == 4:
                L_remove.append(xy)
            while event == 0:
                randir = random.randint(0, len(L_bonds) - 1)
                direct = L_bonds[randir]
                xnew, ynew = coordinates(direct, xy)
                if L_pos[xnew][ynew] == 2:
                    p = random.random()
                    if p < b / float(b + k):
                        L_pos[xnew][ynew] = 1
                        L_add.append((xnew, ynew))

                    else:
                        L_pos[x][y] = 3
                        L_remove.append((x,y))

                    event = 1

                else:
                    L_bonds.remove(direct)
    
    for xy in L_add:
        L_zomb.append(xy)
        events = events + 1

    for xy in L_remove:
        try:
            L_zomb.remove(xy)

        except:
            pass

    return L_pos, L_zomb, events

n = 200
L_pos, L_zomb = zombies(n, 1.)
iterations = 0
events = 1
L_Nzomb, L_t = [], []

while events != 0:
    L_pos, L_zomb, events = interactie(L_pos, L_zomb, 1, 0.2)
    iterations = iterations + 1
    L_Nzomb.append(iterations)

plt.figure(1)
data = np.array(L_pos)
plt.xlim(-0.5, n - 0.5)
plt.ylim(-0.5, n - 0.5)
cmap = colors.ListedColormap(['white', 'red', 'green', 'black'])
plt.imshow(data, interpolation='none', cmap=cmap, origin = 'lower')
plt.show()