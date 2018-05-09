import random
import matplotlib.pyplot as plt
from matplotlib import colors
import math
import numpy as np
import time

L_bonds = ['u', 'r', 'd', 'l']

def removekey(d, key):
    r = dict(d)
    del r[key]
    return r

def opposite(direct):
    if direct == 'u':
        opp = 'd'
    
    elif direct == 'd':
        opp = 'u'
    
    elif direct == 'r':
        opp = 'l'
    
    elif direct== 'l':
        opp = 'r'
    
    return opp

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

def randen(dick, xy, n):
    x0 = xy[0]
    y0 = xy[1]
    if y0 == n - 1:
        dick[xy].remove('u')
    
    elif y0 == 0:
        dick[xy].remove('d')
    
    elif x0 == n - 1:
        dick[xy].remove('r')
    
    elif x0 == 0:
        dick[xy].remove('l')

    return dick
    
def zombies(n, p_thres):
    count = 0
    start1 = time.time()
    x0 = random.randint(0, n - 1)
    y0 = random.randint(0, n - 1)
    L_pos = [[0] * (n + 1) for i in range(n + 1)] 
    L_pos[x0][y0] = 1
    xy = tuple([x0, y0])
    L_zomb = [xy]
    dick = {xy:L_bonds}
    dick = randen(dick, xy, n)
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
    return L_pos, L_zomb, dick

def interactie(L_pos, L_zomb, dick, b, k):
    L_add, L_delete, L_remove = [], [], []
    for xy in dick:
        x = xy[0]
        y = xy[1]
        #print dick[xy]
        for direct in dick[xy]:
            L_dir = ['u', 'd', 'l', 'r']
            p = random.random()
            xnew, ynew = coordinates(direct, xy)
            #print direct
            if b / float(b + k) > p and xnew < len(L_pos[0]) and ynew < len(L_pos):
                L_pos[xnew][ynew] = 1
                L_remove.append((xy, direct))
                L_dir.remove(opposite(direct))
                L_add.append((xnew, ynew, L_dir))
            
            elif k / float(b + k) > p:
                L_pos[x][y] = 3
                L_delete.append(xy)
                break

    for newzomb in L_add:
        xnew, ynew, L_dir = newzomb
        dick[(xnew, ynew)] = L_dir
    #print L_delete
    for zomb in L_remove:
        xy, direct = zomb
        dick[xy].remove(direct)
    for xy in L_delete:
        #print dick
        dick = removekey(dick, xy)
        for direct in L_bonds:
            xnew, ynew = coordinates(direct, xy)
            if (xnew, ynew) in dick:
                L = dick[(xnew, ynew)]

                try:
                    L.remove(opposite(direct))
                    dick[(xnew, ynew)] = L

                except:
                    b = 1

                

    return L_pos, L_zomb, dick

n = 200
L_pos, L_zomb, dick = zombies(n, 1.)
#print "%s" % len(L_pos[1])
data = np.array(L_pos)
plt.figure(1)
plt.xlim(-0.5, n - 0.5)
plt.ylim(-0.5, n - 0.5)
cmap = colors.ListedColormap(['white', 'red', 'green', 'black'])
plt.imshow(data, interpolation='none', cmap=cmap, origin = 'lower')
plt.figure(2)
for i in range(100):
    L_pos, L_zomb, dick = interactie(L_pos, L_zomb, dick, 1, 0.43)

data = np.array(L_pos)
plt.xlim(-0.5, n - 0.5)
plt.ylim(-0.5, n - 0.5)
cmap = colors.ListedColormap(['black','red','green', 'white'])
plt.imshow(data, interpolation='none', cmap=cmap, origin = 'lower')
plt.show()