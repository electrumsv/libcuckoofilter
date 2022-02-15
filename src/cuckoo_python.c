/*
      <AdditionalIncludeDirectories>
      C:\Data\Git\electrumsv\contrib\build-windows\amd64\Python-3.10.0\Include
      C:\Data\Git\electrumsv\contrib\build-windows\amd64\Python-3.10.0\PC
    </ClCompile>
    <Link>
      <AdditionalLibraryDirectories>
        C:\Data\Git\electrumsv\contrib\build-windows\amd64\Python-3.10.0\PCbuild\amd64

*/


// #ifdef _MSC_VER
// #pragma warning(disable : 4996)
// #endif

#define PY_SSIZE_T_CLEAN
#include "Python.h"

#include "cuckoo_filter.h"

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
    cuckoo_filter_t *filter;
} CuckooFilterObject;


static void
bsvcuckoo_dealloc(CuckooFilterObject *self)
{
    cuckoo_filter_free(&(self->filter));
    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject *
bsvcuckoo_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    CuckooFilterObject *self;
    self = (CuckooFilterObject *) type->tp_alloc(type, 0);
    if (self != NULL) {
        size_t max_key_count = 500000;
        size_t max_kick_count = 100;
        uint32_t seed = 10301212;
        CUCKOO_FILTER_RETURN result = cuckoo_filter_new(&(self->filter), max_key_count,
            max_kick_count, seed);
        if (result != CUCKOO_FILTER_OK) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject *) self;
}

static int
bsvcuckoo_init(CuckooFilterObject *self, PyObject *args, PyObject *kwds)
{
    // static char *kwlist[] = {"first", "last", "number", NULL};
    // PyObject *first = NULL, *last = NULL, *tmp;

    // if (!PyArg_ParseTupleAndKeywords(args, kwds, "|OOi", kwlist,
    //                                  &first, &last,
    //                                  &self->number))
    //     return -1;

    // if (first) {
    //     tmp = self->first;
    //     Py_INCREF(first);
    //     self->first = first;
    //     Py_XDECREF(tmp);
    // }
    // if (last) {
    //     tmp = self->last;
    //     Py_INCREF(last);
    //     self->last = last;
    //     Py_XDECREF(tmp);
    // }
    return 0;
}

// static PyMemberDef bsvcuckoo_members[] = {
//     // {"first", T_OBJECT_EX, offsetof(CuckooFilterObject, first), 0,
//     //  "first name"},
//     // {"last", T_OBJECT_EX, offsetof(CuckooFilterObject, last), 0,
//     //  "last name"},
//     // {"number", T_INT, offsetof(CuckooFilterObject, number), 0,
//     //  "custom number"},
//     {NULL}  /* Sentinel */
// };

static PyObject *
bsvcuckoo_add(CuckooFilterObject *self, PyObject *args)
{
    void *key;
    Py_ssize_t key_length;

    if (!PyArg_ParseTuple(args, "y#", &key, &key_length))
        return NULL;

    CUCKOO_FILTER_RETURN result = cuckoo_filter_add(self->filter, key, key_length);
    return PyLong_FromLong(result);
}

static PyObject *
bsvcuckoo_contains(CuckooFilterObject *self, PyObject *args)
{
    void *key;
    Py_ssize_t key_length;

    if (!PyArg_ParseTuple(args, "y#", &key, &key_length))
        return NULL;

    CUCKOO_FILTER_RETURN result = cuckoo_filter_contains(self->filter, key, key_length);
    return PyLong_FromLong(result);
}

static PyObject *
bsvcuckoo_contains_hash(CuckooFilterObject *self, PyObject *args)
{
    uint32_t fingerprint;
    uint32_t h1;

    if (!PyArg_ParseTuple(args, "kk", &fingerprint, &h1))
        return NULL;

    CUCKOO_FILTER_RETURN result = cuckoo_filter_contains_hash(self->filter, fingerprint, h1);
    return PyLong_FromLong(result);
}

static PyObject *
bsvcuckoo_hash(CuckooFilterObject *self, PyObject *args)
{
    uint32_t fingerprint;
    uint32_t h1;
    void *key;
    Py_ssize_t key_length;

    if (!PyArg_ParseTuple(args, "y#", &key, &key_length))
        return NULL;

    cuckoo_filter_hash(self->filter, key, key_length, &fingerprint, &h1);

    PyObject *fingerprint_object = PyLong_FromUnsignedLong(fingerprint);
    if (fingerprint_object == NULL) {
        PyErr_SetObject(PyExc_Exception,
            PyUnicode_FromString("Error allocating 'fingerprint' object."));
        return NULL;
    }

    PyObject *h1_object = PyLong_FromUnsignedLong(h1);
    if (h1_object == NULL) {
        Py_DECREF(fingerprint_object);
        PyErr_SetObject(PyExc_Exception,
            PyUnicode_FromString("Error allocating 'h1' object."));
        return NULL;
    }

    return PyTuple_Pack(2, fingerprint_object, h1_object);
}

static PyObject *
bsvcuckoo_remove(CuckooFilterObject *self, PyObject *args)
{
    void *key;
    Py_ssize_t key_length;

    if (!PyArg_ParseTuple(args, "y#", &key, &key_length))
        return NULL;

    CUCKOO_FILTER_RETURN result = cuckoo_filter_remove(self->filter, key, key_length);
    return PyLong_FromLong(result);
}

static PyMethodDef bsvcuckoo_methods[] = {
    {"add", (PyCFunction) bsvcuckoo_add, METH_VARARGS,
         "Add an item to the cuckoo filter."
    },
    {"contains", (PyCFunction) bsvcuckoo_contains, METH_VARARGS,
         "Check if an item is possibly in the cuckoo filter. This can return false positives."
    },
    {"contains_hash", (PyCFunction) bsvcuckoo_contains_hash, METH_VARARGS,
         "Check if an item is possibly in the cuckoo filter. This can return false positives."
    },
    {"hash", (PyCFunction) bsvcuckoo_hash, METH_VARARGS,
         "Get the hash values for the given item."
    },
    {"remove", (PyCFunction) bsvcuckoo_remove, METH_VARARGS,
         "Remove an item from the cuckoo filter."
    },
    {NULL}  /* Sentinel */
};

static PyTypeObject CuckooFilterType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "bsvcuckoo.CuckooFilter",
    .tp_doc = "A cuckoo filter instance",
    .tp_basicsize = sizeof(CuckooFilterObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = bsvcuckoo_new,
    .tp_init = (initproc) bsvcuckoo_init,
    .tp_dealloc = (destructor) bsvcuckoo_dealloc,
    // .tp_members = bsvcuckoo_members,
    .tp_methods = bsvcuckoo_methods,
};


// static PyObject* create_cuckoo_filter(PyObject* self, PyObject* args)
// {
//     const char* file_name;
//     const unsigned char* hash_data;
//     Py_ssize_t hash_size;
//     unsigned char jpg_quality;

//     if (!PyArg_ParseTuple(args, "sy#b", &file_name, &hash_data, &hash_size, &jpg_quality))
//         return NULL;

//     return PyLong_FromLong(1);
// }

// static PyMethodDef bsvcuckoo_methods[] = {
//     {"create",  create_cuckoo_filter, METH_VARARGS, "Create a new cuckoo filter"},
//     {NULL, NULL, 0, NULL}        /* Sentinel */
// };

static struct PyModuleDef bsvcuckoo_module = {
    PyModuleDef_HEAD_INIT,
    "bsvcuckoo",   /* name of module */
    NULL, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    NULL // bsvcuckoo_methods
};

PyMODINIT_FUNC
PyInit_bsvcuckoo(void)
{
    PyObject *module;
    if (PyType_Ready(&CuckooFilterType) < 0)
        return NULL;

    module = PyModule_Create(&bsvcuckoo_module);
    if (module == NULL)
        return NULL;

    Py_INCREF(&CuckooFilterType);
    if (PyModule_AddObject(module, "CuckooFilter", (PyObject *) &CuckooFilterType) < 0) {
        Py_DECREF(&CuckooFilterType);
        Py_DECREF(module);
        return NULL;
    }

    return module;
}

