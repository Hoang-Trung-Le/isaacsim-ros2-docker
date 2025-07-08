from __future__ import annotations
import numpy.core._multiarray_tests
import typing

__all__ = [
    "IsPythonScalar",
    "argparse_example_function",
    "array_indexing",
    "corrupt_or_fix_bufferinfo",
    "create_custom_field_dtype",
    "extint_add_128",
    "extint_ceildiv_128_64",
    "extint_divmod_128_64",
    "extint_floordiv_128_64",
    "extint_gt_128",
    "extint_mul_64_64",
    "extint_neg_128",
    "extint_safe_binop",
    "extint_shl_128",
    "extint_shr_128",
    "extint_sub_128",
    "extint_to_128",
    "extint_to_64",
    "format_float_OSprintf_g",
    "fromstring_null_term_c_api",
    "get_all_cast_information",
    "get_buffer_info",
    "get_c_wrapping_array",
    "get_fpu_mode",
    "get_struct_alignments",
    "getset_numericops",
    "identityhash_tester",
    "incref_elide",
    "incref_elide_l",
    "internal_overlap",
    "npy_abuse_writebackifcopy",
    "npy_cabs",
    "npy_cabsf",
    "npy_cabsl",
    "npy_carg",
    "npy_cargf",
    "npy_cargl",
    "npy_char_deprecation",
    "npy_cosh",
    "npy_coshf",
    "npy_coshl",
    "npy_create_writebackifcopy",
    "npy_discard",
    "npy_ensurenocopy",
    "npy_log10",
    "npy_log10f",
    "npy_log10l",
    "npy_pyarrayas1d_deprecation",
    "npy_pyarrayas2d_deprecation",
    "npy_resolve",
    "npy_sinh",
    "npy_sinhf",
    "npy_sinhl",
    "npy_tan",
    "npy_tanf",
    "npy_tanh",
    "npy_tanhf",
    "npy_tanhl",
    "npy_tanl",
    "run_byteorder_converter",
    "run_casting_converter",
    "run_clipmode_converter",
    "run_intp_converter",
    "run_order_converter",
    "run_scalar_intp_converter",
    "run_scalar_intp_from_sequence",
    "run_searchside_converter",
    "run_selectkind_converter",
    "run_sortkind_converter",
    "solve_diophantine",
    "test_as_c_array",
    "test_inplace_increment",
    "test_nditer_too_large",
    "test_neighborhood_iterator",
    "test_neighborhood_iterator_oob",
    "test_pydatamem_seteventhook_end",
    "test_pydatamem_seteventhook_start"
]


def IsPythonScalar(*args, **kwargs) -> typing.Any:
    pass
def argparse_example_function(*args, **kwargs) -> typing.Any:
    pass
def array_indexing(*args, **kwargs) -> typing.Any:
    pass
def corrupt_or_fix_bufferinfo(*args, **kwargs) -> typing.Any:
    pass
def create_custom_field_dtype(*args, **kwargs) -> typing.Any:
    pass
def extint_add_128(*args, **kwargs) -> typing.Any:
    pass
def extint_ceildiv_128_64(*args, **kwargs) -> typing.Any:
    pass
def extint_divmod_128_64(*args, **kwargs) -> typing.Any:
    pass
def extint_floordiv_128_64(*args, **kwargs) -> typing.Any:
    pass
def extint_gt_128(*args, **kwargs) -> typing.Any:
    pass
def extint_mul_64_64(*args, **kwargs) -> typing.Any:
    pass
def extint_neg_128(*args, **kwargs) -> typing.Any:
    pass
def extint_safe_binop(*args, **kwargs) -> typing.Any:
    pass
def extint_shl_128(*args, **kwargs) -> typing.Any:
    pass
def extint_shr_128(*args, **kwargs) -> typing.Any:
    pass
def extint_sub_128(*args, **kwargs) -> typing.Any:
    pass
def extint_to_128(*args, **kwargs) -> typing.Any:
    pass
def extint_to_64(*args, **kwargs) -> typing.Any:
    pass
def format_float_OSprintf_g(*args, **kwargs) -> typing.Any:
    """
    Print a floating point scalar using the system's printf function,
    equivalent to:

        printf("%.*g", precision, val);

    for half/float/double, or replacing 'g' by 'Lg' for longdouble. This
    method is designed to help cross-validate the format_float_* methods.

    Parameters
    ----------
    val : python float or numpy floating scalar
        Value to format.

    precision : non-negative integer, optional
        Precision given to printf.

    Returns
    -------
    rep : string
        The string representation of the floating point value

    See Also
    --------
    format_float_scientific
    format_float_positional
    """
def fromstring_null_term_c_api(*args, **kwargs) -> typing.Any:
    pass
def get_all_cast_information(*args, **kwargs) -> typing.Any:
    """
    Return a list with info on all available casts. Some of the infomay differ for an actual cast if it uses value-based casting (flexible types).
    """
def get_buffer_info(*args, **kwargs) -> typing.Any:
    pass
def get_c_wrapping_array(*args, **kwargs) -> typing.Any:
    pass
def get_fpu_mode(*args, **kwargs) -> typing.Any:
    """
    Get the current FPU control word, in a platform-dependent format.
    Returns None if not implemented on current platform.
    """
def get_struct_alignments(*args, **kwargs) -> typing.Any:
    pass
def getset_numericops(*args, **kwargs) -> typing.Any:
    pass
def identityhash_tester(*args, **kwargs) -> typing.Any:
    pass
def incref_elide(*args, **kwargs) -> typing.Any:
    pass
def incref_elide_l(*args, **kwargs) -> typing.Any:
    pass
def internal_overlap(*args, **kwargs) -> typing.Any:
    pass
def npy_abuse_writebackifcopy(*args, **kwargs) -> typing.Any:
    pass
def npy_cabs(*args, **kwargs) -> typing.Any:
    pass
def npy_cabsf(*args, **kwargs) -> typing.Any:
    pass
def npy_cabsl(*args, **kwargs) -> typing.Any:
    pass
def npy_carg(*args, **kwargs) -> typing.Any:
    pass
def npy_cargf(*args, **kwargs) -> typing.Any:
    pass
def npy_cargl(*args, **kwargs) -> typing.Any:
    pass
def npy_char_deprecation(*args, **kwargs) -> typing.Any:
    pass
def npy_cosh(*args, **kwargs) -> typing.Any:
    pass
def npy_coshf(*args, **kwargs) -> typing.Any:
    pass
def npy_coshl(*args, **kwargs) -> typing.Any:
    pass
def npy_create_writebackifcopy(*args, **kwargs) -> typing.Any:
    pass
def npy_discard(*args, **kwargs) -> typing.Any:
    pass
def npy_ensurenocopy(*args, **kwargs) -> typing.Any:
    pass
def npy_log10(*args, **kwargs) -> typing.Any:
    pass
def npy_log10f(*args, **kwargs) -> typing.Any:
    pass
def npy_log10l(*args, **kwargs) -> typing.Any:
    pass
def npy_pyarrayas1d_deprecation(*args, **kwargs) -> typing.Any:
    pass
def npy_pyarrayas2d_deprecation(*args, **kwargs) -> typing.Any:
    pass
def npy_resolve(*args, **kwargs) -> typing.Any:
    pass
def npy_sinh(*args, **kwargs) -> typing.Any:
    pass
def npy_sinhf(*args, **kwargs) -> typing.Any:
    pass
def npy_sinhl(*args, **kwargs) -> typing.Any:
    pass
def npy_tan(*args, **kwargs) -> typing.Any:
    pass
def npy_tanf(*args, **kwargs) -> typing.Any:
    pass
def npy_tanh(*args, **kwargs) -> typing.Any:
    pass
def npy_tanhf(*args, **kwargs) -> typing.Any:
    pass
def npy_tanhl(*args, **kwargs) -> typing.Any:
    pass
def npy_tanl(*args, **kwargs) -> typing.Any:
    pass
def run_byteorder_converter(*args, **kwargs) -> typing.Any:
    pass
def run_casting_converter(*args, **kwargs) -> typing.Any:
    pass
def run_clipmode_converter(*args, **kwargs) -> typing.Any:
    pass
def run_intp_converter(*args, **kwargs) -> typing.Any:
    pass
def run_order_converter(*args, **kwargs) -> typing.Any:
    pass
def run_scalar_intp_converter(*args, **kwargs) -> typing.Any:
    pass
def run_scalar_intp_from_sequence(*args, **kwargs) -> typing.Any:
    pass
def run_searchside_converter(*args, **kwargs) -> typing.Any:
    pass
def run_selectkind_converter(*args, **kwargs) -> typing.Any:
    pass
def run_sortkind_converter(*args, **kwargs) -> typing.Any:
    pass
def solve_diophantine(*args, **kwargs) -> typing.Any:
    pass
def test_as_c_array(*args, **kwargs) -> typing.Any:
    pass
def test_inplace_increment(*args, **kwargs) -> typing.Any:
    pass
def test_nditer_too_large(*args, **kwargs) -> typing.Any:
    pass
def test_neighborhood_iterator(*args, **kwargs) -> typing.Any:
    pass
def test_neighborhood_iterator_oob(*args, **kwargs) -> typing.Any:
    pass
def test_pydatamem_seteventhook_end(*args, **kwargs) -> typing.Any:
    pass
def test_pydatamem_seteventhook_start(*args, **kwargs) -> typing.Any:
    pass
