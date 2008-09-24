/*
 * A set of python wrappers around C levinson, etc...
 */

#include <Python.h>
#include <numpy/arrayobject.h>

#include "levinson.h"

static PyObject *LpcError;

/*
 * Levinson-Durbin recursion on one array. Output arrays are put into
 * alpccoeff, klpccoeff and elpc.
 */
int array_levinson_1d(PyArrayObject *arr, long order, PyArrayObject** alpccoeff,
	              PyArrayObject **klpccoeff, PyArrayObject **elpc)
{
	double *acoeff, *kcoeff, *tmp, *err;
	npy_int alpc_size = (order + 1);
	npy_int klpc_size = order;
	npy_int elpc_size = 1;

	/* XXX: use data malloc from numpy */
	acoeff = malloc(sizeof(*acoeff) * (order + 1));
	if (acoeff == NULL) {
		return -1;
	}
	err = malloc(sizeof(*err));
	if (err == NULL) {
                goto clean_acoeff;
	}
	kcoeff = malloc(sizeof(*kcoeff) * order);
	if (kcoeff == NULL) {
                goto clean_err;
	}
	tmp = malloc(sizeof(*tmp) * order);
	if (tmp == NULL) {
                goto clean_kcoeff;
	}

	levinson((double*)(arr->data), order, acoeff, err, kcoeff, tmp);

	*alpccoeff = (PyArrayObject*)PyArray_SimpleNewFromData(1, &alpc_size,
						      PyArray_DOUBLE, acoeff);
        if(*alpccoeff == NULL) {
                goto clean_tmp;
        }

	*klpccoeff = (PyArrayObject*)PyArray_SimpleNewFromData(1, &klpc_size,
						      NPY_DOUBLE, kcoeff);
        if(*klpccoeff == NULL) {
                goto clean_alpccoeff;
        }

	*elpc = (PyArrayObject*)PyArray_SimpleNewFromData(1, &elpc_size, NPY_DOUBLE,
						 err);
        if(*elpc == NULL) {
                goto clean_klpccoeff;
        }

	return 0;

clean_klpccoeff:
        Py_DECREF(*klpccoeff);
clean_alpccoeff:
        Py_DECREF(*alpccoeff);
clean_tmp:
        free(tmp);
clean_kcoeff:
        free(kcoeff);
clean_err:
        free(err);
clean_acoeff:
        free(acoeff);
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
	npy_int *alpc_size;
	npy_int *klpc_size;
	npy_int *elpc_size;
	npy_int n, nrepeat;
	int i;

	rank = PyArray_NDIM(arr);
	if (rank < 2) {
		return -1;
	}

	/* Set dimensions for output array */
	alpc_size = malloc(sizeof(*alpc_size) * rank);
	if (alpc_size == NULL) {
		return -1;
	}
	klpc_size = malloc(sizeof(*klpc_size) * rank);
	if (klpc_size == NULL) {
		return -1;
	}
	elpc_size = malloc(sizeof(*elpc_size) * (rank-1));
	if (elpc_size == NULL) {
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

	/* XXX: use data malloc from numpy */
	acoeff = malloc(sizeof(*acoeff) * nrepeat * (order + 1));
	if (acoeff == NULL) {
		return -1;
	}
	kcoeff = malloc(sizeof(*kcoeff) * nrepeat * order);
	if (kcoeff == NULL) {
		return -1;
	}
	err = malloc(sizeof(*err) * nrepeat);
	if (err == NULL) {
		return -1;
	}
	tmp = malloc(sizeof(*tmp) * order);
	if (tmp == NULL) {
		return -1;
	}

	*alpccoeff = (PyArrayObject*)PyArray_SimpleNewFromData(rank, alpc_size,
						      PyArray_DOUBLE, acoeff);
	*klpccoeff = (PyArrayObject*)PyArray_SimpleNewFromData(rank, klpc_size,
						      NPY_DOUBLE, kcoeff);
	*elpc = (PyArrayObject*)PyArray_SimpleNewFromData(rank-1, elpc_size, NPY_DOUBLE,
						 err);

	data = (double*)arr->data;
	n = PyArray_DIM(arr, rank-1);
	for(i = 0; i < nrepeat; ++i) {
		levinson(data, order, acoeff, err, kcoeff, tmp);
		data += n;
		acoeff += order + 1;
		kcoeff += order;
		err += 1;
	}
	return 0;
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
		return NULL;
	}

	rank = PyArray_NDIM(arr);
	n = PyArray_DIM(arr, rank-1);
	if (n <= order) {
		PyErr_SetString(LpcError, "Order has to be < input size");
		return NULL;
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

	out = PyTuple_New(3);
	Py_INCREF(alpc);
	PyTuple_SET_ITEM(out, 0, (PyObject*)alpc);

	Py_INCREF(err);
	PyTuple_SET_ITEM(out, 1, (PyObject*)err);

	Py_INCREF(klpc);
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
