from __future__ import annotations
import numpy.random._common
import typing
from importlib._bootstrap import interface
import numpy
import sys
_Shape = typing.Tuple[int, ...]

__all__ = [
    "interface"
]


__all__ = ['interface']
__pyx_capi__: dict # value = {'POISSON_LAM_MAX': <capsule object "double">, 'LEGACY_POISSON_LAM_MAX': <capsule object "double">, 'MAXSIZE': <capsule object "uint64_t">, 'benchmark': <capsule object "PyObject *(bitgen_t *, PyObject *, Py_ssize_t, PyObject *)">, 'random_raw': <capsule object "PyObject *(bitgen_t *, PyObject *, PyObject *, PyObject *)">, 'prepare_cffi': <capsule object "PyObject *(bitgen_t *)">, 'prepare_ctypes': <capsule object "PyObject *(bitgen_t *)">, 'check_constraint': <capsule object "int (double, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)">, 'check_array_constraint': <capsule object "int (PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)">, 'kahan_sum': <capsule object "double (double *, npy_intp)">, 'double_fill': <capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *)">, 'float_fill': <capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *)">, 'float_fill_from_double': <capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *)">, 'wrap_int': <capsule object "PyObject *(PyObject *, PyObject *)">, 'int_to_array': <capsule object "PyArrayObject *(PyObject *, PyObject *, PyObject *, PyObject *)">, 'validate_output_shape': <capsule object "PyObject *(PyObject *, PyArrayObject *)">, 'cont': <capsule object "PyObject *(void *, void *, PyObject *, PyObject *, int, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *)">, 'disc': <capsule object "PyObject *(void *, void *, PyObject *, PyObject *, int, int, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)">, 'cont_f': <capsule object "PyObject *(void *, bitgen_t *, PyObject *, PyObject *, PyObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyObject *)">, 'cont_broadcast_3': <capsule object "PyObject *(void *, void *, PyObject *, PyObject *, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)">, 'discrete_broadcast_iii': <capsule object "PyObject *(void *, void *, PyObject *, PyObject *, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type, PyArrayObject *, PyObject *, __pyx_t_5numpy_6random_7_common_constraint_type)">}
__test__ = {}
np = numpy
sys = sys
