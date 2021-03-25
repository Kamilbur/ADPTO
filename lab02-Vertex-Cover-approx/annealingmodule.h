/*-
 * Author: Kamil Burkiewicz
 *
 * Tried to stick to PEP 7 :)
 */

#ifndef ANNEALING_H
#  define ANNEALING_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

static PyObject *AnnealError;

struct Graph {
    int v_num;
    short int **adj;
};

#endif
