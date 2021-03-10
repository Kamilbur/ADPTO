from itertools import *
from dimacs import *
from copy import deepcopy
import sys


def brute(G):
    E = edgeList(G)
    for k in range(1, len(G)):
        print(k)
        for C in combinations(range(len(G)), k):
            if isVC(E, C):
                return C

def VC_2k(G):
    S = set()
    E = edgeList(G)
    for k in range(1, len(G)):
        print(k)
        S = set()
        S = VC_2k_recursion(E.copy(), k, S)
        if S:
            break
    return S

def VC_2k_recursion(E, k, S):
    # find not covered edge
    free_edge = None
    idx = None
    for i, e in enumerate(E):
        if e[0] not in S and e[1] not in S:
            free_edge = e
            idx = i
            break

    if free_edge is None:
        return S

    if k == 0:
        return None

    E = E[idx:]

    u, v = free_edge
    S1 = VC_2k_recursion(E, k-1, S.union({u}))
    if S1:
        return S1
    S2 = VC_2k_recursion(E, k-1, S.union({v}))

    return S2


def VC_1_6k(G):
    S = set()
    E = edgeList(G)
    for k in range(1, len(G)):
        print(k)
        S = set()
        S = VC_1_6k_recursion(deepcopy(G), k, S)
        if S and isVC(E, S):
            break

    return S


def VC_1_6k_recursion(G, k, S):
    if k < 0:
        return None

    vertex = None
    for u in range(1, len(G)):
        if len(G[u]) > 0: #deg check
            vertex = u
            break

    if vertex == None:  # there are no edges
        return S
    if k == 0:
        return None
    
    # delete choosen vertex
    N = []
    for u in G[vertex].copy():
        N += [(u,vertex)]
        G[u].remove(vertex)
        G[vertex].remove(u)

    
    S1 = VC_1_6k_recursion(G, k-1, S.union({vertex}))
    if S1:
        return S1

    # restore chosen vertex
    for (u,v) in N:
        G[u].add(v)
        G[v].add(u)

    # prepare set S extended by neighbors
    newS = S.copy()

    vertex_neighborhood_size = len(G[vertex])

    for u in G[vertex]:
        newS = newS.union({u})

    N = []
    for u in G[vertex].copy():
        for v in G[u].copy():
            N += [(u,v)]
            G[u].remove(v)
            G[v].remove(u)

    S2 = VC_1_6k_recursion(G, k - vertex_neighborhood_size, newS)

    return S2


def VC_1_4k(G):
    S = set()
    E = edgeList(G)
    for k in range(1, len(G)):
        print(k)
        S = set()
        S = VC_1_4k_recursion(deepcopy(G), k, S)
        if S and isVC(E, S):
            break

    return S


def VC_1_4k_recursion(G, k, S):
#    print(f'rec call {G}     {k}      {S}')
    if k < 0:
        return None

    # vertex with maximal degree
    vertex = max(range(1, len(G)), key=lambda u: len(G[u]))

#    print(f'max vertex {vertex}')

    if len(G[vertex]) == 0:  # there are no edges
        return S

    if len(G[vertex]) <= 2: # polynomial algorithm
        degree = [len(G[u]) for u in range(1, len(G))]
        newS = S.copy()
        E = edgeList(G)
#        print(S)
#        print(E)
        for (u, v) in E:
            if u not in newS and v not in newS:
#                print(f'it is sensible to add {u} or {v}, because newS is {newS}')
                if degree[u] == 1:
#                    print(f'added {v}')
                    newS.add(v)
                    for w in G[v]:
                        degree[w] -= 1
                else:
#                    print(f'added {u}')
                    newS.add(u)
                    for w in G[u]:
                        degree[w] -= 1

        return newS

    if k == 0:
        return None
    
    # delete choosen vertex
    N = []
    for u in G[vertex].copy():
        N += [(u,vertex)]
        G[u].remove(vertex)
        G[vertex].remove(u)

    
    S1 = VC_1_6k_recursion(G, k-1, S.union({vertex}))
    if S1:
        return S1

    # restore chosen vertex
    for (u,v) in N:
        G[u].add(v)
        G[v].add(u)

    # prepare set S extended by neighbors
    newS = S.copy()

    vertex_neighborhood_size = len(G[vertex])

    for u in G[vertex]:
        newS = newS.union({u})

    N = []
    for u in G[vertex].copy():
        for v in G[u].copy():
            N += [(u,v)]
            G[u].remove(v)
            G[v].remove(u)

    S2 = VC_1_6k_recursion(G, k - vertex_neighborhood_size, newS)

    return S2


def input_error():
    warning_text = """Wrong specification: give algorithm name {bf, 2k, 1.6k, 1.4k}:
        bf - bruteforce
        2k - 2^k algorithm
        1.618^k algorithm
        1.47^k algorithm
        and list of files to process"""
    print(warning_text)
    sys.exit(1)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        input_error()

    for i in range(2, len(sys.argv)):
        filename = sys.argv[i]
        print(filename)
        G = loadGraph(filename)
        C = None
        if sys.argv[1] == 'bf':
            C = brute(G)
        elif sys.argv[1] == '2k':
            C = VC_2k(G)
        elif sys.argv[1] == '1.6k':
            C = VC_1_6k(G)
        elif sys.argv[1] == '1.4k':
            C = VC_1_4k(G)
        else:
            input_error()

        print(C)
        saveSolution(filename + '.sol', C)

