import numpy as np

totSum = np.load('totsum.npy')
highSum = np.load('highsum.npy')

print(totSum)
print(highSum)
print(np.argmin(totSum))
print(np.argmin(highSum))


print(np.where(highSum == np.amin(highSum)))
print(np.amin(highSum))
print(highSum[np.where(highSum == np.amin(highSum))])
