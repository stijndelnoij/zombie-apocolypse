import random
import matplotlib.pyplot as plt
from matplotlib import colors
import math
import numpy as np
import time

L_bonds = ['u', 'd', 'l', 'r']

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
    L_pos = [[0] * n for i in range(n)] 
    L_pos[x0][y0] = 1
    xy = tuple([x0, y0])
    L_zomb = [xy]
    dick = {xy:L_bonds}
    dick = randen(dick, xy, n)
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
    for xy in L_zomb:
        x = xy[0]
        y = xy[1]
        for direct in dick[xy]:
            p = random.random()
            if b / float(b + k) > p:
                if direct == 'u':
                    L_pos[x][y+1] = 2
                    dick[(x,y)].remove('u')
                    dick[(x,y+1)]=['d','l','r']
                elif direct == 'd':
                    L_pos[x][y-1] = 2
                    dick[(x,y)].remove('d')
                    dick[()]

L_pos, L_zomb, dick = zombies(200, 0.5)
data = np.array(L_pos)
cmap = colors.ListedColormap(['black','red','green'])
plt.imshow(data, interpolation='none', cmap=cmap, origin = 'lower')
plt.show()