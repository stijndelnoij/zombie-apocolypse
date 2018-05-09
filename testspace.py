from scipy import ndimage
import numpy as np

dick = {(1,3):1, (2,4):2, (3,5):3}
for key in dick:
    print key
print (1,3) in dick
L=['a','b','c','d']
L.remove('b')
print '%s' % L
arr=[[2,3],[3,4],[4,5]]
print '%d %d' % (len(arr), len(arr[0]))
k=0
k=k+1
print k

array = np.random.randint(0, 3, size=(200, 200))

label, num_label = ndimage.label(array == 0)
size = np.bincount(label.ravel())
biggest_label = size[1:].argmax() + 1
clump_mask = label == biggest_label