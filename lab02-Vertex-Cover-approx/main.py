""" Author: Kamil Burkiewicz 2021

    Vertex Cover approximations

"""

import sys
import math
from copy import deepcopy
from multiprocessing import Pool
import numpy as np
from dimacs import edgeList, loadGraph, saveSolution


def VC_two_approx(G):
    """ 2-approx algorithm

    For every not covered edge take its two ends.
    """

    S = set()
    E = edgeList(G)

    for (u, v) in E:
        if u not in S and v not in S:
            S.add(u)
            S.add(v)

    return S


def VC_logn_approx(G):
    """ logn-approx algorithm

    Take max degree vertex to a cover and remove it.
    """

    H = deepcopy(G)
    S = set()

    last_max_bucket = 0
    vertices_by_deg = [[] for v in range(0, len(H) - 1)]

    for v in range(len(G)):
        if last_max_bucket < len(H[v]):
            last_max_bucket = len(H[v])
        vertices_by_deg[len(H[v])] += [v]

    while len(vertices_by_deg[0]) < len(H):
        idx = last_max_bucket
        while len(vertices_by_deg[idx]) == 0:
            idx -= 1
        last_max_bucket = idx
        u = vertices_by_deg[idx][-1]
        vertices_by_deg[idx].remove(u)

        S.add(u)
        for v in H[u].copy():
            vertices_by_deg[len(H[v])].remove(v)
            H[v].remove(u)
            vertices_by_deg[len(H[v])].append(v)
        H[u] = set()
        vertices_by_deg[0].append(u)

    return S


def VC_annealing(G):
    """ Simulated annealing optimization

    Simulated annealing algorithm for minimal Vertex Cover.
    """

    S = [0] + [1] * (len(G) - 1)
    iterations = 1000 * 1000
    E = edgeList(G)
    degree = [0] + [len(G[u]) for u in range(1, len(G))]

    def prob(deg, temperature):
        return math.exp(- deg / temperature)

    log_threshold = iterations // 10
    for k in range(1, iterations):

        if k % log_threshold == 0:
            print(k)
        temperature = iterations - k

        nonzero_idxs, = np.nonzero(S)

        # Take random vertex from S
        v = np.random.choice(nonzero_idxs, size=1)[0]

        # Remove vertex from S
        S[v] = 0

        is_vc = True
        for u in G[v]:
            if S[u] != 0:
                is_vc = False
                break

        probabl = prob(degree[v] / len(E), temperature)
        rand = np.random.uniform(0, 1)

        if not is_vc or probabl < rand:
            for u in G[v]:
                degree[v] -= 1
            degree[u] = 0
            S[v] = 1

    return set(u for u in range(1, len(G)) if S[u] == 1)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        input_error()

    for i in range(1, len(sys.argv)):
        filename = sys.argv[i]
        print(filename)
        G = loadGraph(filename)

        Cs = []

        # Deterministic algorithms
        Cs += [VC_two_approx(G)]
        Cs += [VC_logn_approx(G)]

        threads_num = 12
        with Pool(threads_num) as p:
            pass
#            Cs += p.map(VC_annealing, [G] * threads_num)

        C = min(Cs, key=len)

        print(len(C))
        saveSolution(filename + '.sol', C)
