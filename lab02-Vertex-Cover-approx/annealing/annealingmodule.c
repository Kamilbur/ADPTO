#include "annealingmodule.h"


extern PyObject *AnnealError;

extern PyMODINIT_FUNC
PyInit_annealing(void)
{
    /*
     * Module initialization.
     */

    PyObject *module;

    module = PyModule_Create(&annealingmodule);
    if (module == NULL) {
        return NULL;
    }

    AnnealError = PyErr_NewException("annealing.AnnealError", NULL, NULL);
    Py_XINCREF(AnnealError);
    if (PyModule_AddObject(module, "AnnealError", AnnealError) < 0) {
        Py_XDECREF(AnnealError);
        Py_CLEAR(AnnealError);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}


extern PyObject *
annealing_simulate(PyObject *self, PyObject *args)
{
    /*
     * Annealing startup.
     */




//
// For now it is just a prototype and a proof of concept for me.
//

    struct graph *c_graph = NULL;
    PyObject *Graph = NULL;
    PyObject *retval = NULL;

    if ( ! PyArg_ParseTuple(args, "O|:ref", &Graph)) {
        goto error;
    }

    if ( ! PyList_Check(Graph)) {
        PyErr_SetString(AnnealError, "The argument is not a Graph - List[set(int)] - adjacency list");
        goto error;
    }

    if ( (c_graph = to_c_graph(Graph)) == NULL) {
        goto error;
    }

    c_graph_print(c_graph);

    if ( (retval = from_c_graph(c_graph)) == NULL) {
        goto error;
    }

    c_graph_free(c_graph);

    return retval;

error:
    Py_XDECREF(Graph);
    
    return NULL;
}


extern PyObject *
from_c_graph(struct graph *c_graph)
{
    /*
     * Make python Graph List[set()] from struct graph.
     *
     * By the time of the return of this function, here is
     * the only reference to returned object.
     *
     */

    PyObject *Graph = NULL;
    PyObject *Graph_element = NULL;
    Py_ssize_t ii;

    if ( (Graph = PyList_New(c_graph->v_num)) == NULL) {
        goto error;
    }

    for (ii = 0; ii < c_graph->v_num; ii++) {
        Graph_element = populate_set_from_short_int_array(c_graph->adj[ii], c_graph->v_num);
        if (Graph_element == NULL) {
            goto error;
        }
        
        if (PyList_SetItem(Graph, ii, Graph_element) == -1) {
            goto error;
        }
    }

    return Graph;

error:
    Py_XDECREF(Graph);
    Py_XDECREF(Graph_element);

    return NULL;
}

extern struct graph *
to_c_graph(PyObject *Graph)
{
    /*
     * Make struct graph from python Graph List[set()].
     */

    PyObject *neighbors = NULL, *idx = NULL;
    struct graph *c_graph = NULL;
    Py_ssize_t ii, jj;
    int retval;


    if ( (c_graph = malloc(sizeof(struct graph))) == NULL) {
        goto error;
    }

    c_graph->v_num = PyList_Size(Graph);
    if (c_graph->v_num < 0) {
        /* Not a list. */
        return NULL;
    }
    
    if ( (c_graph->adj = calloc((size_t) c_graph->v_num, sizeof(short int *))) == NULL) {
        goto error;
    }
    for (ii = 0; ii < c_graph->v_num; ii++) {
        if ( (c_graph->adj[ii] = calloc((size_t) c_graph->v_num, sizeof(short int))) == NULL) {
            goto error;
        }
    }

    for (ii = 0; ii < c_graph->v_num; ii++) {
        neighbors = PyList_GetItem(Graph, ii);
        if ( ! PySet_Check(neighbors)) {
            goto error;
        }
        for (jj = 0; jj < c_graph->v_num; jj++) {
            idx = PyLong_FromSsize_t(jj);

            if ( ! PyLong_Check(idx)) {
                goto error;
            }

            retval = PySet_Contains(neighbors, idx);
            if (retval == -1 && PyErr_Occurred()) {
                goto error;
            }
            else if (retval) {
                c_graph->adj[ii][jj] = 1;
            }
            else {
                c_graph->adj[ii][jj] = 0;
            }

            Py_XDECREF(idx);
        }
    }

    return c_graph;

error:
    Py_XDECREF(idx);

    return NULL;
}


extern PyObject *
populate_set_from_short_int_array(short int *array, Py_ssize_t size)
{
    /*
     * Populate python set with non zero indexes of the elements 
     * of a short int array of a given size.
     */

    PyObject *list = NULL;
    PyObject *item = NULL;
    PyObject *set = NULL;
    Py_ssize_t ii;


    if ( (list = PyList_New(0)) == NULL) {
        goto error;
    }


    for (ii = 0; ii < size; ii++) {
        if (array[ii]) {
            if ( (item = PyLong_FromLong(ii)) == NULL) {
                goto error;
            }
            if (PyList_Append(list, item) == -1) {
                goto error;
            }
            Py_XDECREF(item);
        }
    }

    if ( (set = PySet_New(list)) == NULL) {
        goto error;
    }

    Py_XDECREF(list);

    return set;

error:
    Py_XDECREF(list);
    Py_XDECREF(item);
    Py_XDECREF(set);

    return NULL;
}


extern void
c_graph_print(struct graph *c_graph)
{
    for (int ii = 0; ii < c_graph->v_num; ii++) {
        for (int jj = 0; jj < c_graph->v_num; jj++) {
            printf("%d ", c_graph->adj[ii][jj]);
        }
        printf("\n");
    }
}


extern void
c_graph_free(struct graph *c_graph)
{
    Py_ssize_t ii = 0;

    if (c_graph == NULL) return;

    for (ii = 0; ii < c_graph->v_num; ii++) {
        free(c_graph->adj[ii]);
    }
    free(c_graph->adj);
    free(c_graph);
}

