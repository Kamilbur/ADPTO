import annealing
import random
import sys

print(annealing.AnnealError)

# Graph
G = [set() for i in range(10)]

G[1].add(2)
G[2].add(1)

print(G)

x = annealing.simulate(G)

print(x)

# -1 due to the reference holding by getrefcount during getting refcount
print(f'x ref count: {sys.getrefcount(x) - 1}')
print(f'G ref count: {sys.getrefcount(G) - 1}')

