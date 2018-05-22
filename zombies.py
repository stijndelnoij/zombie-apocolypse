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
    
def zombies(n, p_human, p_zombie):
    c = 1 / (p_human + p_zombie)
    p_human = c * p_human
    p_zombie = c * p_zombie
    p_zombie = p_human + p_zombie
    L_zomb = []
    count = -1
    start1 = time.time()
    L_pos = [[0] * (n + 1) for i in range(n + 1)] 
    for i in range(n):
        L_pos[i][n] = 3

    for i in range(n):
        for j in range(n):
            p = random.random()
            if p < p_human:
                L_pos[i][j] = 2
                count = count + 1
            elif p < p_zombie:
                L_pos[i][j] = 1
                L_zomb.append((i, j))
                count = count - 1
            else: L_pos[i][j] = 0

    x0 = random.randint(0, n - 1)
    y0 = random.randint(0, n - 1)
    L_pos[x0][y0] = 1
    xy = (x0, y0)
    L_zomb.append(xy)
        
    end1 = time.time()
    #print "Runtime is %f" % (end1 - start1)
    #print "Factor mensen is %f" % (count / float(n ** 2))
    return L_pos, L_zomb, count

def interactie(L_pos, L_zomb, a, N_human, N_removed, N_zomb):
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
                        N_zomb = N_zomb + 1
                        N_human = N_human - 1

                    else:
                        L_pos[x][y] = 3
                        N_removed = N_removed + 1
                        N_zomb = N_zomb - 1
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

    return L_pos, L_zomb, events, N_human, N_removed, N_zomb

def cluster(L_posfinal):
    percolates = False
    L_arrays = [L_posfinal, [list(x) for x in zip(*L_posfinal)]]
    L_bonds = ['u', 'r', 'd', 'l']
    events = 0
    for L_posfinal in L_arrays:
        n = len(L_posfinal)
        L_cluster, L_tobechecked = [], []
        for y in range(n):
            if L_posfinal[0][y] == 1 and L_posfinal[1][y] == 1:
                L_cluster.append((0, y))
                L_tobechecked.append((0, y))
                events = events + 1

        while events != 0:
            events = 0
            for xy in L_tobechecked:
                for direct in L_bonds:
                    xnew, ynew = coordinates(direct, xy)
                    if L_posfinal[xnew][ynew] == 1 and (xnew, ynew) not in L_cluster:
                        L_cluster.append((xnew, ynew))
                        L_tobechecked.append((xnew, ynew))
                        events = events + 1
            
            L_tobechecked = []

        for y in range(n):
            if (n - 2, y) in L_cluster:
                percolates = True
                break

    return percolates
        
#def rand(L_cluster, L_pos):

n = 1000
a = 0.35
L_pos, L_zomb, N_human = zombies(n, 1., 0)
events = 1
N_zombie = len(L_zomb)
N_removed = 0
L_Nhuman, L_Nremoved, L_Nzombie = [N_human], [N_removed], [N_zombie]
L_t = [0]
t = 0
tijd = 0

# plt.figure(1)
# cmap = colors.ListedColormap(['white', 'red', 'green', 'black'])
while events != 0:
    L_pos, L_zomb, events, N_human, N_removed, N_zombie = interactie(L_pos, L_zomb, a, N_human, N_removed, N_zombie)
    start = time.time()
    L_Nhuman.append(N_human)
    L_Nremoved.append(N_removed)
    L_Nzombie.append(N_zombie)
    end = time.time()
    tijd = tijd + end - start
    if t % 100 == 0:
        print tijd
        tijd = 0

    #print len(L_zomb)
    t = t + 1
    L_t.append(t)
    # plt.clf()
    # plt.xlim(-0.5, n - 0.5)
    # plt.ylim(-0.5, n - 0.5)
    # data = np.array(L_pos)
    # plt.imshow(data, interpolation='none', cmap=cmap, origin = 'lower')
    # plt.draw()
    # plt.pause(0.1)

if cluster(L_pos):
    print 'This cluster of zombies does percolate'


else:
    print 'This cluster of zombies does not percolate'

# def testcritical(a, b, n, iterations):
#     for i in range(iterations):
#         alpha = (a + b) / 2.
#         for j in range(720):
#             L_pos, L_zomb = zombies(n, 1., 0)
#             events = 1
#             while events != 0:
#                 L_pos, L_zomb, events = interactie(L_pos, L_zomb, alpha)

#             if cluster(L_pos):
#                 a = alpha
#                 break

#         if j == 719:
#             b = alpha
    
#     return a, b

# a, b = testcritical(0.3, 0.5, 500, 1)
# print a, b

plt.figure(2)
data = np.array(L_pos)
plt.xlim(-0.5, n - 0.5)
plt.ylim(-0.5, n - 0.5)
cmap = colors.ListedColormap(['white', 'red', 'green', 'black'])
plt.imshow(data, interpolation='none', cmap=cmap, origin = 'lower')
print L_Nzombie[-1] + L_Nremoved[-1] + L_Nhuman[-1]
plt.figure(3)
plt.plot(L_t, L_Nhuman, label = 'human')
plt.plot(L_t, L_Nremoved, label = 'removed')
plt.plot(L_t, L_Nzombie, label = 'zombie')
plt.legend()

# plt.figure(3)
# plt.plot(L_Nzomb, L_t, 'bo')
plt.show()