/*
 * A set of python wrappers around C levinson, etc...
 */

#include <Python.h>
#include <numpy/arrayobject.h>

#include "levinson.h"

/*
 * Levinson-Durbin recursion on one array. Output arrays are put into
 * alpccoeff, klpccoeff and elpc.
 */
int array_levinson_1d(PyArrayObject *arr, long order, PyArrayObject** alpccoeff,
	              PyArrayObject **klpccoeff, PyArrayObject **elpc)
{
	double *tmp;
	npy_intp alpc_size = (order + 1);
	npy_intp klpc_size = order;
	npy_intp elpc_size = 1;

	*alpccoeff = (PyArrayObject*)PyArray_SimpleNew(1, &alpc_size,
                                                       PyArray_DOUBLE);
        if(*alpccoeff == NULL) {
                return -1;
        }

	*klpccoeff = (PyArrayObject*)PyArray_SimpleNew(1, &klpc_size,
						       NPY_DOUBLE);
        if(*klpccoeff == NULL) {
                goto clean_alpccoeff;
        }

        *elpc = (PyArrayObject*)PyArray_SimpleNew(1, &elpc_size, NPY_DOUBLE);
        if(*elpc == NULL) {
                goto clean_klpccoeff;
        }

        tmp = malloc(sizeof(*tmp) * order);
	if (tmp == NULL) {
                goto clean_elpc;
	}

        levinson((double*)(arr->data), order, 
                 (double*)((*alpccoeff)->data), (double*)((*elpc)->data),
                 (double*)((*klpccoeff)->data), tmp);

        free(tmp);

	return 0;

clean_elpc:
        Py_DECREF(*elpc);
clean_klpccoeff:
        Py_DECREF(*klpccoeff);
clean_alpccoeff:
        Py_DECREF(*alpccoeff);
        return -1;
}

int array_levinson_nd(PyArrayObject *arr, long order,
                      PyArrayObject** alpccoeff,
                      PyArrayObject **klpccoeff, PyArrayObject **elpc)
{
	double *acoeff, *kcoeff, *tmp;
	double *err;
	double *data;
	npy_int rank;
	npy_intp alpc_size[NPY_MAXDIMS];
	npy_intp klpc_size[NPY_MAXDIMS];
	npy_intp elpc_size[NPY_MAXDIMS];
	npy_int n, nrepeat;
	int i;

	rank = PyArray_NDIM(arr);
	if (rank < 2) {
		return -1;
	}

	nrepeat = 1;
	for (i = 0; i < rank - 1; ++i) {
		nrepeat *= PyArray_DIM(arr, i);
		alpc_size[i] = PyArray_DIM(arr, i);
		klpc_size[i] = PyArray_DIM(arr, i);
		elpc_size[i] = PyArray_DIM(arr, i);
	}
	alpc_size[rank-1] = order + 1;
	klpc_size[rank-1] = order;

	*alpccoeff = (PyArrayObject*)PyArray_SimpleNew(rank, alpc_size,
                                                       PyArray_DOUBLE);
        if(*alpccoeff == NULL) {
                return -1;
        }

	*klpccoeff = (PyArrayObject*)PyArray_SimpleNew(rank, klpc_size,
						       NPY_DOUBLE);
        if(*klpccoeff == NULL) {
                goto clean_alpccoeff;
        }

        *elpc = (PyArrayObject*)PyArray_SimpleNew(rank-1, elpc_size, NPY_DOUBLE);
        if(*elpc == NULL) {
                goto clean_klpccoeff;
        }

	tmp = malloc(sizeof(*tmp) * order);
	if (tmp == NULL) {
                goto clean_elpc;
	}

	data = (double*)arr->data;
	acoeff = (double*)((*alpccoeff)->data);
	kcoeff = (double*)((*klpccoeff)->data);
	err = (double*)((*elpc)->data);
	n = PyArray_DIM(arr, rank-1);
	for(i = 0; i < nrepeat; ++i) {
		levinson(data, order, acoeff, err, kcoeff, tmp);
		data += n;
		acoeff += order + 1;
		kcoeff += order;
		err += 1;
	}

        free(tmp);
        return 0;

clean_elpc:
        Py_DECREF(*elpc);
clean_klpccoeff:
        Py_DECREF(*klpccoeff);
clean_alpccoeff:
        Py_DECREF(*alpccoeff);
	return -1;
}

PyObject* array_levinson(PyObject* in, long order)
{
	npy_intp rank, size, n;
	PyArrayObject *arr;
	PyObject *out = NULL;
	PyArrayObject *alpc, *klpc, *err;

	arr = (PyArrayObject*)PyArray_ContiguousFromObject(in, PyArray_DOUBLE,
							   1, 0);
	if (arr == NULL) {
		return NULL;
	}

	size = PyArray_SIZE(arr);
	if  (size < 1) {
		PyErr_SetString(PyExc_ValueError, "Cannot operate on empty array !");
		goto fail;
	}

	rank = PyArray_NDIM(arr);
	n = PyArray_DIM(arr, rank-1);
	if (n <= order) {
		PyErr_SetString(PyExc_ValueError, "Order should be <= size-1");
		goto fail;
	}

	switch(rank) {
		case 1:
			array_levinson_1d(arr, order, &alpc, &klpc, &err);
			break;
		default:
			/* Iteratively run levinson recursion on last axis */
			array_levinson_nd(arr, order, &alpc, &klpc, &err);
			break;
	}
        Py_DECREF(arr);

	out = PyTuple_New(3);

	PyTuple_SET_ITEM(out, 0, (PyObject*)alpc);
	PyTuple_SET_ITEM(out, 1, (PyObject*)err);
	PyTuple_SET_ITEM(out, 2, (PyObject*)klpc);

	return out;

fail:
    Py_DECREF(arr);
    return NULL;
}

PyObject* PyArray_Levinson(PyObject* self, PyObject* args)
{
	long order;
	PyObject *in = NULL;
	PyObject *out = NULL;

	if (!PyArg_ParseTuple(args, "Ol", &in, &order)) {
		return NULL;
	}

	out = array_levinson(in, order);
        if (out == NULL) {
                if (!PyErr_ExceptionMatches(PyExc_ValueError)) {
                        return NULL;
                }
        }

	return out;
}

static PyMethodDef lpcmethods[] = {
	{"levinson", PyArray_Levinson, METH_VARARGS, NULL}
};

PyMODINIT_FUNC init_lpc(void)
{
	Py_InitModule("_lpc", lpcmethods);
	import_array();
}
