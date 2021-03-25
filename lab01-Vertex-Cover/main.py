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

    # Max degree vertex
    vertex = None
    for u in range(1, len(G)):
        if len(G[u]) > 0:
            vertex = u
            break

    if vertex is None:
        return S
    if k == 0:
        return None

    # delete choosen vertex
    N = []
    for u in G[vertex].copy():
        N += [(u, vertex)]
        G[u].remove(vertex)
        G[vertex].remove(u)

    S1 = VC_1_6k_recursion(G, k-1, S.union({vertex}))
    if S1:
        return S1

    # restore chosen vertex
    for (u, v) in N:
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
            N += [(u, v)]
            G[u].remove(v)
            G[v].remove(u)

    S2 = VC_1_6k_recursion(G, k - vertex_neighborhood_size, newS)

    # restore chosen vertex
    for (u, v) in N:
        G[u].add(v)
        G[v].add(u)

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
    if k < 0:
        return None

    # vertex with maximal degree
    vertex = max(range(1, len(G)), key=lambda u: len(G[u]))

    if len(G[vertex]) == 0:  # There are no edges
        return S

    if len(G[vertex]) <= 2:  # Polynomial algorithm
        degree = [0] + [len(G[u]) for u in range(1, len(G))]

        new_S = S.copy()

        while 1 in degree or 2 in degree:
            try:
                u = degree.index(1)
                for v in G[u]:
                    for w in G[v]:
                        degree[w] -= 1
                    new_S.add(v)
                    degree[v] = 0
                degree[u] = 0
            except Exception as ignored:
                u = degree.index(2)
                new_S.add(u)
                for w in G[u]:
                    degree[w] -= 1
                degree[u] = 0

        return new_S

    if k == 0:
        return None

    # delete choosen vertex
    N = []
    for u in G[vertex].copy():
        N += [(u, vertex)]
        G[u].remove(vertex)
        G[vertex].remove(u)

    S1 = VC_1_4k_recursion(G, k-1, S.union({vertex}))
    if S1:
        return S1

    # restore chosen vertex
    for (u, v) in N:
        G[u].add(v)
        G[v].add(u)

    # prepare set S extended by neighbors
    new_S = S.copy()

    vertex_neighborhood_size = len(G[vertex])

    for u in G[vertex]:
        new_S = new_S.union({u})

    N = []
    for u in G[vertex].copy():
        for v in G[u].copy():
            N += [(u, v)]
            G[u].remove(v)
            G[v].remove(u)

    S2 = VC_1_4k_recursion(G, k - vertex_neighborhood_size, new_S)

    for (u, v) in N:
        G[u].add(v)
        G[v].add(u)

    return S2


def VC_kernelization(G):
    min_k = len(approx(G)) // 2
    S = set()
    E = edgeList(G)
    for k in range(min_k, len(G)):
        print(k)
        S = set()
        S, H, new_k = kernelize(G, k)
        print('kernelization done')

        H_E = edgeList(H)

        if len(H_E) > new_k * new_k:
            continue

        S = VC_1_4k_recursion(H, new_k, S)

        if S and isVC(E, S):
            break

    return S


def kernelize(G, k):
    H = deepcopy(G)
    degree = [0] + [len(G[u]) for u in range(1, len(G))]

    new_k = k

    S = set()
    vertices_alive = set(filter(lambda key: degree[key], range(1, len(G))))
    new_alive = vertices_alive
    not_kernelized = True
    while not_kernelized and new_k >= 0:
        not_kernelized = False
        vertices_alive = new_alive
        new_alive = vertices_alive.copy()
        for v in vertices_alive:
            if new_k <= 0 and max(degree) >= 0:
                return S, H, new_k
            if degree[v] == 1:
                u = H[v].pop()
                new_k -= 1
                S.add(u)
                for w in H[u]:
                    if w != v:
                        H[w].remove(u)
                    degree[w] -= 1
                    if degree[w] == 0:
                        new_alive.remove(w)
                H[u] = set()
                degree[v] = 0
                if v in new_alive:
                    new_alive.remove(v)
                degree[u] = 0
                if u in new_alive:
                    new_alive.remove(u)
                not_kernelized = True
            elif degree[v] > new_k:
                new_k -= 1
                for u in H[v]:
                    H[u].remove(v)
                    degree[u] -= 1
                    if degree[u] == 0:
                        new_alive.remove(u)
                H[v] = set()
                degree[v] = 0
                if v in new_alive:
                    new_alive.remove(v)
                not_kernelized = True
    return S, H, new_k


def approx(G):
    """ Simple approx using 2-approx and logn-approx
    """

    H = deepcopy(G)
    S1 = set()
    E = edgeList(H)

    for (u, v) in E:
        if u not in S1 and v not in S1:
            S1.add(u)
            S1.add(v)

    degree = [len(G[u]) for u in range(len(H))]

    S2 = set()

    while sum(degree) > 0:
        u = max(range(1, len(H)), key=lambda v: degree[v])
        S2.add(u)
        for v in H[u].copy():
            degree[v] -= 1
            H[u].remove(v)
            H[v].remove(u)
        degree[u] = 0

    return S1 if len(S1) < len(S2) else S2


def input_error():
    warning_text = """Wrong specification: give algorithm name:
        bf - bruteforce
        2k - 2^k algorithm
        1.6k - 1.618^k algorithm
        1.4k - 1.47^k algorithm
        appr - approximation algorithm
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
        elif sys.argv[1] == 'kern':
            C = VC_kernelization(G)
        elif sys.argv[1] == 'appr':
            C = approx(G)
        else:
            input_error()

        print(C)
        saveSolution(filename + '.sol', C)
