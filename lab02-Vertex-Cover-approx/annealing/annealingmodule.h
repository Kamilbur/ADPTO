/*-
 * Author: Kamil Burkiewicz
 *
 * Tried to stick to PEP 7 :)
 */

#ifndef ANNEALING_H
#define ANNEALING_H

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdio.h>

/*
 * Debugging
 */


// one printy boi
#ifdef DEBUG_MODULE
#  warning "debbuging mode ON"
#  define dprint(msg) do {fprintf(stderr, msg " line[%d]\n", __LINE__); fflush(stderr);} while (0)
#else
#  define dprint(msg) 
#endif

/*
 * Errors and exceptions.
 */
static PyObject *AnnealError;


struct graph {
    Py_ssize_t v_num;
    short int **adj;
};




extern PyObject *from_c_graph(struct graph *c_graph);
extern struct graph *to_c_graph(PyObject *Graph);
extern PyObject *populate_set_from_short_int_array(short int *array, Py_ssize_t size);
extern void c_graph_print(struct graph *c_graph);
extern void c_graph_free(struct graph *c_graph);


extern PyObject *annealing_simulate(PyObject *self, PyObject *args);
extern PyMODINIT_FUNC PyInit_annealing(void);



static PyMethodDef AnnealingMethods[] = {
    {
        "simulate",
        (PyCFunction) annealing_simulate,
        METH_VARARGS,
        PyDoc_STR("Start simulation")
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};


static struct PyModuleDef annealingmodule = {
    PyModuleDef_HEAD_INIT,
    "annealing",   /* name of module */
    NULL,          /* module documentation, may be NULL */
    -1,            /* size of per-interpreter state of the module,
                    or -1 if the module keeps state in global variables. */
    AnnealingMethods
};

#endif
