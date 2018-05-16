import random
import matplotlib.pyplot as plt
from matplotlib import colors
import math
import numpy as np
import time

def coordinates(direct, xy): # coordinaten transformatie
    x = xy[0] 
    y = xy[1]
    dick = {'u':[x, y + 1], 'd':[x, y - 1], 'l':[x - 1, y], 'r':[x + 1, y]}
    templist = dick[direct]

    return templist[0], templist[1]
    
def zombies(n, p_human):
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
            if p < p_human and L_pos[i][j] == 0:
                L_pos[i][j] = 2
                count = count + 1
        
    end1 = time.time()
    print "Runtime is %f" % (end1 - start1)
    print "Factor mensen is %f" % (count / float(n ** 2))
    return L_pos, L_zomb

def interactie(L_pos, L_zomb, a):
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
            while event == 0:
                randir = random.randint(0, len(L_bonds) - 1)
                direct = L_bonds[randir]
                xnew, ynew = coordinates(direct, xy)
                if L_pos[xnew][ynew] == 2:
                    p = random.random()
                    if p < 1 / float(1 + a):
                        L_pos[xnew][ynew] = 1
                        L_add.append((xnew, ynew))

                    else:
                        L_pos[x][y] = 3
                        L_remove.append((x,y))

                    event = 1

                else:
                    L_bonds.remove(direct)
        else:
            L_remove.append(xy)
    
    for xy in L_add:
        L_zomb.append(xy)
        events = events + 1

    for xy in L_remove:
        try:
            L_zomb.remove(xy)
            events = events + 1

        except:
            pass

    return L_pos, L_zomb, events

n = 200
L_pos, L_zomb = zombies(n, 1.)
iterations = 0
events = 1
L_Nzomb, L_t = [], []

while events != 0:
    start = time.time()
    L_pos, L_zomb, events = interactie(L_pos, L_zomb, 0.4373)
    end = time.time()
    iterations = iterations + 1
    dt = end - start
    L_t.append(dt)
    L_Nzomb.append(len(L_zomb))

plt.figure(1)
data = np.array(L_pos)
plt.xlim(-0.5, n - 0.5)
plt.ylim(-0.5, n - 0.5)
cmap = colors.ListedColormap(['white', 'red', 'green', 'black'])
plt.imshow(data, interpolation='none', cmap=cmap, origin = 'lower')
plt.figure(2)
plt.plot(L_Nzomb, L_t)
plt.show()