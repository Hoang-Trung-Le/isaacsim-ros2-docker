from __future__ import annotations
import numpy.core._multiarray_umath
import typing
from numpy.core.multiarray import flagsobj
from numpy.core.multiarray import typeinforanged
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "ALLOW_THREADS",
    "BUFSIZE",
    "CLIP",
    "DATETIMEUNITS",
    "ERR_CALL",
    "ERR_DEFAULT",
    "ERR_IGNORE",
    "ERR_LOG",
    "ERR_PRINT",
    "ERR_RAISE",
    "ERR_WARN",
    "FLOATING_POINT_SUPPORT",
    "FPE_DIVIDEBYZERO",
    "FPE_INVALID",
    "FPE_OVERFLOW",
    "FPE_UNDERFLOW",
    "ITEM_HASOBJECT",
    "ITEM_IS_POINTER",
    "LIST_PICKLE",
    "MAXDIMS",
    "MAY_SHARE_BOUNDS",
    "MAY_SHARE_EXACT",
    "NAN",
    "NEEDS_INIT",
    "NEEDS_PYAPI",
    "NINF",
    "NZERO",
    "PINF",
    "PZERO",
    "RAISE",
    "SHIFT_DIVIDEBYZERO",
    "SHIFT_INVALID",
    "SHIFT_OVERFLOW",
    "SHIFT_UNDERFLOW",
    "UFUNC_BUFSIZE_DEFAULT",
    "UFUNC_PYVALS_NAME",
    "USE_GETITEM",
    "USE_SETITEM",
    "WRAP",
    "absolute",
    "add",
    "add_docstring",
    "arange",
    "arccos",
    "arccosh",
    "arcsin",
    "arcsinh",
    "arctan",
    "arctan2",
    "arctanh",
    "array",
    "asanyarray",
    "asarray",
    "ascontiguousarray",
    "asfortranarray",
    "bincount",
    "bitwise_and",
    "bitwise_or",
    "bitwise_xor",
    "broadcast",
    "busday_count",
    "busday_offset",
    "busdaycalendar",
    "c_einsum",
    "can_cast",
    "cbrt",
    "ceil",
    "clip",
    "compare_chararrays",
    "concatenate",
    "conj",
    "conjugate",
    "copysign",
    "copyto",
    "correlate",
    "correlate2",
    "cos",
    "cosh",
    "count_nonzero",
    "datetime_as_string",
    "datetime_data",
    "deg2rad",
    "degrees",
    "divide",
    "divmod",
    "dot",
    "dragon4_positional",
    "dragon4_scientific",
    "dtype",
    "e",
    "empty",
    "empty_like",
    "equal",
    "error",
    "euler_gamma",
    "exp",
    "exp2",
    "expm1",
    "fabs",
    "fastCopyAndTranspose",
    "flagsobj",
    "flatiter",
    "float_power",
    "floor",
    "floor_divide",
    "fmax",
    "fmin",
    "fmod",
    "format_longfloat",
    "frexp",
    "from_dlpack",
    "frombuffer",
    "fromfile",
    "fromiter",
    "frompyfunc",
    "fromstring",
    "gcd",
    "get_handler_name",
    "get_handler_version",
    "geterrobj",
    "greater",
    "greater_equal",
    "heaviside",
    "hypot",
    "inner",
    "interp",
    "interp_complex",
    "invert",
    "is_busday",
    "isfinite",
    "isinf",
    "isnan",
    "isnat",
    "lcm",
    "ldexp",
    "left_shift",
    "less",
    "less_equal",
    "lexsort",
    "log",
    "log10",
    "log1p",
    "log2",
    "logaddexp",
    "logaddexp2",
    "logical_and",
    "logical_not",
    "logical_or",
    "logical_xor",
    "matmul",
    "maximum",
    "may_share_memory",
    "min_scalar_type",
    "minimum",
    "mod",
    "modf",
    "multiply",
    "ndarray",
    "nditer",
    "negative",
    "nested_iters",
    "nextafter",
    "normalize_axis_index",
    "not_equal",
    "packbits",
    "pi",
    "positive",
    "power",
    "promote_types",
    "putmask",
    "rad2deg",
    "radians",
    "ravel_multi_index",
    "reciprocal",
    "remainder",
    "result_type",
    "right_shift",
    "rint",
    "scalar",
    "set_datetimeparse_function",
    "set_legacy_print_mode",
    "set_numeric_ops",
    "set_string_function",
    "set_typeDict",
    "seterrobj",
    "shares_memory",
    "sign",
    "signbit",
    "sin",
    "sinh",
    "spacing",
    "sqrt",
    "square",
    "subtract",
    "tan",
    "tanh",
    "tracemalloc_domain",
    "true_divide",
    "trunc",
    "typeinfo",
    "typeinforanged",
    "unpackbits",
    "unravel_index",
    "vdot",
    "where",
    "zeros"
]


class _ArrayFunctionDispatcher():
    """
    Class to wrap functions with checks for __array_function__ overrides.

    All arguments are required, and can only be passed by position.

    Parameters
    ----------
    dispatcher : function or None
        The dispatcher function that returns a single sequence-like object
        of all arguments relevant.  It must have the same signature (except
        the default values) as the actual implementation.
        If ``None``, this is a ``like=`` dispatcher and the
        ``_ArrayFunctionDispatcher`` must be called with ``like`` as the
        first (additional and positional) argument.
    implementation : function
        Function that implements the operation on NumPy arrays without
        overrides.  Arguments passed calling the ``_ArrayFunctionDispatcher``
        will be forwarded to this (and the ``dispatcher``) as if using
        ``*args, **kwargs``.

    Attributes
    ----------
    _implementation : function
        The original implementation passed in.
    """
    _implementation: getset_descriptor # value = <attribute '_implementation' of 'numpy._ArrayFunctionDispatcher' objects>
    pass
class broadcast():
    """
    Produce an object that mimics broadcasting.

        Parameters
        ----------
        in1, in2, ... : array_like
            Input parameters.

        Returns
        -------
        b : broadcast object
            Broadcast the input parameters against one another, and
            return an object that encapsulates the result.
            Amongst others, it has ``shape`` and ``nd`` properties, and
            may be used as an iterator.

        See Also
        --------
        broadcast_arrays
        broadcast_to
        broadcast_shapes

        Examples
        --------

        Manually adding two vectors, using broadcasting:

        >>> x = np.array([[1], [2], [3]])
        >>> y = np.array([4, 5, 6])
        >>> b = np.broadcast(x, y)

        >>> out = np.empty(b.shape)
        >>> out.flat = [u+v for (u,v) in b]
        >>> out
        array([[5.,  6.,  7.],
               [6.,  7.,  8.],
               [7.,  8.,  9.]])

        Compare against built-in broadcasting:

        >>> x + y
        array([[5, 6, 7],
               [6, 7, 8],
               [7, 8, 9]])
    """
    @staticmethod
    def reset(*args, **kwargs) -> typing.Any: 
        """
        Reset the broadcasted result's iterator(s).

        Parameters
        ----------
        None

        Returns
        -------
        None

        Examples
        --------
        >>> x = np.array([1, 2, 3])
        >>> y = np.array([[4], [5], [6]])
        >>> b = np.broadcast(x, y)
        >>> b.index
        0
        >>> next(b), next(b), next(b)
        ((1, 4), (2, 4), (3, 4))
        >>> b.index
        3
        >>> b.reset()
        >>> b.index
        0
        """
    index: getset_descriptor # value = <attribute 'index' of 'numpy.broadcast' objects>
    iters: getset_descriptor # value = <attribute 'iters' of 'numpy.broadcast' objects>
    nd: member_descriptor # value = <member 'nd' of 'numpy.broadcast' objects>
    ndim: member_descriptor # value = <member 'ndim' of 'numpy.broadcast' objects>
    numiter: member_descriptor # value = <member 'numiter' of 'numpy.broadcast' objects>
    shape: getset_descriptor # value = <attribute 'shape' of 'numpy.broadcast' objects>
    size: getset_descriptor # value = <attribute 'size' of 'numpy.broadcast' objects>
    pass
class busdaycalendar():
    """
    busdaycalendar(weekmask='1111100', holidays=None)

        A business day calendar object that efficiently stores information
        defining valid days for the busday family of functions.

        The default valid days are Monday through Friday ("business days").
        A busdaycalendar object can be specified with any set of weekly
        valid days, plus an optional "holiday" dates that always will be invalid.

        Once a busdaycalendar object is created, the weekmask and holidays
        cannot be modified.

        .. versionadded:: 1.7.0

        Parameters
        ----------
        weekmask : str or array_like of bool, optional
            A seven-element array indicating which of Monday through Sunday are
            valid days. May be specified as a length-seven list or array, like
            [1,1,1,1,1,0,0]; a length-seven string, like '1111100'; or a string
            like "Mon Tue Wed Thu Fri", made up of 3-character abbreviations for
            weekdays, optionally separated by white space. Valid abbreviations
            are: Mon Tue Wed Thu Fri Sat Sun
        holidays : array_like of datetime64[D], optional
            An array of dates to consider as invalid dates, no matter which
            weekday they fall upon.  Holiday dates may be specified in any
            order, and NaT (not-a-time) dates are ignored.  This list is
            saved in a normalized form that is suited for fast calculations
            of valid days.

        Returns
        -------
        out : busdaycalendar
            A business day calendar object containing the specified
            weekmask and holidays values.

        See Also
        --------
        is_busday : Returns a boolean array indicating valid days.
        busday_offset : Applies an offset counted in valid days.
        busday_count : Counts how many valid days are in a half-open date range.

        Attributes
        ----------
        Note: once a busdaycalendar object is created, you cannot modify the
        weekmask or holidays.  The attributes return copies of internal data.
        weekmask : (copy) seven-element array of bool
        holidays : (copy) sorted array of datetime64[D]

        Examples
        --------
        >>> # Some important days in July
        ... bdd = np.busdaycalendar(
        ...             holidays=['2011-07-01', '2011-07-04', '2011-07-17'])
        >>> # Default is Monday to Friday weekdays
        ... bdd.weekmask
        array([ True,  True,  True,  True,  True, False, False])
        >>> # Any holidays already on the weekend are removed
        ... bdd.holidays
        array(['2011-07-01', '2011-07-04'], dtype='datetime64[D]')
    """
    holidays: getset_descriptor # value = <attribute 'holidays' of 'numpy.busdaycalendar' objects>
    weekmask: getset_descriptor # value = <attribute 'weekmask' of 'numpy.busdaycalendar' objects>
    pass
class dtype():
    """
    dtype(dtype, align=False, copy=False, [metadata])

        Create a data type object.

        A numpy array is homogeneous, and contains elements described by a
        dtype object. A dtype object can be constructed from different
        combinations of fundamental numeric types.

        Parameters
        ----------
        dtype
            Object to be converted to a data type object.
        align : bool, optional
            Add padding to the fields to match what a C compiler would output
            for a similar C-struct. Can be ``True`` only if `obj` is a dictionary
            or a comma-separated string. If a struct dtype is being created,
            this also sets a sticky alignment flag ``isalignedstruct``.
        copy : bool, optional
            Make a new copy of the data-type object. If ``False``, the result
            may just be a reference to a built-in data-type object.
        metadata : dict, optional
            An optional dictionary with dtype metadata.

        See also
        --------
        result_type

        Examples
        --------
        Using array-scalar type:

        >>> np.dtype(np.int16)
        dtype('int16')

        Structured type, one field name 'f1', containing int16:

        >>> np.dtype([('f1', np.int16)])
        dtype([('f1', '<i2')])

        Structured type, one field named 'f1', in itself containing a structured
        type with one field:

        >>> np.dtype([('f1', [('f1', np.int16)])])
        dtype([('f1', [('f1', '<i2')])])

        Structured type, two fields: the first field contains an unsigned int, the
        second an int32:

        >>> np.dtype([('f1', np.uint64), ('f2', np.int32)])
        dtype([('f1', '<u8'), ('f2', '<i4')])

        Using array-protocol type strings:

        >>> np.dtype([('a','f8'),('b','S10')])
        dtype([('a', '<f8'), ('b', 'S10')])

        Using comma-separated field formats.  The shape is (2,3):

        >>> np.dtype("i4, (2,3)f8")
        dtype([('f0', '<i4'), ('f1', '<f8', (2, 3))])

        Using tuples.  ``int`` is a fixed type, 3 the field's shape.  ``void``
        is a flexible type, here of size 10:

        >>> np.dtype([('hello',(np.int64,3)),('world',np.void,10)])
        dtype([('hello', '<i8', (3,)), ('world', 'V10')])

        Subdivide ``int16`` into 2 ``int8``'s, called x and y.  0 and 1 are
        the offsets in bytes:

        >>> np.dtype((np.int16, {'x':(np.int8,0), 'y':(np.int8,1)}))
        dtype((numpy.int16, [('x', 'i1'), ('y', 'i1')]))

        Using dictionaries.  Two fields named 'gender' and 'age':

        >>> np.dtype({'names':['gender','age'], 'formats':['S1',np.uint8]})
        dtype([('gender', 'S1'), ('age', 'u1')])

        Offsets in bytes, here 0 and 25:

        >>> np.dtype({'surname':('S25',0),'age':(np.uint8,25)})
        dtype([('surname', 'S25'), ('age', 'u1')])
    """
    @staticmethod
    def newbyteorder(*args, **kwargs) -> typing.Any: 
        """
        Return a new dtype with a different byte order.

        Changes are also made in all fields and sub-arrays of the data type.

        Parameters
        ----------
        new_order : string, optional
            Byte order to force; a value from the byte order specifications
            below.  The default value ('S') results in swapping the current
            byte order.  `new_order` codes can be any of:

            * 'S' - swap dtype from current to opposite endian
            * {'<', 'little'} - little endian
            * {'>', 'big'} - big endian
            * {'=', 'native'} - native order
            * {'|', 'I'} - ignore (no change to byte order)

        Returns
        -------
        new_dtype : dtype
            New dtype object with the given change to the byte order.

        Notes
        -----
        Changes are also made in all fields and sub-arrays of the data type.

        Examples
        --------
        >>> import sys
        >>> sys_is_le = sys.byteorder == 'little'
        >>> native_code = '<' if sys_is_le else '>'
        >>> swapped_code = '>' if sys_is_le else '<'
        >>> native_dt = np.dtype(native_code+'i2')
        >>> swapped_dt = np.dtype(swapped_code+'i2')
        >>> native_dt.newbyteorder('S') == swapped_dt
        True
        >>> native_dt.newbyteorder() == swapped_dt
        True
        >>> native_dt == swapped_dt.newbyteorder('S')
        True
        >>> native_dt == swapped_dt.newbyteorder('=')
        True
        >>> native_dt == swapped_dt.newbyteorder('N')
        True
        >>> native_dt == native_dt.newbyteorder('|')
        True
        >>> np.dtype('<i2') == native_dt.newbyteorder('<')
        True
        >>> np.dtype('<i2') == native_dt.newbyteorder('L')
        True
        >>> np.dtype('>i2') == native_dt.newbyteorder('>')
        True
        >>> np.dtype('>i2') == native_dt.newbyteorder('B')
        True
        """
    alignment: member_descriptor # value = <member 'alignment' of 'numpy.dtype' objects>
    base: getset_descriptor # value = <attribute 'base' of 'numpy.dtype' objects>
    byteorder: member_descriptor # value = <member 'byteorder' of 'numpy.dtype' objects>
    char: member_descriptor # value = <member 'char' of 'numpy.dtype' objects>
    descr: getset_descriptor # value = <attribute 'descr' of 'numpy.dtype' objects>
    fields: getset_descriptor # value = <attribute 'fields' of 'numpy.dtype' objects>
    flags: member_descriptor # value = <member 'flags' of 'numpy.dtype' objects>
    hasobject: getset_descriptor # value = <attribute 'hasobject' of 'numpy.dtype' objects>
    isalignedstruct: getset_descriptor # value = <attribute 'isalignedstruct' of 'numpy.dtype' objects>
    isbuiltin: getset_descriptor # value = <attribute 'isbuiltin' of 'numpy.dtype' objects>
    isnative: getset_descriptor # value = <attribute 'isnative' of 'numpy.dtype' objects>
    itemsize: member_descriptor # value = <member 'itemsize' of 'numpy.dtype' objects>
    kind: member_descriptor # value = <member 'kind' of 'numpy.dtype' objects>
    metadata: getset_descriptor # value = <attribute 'metadata' of 'numpy.dtype' objects>
    name: getset_descriptor # value = <attribute 'name' of 'numpy.dtype' objects>
    names: getset_descriptor # value = <attribute 'names' of 'numpy.dtype' objects>
    ndim: getset_descriptor # value = <attribute 'ndim' of 'numpy.dtype' objects>
    num: member_descriptor # value = <member 'num' of 'numpy.dtype' objects>
    shape: getset_descriptor # value = <attribute 'shape' of 'numpy.dtype' objects>
    str: getset_descriptor # value = <attribute 'str' of 'numpy.dtype' objects>
    subdtype: getset_descriptor # value = <attribute 'subdtype' of 'numpy.dtype' objects>
    type = None
    pass
class flatiter():
    """
    Flat iterator object to iterate over arrays.

        A `flatiter` iterator is returned by ``x.flat`` for any array `x`.
        It allows iterating over the array as if it were a 1-D array,
        either in a for-loop or by calling its `next` method.

        Iteration is done in row-major, C-style order (the last
        index varying the fastest). The iterator can also be indexed using
        basic slicing or advanced indexing.

        See Also
        --------
        ndarray.flat : Return a flat iterator over an array.
        ndarray.flatten : Returns a flattened copy of an array.

        Notes
        -----
        A `flatiter` iterator can not be constructed directly from Python code
        by calling the `flatiter` constructor.

        Examples
        --------
        >>> x = np.arange(6).reshape(2, 3)
        >>> fl = x.flat
        >>> type(fl)
        <class 'numpy.flatiter'>
        >>> for item in fl:
        ...     print(item)
        ...
        0
        1
        2
        3
        4
        5

        >>> fl[2:4]
        array([2, 3])
    """
    @staticmethod
    def copy(*args, **kwargs) -> typing.Any: 
        """
        Get a copy of the iterator as a 1-D array.

        Examples
        --------
        >>> x = np.arange(6).reshape(2, 3)
        >>> x
        array([[0, 1, 2],
               [3, 4, 5]])
        >>> fl = x.flat
        >>> fl.copy()
        array([0, 1, 2, 3, 4, 5])
        """
    __hash__ = None
    base: member_descriptor # value = <member 'base' of 'numpy.flatiter' objects>
    coords: getset_descriptor # value = <attribute 'coords' of 'numpy.flatiter' objects>
    index: getset_descriptor # value = <attribute 'index' of 'numpy.flatiter' objects>
    pass
class ndarray():
    """
    ndarray(shape, dtype=float, buffer=None, offset=0,
                strides=None, order=None)

        An array object represents a multidimensional, homogeneous array
        of fixed-size items.  An associated data-type object describes the
        format of each element in the array (its byte-order, how many bytes it
        occupies in memory, whether it is an integer, a floating point number,
        or something else, etc.)

        Arrays should be constructed using `array`, `zeros` or `empty` (refer
        to the See Also section below).  The parameters given here refer to
        a low-level method (`ndarray(...)`) for instantiating an array.

        For more information, refer to the `numpy` module and examine the
        methods and attributes of an array.

        Parameters
        ----------
        (for the __new__ method; see Notes below)

        shape : tuple of ints
            Shape of created array.
        dtype : data-type, optional
            Any object that can be interpreted as a numpy data type.
        buffer : object exposing buffer interface, optional
            Used to fill the array with data.
        offset : int, optional
            Offset of array data in buffer.
        strides : tuple of ints, optional
            Strides of data in memory.
        order : {'C', 'F'}, optional
            Row-major (C-style) or column-major (Fortran-style) order.

        Attributes
        ----------
        T : ndarray
            Transpose of the array.
        data : buffer
            The array's elements, in memory.
        dtype : dtype object
            Describes the format of the elements in the array.
        flags : dict
            Dictionary containing information related to memory use, e.g.,
            'C_CONTIGUOUS', 'OWNDATA', 'WRITEABLE', etc.
        flat : numpy.flatiter object
            Flattened version of the array as an iterator.  The iterator
            allows assignments, e.g., ``x.flat = 3`` (See `ndarray.flat` for
            assignment examples; TODO).
        imag : ndarray
            Imaginary part of the array.
        real : ndarray
            Real part of the array.
        size : int
            Number of elements in the array.
        itemsize : int
            The memory use of each array element in bytes.
        nbytes : int
            The total number of bytes required to store the array data,
            i.e., ``itemsize * size``.
        ndim : int
            The array's number of dimensions.
        shape : tuple of ints
            Shape of the array.
        strides : tuple of ints
            The step-size required to move from one element to the next in
            memory. For example, a contiguous ``(3, 4)`` array of type
            ``int16`` in C-order has strides ``(8, 2)``.  This implies that
            to move from element to element in memory requires jumps of 2 bytes.
            To move from row-to-row, one needs to jump 8 bytes at a time
            (``2 * 4``).
        ctypes : ctypes object
            Class containing properties of the array needed for interaction
            with ctypes.
        base : ndarray
            If the array is a view into another array, that array is its `base`
            (unless that array is also a view).  The `base` array is where the
            array data is actually stored.

        See Also
        --------
        array : Construct an array.
        zeros : Create an array, each element of which is zero.
        empty : Create an array, but leave its allocated memory unchanged (i.e.,
                it contains "garbage").
        dtype : Create a data-type.
        numpy.typing.NDArray : An ndarray alias :term:`generic <generic type>`
                               w.r.t. its `dtype.type <numpy.dtype.type>`.

        Notes
        -----
        There are two modes of creating an array using ``__new__``:

        1. If `buffer` is None, then only `shape`, `dtype`, and `order`
           are used.
        2. If `buffer` is an object exposing the buffer interface, then
           all keywords are interpreted.

        No ``__init__`` method is needed because the array is fully initialized
        after the ``__new__`` method.

        Examples
        --------
        These examples illustrate the low-level `ndarray` constructor.  Refer
        to the `See Also` section above for easier ways of constructing an
        ndarray.

        First mode, `buffer` is None:

        >>> np.ndarray(shape=(2,2), dtype=float, order='F')
        array([[0.0e+000, 0.0e+000], # random
               [     nan, 2.5e-323]])

        Second mode:

        >>> np.ndarray((2,), buffer=np.array([1,2,3]),
        ...            offset=np.int_().itemsize,
        ...            dtype=int) # offset = 1*itemsize, i.e. skip first element
        array([2, 3])
    """
    @staticmethod
    def all(*args, **kwargs) -> typing.Any: 
        """
        a.all(axis=None, out=None, keepdims=False, *, where=True)

            Returns True if all elements evaluate to True.

            Refer to `numpy.all` for full documentation.

            See Also
            --------
            numpy.all : equivalent function
        """
    @staticmethod
    def any(*args, **kwargs) -> typing.Any: 
        """
        a.any(axis=None, out=None, keepdims=False, *, where=True)

            Returns True if any of the elements of `a` evaluate to True.

            Refer to `numpy.any` for full documentation.

            See Also
            --------
            numpy.any : equivalent function
        """
    @staticmethod
    def argmax(*args, **kwargs) -> typing.Any: 
        """
        a.argmax(axis=None, out=None, *, keepdims=False)

            Return indices of the maximum values along the given axis.

            Refer to `numpy.argmax` for full documentation.

            See Also
            --------
            numpy.argmax : equivalent function
        """
    @staticmethod
    def argmin(*args, **kwargs) -> typing.Any: 
        """
        a.argmin(axis=None, out=None, *, keepdims=False)

            Return indices of the minimum values along the given axis.

            Refer to `numpy.argmin` for detailed documentation.

            See Also
            --------
            numpy.argmin : equivalent function
        """
    @staticmethod
    def argpartition(*args, **kwargs) -> typing.Any: 
        """
        a.argpartition(kth, axis=-1, kind='introselect', order=None)

            Returns the indices that would partition this array.

            Refer to `numpy.argpartition` for full documentation.

            .. versionadded:: 1.8.0

            See Also
            --------
            numpy.argpartition : equivalent function
        """
    @staticmethod
    def argsort(*args, **kwargs) -> typing.Any: 
        """
        a.argsort(axis=-1, kind=None, order=None)

            Returns the indices that would sort this array.

            Refer to `numpy.argsort` for full documentation.

            See Also
            --------
            numpy.argsort : equivalent function
        """
    @staticmethod
    def astype(*args, **kwargs) -> typing.Any: 
        """
        a.astype(dtype, order='K', casting='unsafe', subok=True, copy=True)

            Copy of the array, cast to a specified type.

            Parameters
            ----------
            dtype : str or dtype
                Typecode or data-type to which the array is cast.
            order : {'C', 'F', 'A', 'K'}, optional
                Controls the memory layout order of the result.
                'C' means C order, 'F' means Fortran order, 'A'
                means 'F' order if all the arrays are Fortran contiguous,
                'C' order otherwise, and 'K' means as close to the
                order the array elements appear in memory as possible.
                Default is 'K'.
            casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
                Controls what kind of data casting may occur. Defaults to 'unsafe'
                for backwards compatibility.

                  * 'no' means the data types should not be cast at all.
                  * 'equiv' means only byte-order changes are allowed.
                  * 'safe' means only casts which can preserve values are allowed.
                  * 'same_kind' means only safe casts or casts within a kind,
                    like float64 to float32, are allowed.
                  * 'unsafe' means any data conversions may be done.
            subok : bool, optional
                If True, then sub-classes will be passed-through (default), otherwise
                the returned array will be forced to be a base-class array.
            copy : bool, optional
                By default, astype always returns a newly allocated array. If this
                is set to false, and the `dtype`, `order`, and `subok`
                requirements are satisfied, the input array is returned instead
                of a copy.

            Returns
            -------
            arr_t : ndarray
                Unless `copy` is False and the other conditions for returning the input
                array are satisfied (see description for `copy` input parameter), `arr_t`
                is a new array of the same shape as the input array, with dtype, order
                given by `dtype`, `order`.

            Notes
            -----
            .. versionchanged:: 1.17.0
               Casting between a simple data type and a structured one is possible only
               for "unsafe" casting.  Casting to multiple fields is allowed, but
               casting from multiple fields is not.

            .. versionchanged:: 1.9.0
               Casting from numeric to string types in 'safe' casting mode requires
               that the string dtype length is long enough to store the max
               integer/float value converted.

            Raises
            ------
            ComplexWarning
                When casting from complex to float or int. To avoid this,
                one should use ``a.real.astype(t)``.

            Examples
            --------
            >>> x = np.array([1, 2, 2.5])
            >>> x
            array([1. ,  2. ,  2.5])

            >>> x.astype(int)
            array([1, 2, 2])
        """
    @staticmethod
    def byteswap(*args, **kwargs) -> typing.Any: 
        """
        a.byteswap(inplace=False)

            Swap the bytes of the array elements

            Toggle between low-endian and big-endian data representation by
            returning a byteswapped array, optionally swapped in-place.
            Arrays of byte-strings are not swapped. The real and imaginary
            parts of a complex number are swapped individually.

            Parameters
            ----------
            inplace : bool, optional
                If ``True``, swap bytes in-place, default is ``False``.

            Returns
            -------
            out : ndarray
                The byteswapped array. If `inplace` is ``True``, this is
                a view to self.

            Examples
            --------
            >>> A = np.array([1, 256, 8755], dtype=np.int16)
            >>> list(map(hex, A))
            ['0x1', '0x100', '0x2233']
            >>> A.byteswap(inplace=True)
            array([  256,     1, 13090], dtype=int16)
            >>> list(map(hex, A))
            ['0x100', '0x1', '0x3322']

            Arrays of byte-strings are not swapped

            >>> A = np.array([b'ceg', b'fac'])
            >>> A.byteswap()
            array([b'ceg', b'fac'], dtype='|S3')

            ``A.newbyteorder().byteswap()`` produces an array with the same values
              but different representation in memory

            >>> A = np.array([1, 2, 3])
            >>> A.view(np.uint8)
            array([1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0,
                   0, 0], dtype=uint8)
            >>> A.newbyteorder().byteswap(inplace=True)
            array([1, 2, 3])
            >>> A.view(np.uint8)
            array([0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0,
                   0, 3], dtype=uint8)
        """
    @staticmethod
    def choose(*args, **kwargs) -> typing.Any: 
        """
        a.choose(choices, out=None, mode='raise')

            Use an index array to construct a new array from a set of choices.

            Refer to `numpy.choose` for full documentation.

            See Also
            --------
            numpy.choose : equivalent function
        """
    @staticmethod
    def clip(*args, **kwargs) -> typing.Any: 
        """
        a.clip(min=None, max=None, out=None, **kwargs)

            Return an array whose values are limited to ``[min, max]``.
            One of max or min must be given.

            Refer to `numpy.clip` for full documentation.

            See Also
            --------
            numpy.clip : equivalent function
        """
    @staticmethod
    def compress(*args, **kwargs) -> typing.Any: 
        """
        a.compress(condition, axis=None, out=None)

            Return selected slices of this array along given axis.

            Refer to `numpy.compress` for full documentation.

            See Also
            --------
            numpy.compress : equivalent function
        """
    @staticmethod
    def conj(*args, **kwargs) -> typing.Any: 
        """
        a.conj()

            Complex-conjugate all elements.

            Refer to `numpy.conjugate` for full documentation.

            See Also
            --------
            numpy.conjugate : equivalent function
        """
    @staticmethod
    def conjugate(*args, **kwargs) -> typing.Any: 
        """
        a.conjugate()

            Return the complex conjugate, element-wise.

            Refer to `numpy.conjugate` for full documentation.

            See Also
            --------
            numpy.conjugate : equivalent function
        """
    @staticmethod
    def copy(*args, **kwargs) -> typing.Any: 
        """
        a.copy(order='C')

            Return a copy of the array.

            Parameters
            ----------
            order : {'C', 'F', 'A', 'K'}, optional
                Controls the memory layout of the copy. 'C' means C-order,
                'F' means F-order, 'A' means 'F' if `a` is Fortran contiguous,
                'C' otherwise. 'K' means match the layout of `a` as closely
                as possible. (Note that this function and :func:`numpy.copy` are very
                similar but have different default values for their order=
                arguments, and this function always passes sub-classes through.)

            See also
            --------
            numpy.copy : Similar function with different default behavior
            numpy.copyto

            Notes
            -----
            This function is the preferred method for creating an array copy.  The
            function :func:`numpy.copy` is similar, but it defaults to using order 'K',
            and will not pass sub-classes through by default.

            Examples
            --------
            >>> x = np.array([[1,2,3],[4,5,6]], order='F')

            >>> y = x.copy()

            >>> x.fill(0)

            >>> x
            array([[0, 0, 0],
                   [0, 0, 0]])

            >>> y
            array([[1, 2, 3],
                   [4, 5, 6]])

            >>> y.flags['C_CONTIGUOUS']
            True
        """
    @staticmethod
    def cumprod(*args, **kwargs) -> typing.Any: 
        """
        a.cumprod(axis=None, dtype=None, out=None)

            Return the cumulative product of the elements along the given axis.

            Refer to `numpy.cumprod` for full documentation.

            See Also
            --------
            numpy.cumprod : equivalent function
        """
    @staticmethod
    def cumsum(*args, **kwargs) -> typing.Any: 
        """
        a.cumsum(axis=None, dtype=None, out=None)

            Return the cumulative sum of the elements along the given axis.

            Refer to `numpy.cumsum` for full documentation.

            See Also
            --------
            numpy.cumsum : equivalent function
        """
    @staticmethod
    def diagonal(*args, **kwargs) -> typing.Any: 
        """
        a.diagonal(offset=0, axis1=0, axis2=1)

            Return specified diagonals. In NumPy 1.9 the returned array is a
            read-only view instead of a copy as in previous NumPy versions.  In
            a future version the read-only restriction will be removed.

            Refer to :func:`numpy.diagonal` for full documentation.

            See Also
            --------
            numpy.diagonal : equivalent function
        """
    @staticmethod
    def dot(*args, **kwargs) -> typing.Any: ...
    @staticmethod
    def dump(*args, **kwargs) -> typing.Any: 
        """
        a.dump(file)

            Dump a pickle of the array to the specified file.
            The array can be read back with pickle.load or numpy.load.

            Parameters
            ----------
            file : str or Path
                A string naming the dump file.

                .. versionchanged:: 1.17.0
                    `pathlib.Path` objects are now accepted.
        """
    @staticmethod
    def dumps(*args, **kwargs) -> typing.Any: 
        """
        a.dumps()

            Returns the pickle of the array as a string.
            pickle.loads will convert the string back to an array.

            Parameters
            ----------
            None
        """
    @staticmethod
    def fill(*args, **kwargs) -> typing.Any: 
        """
        a.fill(value)

            Fill the array with a scalar value.

            Parameters
            ----------
            value : scalar
                All elements of `a` will be assigned this value.

            Examples
            --------
            >>> a = np.array([1, 2])
            >>> a.fill(0)
            >>> a
            array([0, 0])
            >>> a = np.empty(2)
            >>> a.fill(1)
            >>> a
            array([1.,  1.])

            Fill expects a scalar value and always behaves the same as assigning
            to a single array element.  The following is a rare example where this
            distinction is important:

            >>> a = np.array([None, None], dtype=object)
            >>> a[0] = np.array(3)
            >>> a
            array([array(3), None], dtype=object)
            >>> a.fill(np.array(3))
            >>> a
            array([array(3), array(3)], dtype=object)

            Where other forms of assignments will unpack the array being assigned:

            >>> a[...] = np.array(3)
            >>> a
            array([3, 3], dtype=object)
        """
    @staticmethod
    def flatten(*args, **kwargs) -> typing.Any: 
        """
        a.flatten(order='C')

            Return a copy of the array collapsed into one dimension.

            Parameters
            ----------
            order : {'C', 'F', 'A', 'K'}, optional
                'C' means to flatten in row-major (C-style) order.
                'F' means to flatten in column-major (Fortran-
                style) order. 'A' means to flatten in column-major
                order if `a` is Fortran *contiguous* in memory,
                row-major order otherwise. 'K' means to flatten
                `a` in the order the elements occur in memory.
                The default is 'C'.

            Returns
            -------
            y : ndarray
                A copy of the input array, flattened to one dimension.

            See Also
            --------
            ravel : Return a flattened array.
            flat : A 1-D flat iterator over the array.

            Examples
            --------
            >>> a = np.array([[1,2], [3,4]])
            >>> a.flatten()
            array([1, 2, 3, 4])
            >>> a.flatten('F')
            array([1, 3, 2, 4])
        """
    @staticmethod
    def getfield(*args, **kwargs) -> typing.Any: 
        """
        a.getfield(dtype, offset=0)

            Returns a field of the given array as a certain type.

            A field is a view of the array data with a given data-type. The values in
            the view are determined by the given type and the offset into the current
            array in bytes. The offset needs to be such that the view dtype fits in the
            array dtype; for example an array of dtype complex128 has 16-byte elements.
            If taking a view with a 32-bit integer (4 bytes), the offset needs to be
            between 0 and 12 bytes.

            Parameters
            ----------
            dtype : str or dtype
                The data type of the view. The dtype size of the view can not be larger
                than that of the array itself.
            offset : int
                Number of bytes to skip before beginning the element view.

            Examples
            --------
            >>> x = np.diag([1.+1.j]*2)
            >>> x[1, 1] = 2 + 4.j
            >>> x
            array([[1.+1.j,  0.+0.j],
                   [0.+0.j,  2.+4.j]])
            >>> x.getfield(np.float64)
            array([[1.,  0.],
                   [0.,  2.]])

            By choosing an offset of 8 bytes we can select the complex part of the
            array for our view:

            >>> x.getfield(np.float64, offset=8)
            array([[1.,  0.],
                   [0.,  4.]])
        """
    @staticmethod
    def item(*args, **kwargs) -> typing.Any: 
        """
        a.item(*args)

            Copy an element of an array to a standard Python scalar and return it.

            Parameters
            ----------
            \\*args : Arguments (variable number and type)

                * none: in this case, the method only works for arrays
                  with one element (`a.size == 1`), which element is
                  copied into a standard Python scalar object and returned.

                * int_type: this argument is interpreted as a flat index into
                  the array, specifying which element to copy and return.

                * tuple of int_types: functions as does a single int_type argument,
                  except that the argument is interpreted as an nd-index into the
                  array.

            Returns
            -------
            z : Standard Python scalar object
                A copy of the specified element of the array as a suitable
                Python scalar

            Notes
            -----
            When the data type of `a` is longdouble or clongdouble, item() returns
            a scalar array object because there is no available Python scalar that
            would not lose information. Void arrays return a buffer object for item(),
            unless fields are defined, in which case a tuple is returned.

            `item` is very similar to a[args], except, instead of an array scalar,
            a standard Python scalar is returned. This can be useful for speeding up
            access to elements of the array and doing arithmetic on elements of the
            array using Python's optimized math.

            Examples
            --------
            >>> np.random.seed(123)
            >>> x = np.random.randint(9, size=(3, 3))
            >>> x
            array([[2, 2, 6],
                   [1, 3, 6],
                   [1, 0, 1]])
            >>> x.item(3)
            1
            >>> x.item(7)
            0
            >>> x.item((0, 1))
            2
            >>> x.item((2, 2))
            1
        """
    @staticmethod
    def itemset(*args, **kwargs) -> typing.Any: 
        """
        a.itemset(*args)

            Insert scalar into an array (scalar is cast to array's dtype, if possible)

            There must be at least 1 argument, and define the last argument
            as *item*.  Then, ``a.itemset(*args)`` is equivalent to but faster
            than ``a[args] = item``.  The item should be a scalar value and `args`
            must select a single item in the array `a`.

            Parameters
            ----------
            \\*args : Arguments
                If one argument: a scalar, only used in case `a` is of size 1.
                If two arguments: the last argument is the value to be set
                and must be a scalar, the first argument specifies a single array
                element location. It is either an int or a tuple.

            Notes
            -----
            Compared to indexing syntax, `itemset` provides some speed increase
            for placing a scalar into a particular location in an `ndarray`,
            if you must do this.  However, generally this is discouraged:
            among other problems, it complicates the appearance of the code.
            Also, when using `itemset` (and `item`) inside a loop, be sure
            to assign the methods to a local variable to avoid the attribute
            look-up at each loop iteration.

            Examples
            --------
            >>> np.random.seed(123)
            >>> x = np.random.randint(9, size=(3, 3))
            >>> x
            array([[2, 2, 6],
                   [1, 3, 6],
                   [1, 0, 1]])
            >>> x.itemset(4, 0)
            >>> x.itemset((2, 2), 9)
            >>> x
            array([[2, 2, 6],
                   [1, 0, 6],
                   [1, 0, 9]])
        """
    @staticmethod
    def max(*args, **kwargs) -> typing.Any: 
        """
        a.max(axis=None, out=None, keepdims=False, initial=<no value>, where=True)

            Return the maximum along a given axis.

            Refer to `numpy.amax` for full documentation.

            See Also
            --------
            numpy.amax : equivalent function
        """
    @staticmethod
    def mean(*args, **kwargs) -> typing.Any: 
        """
        a.mean(axis=None, dtype=None, out=None, keepdims=False, *, where=True)

            Returns the average of the array elements along given axis.

            Refer to `numpy.mean` for full documentation.

            See Also
            --------
            numpy.mean : equivalent function
        """
    @staticmethod
    def min(*args, **kwargs) -> typing.Any: 
        """
        a.min(axis=None, out=None, keepdims=False, initial=<no value>, where=True)

            Return the minimum along a given axis.

            Refer to `numpy.amin` for full documentation.

            See Also
            --------
            numpy.amin : equivalent function
        """
    @staticmethod
    def newbyteorder(*args, **kwargs) -> typing.Any: 
        """
        arr.newbyteorder(new_order='S', /)

            Return the array with the same data viewed with a different byte order.

            Equivalent to::

                arr.view(arr.dtype.newbytorder(new_order))

            Changes are also made in all fields and sub-arrays of the array data
            type.



            Parameters
            ----------
            new_order : string, optional
                Byte order to force; a value from the byte order specifications
                below. `new_order` codes can be any of:

                * 'S' - swap dtype from current to opposite endian
                * {'<', 'little'} - little endian
                * {'>', 'big'} - big endian
                * {'=', 'native'} - native order, equivalent to `sys.byteorder`
                * {'|', 'I'} - ignore (no change to byte order)

                The default value ('S') results in swapping the current
                byte order.


            Returns
            -------
            new_arr : array
                New array object with the dtype reflecting given change to the
                byte order.
        """
    @staticmethod
    def nonzero(*args, **kwargs) -> typing.Any: 
        """
        a.nonzero()

            Return the indices of the elements that are non-zero.

            Refer to `numpy.nonzero` for full documentation.

            See Also
            --------
            numpy.nonzero : equivalent function
        """
    @staticmethod
    def partition(*args, **kwargs) -> typing.Any: 
        """
        a.partition(kth, axis=-1, kind='introselect', order=None)

            Rearranges the elements in the array in such a way that the value of the
            element in kth position is in the position it would be in a sorted array.
            All elements smaller than the kth element are moved before this element and
            all equal or greater are moved behind it. The ordering of the elements in
            the two partitions is undefined.

            .. versionadded:: 1.8.0

            Parameters
            ----------
            kth : int or sequence of ints
                Element index to partition by. The kth element value will be in its
                final sorted position and all smaller elements will be moved before it
                and all equal or greater elements behind it.
                The order of all elements in the partitions is undefined.
                If provided with a sequence of kth it will partition all elements
                indexed by kth of them into their sorted position at once.

                .. deprecated:: 1.22.0
                    Passing booleans as index is deprecated.
            axis : int, optional
                Axis along which to sort. Default is -1, which means sort along the
                last axis.
            kind : {'introselect'}, optional
                Selection algorithm. Default is 'introselect'.
            order : str or list of str, optional
                When `a` is an array with fields defined, this argument specifies
                which fields to compare first, second, etc. A single field can
                be specified as a string, and not all fields need to be specified,
                but unspecified fields will still be used, in the order in which
                they come up in the dtype, to break ties.

            See Also
            --------
            numpy.partition : Return a partitioned copy of an array.
            argpartition : Indirect partition.
            sort : Full sort.

            Notes
            -----
            See ``np.partition`` for notes on the different algorithms.

            Examples
            --------
            >>> a = np.array([3, 4, 2, 1])
            >>> a.partition(3)
            >>> a
            array([2, 1, 3, 4])

            >>> a.partition((1, 3))
            >>> a
            array([1, 2, 3, 4])
        """
    @staticmethod
    def prod(*args, **kwargs) -> typing.Any: 
        """
        a.prod(axis=None, dtype=None, out=None, keepdims=False, initial=1, where=True)

            Return the product of the array elements over the given axis

            Refer to `numpy.prod` for full documentation.

            See Also
            --------
            numpy.prod : equivalent function
        """
    @staticmethod
    def ptp(*args, **kwargs) -> typing.Any: 
        """
        a.ptp(axis=None, out=None, keepdims=False)

            Peak to peak (maximum - minimum) value along a given axis.

            Refer to `numpy.ptp` for full documentation.

            See Also
            --------
            numpy.ptp : equivalent function
        """
    @staticmethod
    def put(*args, **kwargs) -> typing.Any: 
        """
        a.put(indices, values, mode='raise')

            Set ``a.flat[n] = values[n]`` for all `n` in indices.

            Refer to `numpy.put` for full documentation.

            See Also
            --------
            numpy.put : equivalent function
        """
    @staticmethod
    def ravel(*args, **kwargs) -> typing.Any: 
        """
        a.ravel([order])

            Return a flattened array.

            Refer to `numpy.ravel` for full documentation.

            See Also
            --------
            numpy.ravel : equivalent function

            ndarray.flat : a flat iterator on the array.
        """
    @staticmethod
    def repeat(*args, **kwargs) -> typing.Any: 
        """
        a.repeat(repeats, axis=None)

            Repeat elements of an array.

            Refer to `numpy.repeat` for full documentation.

            See Also
            --------
            numpy.repeat : equivalent function
        """
    @staticmethod
    def reshape(*args, **kwargs) -> typing.Any: 
        """
        a.reshape(shape, order='C')

            Returns an array containing the same data with a new shape.

            Refer to `numpy.reshape` for full documentation.

            See Also
            --------
            numpy.reshape : equivalent function

            Notes
            -----
            Unlike the free function `numpy.reshape`, this method on `ndarray` allows
            the elements of the shape parameter to be passed in as separate arguments.
            For example, ``a.reshape(10, 11)`` is equivalent to
            ``a.reshape((10, 11))``.
        """
    @staticmethod
    def resize(*args, **kwargs) -> typing.Any: 
        """
        a.resize(new_shape, refcheck=True)

            Change shape and size of array in-place.

            Parameters
            ----------
            new_shape : tuple of ints, or `n` ints
                Shape of resized array.
            refcheck : bool, optional
                If False, reference count will not be checked. Default is True.

            Returns
            -------
            None

            Raises
            ------
            ValueError
                If `a` does not own its own data or references or views to it exist,
                and the data memory must be changed.
                PyPy only: will always raise if the data memory must be changed, since
                there is no reliable way to determine if references or views to it
                exist.

            SystemError
                If the `order` keyword argument is specified. This behaviour is a
                bug in NumPy.

            See Also
            --------
            resize : Return a new array with the specified shape.

            Notes
            -----
            This reallocates space for the data area if necessary.

            Only contiguous arrays (data elements consecutive in memory) can be
            resized.

            The purpose of the reference count check is to make sure you
            do not use this array as a buffer for another Python object and then
            reallocate the memory. However, reference counts can increase in
            other ways so if you are sure that you have not shared the memory
            for this array with another Python object, then you may safely set
            `refcheck` to False.

            Examples
            --------
            Shrinking an array: array is flattened (in the order that the data are
            stored in memory), resized, and reshaped:

            >>> a = np.array([[0, 1], [2, 3]], order='C')
            >>> a.resize((2, 1))
            >>> a
            array([[0],
                   [1]])

            >>> a = np.array([[0, 1], [2, 3]], order='F')
            >>> a.resize((2, 1))
            >>> a
            array([[0],
                   [2]])

            Enlarging an array: as above, but missing entries are filled with zeros:

            >>> b = np.array([[0, 1], [2, 3]])
            >>> b.resize(2, 3) # new_shape parameter doesn't have to be a tuple
            >>> b
            array([[0, 1, 2],
                   [3, 0, 0]])

            Referencing an array prevents resizing...

            >>> c = a
            >>> a.resize((1, 1))
            Traceback (most recent call last):
            ...
            ValueError: cannot resize an array that references or is referenced ...

            Unless `refcheck` is False:

            >>> a.resize((1, 1), refcheck=False)
            >>> a
            array([[0]])
            >>> c
            array([[0]])
        """
    @staticmethod
    def round(*args, **kwargs) -> typing.Any: 
        """
        a.round(decimals=0, out=None)

            Return `a` with each element rounded to the given number of decimals.

            Refer to `numpy.around` for full documentation.

            See Also
            --------
            numpy.around : equivalent function
        """
    @staticmethod
    def searchsorted(*args, **kwargs) -> typing.Any: 
        """
        a.searchsorted(v, side='left', sorter=None)

            Find indices where elements of v should be inserted in a to maintain order.

            For full documentation, see `numpy.searchsorted`

            See Also
            --------
            numpy.searchsorted : equivalent function
        """
    @staticmethod
    def setfield(*args, **kwargs) -> typing.Any: 
        """
        a.setfield(val, dtype, offset=0)

            Put a value into a specified place in a field defined by a data-type.

            Place `val` into `a`'s field defined by `dtype` and beginning `offset`
            bytes into the field.

            Parameters
            ----------
            val : object
                Value to be placed in field.
            dtype : dtype object
                Data-type of the field in which to place `val`.
            offset : int, optional
                The number of bytes into the field at which to place `val`.

            Returns
            -------
            None

            See Also
            --------
            getfield

            Examples
            --------
            >>> x = np.eye(3)
            >>> x.getfield(np.float64)
            array([[1.,  0.,  0.],
                   [0.,  1.,  0.],
                   [0.,  0.,  1.]])
            >>> x.setfield(3, np.int32)
            >>> x.getfield(np.int32)
            array([[3, 3, 3],
                   [3, 3, 3],
                   [3, 3, 3]], dtype=int32)
            >>> x
            array([[1.0e+000, 1.5e-323, 1.5e-323],
                   [1.5e-323, 1.0e+000, 1.5e-323],
                   [1.5e-323, 1.5e-323, 1.0e+000]])
            >>> x.setfield(np.eye(3), np.int32)
            >>> x
            array([[1.,  0.,  0.],
                   [0.,  1.,  0.],
                   [0.,  0.,  1.]])
        """
    @staticmethod
    def setflags(*args, **kwargs) -> typing.Any: 
        """
        a.setflags(write=None, align=None, uic=None)

            Set array flags WRITEABLE, ALIGNED, WRITEBACKIFCOPY,
            respectively.

            These Boolean-valued flags affect how numpy interprets the memory
            area used by `a` (see Notes below). The ALIGNED flag can only
            be set to True if the data is actually aligned according to the type.
            The WRITEBACKIFCOPY and flag can never be set
            to True. The flag WRITEABLE can only be set to True if the array owns its
            own memory, or the ultimate owner of the memory exposes a writeable buffer
            interface, or is a string. (The exception for string is made so that
            unpickling can be done without copying memory.)

            Parameters
            ----------
            write : bool, optional
                Describes whether or not `a` can be written to.
            align : bool, optional
                Describes whether or not `a` is aligned properly for its type.
            uic : bool, optional
                Describes whether or not `a` is a copy of another "base" array.

            Notes
            -----
            Array flags provide information about how the memory area used
            for the array is to be interpreted. There are 7 Boolean flags
            in use, only four of which can be changed by the user:
            WRITEBACKIFCOPY, WRITEABLE, and ALIGNED.

            WRITEABLE (W) the data area can be written to;

            ALIGNED (A) the data and strides are aligned appropriately for the hardware
            (as determined by the compiler);

            WRITEBACKIFCOPY (X) this array is a copy of some other array (referenced
            by .base). When the C-API function PyArray_ResolveWritebackIfCopy is
            called, the base array will be updated with the contents of this array.

            All flags can be accessed using the single (upper case) letter as well
            as the full name.

            Examples
            --------
            >>> y = np.array([[3, 1, 7],
            ...               [2, 0, 0],
            ...               [8, 5, 9]])
            >>> y
            array([[3, 1, 7],
                   [2, 0, 0],
                   [8, 5, 9]])
            >>> y.flags
              C_CONTIGUOUS : True
              F_CONTIGUOUS : False
              OWNDATA : True
              WRITEABLE : True
              ALIGNED : True
              WRITEBACKIFCOPY : False
            >>> y.setflags(write=0, align=0)
            >>> y.flags
              C_CONTIGUOUS : True
              F_CONTIGUOUS : False
              OWNDATA : True
              WRITEABLE : False
              ALIGNED : False
              WRITEBACKIFCOPY : False
            >>> y.setflags(uic=1)
            Traceback (most recent call last):
              File "<stdin>", line 1, in <module>
            ValueError: cannot set WRITEBACKIFCOPY flag to True
        """
    @staticmethod
    def sort(*args, **kwargs) -> typing.Any: 
        """
        a.sort(axis=-1, kind=None, order=None)

            Sort an array in-place. Refer to `numpy.sort` for full documentation.

            Parameters
            ----------
            axis : int, optional
                Axis along which to sort. Default is -1, which means sort along the
                last axis.
            kind : {'quicksort', 'mergesort', 'heapsort', 'stable'}, optional
                Sorting algorithm. The default is 'quicksort'. Note that both 'stable'
                and 'mergesort' use timsort under the covers and, in general, the
                actual implementation will vary with datatype. The 'mergesort' option
                is retained for backwards compatibility.

                .. versionchanged:: 1.15.0
                   The 'stable' option was added.

            order : str or list of str, optional
                When `a` is an array with fields defined, this argument specifies
                which fields to compare first, second, etc.  A single field can
                be specified as a string, and not all fields need be specified,
                but unspecified fields will still be used, in the order in which
                they come up in the dtype, to break ties.

            See Also
            --------
            numpy.sort : Return a sorted copy of an array.
            numpy.argsort : Indirect sort.
            numpy.lexsort : Indirect stable sort on multiple keys.
            numpy.searchsorted : Find elements in sorted array.
            numpy.partition: Partial sort.

            Notes
            -----
            See `numpy.sort` for notes on the different sorting algorithms.

            Examples
            --------
            >>> a = np.array([[1,4], [3,1]])
            >>> a.sort(axis=1)
            >>> a
            array([[1, 4],
                   [1, 3]])
            >>> a.sort(axis=0)
            >>> a
            array([[1, 3],
                   [1, 4]])

            Use the `order` keyword to specify a field to use when sorting a
            structured array:

            >>> a = np.array([('a', 2), ('c', 1)], dtype=[('x', 'S1'), ('y', int)])
            >>> a.sort(order='y')
            >>> a
            array([(b'c', 1), (b'a', 2)],
                  dtype=[('x', 'S1'), ('y', '<i8')])
        """
    @staticmethod
    def squeeze(*args, **kwargs) -> typing.Any: 
        """
        a.squeeze(axis=None)

            Remove axes of length one from `a`.

            Refer to `numpy.squeeze` for full documentation.

            See Also
            --------
            numpy.squeeze : equivalent function
        """
    @staticmethod
    def std(*args, **kwargs) -> typing.Any: 
        """
        a.std(axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=True)

            Returns the standard deviation of the array elements along given axis.

            Refer to `numpy.std` for full documentation.

            See Also
            --------
            numpy.std : equivalent function
        """
    @staticmethod
    def sum(*args, **kwargs) -> typing.Any: 
        """
        a.sum(axis=None, dtype=None, out=None, keepdims=False, initial=0, where=True)

            Return the sum of the array elements over the given axis.

            Refer to `numpy.sum` for full documentation.

            See Also
            --------
            numpy.sum : equivalent function
        """
    @staticmethod
    def swapaxes(*args, **kwargs) -> typing.Any: 
        """
        a.swapaxes(axis1, axis2)

            Return a view of the array with `axis1` and `axis2` interchanged.

            Refer to `numpy.swapaxes` for full documentation.

            See Also
            --------
            numpy.swapaxes : equivalent function
        """
    @staticmethod
    def take(*args, **kwargs) -> typing.Any: 
        """
        a.take(indices, axis=None, out=None, mode='raise')

            Return an array formed from the elements of `a` at the given indices.

            Refer to `numpy.take` for full documentation.

            See Also
            --------
            numpy.take : equivalent function
        """
    @staticmethod
    def tobytes(*args, **kwargs) -> typing.Any: 
        """
        a.tobytes(order='C')

            Construct Python bytes containing the raw data bytes in the array.

            Constructs Python bytes showing a copy of the raw contents of
            data memory. The bytes object is produced in C-order by default.
            This behavior is controlled by the ``order`` parameter.

            .. versionadded:: 1.9.0

            Parameters
            ----------
            order : {'C', 'F', 'A'}, optional
                Controls the memory layout of the bytes object. 'C' means C-order,
                'F' means F-order, 'A' (short for *Any*) means 'F' if `a` is
                Fortran contiguous, 'C' otherwise. Default is 'C'.

            Returns
            -------
            s : bytes
                Python bytes exhibiting a copy of `a`'s raw data.

            See also
            --------
            frombuffer
                Inverse of this operation, construct a 1-dimensional array from Python
                bytes.

            Examples
            --------
            >>> x = np.array([[0, 1], [2, 3]], dtype='<u2')
            >>> x.tobytes()
            b'\\x00\\x00\\x01\\x00\\x02\\x00\\x03\\x00'
            >>> x.tobytes('C') == x.tobytes()
            True
            >>> x.tobytes('F')
            b'\\x00\\x00\\x02\\x00\\x01\\x00\\x03\\x00'
        """
    @staticmethod
    def tofile(*args, **kwargs) -> typing.Any: 
        """
        a.tofile(fid, sep="", format="%s")

            Write array to a file as text or binary (default).

            Data is always written in 'C' order, independent of the order of `a`.
            The data produced by this method can be recovered using the function
            fromfile().

            Parameters
            ----------
            fid : file or str or Path
                An open file object, or a string containing a filename.

                .. versionchanged:: 1.17.0
                    `pathlib.Path` objects are now accepted.

            sep : str
                Separator between array items for text output.
                If "" (empty), a binary file is written, equivalent to
                ``file.write(a.tobytes())``.
            format : str
                Format string for text file output.
                Each entry in the array is formatted to text by first converting
                it to the closest Python type, and then using "format" % item.

            Notes
            -----
            This is a convenience function for quick storage of array data.
            Information on endianness and precision is lost, so this method is not a
            good choice for files intended to archive data or transport data between
            machines with different endianness. Some of these problems can be overcome
            by outputting the data as text files, at the expense of speed and file
            size.

            When fid is a file object, array contents are directly written to the
            file, bypassing the file object's ``write`` method. As a result, tofile
            cannot be used with files objects supporting compression (e.g., GzipFile)
            or file-like objects that do not support ``fileno()`` (e.g., BytesIO).
        """
    @staticmethod
    def tolist(*args, **kwargs) -> typing.Any: 
        """
        a.tolist()

            Return the array as an ``a.ndim``-levels deep nested list of Python scalars.

            Return a copy of the array data as a (nested) Python list.
            Data items are converted to the nearest compatible builtin Python type, via
            the `~numpy.ndarray.item` function.

            If ``a.ndim`` is 0, then since the depth of the nested list is 0, it will
            not be a list at all, but a simple Python scalar.

            Parameters
            ----------
            none

            Returns
            -------
            y : object, or list of object, or list of list of object, or ...
                The possibly nested list of array elements.

            Notes
            -----
            The array may be recreated via ``a = np.array(a.tolist())``, although this
            may sometimes lose precision.

            Examples
            --------
            For a 1D array, ``a.tolist()`` is almost the same as ``list(a)``,
            except that ``tolist`` changes numpy scalars to Python scalars:

            >>> a = np.uint32([1, 2])
            >>> a_list = list(a)
            >>> a_list
            [1, 2]
            >>> type(a_list[0])
            <class 'numpy.uint32'>
            >>> a_tolist = a.tolist()
            >>> a_tolist
            [1, 2]
            >>> type(a_tolist[0])
            <class 'int'>

            Additionally, for a 2D array, ``tolist`` applies recursively:

            >>> a = np.array([[1, 2], [3, 4]])
            >>> list(a)
            [array([1, 2]), array([3, 4])]
            >>> a.tolist()
            [[1, 2], [3, 4]]

            The base case for this recursion is a 0D array:

            >>> a = np.array(1)
            >>> list(a)
            Traceback (most recent call last):
              ...
            TypeError: iteration over a 0-d array
            >>> a.tolist()
            1
        """
    @staticmethod
    def tostring(*args, **kwargs) -> typing.Any: 
        """
        a.tostring(order='C')

            A compatibility alias for `tobytes`, with exactly the same behavior.

            Despite its name, it returns `bytes` not `str`\\ s.

            .. deprecated:: 1.19.0
        """
    @staticmethod
    def trace(*args, **kwargs) -> typing.Any: 
        """
        a.trace(offset=0, axis1=0, axis2=1, dtype=None, out=None)

            Return the sum along diagonals of the array.

            Refer to `numpy.trace` for full documentation.

            See Also
            --------
            numpy.trace : equivalent function
        """
    @staticmethod
    def transpose(*args, **kwargs) -> typing.Any: 
        """
        a.transpose(*axes)

            Returns a view of the array with axes transposed.

            Refer to `numpy.transpose` for full documentation.

            Parameters
            ----------
            axes : None, tuple of ints, or `n` ints

             * None or no argument: reverses the order of the axes.

             * tuple of ints: `i` in the `j`-th place in the tuple means that the
               array's `i`-th axis becomes the transposed array's `j`-th axis.

             * `n` ints: same as an n-tuple of the same ints (this form is
               intended simply as a "convenience" alternative to the tuple form).

            Returns
            -------
            p : ndarray
                View of the array with its axes suitably permuted.

            See Also
            --------
            transpose : Equivalent function.
            ndarray.T : Array property returning the array transposed.
            ndarray.reshape : Give a new shape to an array without changing its data.

            Examples
            --------
            >>> a = np.array([[1, 2], [3, 4]])
            >>> a
            array([[1, 2],
                   [3, 4]])
            >>> a.transpose()
            array([[1, 3],
                   [2, 4]])
            >>> a.transpose((1, 0))
            array([[1, 3],
                   [2, 4]])
            >>> a.transpose(1, 0)
            array([[1, 3],
                   [2, 4]])

            >>> a = np.array([1, 2, 3, 4])
            >>> a
            array([1, 2, 3, 4])
            >>> a.transpose()
            array([1, 2, 3, 4])
        """
    @staticmethod
    def var(*args, **kwargs) -> typing.Any: 
        """
        a.var(axis=None, dtype=None, out=None, ddof=0, keepdims=False, *, where=True)

            Returns the variance of the array elements, along given axis.

            Refer to `numpy.var` for full documentation.

            See Also
            --------
            numpy.var : equivalent function
        """
    @staticmethod
    def view(*args, **kwargs) -> typing.Any: 
        """
        a.view([dtype][, type])

            New view of array with the same data.

            .. note::
                Passing None for ``dtype`` is different from omitting the parameter,
                since the former invokes ``dtype(None)`` which is an alias for
                ``dtype('float_')``.

            Parameters
            ----------
            dtype : data-type or ndarray sub-class, optional
                Data-type descriptor of the returned view, e.g., float32 or int16.
                Omitting it results in the view having the same data-type as `a`.
                This argument can also be specified as an ndarray sub-class, which
                then specifies the type of the returned object (this is equivalent to
                setting the ``type`` parameter).
            type : Python type, optional
                Type of the returned view, e.g., ndarray or matrix.  Again, omission
                of the parameter results in type preservation.

            Notes
            -----
            ``a.view()`` is used two different ways:

            ``a.view(some_dtype)`` or ``a.view(dtype=some_dtype)`` constructs a view
            of the array's memory with a different data-type.  This can cause a
            reinterpretation of the bytes of memory.

            ``a.view(ndarray_subclass)`` or ``a.view(type=ndarray_subclass)`` just
            returns an instance of `ndarray_subclass` that looks at the same array
            (same shape, dtype, etc.)  This does not cause a reinterpretation of the
            memory.

            For ``a.view(some_dtype)``, if ``some_dtype`` has a different number of
            bytes per entry than the previous dtype (for example, converting a regular
            array to a structured array), then the last axis of ``a`` must be
            contiguous. This axis will be resized in the result.

            .. versionchanged:: 1.23.0
               Only the last axis needs to be contiguous. Previously, the entire array
               had to be C-contiguous.

            Examples
            --------
            >>> x = np.array([(1, 2)], dtype=[('a', np.int8), ('b', np.int8)])

            Viewing array data using a different type and dtype:

            >>> y = x.view(dtype=np.int16, type=np.matrix)
            >>> y
            matrix([[513]], dtype=int16)
            >>> print(type(y))
            <class 'numpy.matrix'>

            Creating a view on a structured array so it can be used in calculations

            >>> x = np.array([(1, 2),(3,4)], dtype=[('a', np.int8), ('b', np.int8)])
            >>> xv = x.view(dtype=np.int8).reshape(-1,2)
            >>> xv
            array([[1, 2],
                   [3, 4]], dtype=int8)
            >>> xv.mean(0)
            array([2.,  3.])

            Making changes to the view changes the underlying array

            >>> xv[0,1] = 20
            >>> x
            array([(1, 20), (3,  4)], dtype=[('a', 'i1'), ('b', 'i1')])

            Using a view to convert an array to a recarray:

            >>> z = x.view(np.recarray)
            >>> z.a
            array([1, 3], dtype=int8)

            Views share data:

            >>> x[0] = (9, 10)
            >>> z[0]
            (9, 10)

            Views that change the dtype size (bytes per entry) should normally be
            avoided on arrays defined by slices, transposes, fortran-ordering, etc.:

            >>> x = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int16)
            >>> y = x[:, ::2]
            >>> y
            array([[1, 3],
                   [4, 6]], dtype=int16)
            >>> y.view(dtype=[('width', np.int16), ('length', np.int16)])
            Traceback (most recent call last):
                ...
            ValueError: To change to a dtype of a different size, the last axis must be contiguous
            >>> z = y.copy()
            >>> z.view(dtype=[('width', np.int16), ('length', np.int16)])
            array([[(1, 3)],
                   [(4, 6)]], dtype=[('width', '<i2'), ('length', '<i2')])

            However, views that change dtype are totally fine for arrays with a
            contiguous last axis, even if the rest of the axes are not C-contiguous:

            >>> x = np.arange(2 * 3 * 4, dtype=np.int8).reshape(2, 3, 4)
            >>> x.transpose(1, 0, 2).view(np.int16)
            array([[[ 256,  770],
                    [3340, 3854]],
            <BLANKLINE>
                   [[1284, 1798],
                    [4368, 4882]],
            <BLANKLINE>
                   [[2312, 2826],
                    [5396, 5910]]], dtype=int16)
        """
    T: getset_descriptor # value = <attribute 'T' of 'numpy.ndarray' objects>
    __array_interface__: getset_descriptor # value = <attribute '__array_interface__' of 'numpy.ndarray' objects>
    __array_priority__: getset_descriptor # value = <attribute '__array_priority__' of 'numpy.ndarray' objects>
    __array_struct__: getset_descriptor # value = <attribute '__array_struct__' of 'numpy.ndarray' objects>
    __hash__ = None
    base: getset_descriptor # value = <attribute 'base' of 'numpy.ndarray' objects>
    ctypes: getset_descriptor # value = <attribute 'ctypes' of 'numpy.ndarray' objects>
    data: getset_descriptor # value = <attribute 'data' of 'numpy.ndarray' objects>
    dtype: getset_descriptor # value = <attribute 'dtype' of 'numpy.ndarray' objects>
    flags: getset_descriptor # value = <attribute 'flags' of 'numpy.ndarray' objects>
    flat: getset_descriptor # value = <attribute 'flat' of 'numpy.ndarray' objects>
    imag: getset_descriptor # value = <attribute 'imag' of 'numpy.ndarray' objects>
    itemsize: getset_descriptor # value = <attribute 'itemsize' of 'numpy.ndarray' objects>
    nbytes: getset_descriptor # value = <attribute 'nbytes' of 'numpy.ndarray' objects>
    ndim: getset_descriptor # value = <attribute 'ndim' of 'numpy.ndarray' objects>
    real: getset_descriptor # value = <attribute 'real' of 'numpy.ndarray' objects>
    shape: getset_descriptor # value = <attribute 'shape' of 'numpy.ndarray' objects>
    size: getset_descriptor # value = <attribute 'size' of 'numpy.ndarray' objects>
    strides: getset_descriptor # value = <attribute 'strides' of 'numpy.ndarray' objects>
    pass
class nditer():
    """
    nditer(op, flags=None, op_flags=None, op_dtypes=None, order='K', casting='safe', op_axes=None, itershape=None, buffersize=0)

        Efficient multi-dimensional iterator object to iterate over arrays.
        To get started using this object, see the
        :ref:`introductory guide to array iteration <arrays.nditer>`.

        Parameters
        ----------
        op : ndarray or sequence of array_like
            The array(s) to iterate over.

        flags : sequence of str, optional
              Flags to control the behavior of the iterator.

              * ``buffered`` enables buffering when required.
              * ``c_index`` causes a C-order index to be tracked.
              * ``f_index`` causes a Fortran-order index to be tracked.
              * ``multi_index`` causes a multi-index, or a tuple of indices
                with one per iteration dimension, to be tracked.
              * ``common_dtype`` causes all the operands to be converted to
                a common data type, with copying or buffering as necessary.
              * ``copy_if_overlap`` causes the iterator to determine if read
                operands have overlap with write operands, and make temporary
                copies as necessary to avoid overlap. False positives (needless
                copying) are possible in some cases.
              * ``delay_bufalloc`` delays allocation of the buffers until
                a reset() call is made. Allows ``allocate`` operands to
                be initialized before their values are copied into the buffers.
              * ``external_loop`` causes the ``values`` given to be
                one-dimensional arrays with multiple values instead of
                zero-dimensional arrays.
              * ``grow_inner`` allows the ``value`` array sizes to be made
                larger than the buffer size when both ``buffered`` and
                ``external_loop`` is used.
              * ``ranged`` allows the iterator to be restricted to a sub-range
                of the iterindex values.
              * ``refs_ok`` enables iteration of reference types, such as
                object arrays.
              * ``reduce_ok`` enables iteration of ``readwrite`` operands
                which are broadcasted, also known as reduction operands.
              * ``zerosize_ok`` allows `itersize` to be zero.
        op_flags : list of list of str, optional
              This is a list of flags for each operand. At minimum, one of
              ``readonly``, ``readwrite``, or ``writeonly`` must be specified.

              * ``readonly`` indicates the operand will only be read from.
              * ``readwrite`` indicates the operand will be read from and written to.
              * ``writeonly`` indicates the operand will only be written to.
              * ``no_broadcast`` prevents the operand from being broadcasted.
              * ``contig`` forces the operand data to be contiguous.
              * ``aligned`` forces the operand data to be aligned.
              * ``nbo`` forces the operand data to be in native byte order.
              * ``copy`` allows a temporary read-only copy if required.
              * ``updateifcopy`` allows a temporary read-write copy if required.
              * ``allocate`` causes the array to be allocated if it is None
                in the ``op`` parameter.
              * ``no_subtype`` prevents an ``allocate`` operand from using a subtype.
              * ``arraymask`` indicates that this operand is the mask to use
                for selecting elements when writing to operands with the
                'writemasked' flag set. The iterator does not enforce this,
                but when writing from a buffer back to the array, it only
                copies those elements indicated by this mask.
              * ``writemasked`` indicates that only elements where the chosen
                ``arraymask`` operand is True will be written to.
              * ``overlap_assume_elementwise`` can be used to mark operands that are
                accessed only in the iterator order, to allow less conservative
                copying when ``copy_if_overlap`` is present.
        op_dtypes : dtype or tuple of dtype(s), optional
            The required data type(s) of the operands. If copying or buffering
            is enabled, the data will be converted to/from their original types.
        order : {'C', 'F', 'A', 'K'}, optional
            Controls the iteration order. 'C' means C order, 'F' means
            Fortran order, 'A' means 'F' order if all the arrays are Fortran
            contiguous, 'C' order otherwise, and 'K' means as close to the
            order the array elements appear in memory as possible. This also
            affects the element memory order of ``allocate`` operands, as they
            are allocated to be compatible with iteration order.
            Default is 'K'.
        casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
            Controls what kind of data casting may occur when making a copy
            or buffering.  Setting this to 'unsafe' is not recommended,
            as it can adversely affect accumulations.

            * 'no' means the data types should not be cast at all.
            * 'equiv' means only byte-order changes are allowed.
            * 'safe' means only casts which can preserve values are allowed.
            * 'same_kind' means only safe casts or casts within a kind,
              like float64 to float32, are allowed.
            * 'unsafe' means any data conversions may be done.
        op_axes : list of list of ints, optional
            If provided, is a list of ints or None for each operands.
            The list of axes for an operand is a mapping from the dimensions
            of the iterator to the dimensions of the operand. A value of
            -1 can be placed for entries, causing that dimension to be
            treated as `newaxis`.
        itershape : tuple of ints, optional
            The desired shape of the iterator. This allows ``allocate`` operands
            with a dimension mapped by op_axes not corresponding to a dimension
            of a different operand to get a value not equal to 1 for that
            dimension.
        buffersize : int, optional
            When buffering is enabled, controls the size of the temporary
            buffers. Set to 0 for the default value.

        Attributes
        ----------
        dtypes : tuple of dtype(s)
            The data types of the values provided in `value`. This may be
            different from the operand data types if buffering is enabled.
            Valid only before the iterator is closed.
        finished : bool
            Whether the iteration over the operands is finished or not.
        has_delayed_bufalloc : bool
            If True, the iterator was created with the ``delay_bufalloc`` flag,
            and no reset() function was called on it yet.
        has_index : bool
            If True, the iterator was created with either the ``c_index`` or
            the ``f_index`` flag, and the property `index` can be used to
            retrieve it.
        has_multi_index : bool
            If True, the iterator was created with the ``multi_index`` flag,
            and the property `multi_index` can be used to retrieve it.
        index
            When the ``c_index`` or ``f_index`` flag was used, this property
            provides access to the index. Raises a ValueError if accessed
            and ``has_index`` is False.
        iterationneedsapi : bool
            Whether iteration requires access to the Python API, for example
            if one of the operands is an object array.
        iterindex : int
            An index which matches the order of iteration.
        itersize : int
            Size of the iterator.
        itviews
            Structured view(s) of `operands` in memory, matching the reordered
            and optimized iterator access pattern. Valid only before the iterator
            is closed.
        multi_index
            When the ``multi_index`` flag was used, this property
            provides access to the index. Raises a ValueError if accessed
            accessed and ``has_multi_index`` is False.
        ndim : int
            The dimensions of the iterator.
        nop : int
            The number of iterator operands.
        operands : tuple of operand(s)
            The array(s) to be iterated over. Valid only before the iterator is
            closed.
        shape : tuple of ints
            Shape tuple, the shape of the iterator.
        value
            Value of ``operands`` at current iteration. Normally, this is a
            tuple of array scalars, but if the flag ``external_loop`` is used,
            it is a tuple of one dimensional arrays.

        Notes
        -----
        `nditer` supersedes `flatiter`.  The iterator implementation behind
        `nditer` is also exposed by the NumPy C API.

        The Python exposure supplies two iteration interfaces, one which follows
        the Python iterator protocol, and another which mirrors the C-style
        do-while pattern.  The native Python approach is better in most cases, but
        if you need the coordinates or index of an iterator, use the C-style pattern.

        Examples
        --------
        Here is how we might write an ``iter_add`` function, using the
        Python iterator protocol:

        >>> def iter_add_py(x, y, out=None):
        ...     addop = np.add
        ...     it = np.nditer([x, y, out], [],
        ...                 [['readonly'], ['readonly'], ['writeonly','allocate']])
        ...     with it:
        ...         for (a, b, c) in it:
        ...             addop(a, b, out=c)
        ...         return it.operands[2]

        Here is the same function, but following the C-style pattern:

        >>> def iter_add(x, y, out=None):
        ...    addop = np.add
        ...    it = np.nditer([x, y, out], [],
        ...                [['readonly'], ['readonly'], ['writeonly','allocate']])
        ...    with it:
        ...        while not it.finished:
        ...            addop(it[0], it[1], out=it[2])
        ...            it.iternext()
        ...        return it.operands[2]

        Here is an example outer product function:

        >>> def outer_it(x, y, out=None):
        ...     mulop = np.multiply
        ...     it = np.nditer([x, y, out], ['external_loop'],
        ...             [['readonly'], ['readonly'], ['writeonly', 'allocate']],
        ...             op_axes=[list(range(x.ndim)) + [-1] * y.ndim,
        ...                      [-1] * x.ndim + list(range(y.ndim)),
        ...                      None])
        ...     with it:
        ...         for (a, b, c) in it:
        ...             mulop(a, b, out=c)
        ...         return it.operands[2]

        >>> a = np.arange(2)+1
        >>> b = np.arange(3)+1
        >>> outer_it(a,b)
        array([[1, 2, 3],
               [2, 4, 6]])

        Here is an example function which operates like a "lambda" ufunc:

        >>> def luf(lamdaexpr, *args, **kwargs):
        ...    '''luf(lambdaexpr, op1, ..., opn, out=None, order='K', casting='safe', buffersize=0)'''
        ...    nargs = len(args)
        ...    op = (kwargs.get('out',None),) + args
        ...    it = np.nditer(op, ['buffered','external_loop'],
        ...            [['writeonly','allocate','no_broadcast']] +
        ...                            [['readonly','nbo','aligned']]*nargs,
        ...            order=kwargs.get('order','K'),
        ...            casting=kwargs.get('casting','safe'),
        ...            buffersize=kwargs.get('buffersize',0))
        ...    while not it.finished:
        ...        it[0] = lamdaexpr(*it[1:])
        ...        it.iternext()
        ...    return it.operands[0]

        >>> a = np.arange(5)
        >>> b = np.ones(5)
        >>> luf(lambda i,j:i*i + j/2, a, b)
        array([  0.5,   1.5,   4.5,   9.5,  16.5])

        If operand flags ``"writeonly"`` or ``"readwrite"`` are used the
        operands may be views into the original data with the
        `WRITEBACKIFCOPY` flag. In this case `nditer` must be used as a
        context manager or the `nditer.close` method must be called before
        using the result. The temporary data will be written back to the
        original data when the `__exit__` function is called but not before:

        >>> a = np.arange(6, dtype='i4')[::-2]
        >>> with np.nditer(a, [],
        ...        [['writeonly', 'updateifcopy']],
        ...        casting='unsafe',
        ...        op_dtypes=[np.dtype('f4')]) as i:
        ...    x = i.operands[0]
        ...    x[:] = [-1, -2, -3]
        ...    # a still unchanged here
        >>> a, x
        (array([-1, -2, -3], dtype=int32), array([-1., -2., -3.], dtype=float32))

        It is important to note that once the iterator is exited, dangling
        references (like `x` in the example) may or may not share data with
        the original data `a`. If writeback semantics were active, i.e. if
        `x.base.flags.writebackifcopy` is `True`, then exiting the iterator
        will sever the connection between `x` and `a`, writing to `x` will
        no longer write to `a`. If writeback semantics are not active, then
        `x.data` will still point at some part of `a.data`, and writing to
        one will affect the other.

        Context management and the `close` method appeared in version 1.15.0.
    """
    @staticmethod
    def close(*args, **kwargs) -> typing.Any: 
        """
        Resolve all writeback semantics in writeable operands.

        .. versionadded:: 1.15.0

        See Also
        --------

        :ref:`nditer-context-manager`
        """
    @staticmethod
    def copy(*args, **kwargs) -> typing.Any: 
        """
        Get a copy of the iterator in its current state.

        Examples
        --------
        >>> x = np.arange(10)
        >>> y = x + 1
        >>> it = np.nditer([x, y])
        >>> next(it)
        (array(0), array(1))
        >>> it2 = it.copy()
        >>> next(it2)
        (array(1), array(2))
        """
    @staticmethod
    def debug_print(*args, **kwargs) -> typing.Any: 
        """
        Print the current state of the `nditer` instance and debug info to stdout.
        """
    @staticmethod
    def enable_external_loop(*args, **kwargs) -> typing.Any: 
        """
        When the "external_loop" was not used during construction, but
        is desired, this modifies the iterator to behave as if the flag
        was specified.
        """
    @staticmethod
    def iternext(*args, **kwargs) -> typing.Any: 
        """
        Check whether iterations are left, and perform a single internal iteration
        without returning the result.  Used in the C-style pattern do-while
        pattern.  For an example, see `nditer`.

        Returns
        -------
        iternext : bool
            Whether or not there are iterations left.
        """
    @staticmethod
    def remove_axis(*args, **kwargs) -> typing.Any: 
        """
        Removes axis `i` from the iterator. Requires that the flag "multi_index"
        be enabled.
        """
    @staticmethod
    def remove_multi_index(*args, **kwargs) -> typing.Any: 
        """
        When the "multi_index" flag was specified, this removes it, allowing
        the internal iteration structure to be optimized further.
        """
    @staticmethod
    def reset(*args, **kwargs) -> typing.Any: 
        """
        Reset the iterator to its initial state.
        """
    dtypes: getset_descriptor # value = <attribute 'dtypes' of 'numpy.nditer' objects>
    finished: getset_descriptor # value = <attribute 'finished' of 'numpy.nditer' objects>
    has_delayed_bufalloc: getset_descriptor # value = <attribute 'has_delayed_bufalloc' of 'numpy.nditer' objects>
    has_index: getset_descriptor # value = <attribute 'has_index' of 'numpy.nditer' objects>
    has_multi_index: getset_descriptor # value = <attribute 'has_multi_index' of 'numpy.nditer' objects>
    index: getset_descriptor # value = <attribute 'index' of 'numpy.nditer' objects>
    iterationneedsapi: getset_descriptor # value = <attribute 'iterationneedsapi' of 'numpy.nditer' objects>
    iterindex: getset_descriptor # value = <attribute 'iterindex' of 'numpy.nditer' objects>
    iterrange: getset_descriptor # value = <attribute 'iterrange' of 'numpy.nditer' objects>
    itersize: getset_descriptor # value = <attribute 'itersize' of 'numpy.nditer' objects>
    itviews: getset_descriptor # value = <attribute 'itviews' of 'numpy.nditer' objects>
    multi_index: getset_descriptor # value = <attribute 'multi_index' of 'numpy.nditer' objects>
    ndim: getset_descriptor # value = <attribute 'ndim' of 'numpy.nditer' objects>
    nop: getset_descriptor # value = <attribute 'nop' of 'numpy.nditer' objects>
    operands: getset_descriptor # value = <attribute 'operands' of 'numpy.nditer' objects>
    shape: getset_descriptor # value = <attribute 'shape' of 'numpy.nditer' objects>
    value: getset_descriptor # value = <attribute 'value' of 'numpy.nditer' objects>
    pass
def _add_newdoc_ufunc(*args, **kwargs) -> typing.Any:
    """
    Replace the docstring for a ufunc with new_docstring.
    This method will only work if the current docstring for
    the ufunc is NULL. (At the C level, i.e. when ufunc->doc is NULL.)

    Parameters
    ----------
    ufunc : numpy.ufunc
        A ufunc whose current doc is NULL.
    new_docstring : string
        The new docstring for the ufunc.

    Notes
    -----
    This method allocates memory for new_docstring on
    the heap. Technically this creates a mempory leak, since this
    memory will not be reclaimed until the end of the program
    even if the ufunc itself is removed. However this will only
    be a problem if the user is repeatedly creating ufuncs with
    no documentation, adding documentation via add_newdoc_ufunc,
    and then throwing away the ufunc.
    """
def _discover_array_parameters(*args, **kwargs) -> typing.Any:
    pass
def _get_castingimpl(*args, **kwargs) -> typing.Any:
    pass
def _get_experimental_dtype_api(*args, **kwargs) -> typing.Any:
    pass
def _get_implementing_args(*args, **kwargs) -> typing.Any:
    """
    Collect arguments on which to call __array_function__.

    Parameters
    ----------
    relevant_args : iterable of array-like
        Iterable of possibly array-like arguments to check for
        __array_function__ methods.

    Returns
    -------
    Sequence of arguments with __array_function__ methods, in the order in
    which they should be called.
    """
def _get_madvise_hugepage() -> bool:
    """
    Get use of ``madvise (2)`` MADV_HUGEPAGE support when
    allocating the array data. Returns the currently set value.
    See `global_state` for more information.
    """
def _get_ndarray_c_version(*args, **kwargs) -> typing.Any:
    """
    Return the compile time NPY_VERSION (formerly called NDARRAY_VERSION) number.
    """
def _get_promotion_state(*args, **kwargs) -> typing.Any:
    """
    Get the current NEP 50 promotion state.
    """
def _get_sfloat_dtype(*args, **kwargs) -> typing.Any:
    pass
def _load_from_filelike(*args, **kwargs) -> typing.Any:
    pass
def _monotonicity(*args, **kwargs) -> typing.Any:
    pass
def _place(*args, **kwargs) -> typing.Any:
    """
    Insert vals sequentially into equivalent 1-d positions indicated by mask.
    """
def _reconstruct(*args, **kwargs) -> typing.Any:
    """
    Construct an empty array. Used by Pickles.
    """
def _reload_guard(*args, **kwargs) -> typing.Any:
    """
    Give a warning on reload and big warning in sub-interpreters.
    """
def _set_madvise_hugepage(enabled: bool) -> bool:
    """
    Set  or unset use of ``madvise (2)`` MADV_HUGEPAGE support when
    allocating the array data. Returns the previously set value.
    See `global_state` for more information.
    """
def _set_numpy_warn_if_no_mem_policy(*args, **kwargs) -> typing.Any:
    """
    Change the warn if no mem policy flag for testing.
    """
def _set_promotion_state(*args, **kwargs) -> typing.Any:
    """
    Set the NEP 50 promotion state.  This is not thread-safe.
    The optional warnings can be safely silenced using the 
    `np._no_nep50_warning()` context manager.
    """
def _using_numpy2_behavior(*args, **kwargs) -> typing.Any:
    pass
def _vec_string(*args, **kwargs) -> typing.Any:
    pass
def add_docstring(*args, **kwargs) -> typing.Any:
    """
    Add a docstring to a built-in obj if possible.
    If the obj already has a docstring raise a RuntimeError
    If this routine does not know how to add a docstring to the object
    raise a TypeError
    """
def arange(*args, **kwargs) -> typing.Any:
    """
    Return evenly spaced values within a given interval.

    ``arange`` can be called with a varying number of positional arguments:

    * ``arange(stop)``: Values are generated within the half-open interval
      ``[0, stop)`` (in other words, the interval including `start` but
      excluding `stop`).
    * ``arange(start, stop)``: Values are generated within the half-open
      interval ``[start, stop)``.
    * ``arange(start, stop, step)`` Values are generated within the half-open
      interval ``[start, stop)``, with spacing between values given by
      ``step``.

    For integer arguments the function is roughly equivalent to the Python
    built-in :py:class:`range`, but returns an ndarray rather than a ``range``
    instance.

    When using a non-integer step, such as 0.1, it is often better to use
    `numpy.linspace`.

    See the Warning sections below for more information.

    Parameters
    ----------
    start : integer or real, optional
        Start of interval.  The interval includes this value.  The default
        start value is 0.
    stop : integer or real
        End of interval.  The interval does not include this value, except
        in some cases where `step` is not an integer and floating point
        round-off affects the length of `out`.
    step : integer or real, optional
        Spacing between values.  For any output `out`, this is the distance
        between two adjacent values, ``out[i+1] - out[i]``.  The default
        step size is 1.  If `step` is specified as a position argument,
        `start` must also be given.
    dtype : dtype, optional
        The type of the output array.  If `dtype` is not given, infer the data
        type from the other input arguments.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    arange : ndarray
        Array of evenly spaced values.

        For floating point arguments, the length of the result is
        ``ceil((stop - start)/step)``.  Because of floating point overflow,
        this rule may result in the last element of `out` being greater
        than `stop`.

    Warnings
    --------
    The length of the output might not be numerically stable.

    Another stability issue is due to the internal implementation of
    `numpy.arange`.
    The actual step value used to populate the array is
    ``dtype(start + step) - dtype(start)`` and not `step`. Precision loss
    can occur here, due to casting or due to using floating points when
    `start` is much larger than `step`. This can lead to unexpected
    behaviour. For example::

      >>> np.arange(0, 5, 0.5, dtype=int)
      array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
      >>> np.arange(-3, 3, 0.5, dtype=int)
      array([-3, -2, -1,  0,  1,  2,  3,  4,  5,  6,  7,  8])

    In such cases, the use of `numpy.linspace` should be preferred.

    The built-in :py:class:`range` generates :std:doc:`Python built-in integers
    that have arbitrary size <python:c-api/long>`, while `numpy.arange`
    produces `numpy.int32` or `numpy.int64` numbers. This may result in
    incorrect results for large integer values::

      >>> power = 40
      >>> modulo = 10000
      >>> x1 = [(n ** power) % modulo for n in range(8)]
      >>> x2 = [(n ** power) % modulo for n in np.arange(8)]
      >>> print(x1)
      [0, 1, 7776, 8801, 6176, 625, 6576, 4001]  # correct
      >>> print(x2)
      [0, 1, 7776, 7185, 0, 5969, 4816, 3361]  # incorrect

    See Also
    --------
    numpy.linspace : Evenly spaced numbers with careful handling of endpoints.
    numpy.ogrid: Arrays of evenly spaced numbers in N-dimensions.
    numpy.mgrid: Grid-shaped arrays of evenly spaced numbers in N-dimensions.
    :ref:`how-to-partition`

    Examples
    --------
    >>> np.arange(3)
    array([0, 1, 2])
    >>> np.arange(3.0)
    array([ 0.,  1.,  2.])
    >>> np.arange(3,7)
    array([3, 4, 5, 6])
    >>> np.arange(3,7,2)
    array([3, 5])
    """
def array(*args, **kwargs) -> typing.Any:
    """
    array(object, dtype=None, *, copy=True, order='K', subok=False, ndmin=0,
              like=None)

        Create an array.

        Parameters
        ----------
        object : array_like
            An array, any object exposing the array interface, an object whose
            ``__array__`` method returns an array, or any (nested) sequence.
            If object is a scalar, a 0-dimensional array containing object is
            returned.
        dtype : data-type, optional
            The desired data-type for the array. If not given, NumPy will try to use
            a default ``dtype`` that can represent the values (by applying promotion
            rules when necessary.)
        copy : bool, optional
            If true (default), then the object is copied.  Otherwise, a copy will
            only be made if ``__array__`` returns a copy, if obj is a nested
            sequence, or if a copy is needed to satisfy any of the other
            requirements (``dtype``, ``order``, etc.).
        order : {'K', 'A', 'C', 'F'}, optional
            Specify the memory layout of the array. If object is not an array, the
            newly created array will be in C order (row major) unless 'F' is
            specified, in which case it will be in Fortran order (column major).
            If object is an array the following holds.

            ===== ========= ===================================================
            order  no copy                     copy=True
            ===== ========= ===================================================
            'K'   unchanged F & C order preserved, otherwise most similar order
            'A'   unchanged F order if input is F and not C, otherwise C order
            'C'   C order   C order
            'F'   F order   F order
            ===== ========= ===================================================

            When ``copy=False`` and a copy is made for other reasons, the result is
            the same as if ``copy=True``, with some exceptions for 'A', see the
            Notes section. The default order is 'K'.
        subok : bool, optional
            If True, then sub-classes will be passed-through, otherwise
            the returned array will be forced to be a base-class array (default).
        ndmin : int, optional
            Specifies the minimum number of dimensions that the resulting
            array should have.  Ones will be prepended to the shape as
            needed to meet this requirement.
        like : array_like, optional
            Reference object to allow the creation of arrays which are not
            NumPy arrays. If an array-like passed in as ``like`` supports
            the ``__array_function__`` protocol, the result will be defined
            by it. In this case, it ensures the creation of an array object
            compatible with that passed in via this argument.

            .. versionadded:: 1.20.0

        Returns
        -------
        out : ndarray
            An array object satisfying the specified requirements.

        See Also
        --------
        empty_like : Return an empty array with shape and type of input.
        ones_like : Return an array of ones with shape and type of input.
        zeros_like : Return an array of zeros with shape and type of input.
        full_like : Return a new array with shape of input filled with value.
        empty : Return a new uninitialized array.
        ones : Return a new array setting values to one.
        zeros : Return a new array setting values to zero.
        full : Return a new array of given shape filled with value.


        Notes
        -----
        When order is 'A' and ``object`` is an array in neither 'C' nor 'F' order,
        and a copy is forced by a change in dtype, then the order of the result is
        not necessarily 'C' as expected. This is likely a bug.

        Examples
        --------
        >>> np.array([1, 2, 3])
        array([1, 2, 3])

        Upcasting:

        >>> np.array([1, 2, 3.0])
        array([ 1.,  2.,  3.])

        More than one dimension:

        >>> np.array([[1, 2], [3, 4]])
        array([[1, 2],
               [3, 4]])

        Minimum dimensions 2:

        >>> np.array([1, 2, 3], ndmin=2)
        array([[1, 2, 3]])

        Type provided:

        >>> np.array([1, 2, 3], dtype=complex)
        array([ 1.+0.j,  2.+0.j,  3.+0.j])

        Data-type consisting of more than one element:

        >>> x = np.array([(1,2),(3,4)],dtype=[('a','<i4'),('b','<i4')])
        >>> x['a']
        array([1, 3])

        Creating an array from sub-classes:

        >>> np.array(np.mat('1 2; 3 4'))
        array([[1, 2],
               [3, 4]])

        >>> np.array(np.mat('1 2; 3 4'), subok=True)
        matrix([[1, 2],
                [3, 4]])
    """
def asanyarray(*args, **kwargs) -> typing.Any:
    """
    Convert the input to an ndarray, but pass ndarray subclasses through.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes scalars, lists, lists of tuples, tuples, tuples of tuples,
        tuples of lists, and ndarrays.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F', 'A', 'K'}, optional
        Memory layout.  'A' and 'K' depend on the order of input array a.
        'C' row-major (C-style),
        'F' column-major (Fortran-style) memory representation.
        'A' (any) means 'F' if `a` is Fortran contiguous, 'C' otherwise
        'K' (keep) preserve input order
        Defaults to 'C'.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray or an ndarray subclass
        Array interpretation of `a`.  If `a` is an ndarray or a subclass
        of ndarray, it is returned as-is and no copy is performed.

    See Also
    --------
    asarray : Similar function which always returns ndarrays.
    ascontiguousarray : Convert input to a contiguous array.
    asfarray : Convert input to a floating point ndarray.
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    asarray_chkfinite : Similar function which checks input for NaNs and
                        Infs.
    fromiter : Create an array from an iterator.
    fromfunction : Construct an array by executing a function on grid
                   positions.

    Examples
    --------
    Convert a list into an array:

    >>> a = [1, 2]
    >>> np.asanyarray(a)
    array([1, 2])

    Instances of `ndarray` subclasses are passed through as-is:

    >>> a = np.array([(1.0, 2), (3.0, 4)], dtype='f4,i4').view(np.recarray)
    >>> np.asanyarray(a) is a
    True
    """
def asarray(*args, **kwargs) -> typing.Any:
    """
    Convert the input to an array.

    Parameters
    ----------
    a : array_like
        Input data, in any form that can be converted to an array.  This
        includes lists, lists of tuples, tuples, tuples of tuples, tuples
        of lists and ndarrays.
    dtype : data-type, optional
        By default, the data-type is inferred from the input data.
    order : {'C', 'F', 'A', 'K'}, optional
        Memory layout.  'A' and 'K' depend on the order of input array a.
        'C' row-major (C-style),
        'F' column-major (Fortran-style) memory representation.
        'A' (any) means 'F' if `a` is Fortran contiguous, 'C' otherwise
        'K' (keep) preserve input order
        Defaults to 'K'.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Array interpretation of `a`.  No copy is performed if the input
        is already an ndarray with matching dtype and order.  If `a` is a
        subclass of ndarray, a base class ndarray is returned.

    See Also
    --------
    asanyarray : Similar function which passes through subclasses.
    ascontiguousarray : Convert input to a contiguous array.
    asfarray : Convert input to a floating point ndarray.
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    asarray_chkfinite : Similar function which checks input for NaNs and Infs.
    fromiter : Create an array from an iterator.
    fromfunction : Construct an array by executing a function on grid
                   positions.

    Examples
    --------
    Convert a list into an array:

    >>> a = [1, 2]
    >>> np.asarray(a)
    array([1, 2])

    Existing arrays are not copied:

    >>> a = np.array([1, 2])
    >>> np.asarray(a) is a
    True

    If `dtype` is set, array is copied only if dtype does not match:

    >>> a = np.array([1, 2], dtype=np.float32)
    >>> np.asarray(a, dtype=np.float32) is a
    True
    >>> np.asarray(a, dtype=np.float64) is a
    False

    Contrary to `asanyarray`, ndarray subclasses are not passed through:

    >>> issubclass(np.recarray, np.ndarray)
    True
    >>> a = np.array([(1.0, 2), (3.0, 4)], dtype='f4,i4').view(np.recarray)
    >>> np.asarray(a) is a
    False
    >>> np.asanyarray(a) is a
    True
    """
def ascontiguousarray(*args, **kwargs) -> typing.Any:
    """
    Return a contiguous array (ndim >= 1) in memory (C order).

    Parameters
    ----------
    a : array_like
        Input array.
    dtype : str or dtype object, optional
        Data-type of returned array.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Contiguous array of same shape and content as `a`, with type `dtype`
        if specified.

    See Also
    --------
    asfortranarray : Convert input to an ndarray with column-major
                     memory order.
    require : Return an ndarray that satisfies requirements.
    ndarray.flags : Information about the memory layout of the array.

    Examples
    --------
    Starting with a Fortran-contiguous array:

    >>> x = np.ones((2, 3), order='F')
    >>> x.flags['F_CONTIGUOUS']
    True

    Calling ``ascontiguousarray`` makes a C-contiguous copy:

    >>> y = np.ascontiguousarray(x)
    >>> y.flags['C_CONTIGUOUS']
    True
    >>> np.may_share_memory(x, y)
    False

    Now, starting with a C-contiguous array:

    >>> x = np.ones((2, 3), order='C')
    >>> x.flags['C_CONTIGUOUS']
    True

    Then, calling ``ascontiguousarray`` returns the same object:

    >>> y = np.ascontiguousarray(x)
    >>> x is y
    True

    Note: This function returns an array with at least one-dimension (1-d)
    so it will not preserve 0-d arrays.
    """
def asfortranarray(*args, **kwargs) -> typing.Any:
    """
    Return an array (ndim >= 1) laid out in Fortran order in memory.

    Parameters
    ----------
    a : array_like
        Input array.
    dtype : str or dtype object, optional
        By default, the data-type is inferred from the input data.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        The input `a` in Fortran, or column-major, order.

    See Also
    --------
    ascontiguousarray : Convert input to a contiguous (C order) array.
    asanyarray : Convert input to an ndarray with either row or
        column-major memory order.
    require : Return an ndarray that satisfies requirements.
    ndarray.flags : Information about the memory layout of the array.

    Examples
    --------
    Starting with a C-contiguous array:

    >>> x = np.ones((2, 3), order='C')
    >>> x.flags['C_CONTIGUOUS']
    True

    Calling ``asfortranarray`` makes a Fortran-contiguous copy:

    >>> y = np.asfortranarray(x)
    >>> y.flags['F_CONTIGUOUS']
    True
    >>> np.may_share_memory(x, y)
    False

    Now, starting with a Fortran-contiguous array:

    >>> x = np.ones((2, 3), order='F')
    >>> x.flags['F_CONTIGUOUS']
    True

    Then, calling ``asfortranarray`` returns the same object:

    >>> y = np.asfortranarray(x)
    >>> x is y
    True

    Note: This function returns an array with at least one-dimension (1-d)
    so it will not preserve 0-d arrays.
    """
def bincount(*args, **kwargs) -> typing.Any:
    """
    bincount(x, /, weights=None, minlength=0)

    Count number of occurrences of each value in array of non-negative ints.

    The number of bins (of size 1) is one larger than the largest value in
    `x`. If `minlength` is specified, there will be at least this number
    of bins in the output array (though it will be longer if necessary,
    depending on the contents of `x`).
    Each bin gives the number of occurrences of its index value in `x`.
    If `weights` is specified the input array is weighted by it, i.e. if a
    value ``n`` is found at position ``i``, ``out[n] += weight[i]`` instead
    of ``out[n] += 1``.

    Parameters
    ----------
    x : array_like, 1 dimension, nonnegative ints
        Input array.
    weights : array_like, optional
        Weights, array of the same shape as `x`.
    minlength : int, optional
        A minimum number of bins for the output array.

        .. versionadded:: 1.6.0

    Returns
    -------
    out : ndarray of ints
        The result of binning the input array.
        The length of `out` is equal to ``np.amax(x)+1``.

    Raises
    ------
    ValueError
        If the input is not 1-dimensional, or contains elements with negative
        values, or if `minlength` is negative.
    TypeError
        If the type of the input is float or complex.

    See Also
    --------
    histogram, digitize, unique

    Examples
    --------
    >>> np.bincount(np.arange(5))
    array([1, 1, 1, 1, 1])
    >>> np.bincount(np.array([0, 1, 1, 3, 2, 1, 7]))
    array([1, 3, 1, 1, 0, 0, 0, 1])

    >>> x = np.array([0, 1, 1, 3, 2, 1, 7, 23])
    >>> np.bincount(x).size == np.amax(x)+1
    True

    The input array needs to be of integer dtype, otherwise a
    TypeError is raised:

    >>> np.bincount(np.arange(5, dtype=float))
    Traceback (most recent call last):
      ...
    TypeError: Cannot cast array data from dtype('float64') to dtype('int64')
    according to the rule 'safe'

    A possible use of ``bincount`` is to perform sums over
    variable-size chunks of an array, using the ``weights`` keyword.

    >>> w = np.array([0.3, 0.5, 0.2, 0.7, 1., -0.6]) # weights
    >>> x = np.array([0, 1, 1, 2, 2, 2])
    >>> np.bincount(x,  weights=w)
    array([ 0.3,  0.7,  1.1])
    """
def busday_count(*args, **kwargs) -> typing.Any:
    """
    busday_count(begindates, enddates, weekmask='1111100', holidays=[], busdaycal=None, out=None)

    Counts the number of valid days between `begindates` and
    `enddates`, not including the day of `enddates`.

    If ``enddates`` specifies a date value that is earlier than the
    corresponding ``begindates`` date value, the count will be negative.

    .. versionadded:: 1.7.0

    Parameters
    ----------
    begindates : array_like of datetime64[D]
        The array of the first dates for counting.
    enddates : array_like of datetime64[D]
        The array of the end dates for counting, which are excluded
        from the count themselves.
    weekmask : str or array_like of bool, optional
        A seven-element array indicating which of Monday through Sunday are
        valid days. May be specified as a length-seven list or array, like
        [1,1,1,1,1,0,0]; a length-seven string, like '1111100'; or a string
        like "Mon Tue Wed Thu Fri", made up of 3-character abbreviations for
        weekdays, optionally separated by white space. Valid abbreviations
        are: Mon Tue Wed Thu Fri Sat Sun
    holidays : array_like of datetime64[D], optional
        An array of dates to consider as invalid dates.  They may be
        specified in any order, and NaT (not-a-time) dates are ignored.
        This list is saved in a normalized form that is suited for
        fast calculations of valid days.
    busdaycal : busdaycalendar, optional
        A `busdaycalendar` object which specifies the valid days. If this
        parameter is provided, neither weekmask nor holidays may be
        provided.
    out : array of int, optional
        If provided, this array is filled with the result.

    Returns
    -------
    out : array of int
        An array with a shape from broadcasting ``begindates`` and ``enddates``
        together, containing the number of valid days between
        the begin and end dates.

    See Also
    --------
    busdaycalendar : An object that specifies a custom set of valid days.
    is_busday : Returns a boolean array indicating valid days.
    busday_offset : Applies an offset counted in valid days.

    Examples
    --------
    >>> # Number of weekdays in January 2011
    ... np.busday_count('2011-01', '2011-02')
    21
    >>> # Number of weekdays in 2011
    >>> np.busday_count('2011', '2012')
    260
    >>> # Number of Saturdays in 2011
    ... np.busday_count('2011', '2012', weekmask='Sat')
    53
    """
def busday_offset(*args, **kwargs) -> typing.Any:
    """
    busday_offset(dates, offsets, roll='raise', weekmask='1111100', holidays=None, busdaycal=None, out=None)

    First adjusts the date to fall on a valid day according to
    the ``roll`` rule, then applies offsets to the given dates
    counted in valid days.

    .. versionadded:: 1.7.0

    Parameters
    ----------
    dates : array_like of datetime64[D]
        The array of dates to process.
    offsets : array_like of int
        The array of offsets, which is broadcast with ``dates``.
    roll : {'raise', 'nat', 'forward', 'following', 'backward', 'preceding', 'modifiedfollowing', 'modifiedpreceding'}, optional
        How to treat dates that do not fall on a valid day. The default
        is 'raise'.

          * 'raise' means to raise an exception for an invalid day.
          * 'nat' means to return a NaT (not-a-time) for an invalid day.
          * 'forward' and 'following' mean to take the first valid day
            later in time.
          * 'backward' and 'preceding' mean to take the first valid day
            earlier in time.
          * 'modifiedfollowing' means to take the first valid day
            later in time unless it is across a Month boundary, in which
            case to take the first valid day earlier in time.
          * 'modifiedpreceding' means to take the first valid day
            earlier in time unless it is across a Month boundary, in which
            case to take the first valid day later in time.
    weekmask : str or array_like of bool, optional
        A seven-element array indicating which of Monday through Sunday are
        valid days. May be specified as a length-seven list or array, like
        [1,1,1,1,1,0,0]; a length-seven string, like '1111100'; or a string
        like "Mon Tue Wed Thu Fri", made up of 3-character abbreviations for
        weekdays, optionally separated by white space. Valid abbreviations
        are: Mon Tue Wed Thu Fri Sat Sun
    holidays : array_like of datetime64[D], optional
        An array of dates to consider as invalid dates.  They may be
        specified in any order, and NaT (not-a-time) dates are ignored.
        This list is saved in a normalized form that is suited for
        fast calculations of valid days.
    busdaycal : busdaycalendar, optional
        A `busdaycalendar` object which specifies the valid days. If this
        parameter is provided, neither weekmask nor holidays may be
        provided.
    out : array of datetime64[D], optional
        If provided, this array is filled with the result.

    Returns
    -------
    out : array of datetime64[D]
        An array with a shape from broadcasting ``dates`` and ``offsets``
        together, containing the dates with offsets applied.

    See Also
    --------
    busdaycalendar : An object that specifies a custom set of valid days.
    is_busday : Returns a boolean array indicating valid days.
    busday_count : Counts how many valid days are in a half-open date range.

    Examples
    --------
    >>> # First business day in October 2011 (not accounting for holidays)
    ... np.busday_offset('2011-10', 0, roll='forward')
    numpy.datetime64('2011-10-03')
    >>> # Last business day in February 2012 (not accounting for holidays)
    ... np.busday_offset('2012-03', -1, roll='forward')
    numpy.datetime64('2012-02-29')
    >>> # Third Wednesday in January 2011
    ... np.busday_offset('2011-01', 2, roll='forward', weekmask='Wed')
    numpy.datetime64('2011-01-19')
    >>> # 2012 Mother's Day in Canada and the U.S.
    ... np.busday_offset('2012-05', 1, roll='forward', weekmask='Sun')
    numpy.datetime64('2012-05-13')

    >>> # First business day on or after a date
    ... np.busday_offset('2011-03-20', 0, roll='forward')
    numpy.datetime64('2011-03-21')
    >>> np.busday_offset('2011-03-22', 0, roll='forward')
    numpy.datetime64('2011-03-22')
    >>> # First business day after a date
    ... np.busday_offset('2011-03-20', 1, roll='backward')
    numpy.datetime64('2011-03-21')
    >>> np.busday_offset('2011-03-22', 1, roll='backward')
    numpy.datetime64('2011-03-23')
    """
def c_einsum(*args, **kwargs) -> typing.Any:
    """
    c_einsum(subscripts, *operands, out=None, dtype=None, order='K',
               casting='safe')

        *This documentation shadows that of the native python implementation of the `einsum` function,
        except all references and examples related to the `optimize` argument (v 0.12.0) have been removed.*

        Evaluates the Einstein summation convention on the operands.

        Using the Einstein summation convention, many common multi-dimensional,
        linear algebraic array operations can be represented in a simple fashion.
        In *implicit* mode `einsum` computes these values.

        In *explicit* mode, `einsum` provides further flexibility to compute
        other array operations that might not be considered classical Einstein
        summation operations, by disabling, or forcing summation over specified
        subscript labels.

        See the notes and examples for clarification.

        Parameters
        ----------
        subscripts : str
            Specifies the subscripts for summation as comma separated list of
            subscript labels. An implicit (classical Einstein summation)
            calculation is performed unless the explicit indicator '->' is
            included as well as subscript labels of the precise output form.
        operands : list of array_like
            These are the arrays for the operation.
        out : ndarray, optional
            If provided, the calculation is done into this array.
        dtype : {data-type, None}, optional
            If provided, forces the calculation to use the data type specified.
            Note that you may have to also give a more liberal `casting`
            parameter to allow the conversions. Default is None.
        order : {'C', 'F', 'A', 'K'}, optional
            Controls the memory layout of the output. 'C' means it should
            be C contiguous. 'F' means it should be Fortran contiguous,
            'A' means it should be 'F' if the inputs are all 'F', 'C' otherwise.
            'K' means it should be as close to the layout of the inputs as
            is possible, including arbitrarily permuted axes.
            Default is 'K'.
        casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
            Controls what kind of data casting may occur.  Setting this to
            'unsafe' is not recommended, as it can adversely affect accumulations.

              * 'no' means the data types should not be cast at all.
              * 'equiv' means only byte-order changes are allowed.
              * 'safe' means only casts which can preserve values are allowed.
              * 'same_kind' means only safe casts or casts within a kind,
                like float64 to float32, are allowed.
              * 'unsafe' means any data conversions may be done.

            Default is 'safe'.
        optimize : {False, True, 'greedy', 'optimal'}, optional
            Controls if intermediate optimization should occur. No optimization
            will occur if False and True will default to the 'greedy' algorithm.
            Also accepts an explicit contraction list from the ``np.einsum_path``
            function. See ``np.einsum_path`` for more details. Defaults to False.

        Returns
        -------
        output : ndarray
            The calculation based on the Einstein summation convention.

        See Also
        --------
        einsum_path, dot, inner, outer, tensordot, linalg.multi_dot

        Notes
        -----
        .. versionadded:: 1.6.0

        The Einstein summation convention can be used to compute
        many multi-dimensional, linear algebraic array operations. `einsum`
        provides a succinct way of representing these.

        A non-exhaustive list of these operations,
        which can be computed by `einsum`, is shown below along with examples:

        * Trace of an array, :py:func:`numpy.trace`.
        * Return a diagonal, :py:func:`numpy.diag`.
        * Array axis summations, :py:func:`numpy.sum`.
        * Transpositions and permutations, :py:func:`numpy.transpose`.
        * Matrix multiplication and dot product, :py:func:`numpy.matmul` :py:func:`numpy.dot`.
        * Vector inner and outer products, :py:func:`numpy.inner` :py:func:`numpy.outer`.
        * Broadcasting, element-wise and scalar multiplication, :py:func:`numpy.multiply`.
        * Tensor contractions, :py:func:`numpy.tensordot`.
        * Chained array operations, in efficient calculation order, :py:func:`numpy.einsum_path`.

        The subscripts string is a comma-separated list of subscript labels,
        where each label refers to a dimension of the corresponding operand.
        Whenever a label is repeated it is summed, so ``np.einsum('i,i', a, b)``
        is equivalent to :py:func:`np.inner(a,b) <numpy.inner>`. If a label
        appears only once, it is not summed, so ``np.einsum('i', a)`` produces a
        view of ``a`` with no changes. A further example ``np.einsum('ij,jk', a, b)``
        describes traditional matrix multiplication and is equivalent to
        :py:func:`np.matmul(a,b) <numpy.matmul>`. Repeated subscript labels in one
        operand take the diagonal. For example, ``np.einsum('ii', a)`` is equivalent
        to :py:func:`np.trace(a) <numpy.trace>`.

        In *implicit mode*, the chosen subscripts are important
        since the axes of the output are reordered alphabetically.  This
        means that ``np.einsum('ij', a)`` doesn't affect a 2D array, while
        ``np.einsum('ji', a)`` takes its transpose. Additionally,
        ``np.einsum('ij,jk', a, b)`` returns a matrix multiplication, while,
        ``np.einsum('ij,jh', a, b)`` returns the transpose of the
        multiplication since subscript 'h' precedes subscript 'i'.

        In *explicit mode* the output can be directly controlled by
        specifying output subscript labels.  This requires the
        identifier '->' as well as the list of output subscript labels.
        This feature increases the flexibility of the function since
        summing can be disabled or forced when required. The call
        ``np.einsum('i->', a)`` is like :py:func:`np.sum(a, axis=-1) <numpy.sum>`,
        and ``np.einsum('ii->i', a)`` is like :py:func:`np.diag(a) <numpy.diag>`.
        The difference is that `einsum` does not allow broadcasting by default.
        Additionally ``np.einsum('ij,jh->ih', a, b)`` directly specifies the
        order of the output subscript labels and therefore returns matrix
        multiplication, unlike the example above in implicit mode.

        To enable and control broadcasting, use an ellipsis.  Default
        NumPy-style broadcasting is done by adding an ellipsis
        to the left of each term, like ``np.einsum('...ii->...i', a)``.
        To take the trace along the first and last axes,
        you can do ``np.einsum('i...i', a)``, or to do a matrix-matrix
        product with the left-most indices instead of rightmost, one can do
        ``np.einsum('ij...,jk...->ik...', a, b)``.

        When there is only one operand, no axes are summed, and no output
        parameter is provided, a view into the operand is returned instead
        of a new array.  Thus, taking the diagonal as ``np.einsum('ii->i', a)``
        produces a view (changed in version 1.10.0).

        `einsum` also provides an alternative way to provide the subscripts
        and operands as ``einsum(op0, sublist0, op1, sublist1, ..., [sublistout])``.
        If the output shape is not provided in this format `einsum` will be
        calculated in implicit mode, otherwise it will be performed explicitly.
        The examples below have corresponding `einsum` calls with the two
        parameter methods.

        .. versionadded:: 1.10.0

        Views returned from einsum are now writeable whenever the input array
        is writeable. For example, ``np.einsum('ijk...->kji...', a)`` will now
        have the same effect as :py:func:`np.swapaxes(a, 0, 2) <numpy.swapaxes>`
        and ``np.einsum('ii->i', a)`` will return a writeable view of the diagonal
        of a 2D array.

        Examples
        --------
        >>> a = np.arange(25).reshape(5,5)
        >>> b = np.arange(5)
        >>> c = np.arange(6).reshape(2,3)

        Trace of a matrix:

        >>> np.einsum('ii', a)
        60
        >>> np.einsum(a, [0,0])
        60
        >>> np.trace(a)
        60

        Extract the diagonal (requires explicit form):

        >>> np.einsum('ii->i', a)
        array([ 0,  6, 12, 18, 24])
        >>> np.einsum(a, [0,0], [0])
        array([ 0,  6, 12, 18, 24])
        >>> np.diag(a)
        array([ 0,  6, 12, 18, 24])

        Sum over an axis (requires explicit form):

        >>> np.einsum('ij->i', a)
        array([ 10,  35,  60,  85, 110])
        >>> np.einsum(a, [0,1], [0])
        array([ 10,  35,  60,  85, 110])
        >>> np.sum(a, axis=1)
        array([ 10,  35,  60,  85, 110])

        For higher dimensional arrays summing a single axis can be done with ellipsis:

        >>> np.einsum('...j->...', a)
        array([ 10,  35,  60,  85, 110])
        >>> np.einsum(a, [Ellipsis,1], [Ellipsis])
        array([ 10,  35,  60,  85, 110])

        Compute a matrix transpose, or reorder any number of axes:

        >>> np.einsum('ji', c)
        array([[0, 3],
               [1, 4],
               [2, 5]])
        >>> np.einsum('ij->ji', c)
        array([[0, 3],
               [1, 4],
               [2, 5]])
        >>> np.einsum(c, [1,0])
        array([[0, 3],
               [1, 4],
               [2, 5]])
        >>> np.transpose(c)
        array([[0, 3],
               [1, 4],
               [2, 5]])

        Vector inner products:

        >>> np.einsum('i,i', b, b)
        30
        >>> np.einsum(b, [0], b, [0])
        30
        >>> np.inner(b,b)
        30

        Matrix vector multiplication:

        >>> np.einsum('ij,j', a, b)
        array([ 30,  80, 130, 180, 230])
        >>> np.einsum(a, [0,1], b, [1])
        array([ 30,  80, 130, 180, 230])
        >>> np.dot(a, b)
        array([ 30,  80, 130, 180, 230])
        >>> np.einsum('...j,j', a, b)
        array([ 30,  80, 130, 180, 230])

        Broadcasting and scalar multiplication:

        >>> np.einsum('..., ...', 3, c)
        array([[ 0,  3,  6],
               [ 9, 12, 15]])
        >>> np.einsum(',ij', 3, c)
        array([[ 0,  3,  6],
               [ 9, 12, 15]])
        >>> np.einsum(3, [Ellipsis], c, [Ellipsis])
        array([[ 0,  3,  6],
               [ 9, 12, 15]])
        >>> np.multiply(3, c)
        array([[ 0,  3,  6],
               [ 9, 12, 15]])

        Vector outer product:

        >>> np.einsum('i,j', np.arange(2)+1, b)
        array([[0, 1, 2, 3, 4],
               [0, 2, 4, 6, 8]])
        >>> np.einsum(np.arange(2)+1, [0], b, [1])
        array([[0, 1, 2, 3, 4],
               [0, 2, 4, 6, 8]])
        >>> np.outer(np.arange(2)+1, b)
        array([[0, 1, 2, 3, 4],
               [0, 2, 4, 6, 8]])

        Tensor contraction:

        >>> a = np.arange(60.).reshape(3,4,5)
        >>> b = np.arange(24.).reshape(4,3,2)
        >>> np.einsum('ijk,jil->kl', a, b)
        array([[ 4400.,  4730.],
               [ 4532.,  4874.],
               [ 4664.,  5018.],
               [ 4796.,  5162.],
               [ 4928.,  5306.]])
        >>> np.einsum(a, [0,1,2], b, [1,0,3], [2,3])
        array([[ 4400.,  4730.],
               [ 4532.,  4874.],
               [ 4664.,  5018.],
               [ 4796.,  5162.],
               [ 4928.,  5306.]])
        >>> np.tensordot(a,b, axes=([1,0],[0,1]))
        array([[ 4400.,  4730.],
               [ 4532.,  4874.],
               [ 4664.,  5018.],
               [ 4796.,  5162.],
               [ 4928.,  5306.]])

        Writeable returned arrays (since version 1.10.0):

        >>> a = np.zeros((3, 3))
        >>> np.einsum('ii->i', a)[:] = 1
        >>> a
        array([[ 1.,  0.,  0.],
               [ 0.,  1.,  0.],
               [ 0.,  0.,  1.]])

        Example of ellipsis use:

        >>> a = np.arange(6).reshape((3,2))
        >>> b = np.arange(12).reshape((4,3))
        >>> np.einsum('ki,jk->ij', a, b)
        array([[10, 28, 46, 64],
               [13, 40, 67, 94]])
        >>> np.einsum('ki,...k->i...', a, b)
        array([[10, 28, 46, 64],
               [13, 40, 67, 94]])
        >>> np.einsum('k...,jk', a, b)
        array([[10, 28, 46, 64],
               [13, 40, 67, 94]])
    """
def can_cast(*args, **kwargs) -> typing.Any:
    """
    can_cast(from_, to, casting='safe')

    Returns True if cast between data types can occur according to the
    casting rule.  If from is a scalar or array scalar, also returns
    True if the scalar value can be cast without overflow or truncation
    to an integer.

    Parameters
    ----------
    from_ : dtype, dtype specifier, scalar, or array
        Data type, scalar, or array to cast from.
    to : dtype or dtype specifier
        Data type to cast to.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur.

          * 'no' means the data types should not be cast at all.
          * 'equiv' means only byte-order changes are allowed.
          * 'safe' means only casts which can preserve values are allowed.
          * 'same_kind' means only safe casts or casts within a kind,
            like float64 to float32, are allowed.
          * 'unsafe' means any data conversions may be done.

    Returns
    -------
    out : bool
        True if cast can occur according to the casting rule.

    Notes
    -----
    .. versionchanged:: 1.17.0
       Casting between a simple data type and a structured one is possible only
       for "unsafe" casting.  Casting to multiple fields is allowed, but
       casting from multiple fields is not.

    .. versionchanged:: 1.9.0
       Casting from numeric to string types in 'safe' casting mode requires
       that the string dtype length is long enough to store the maximum
       integer/float value converted.

    See also
    --------
    dtype, result_type

    Examples
    --------
    Basic examples

    >>> np.can_cast(np.int32, np.int64)
    True
    >>> np.can_cast(np.float64, complex)
    True
    >>> np.can_cast(complex, float)
    False

    >>> np.can_cast('i8', 'f8')
    True
    >>> np.can_cast('i8', 'f4')
    False
    >>> np.can_cast('i4', 'S4')
    False

    Casting scalars

    >>> np.can_cast(100, 'i1')
    True
    >>> np.can_cast(150, 'i1')
    False
    >>> np.can_cast(150, 'u1')
    True

    >>> np.can_cast(3.5e100, np.float32)
    False
    >>> np.can_cast(1000.0, np.float32)
    True

    Array scalar checks the value, array does not

    >>> np.can_cast(np.array(1000.0), np.float32)
    True
    >>> np.can_cast(np.array([1000.0]), np.float32)
    False

    Using the casting rules

    >>> np.can_cast('i8', 'i8', 'no')
    True
    >>> np.can_cast('<i8', '>i8', 'no')
    False

    >>> np.can_cast('<i8', '>i8', 'equiv')
    True
    >>> np.can_cast('<i4', '>i8', 'equiv')
    False

    >>> np.can_cast('<i4', '>i8', 'safe')
    True
    >>> np.can_cast('<i8', '>i4', 'safe')
    False

    >>> np.can_cast('<i8', '>i4', 'same_kind')
    True
    >>> np.can_cast('<i8', '>u4', 'same_kind')
    False

    >>> np.can_cast('<i8', '>u4', 'unsafe')
    True
    """
def compare_chararrays(*args, **kwargs) -> typing.Any:
    """
    Performs element-wise comparison of two string arrays using the
    comparison operator specified by `cmp_op`.

    Parameters
    ----------
    a1, a2 : array_like
        Arrays to be compared.
    cmp : {"<", "<=", "==", ">=", ">", "!="}
        Type of comparison.
    rstrip : Boolean
        If True, the spaces at the end of Strings are removed before the comparison.

    Returns
    -------
    out : ndarray
        The output array of type Boolean with the same shape as a and b.

    Raises
    ------
    ValueError
        If `cmp_op` is not valid.
    TypeError
        If at least one of `a` or `b` is a non-string array

    Examples
    --------
    >>> a = np.array(["a", "b", "cde"])
    >>> b = np.array(["a", "a", "dec"])
    >>> np.compare_chararrays(a, b, ">", True)
    array([False,  True, False])
    """
def concatenate(*args, **kwargs) -> typing.Any:
    """
    concatenate((a1, a2, ...), axis=0, out=None, dtype=None, casting="same_kind")

    Join a sequence of arrays along an existing axis.

    Parameters
    ----------
    a1, a2, ... : sequence of array_like
        The arrays must have the same shape, except in the dimension
        corresponding to `axis` (the first, by default).
    axis : int, optional
        The axis along which the arrays will be joined.  If axis is None,
        arrays are flattened before use.  Default is 0.
    out : ndarray, optional
        If provided, the destination to place the result. The shape must be
        correct, matching that of what concatenate would have returned if no
        out argument were specified.
    dtype : str or dtype
        If provided, the destination array will have this dtype. Cannot be
        provided together with `out`.

        .. versionadded:: 1.20.0

    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur. Defaults to 'same_kind'.

        .. versionadded:: 1.20.0

    Returns
    -------
    res : ndarray
        The concatenated array.

    See Also
    --------
    ma.concatenate : Concatenate function that preserves input masks.
    array_split : Split an array into multiple sub-arrays of equal or
                  near-equal size.
    split : Split array into a list of multiple sub-arrays of equal size.
    hsplit : Split array into multiple sub-arrays horizontally (column wise).
    vsplit : Split array into multiple sub-arrays vertically (row wise).
    dsplit : Split array into multiple sub-arrays along the 3rd axis (depth).
    stack : Stack a sequence of arrays along a new axis.
    block : Assemble arrays from blocks.
    hstack : Stack arrays in sequence horizontally (column wise).
    vstack : Stack arrays in sequence vertically (row wise).
    dstack : Stack arrays in sequence depth wise (along third dimension).
    column_stack : Stack 1-D arrays as columns into a 2-D array.

    Notes
    -----
    When one or more of the arrays to be concatenated is a MaskedArray,
    this function will return a MaskedArray object instead of an ndarray,
    but the input masks are *not* preserved. In cases where a MaskedArray
    is expected as input, use the ma.concatenate function from the masked
    array module instead.

    Examples
    --------
    >>> a = np.array([[1, 2], [3, 4]])
    >>> b = np.array([[5, 6]])
    >>> np.concatenate((a, b), axis=0)
    array([[1, 2],
           [3, 4],
           [5, 6]])
    >>> np.concatenate((a, b.T), axis=1)
    array([[1, 2, 5],
           [3, 4, 6]])
    >>> np.concatenate((a, b), axis=None)
    array([1, 2, 3, 4, 5, 6])

    This function will not preserve masking of MaskedArray inputs.

    >>> a = np.ma.arange(3)
    >>> a[1] = np.ma.masked
    >>> b = np.arange(2, 5)
    >>> a
    masked_array(data=[0, --, 2],
                 mask=[False,  True, False],
           fill_value=999999)
    >>> b
    array([2, 3, 4])
    >>> np.concatenate([a, b])
    masked_array(data=[0, 1, 2, 2, 3, 4],
                 mask=False,
           fill_value=999999)
    >>> np.ma.concatenate([a, b])
    masked_array(data=[0, --, 2, 2, 3, 4],
                 mask=[False,  True, False, False, False, False],
           fill_value=999999)
    """
def copyto(*args, **kwargs) -> typing.Any:
    """
    copyto(dst, src, casting='same_kind', where=True)

    Copies values from one array to another, broadcasting as necessary.

    Raises a TypeError if the `casting` rule is violated, and if
    `where` is provided, it selects which elements to copy.

    .. versionadded:: 1.7.0

    Parameters
    ----------
    dst : ndarray
        The array into which values are copied.
    src : array_like
        The array from which values are copied.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}, optional
        Controls what kind of data casting may occur when copying.

          * 'no' means the data types should not be cast at all.
          * 'equiv' means only byte-order changes are allowed.
          * 'safe' means only casts which can preserve values are allowed.
          * 'same_kind' means only safe casts or casts within a kind,
            like float64 to float32, are allowed.
          * 'unsafe' means any data conversions may be done.
    where : array_like of bool, optional
        A boolean array which is broadcasted to match the dimensions
        of `dst`, and selects elements to copy from `src` to `dst`
        wherever it contains the value True.

    Examples
    --------
    >>> A = np.array([4, 5, 6])
    >>> B = [1, 2, 3]
    >>> np.copyto(A, B)
    >>> A
    array([1, 2, 3])

    >>> A = np.array([[1, 2, 3], [4, 5, 6]])
    >>> B = [[4, 5, 6], [7, 8, 9]]
    >>> np.copyto(A, B)
    >>> A
    array([[4, 5, 6],
           [7, 8, 9]])
    """
def correlate(*args, **kwargs) -> typing.Any:
    pass
def correlate2(*args, **kwargs) -> typing.Any:
    pass
def count_nonzero(*args, **kwargs) -> typing.Any:
    pass
def datetime_as_string(*args, **kwargs) -> typing.Any:
    """
    datetime_as_string(arr, unit=None, timezone='naive', casting='same_kind')

    Convert an array of datetimes into an array of strings.

    Parameters
    ----------
    arr : array_like of datetime64
        The array of UTC timestamps to format.
    unit : str
        One of None, 'auto', or a :ref:`datetime unit <arrays.dtypes.dateunits>`.
    timezone : {'naive', 'UTC', 'local'} or tzinfo
        Timezone information to use when displaying the datetime. If 'UTC', end
        with a Z to indicate UTC time. If 'local', convert to the local timezone
        first, and suffix with a +-#### timezone offset. If a tzinfo object,
        then do as with 'local', but use the specified timezone.
    casting : {'no', 'equiv', 'safe', 'same_kind', 'unsafe'}
        Casting to allow when changing between datetime units.

    Returns
    -------
    str_arr : ndarray
        An array of strings the same shape as `arr`.

    Examples
    --------
    >>> import pytz
    >>> d = np.arange('2002-10-27T04:30', 4*60, 60, dtype='M8[m]')
    >>> d
    array(['2002-10-27T04:30', '2002-10-27T05:30', '2002-10-27T06:30',
           '2002-10-27T07:30'], dtype='datetime64[m]')

    Setting the timezone to UTC shows the same information, but with a Z suffix

    >>> np.datetime_as_string(d, timezone='UTC')
    array(['2002-10-27T04:30Z', '2002-10-27T05:30Z', '2002-10-27T06:30Z',
           '2002-10-27T07:30Z'], dtype='<U35')

    Note that we picked datetimes that cross a DST boundary. Passing in a
    ``pytz`` timezone object will print the appropriate offset

    >>> np.datetime_as_string(d, timezone=pytz.timezone('US/Eastern'))
    array(['2002-10-27T00:30-0400', '2002-10-27T01:30-0400',
           '2002-10-27T01:30-0500', '2002-10-27T02:30-0500'], dtype='<U39')

    Passing in a unit will change the precision

    >>> np.datetime_as_string(d, unit='h')
    array(['2002-10-27T04', '2002-10-27T05', '2002-10-27T06', '2002-10-27T07'],
          dtype='<U32')
    >>> np.datetime_as_string(d, unit='s')
    array(['2002-10-27T04:30:00', '2002-10-27T05:30:00', '2002-10-27T06:30:00',
           '2002-10-27T07:30:00'], dtype='<U38')

    'casting' can be used to specify whether precision can be changed

    >>> np.datetime_as_string(d, unit='h', casting='safe')
    Traceback (most recent call last):
        ...
    TypeError: Cannot create a datetime string as units 'h' from a NumPy
    datetime with units 'm' according to the rule 'safe'
    """
def datetime_data(*args, **kwargs) -> typing.Any:
    """
    Get information about the step size of a date or time type.

    The returned tuple can be passed as the second argument of `numpy.datetime64` and
    `numpy.timedelta64`.

    Parameters
    ----------
    dtype : dtype
        The dtype object, which must be a `datetime64` or `timedelta64` type.

    Returns
    -------
    unit : str
        The :ref:`datetime unit <arrays.dtypes.dateunits>` on which this dtype
        is based.
    count : int
        The number of base units in a step.

    Examples
    --------
    >>> dt_25s = np.dtype('timedelta64[25s]')
    >>> np.datetime_data(dt_25s)
    ('s', 25)
    >>> np.array(10, dt_25s).astype('timedelta64[s]')
    array(250, dtype='timedelta64[s]')

    The result can be used to construct a datetime that uses the same units
    as a timedelta

    >>> np.datetime64('2010', np.datetime_data(dt_25s))
    numpy.datetime64('2010-01-01T00:00:00','25s')
    """
def dot(*args, **kwargs) -> typing.Any:
    """
    dot(a, b, out=None)

    Dot product of two arrays. Specifically,

    - If both `a` and `b` are 1-D arrays, it is inner product of vectors
      (without complex conjugation).

    - If both `a` and `b` are 2-D arrays, it is matrix multiplication,
      but using :func:`matmul` or ``a @ b`` is preferred.

    - If either `a` or `b` is 0-D (scalar), it is equivalent to
      :func:`multiply` and using ``numpy.multiply(a, b)`` or ``a * b`` is
      preferred.

    - If `a` is an N-D array and `b` is a 1-D array, it is a sum product over
      the last axis of `a` and `b`.

    - If `a` is an N-D array and `b` is an M-D array (where ``M>=2``), it is a
      sum product over the last axis of `a` and the second-to-last axis of
      `b`::

        dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])

    It uses an optimized BLAS library when possible (see `numpy.linalg`).

    Parameters
    ----------
    a : array_like
        First argument.
    b : array_like
        Second argument.
    out : ndarray, optional
        Output argument. This must have the exact kind that would be returned
        if it was not used. In particular, it must have the right type, must be
        C-contiguous, and its dtype must be the dtype that would be returned
        for `dot(a,b)`. This is a performance feature. Therefore, if these
        conditions are not met, an exception is raised, instead of attempting
        to be flexible.

    Returns
    -------
    output : ndarray
        Returns the dot product of `a` and `b`.  If `a` and `b` are both
        scalars or both 1-D arrays then a scalar is returned; otherwise
        an array is returned.
        If `out` is given, then it is returned.

    Raises
    ------
    ValueError
        If the last dimension of `a` is not the same size as
        the second-to-last dimension of `b`.

    See Also
    --------
    vdot : Complex-conjugating dot product.
    tensordot : Sum products over arbitrary axes.
    einsum : Einstein summation convention.
    matmul : '@' operator as method with out parameter.
    linalg.multi_dot : Chained dot product.

    Examples
    --------
    >>> np.dot(3, 4)
    12

    Neither argument is complex-conjugated:

    >>> np.dot([2j, 3j], [2j, 3j])
    (-13+0j)

    For 2-D arrays it is the matrix product:

    >>> a = [[1, 0], [0, 1]]
    >>> b = [[4, 1], [2, 2]]
    >>> np.dot(a, b)
    array([[4, 1],
           [2, 2]])

    >>> a = np.arange(3*4*5*6).reshape((3,4,5,6))
    >>> b = np.arange(3*4*5*6)[::-1].reshape((5,4,6,3))
    >>> np.dot(a, b)[2,3,2,1,2,2]
    499128
    >>> sum(a[2,3,2,:] * b[1,2,:,2])
    499128
    """
def dragon4_positional(*args, **kwargs) -> typing.Any:
    pass
def dragon4_scientific(*args, **kwargs) -> typing.Any:
    pass
def empty(*args, **kwargs) -> typing.Any:
    """
    Return a new array of given shape and type, without initializing entries.

    Parameters
    ----------
    shape : int or tuple of int
        Shape of the empty array, e.g., ``(2, 3)`` or ``2``.
    dtype : data-type, optional
        Desired output data-type for the array, e.g, `numpy.int8`. Default is
        `numpy.float64`.
    order : {'C', 'F'}, optional, default: 'C'
        Whether to store multi-dimensional data in row-major
        (C-style) or column-major (Fortran-style) order in
        memory.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Array of uninitialized (arbitrary) data of the given shape, dtype, and
        order.  Object arrays will be initialized to None.

    See Also
    --------
    empty_like : Return an empty array with shape and type of input.
    ones : Return a new array setting values to one.
    zeros : Return a new array setting values to zero.
    full : Return a new array of given shape filled with value.


    Notes
    -----
    `empty`, unlike `zeros`, does not set the array values to zero,
    and may therefore be marginally faster.  On the other hand, it requires
    the user to manually set all the values in the array, and should be
    used with caution.

    Examples
    --------
    >>> np.empty([2, 2])
    array([[ -9.74499359e+001,   6.69583040e-309],
           [  2.13182611e-314,   3.06959433e-309]])         #uninitialized

    >>> np.empty([2, 2], dtype=int)
    array([[-1073741821, -1067949133],
           [  496041986,    19249760]])                     #uninitialized
    """
def empty_like(*args, **kwargs) -> typing.Any:
    """
    empty_like(prototype, dtype=None, order='K', subok=True, shape=None)

    Return a new array with the same shape and type as a given array.

    Parameters
    ----------
    prototype : array_like
        The shape and data-type of `prototype` define these same attributes
        of the returned array.
    dtype : data-type, optional
        Overrides the data type of the result.

        .. versionadded:: 1.6.0
    order : {'C', 'F', 'A', or 'K'}, optional
        Overrides the memory layout of the result. 'C' means C-order,
        'F' means F-order, 'A' means 'F' if `prototype` is Fortran
        contiguous, 'C' otherwise. 'K' means match the layout of `prototype`
        as closely as possible.

        .. versionadded:: 1.6.0
    subok : bool, optional.
        If True, then the newly created array will use the sub-class
        type of `prototype`, otherwise it will be a base-class array. Defaults
        to True.
    shape : int or sequence of ints, optional.
        Overrides the shape of the result. If order='K' and the number of
        dimensions is unchanged, will try to keep order, otherwise,
        order='C' is implied.

        .. versionadded:: 1.17.0

    Returns
    -------
    out : ndarray
        Array of uninitialized (arbitrary) data with the same
        shape and type as `prototype`.

    See Also
    --------
    ones_like : Return an array of ones with shape and type of input.
    zeros_like : Return an array of zeros with shape and type of input.
    full_like : Return a new array with shape of input filled with value.
    empty : Return a new uninitialized array.

    Notes
    -----
    This function does *not* initialize the returned array; to do that use
    `zeros_like` or `ones_like` instead.  It may be marginally faster than
    the functions that do set the array values.

    Examples
    --------
    >>> a = ([1,2,3], [4,5,6])                         # a is array-like
    >>> np.empty_like(a)
    array([[-1073741821, -1073741821,           3],    # uninitialized
           [          0,           0, -1073741821]])
    >>> a = np.array([[1., 2., 3.],[4.,5.,6.]])
    >>> np.empty_like(a)
    array([[ -2.00000715e+000,   1.48219694e-323,  -2.00000572e+000], # uninitialized
           [  4.38791518e-305,  -2.00000715e+000,   4.17269252e-309]])
    """
def fastCopyAndTranspose(*args, **kwargs) -> typing.Any:
    """
    .. deprecated:: 1.24

       fastCopyAndTranspose is deprecated and will be removed. Use the copy and
       transpose methods instead, e.g. ``arr.T.copy()``
    """
def format_longfloat(*args, **kwargs) -> typing.Any:
    pass
def from_dlpack(*args, **kwargs) -> typing.Any:
    """
    Create a NumPy array from an object implementing the ``__dlpack__``
    protocol. Generally, the returned NumPy array is a read-only view
    of the input object. See [1]_ and [2]_ for more details.

    Parameters
    ----------
    x : object
        A Python object that implements the ``__dlpack__`` and
        ``__dlpack_device__`` methods.

    Returns
    -------
    out : ndarray

    References
    ----------
    .. [1] Array API documentation,
       https://data-apis.org/array-api/latest/design_topics/data_interchange.html#syntax-for-data-interchange-with-dlpack

    .. [2] Python specification for DLPack,
       https://dmlc.github.io/dlpack/latest/python_spec.html

    Examples
    --------
    >>> import torch
    >>> x = torch.arange(10)
    >>> # create a view of the torch tensor "x" in NumPy
    >>> y = np.from_dlpack(x)
    """
def frombuffer(*args, **kwargs) -> typing.Any:
    """
    Interpret a buffer as a 1-dimensional array.

    Parameters
    ----------
    buffer : buffer_like
        An object that exposes the buffer interface.
    dtype : data-type, optional
        Data-type of the returned array; default: float.
    count : int, optional
        Number of items to read. ``-1`` means all data in the buffer.
    offset : int, optional
        Start reading the buffer from this offset (in bytes); default: 0.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray

    See also
    --------
    ndarray.tobytes
        Inverse of this operation, construct Python bytes from the raw data
        bytes in the array.

    Notes
    -----
    If the buffer has data that is not in machine byte-order, this should
    be specified as part of the data-type, e.g.::

      >>> dt = np.dtype(int)
      >>> dt = dt.newbyteorder('>')
      >>> np.frombuffer(buf, dtype=dt) # doctest: +SKIP

    The data of the resulting array will not be byteswapped, but will be
    interpreted correctly.

    This function creates a view into the original object.  This should be safe
    in general, but it may make sense to copy the result when the original
    object is mutable or untrusted.

    Examples
    --------
    >>> s = b'hello world'
    >>> np.frombuffer(s, dtype='S1', count=5, offset=6)
    array([b'w', b'o', b'r', b'l', b'd'], dtype='|S1')

    >>> np.frombuffer(b'\\x01\\x02', dtype=np.uint8)
    array([1, 2], dtype=uint8)
    >>> np.frombuffer(b'\\x01\\x02\\x03\\x04\\x05', dtype=np.uint8, count=3)
    array([1, 2, 3], dtype=uint8)
    """
def fromfile(*args, **kwargs) -> typing.Any:
    """
    Construct an array from data in a text or binary file.

    A highly efficient way of reading binary data with a known data-type,
    as well as parsing simply formatted text files.  Data written using the
    `tofile` method can be read using this function.

    Parameters
    ----------
    file : file or str or Path
        Open file object or filename.

        .. versionchanged:: 1.17.0
            `pathlib.Path` objects are now accepted.

    dtype : data-type
        Data type of the returned array.
        For binary files, it is used to determine the size and byte-order
        of the items in the file.
        Most builtin numeric types are supported and extension types may be supported.

        .. versionadded:: 1.18.0
            Complex dtypes.

    count : int
        Number of items to read. ``-1`` means all items (i.e., the complete
        file).
    sep : str
        Separator between items if file is a text file.
        Empty ("") separator means the file should be treated as binary.
        Spaces (" ") in the separator match zero or more whitespace characters.
        A separator consisting only of spaces must match at least one
        whitespace.
    offset : int
        The offset (in bytes) from the file's current position. Defaults to 0.
        Only permitted for binary files.

        .. versionadded:: 1.17.0
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    See also
    --------
    load, save
    ndarray.tofile
    loadtxt : More flexible way of loading data from a text file.

    Notes
    -----
    Do not rely on the combination of `tofile` and `fromfile` for
    data storage, as the binary files generated are not platform
    independent.  In particular, no byte-order or data-type information is
    saved.  Data can be stored in the platform independent ``.npy`` format
    using `save` and `load` instead.

    Examples
    --------
    Construct an ndarray:

    >>> dt = np.dtype([('time', [('min', np.int64), ('sec', np.int64)]),
    ...                ('temp', float)])
    >>> x = np.zeros((1,), dtype=dt)
    >>> x['time']['min'] = 10; x['temp'] = 98.25
    >>> x
    array([((10, 0), 98.25)],
          dtype=[('time', [('min', '<i8'), ('sec', '<i8')]), ('temp', '<f8')])

    Save the raw data to disk:

    >>> import tempfile
    >>> fname = tempfile.mkstemp()[1]
    >>> x.tofile(fname)

    Read the raw data from disk:

    >>> np.fromfile(fname, dtype=dt)
    array([((10, 0), 98.25)],
          dtype=[('time', [('min', '<i8'), ('sec', '<i8')]), ('temp', '<f8')])

    The recommended way to store and load data:

    >>> np.save(fname, x)
    >>> np.load(fname + '.npy')
    array([((10, 0), 98.25)],
          dtype=[('time', [('min', '<i8'), ('sec', '<i8')]), ('temp', '<f8')])
    """
def fromiter(*args, **kwargs) -> typing.Any:
    """
    Create a new 1-dimensional array from an iterable object.

    Parameters
    ----------
    iter : iterable object
        An iterable object providing data for the array.
    dtype : data-type
        The data-type of the returned array.

        .. versionchanged:: 1.23
            Object and subarray dtypes are now supported (note that the final
            result is not 1-D for a subarray dtype).

    count : int, optional
        The number of items to read from *iterable*.  The default is -1,
        which means all data is read.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        The output array.

    Notes
    -----
    Specify `count` to improve performance.  It allows ``fromiter`` to
    pre-allocate the output array, instead of resizing it on demand.

    Examples
    --------
    >>> iterable = (x*x for x in range(5))
    >>> np.fromiter(iterable, float)
    array([  0.,   1.,   4.,   9.,  16.])

    A carefully constructed subarray dtype will lead to higher dimensional
    results:

    >>> iterable = ((x+1, x+2) for x in range(5))
    >>> np.fromiter(iterable, dtype=np.dtype((int, 2)))
    array([[1, 2],
           [2, 3],
           [3, 4],
           [4, 5],
           [5, 6]])
    """
def frompyfunc(*args, **kwargs) -> typing.Any:
    """
    Takes an arbitrary Python function and returns a NumPy ufunc.

    Can be used, for example, to add broadcasting to a built-in Python
    function (see Examples section).

    Parameters
    ----------
    func : Python function object
        An arbitrary Python function.
    nin : int
        The number of input arguments.
    nout : int
        The number of objects returned by `func`.
    identity : object, optional
        The value to use for the `~numpy.ufunc.identity` attribute of the resulting
        object. If specified, this is equivalent to setting the underlying
        C ``identity`` field to ``PyUFunc_IdentityValue``.
        If omitted, the identity is set to ``PyUFunc_None``. Note that this is
        _not_ equivalent to setting the identity to ``None``, which implies the
        operation is reorderable.

    Returns
    -------
    out : ufunc
        Returns a NumPy universal function (``ufunc``) object.

    See Also
    --------
    vectorize : Evaluates pyfunc over input arrays using broadcasting rules of numpy.

    Notes
    -----
    The returned ufunc always returns PyObject arrays.

    Examples
    --------
    Use frompyfunc to add broadcasting to the Python function ``oct``:

    >>> oct_array = np.frompyfunc(oct, 1, 1)
    >>> oct_array(np.array((10, 30, 100)))
    array(['0o12', '0o36', '0o144'], dtype=object)
    >>> np.array((oct(10), oct(30), oct(100))) # for comparison
    array(['0o12', '0o36', '0o144'], dtype='<U5')
    """
def fromstring(*args, **kwargs) -> typing.Any:
    """
    A new 1-D array initialized from text data in a string.

    Parameters
    ----------
    string : str
        A string containing the data.
    dtype : data-type, optional
        The data type of the array; default: float.  For binary input data,
        the data must be in exactly this format. Most builtin numeric types are
        supported and extension types may be supported.

        .. versionadded:: 1.18.0
            Complex dtypes.

    count : int, optional
        Read this number of `dtype` elements from the data.  If this is
        negative (the default), the count will be determined from the
        length of the data.
    sep : str, optional
        The string separating numbers in the data; extra whitespace between
        elements is also ignored.

        .. deprecated:: 1.14
            Passing ``sep=''``, the default, is deprecated since it will
            trigger the deprecated binary mode of this function. This mode
            interprets `string` as binary bytes, rather than ASCII text with
            decimal numbers, an operation which is better spelt
            ``frombuffer(string, dtype, count)``. If `string` contains unicode
            text, the binary mode of `fromstring` will first encode it into
            bytes using utf-8, which will not produce sane results.

    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    arr : ndarray
        The constructed array.

    Raises
    ------
    ValueError
        If the string is not the correct size to satisfy the requested
        `dtype` and `count`.

    See Also
    --------
    frombuffer, fromfile, fromiter

    Examples
    --------
    >>> np.fromstring('1 2', dtype=int, sep=' ')
    array([1, 2])
    >>> np.fromstring('1, 2', dtype=int, sep=',')
    array([1, 2])
    """
def get_handler_name(*args, **kwargs) -> typing.Any:
    """
    Return the name of the memory handler used by `a`. If not provided, return
    the name of the memory handler that will be used to allocate data for the
    next `ndarray` in this context. May return None if `a` does not own its
    memory, in which case you can traverse ``a.base`` for a memory handler.
    """
def get_handler_version(*args, **kwargs) -> typing.Any:
    """
    Return the version of the memory handler used by `a`. If not provided,
    return the version of the memory handler that will be used to allocate data
    for the next `ndarray` in this context. May return None if `a` does not own
    its memory, in which case you can traverse ``a.base`` for a memory handler.
    """
def geterrobj(*args, **kwargs) -> typing.Any:
    """
    Return the current object that defines floating-point error handling.

    The error object contains all information that defines the error handling
    behavior in NumPy. `geterrobj` is used internally by the other
    functions that get and set error handling behavior (`geterr`, `seterr`,
    `geterrcall`, `seterrcall`).

    Returns
    -------
    errobj : list
        The error object, a list containing three elements:
        [internal numpy buffer size, error mask, error callback function].

        The error mask is a single integer that holds the treatment information
        on all four floating point errors. The information for each error type
        is contained in three bits of the integer. If we print it in base 8, we
        can see what treatment is set for "invalid", "under", "over", and
        "divide" (in that order). The printed string can be interpreted with

        * 0 : 'ignore'
        * 1 : 'warn'
        * 2 : 'raise'
        * 3 : 'call'
        * 4 : 'print'
        * 5 : 'log'

    See Also
    --------
    seterrobj, seterr, geterr, seterrcall, geterrcall
    getbufsize, setbufsize

    Notes
    -----
    For complete documentation of the types of floating-point exceptions and
    treatment options, see `seterr`.

    Examples
    --------
    >>> np.geterrobj()  # first get the defaults
    [8192, 521, None]

    >>> def err_handler(type, flag):
    ...     print("Floating point error (%s), with flag %s" % (type, flag))
    ...
    >>> old_bufsize = np.setbufsize(20000)
    >>> old_err = np.seterr(divide='raise')
    >>> old_handler = np.seterrcall(err_handler)
    >>> np.geterrobj()
    [8192, 521, <function err_handler at 0x91dcaac>]

    >>> old_err = np.seterr(all='ignore')
    >>> np.base_repr(np.geterrobj()[1], 8)
    '0'
    >>> old_err = np.seterr(divide='warn', over='log', under='call',
    ...                     invalid='print')
    >>> np.base_repr(np.geterrobj()[1], 8)
    '4351'
    """
def inner(*args, **kwargs) -> typing.Any:
    """
    inner(a, b, /)

    Inner product of two arrays.

    Ordinary inner product of vectors for 1-D arrays (without complex
    conjugation), in higher dimensions a sum product over the last axes.

    Parameters
    ----------
    a, b : array_like
        If `a` and `b` are nonscalar, their last dimensions must match.

    Returns
    -------
    out : ndarray
        If `a` and `b` are both
        scalars or both 1-D arrays then a scalar is returned; otherwise
        an array is returned.
        ``out.shape = (*a.shape[:-1], *b.shape[:-1])``

    Raises
    ------
    ValueError
        If both `a` and `b` are nonscalar and their last dimensions have
        different sizes.

    See Also
    --------
    tensordot : Sum products over arbitrary axes.
    dot : Generalised matrix product, using second last dimension of `b`.
    einsum : Einstein summation convention.

    Notes
    -----
    For vectors (1-D arrays) it computes the ordinary inner-product::

        np.inner(a, b) = sum(a[:]*b[:])

    More generally, if ``ndim(a) = r > 0`` and ``ndim(b) = s > 0``::

        np.inner(a, b) = np.tensordot(a, b, axes=(-1,-1))

    or explicitly::

        np.inner(a, b)[i0,...,ir-2,j0,...,js-2]
             = sum(a[i0,...,ir-2,:]*b[j0,...,js-2,:])

    In addition `a` or `b` may be scalars, in which case::

       np.inner(a,b) = a*b

    Examples
    --------
    Ordinary inner product for vectors:

    >>> a = np.array([1,2,3])
    >>> b = np.array([0,1,0])
    >>> np.inner(a, b)
    2

    Some multidimensional examples:

    >>> a = np.arange(24).reshape((2,3,4))
    >>> b = np.arange(4)
    >>> c = np.inner(a, b)
    >>> c.shape
    (2, 3)
    >>> c
    array([[ 14,  38,  62],
           [ 86, 110, 134]])

    >>> a = np.arange(2).reshape((1,1,2))
    >>> b = np.arange(6).reshape((3,2))
    >>> c = np.inner(a, b)
    >>> c.shape
    (1, 1, 3)
    >>> c
    array([[[1, 3, 5]]])

    An example where `b` is a scalar:

    >>> np.inner(np.eye(2), 7)
    array([[7., 0.],
           [0., 7.]])
    """
def interp(*args, **kwargs) -> typing.Any:
    pass
def interp_complex(*args, **kwargs) -> typing.Any:
    pass
def is_busday(*args, **kwargs) -> typing.Any:
    """
    is_busday(dates, weekmask='1111100', holidays=None, busdaycal=None, out=None)

    Calculates which of the given dates are valid days, and which are not.

    .. versionadded:: 1.7.0

    Parameters
    ----------
    dates : array_like of datetime64[D]
        The array of dates to process.
    weekmask : str or array_like of bool, optional
        A seven-element array indicating which of Monday through Sunday are
        valid days. May be specified as a length-seven list or array, like
        [1,1,1,1,1,0,0]; a length-seven string, like '1111100'; or a string
        like "Mon Tue Wed Thu Fri", made up of 3-character abbreviations for
        weekdays, optionally separated by white space. Valid abbreviations
        are: Mon Tue Wed Thu Fri Sat Sun
    holidays : array_like of datetime64[D], optional
        An array of dates to consider as invalid dates.  They may be
        specified in any order, and NaT (not-a-time) dates are ignored.
        This list is saved in a normalized form that is suited for
        fast calculations of valid days.
    busdaycal : busdaycalendar, optional
        A `busdaycalendar` object which specifies the valid days. If this
        parameter is provided, neither weekmask nor holidays may be
        provided.
    out : array of bool, optional
        If provided, this array is filled with the result.

    Returns
    -------
    out : array of bool
        An array with the same shape as ``dates``, containing True for
        each valid day, and False for each invalid day.

    See Also
    --------
    busdaycalendar : An object that specifies a custom set of valid days.
    busday_offset : Applies an offset counted in valid days.
    busday_count : Counts how many valid days are in a half-open date range.

    Examples
    --------
    >>> # The weekdays are Friday, Saturday, and Monday
    ... np.is_busday(['2011-07-01', '2011-07-02', '2011-07-18'],
    ...                 holidays=['2011-07-01', '2011-07-04', '2011-07-17'])
    array([False, False,  True])
    """
def lexsort(*args, **kwargs) -> typing.Any:
    """
    lexsort(keys, axis=-1)

    Perform an indirect stable sort using a sequence of keys.

    Given multiple sorting keys, which can be interpreted as columns in a
    spreadsheet, lexsort returns an array of integer indices that describes
    the sort order by multiple columns. The last key in the sequence is used
    for the primary sort order, the second-to-last key for the secondary sort
    order, and so on. The keys argument must be a sequence of objects that
    can be converted to arrays of the same shape. If a 2D array is provided
    for the keys argument, its rows are interpreted as the sorting keys and
    sorting is according to the last row, second last row etc.

    Parameters
    ----------
    keys : (k, N) array or tuple containing k (N,)-shaped sequences
        The `k` different "columns" to be sorted.  The last column (or row if
        `keys` is a 2D array) is the primary sort key.
    axis : int, optional
        Axis to be indirectly sorted.  By default, sort over the last axis.

    Returns
    -------
    indices : (N,) ndarray of ints
        Array of indices that sort the keys along the specified axis.

    See Also
    --------
    argsort : Indirect sort.
    ndarray.sort : In-place sort.
    sort : Return a sorted copy of an array.

    Examples
    --------
    Sort names: first by surname, then by name.

    >>> surnames =    ('Hertz',    'Galilei', 'Hertz')
    >>> first_names = ('Heinrich', 'Galileo', 'Gustav')
    >>> ind = np.lexsort((first_names, surnames))
    >>> ind
    array([1, 2, 0])

    >>> [surnames[i] + ", " + first_names[i] for i in ind]
    ['Galilei, Galileo', 'Hertz, Gustav', 'Hertz, Heinrich']

    Sort two columns of numbers:

    >>> a = [1,5,1,4,3,4,4] # First column
    >>> b = [9,4,0,4,0,2,1] # Second column
    >>> ind = np.lexsort((b,a)) # Sort by a, then by b
    >>> ind
    array([2, 0, 4, 6, 5, 3, 1])

    >>> [(a[i],b[i]) for i in ind]
    [(1, 0), (1, 9), (3, 0), (4, 1), (4, 2), (4, 4), (5, 4)]

    Note that sorting is first according to the elements of ``a``.
    Secondary sorting is according to the elements of ``b``.

    A normal ``argsort`` would have yielded:

    >>> [(a[i],b[i]) for i in np.argsort(a)]
    [(1, 9), (1, 0), (3, 0), (4, 4), (4, 2), (4, 1), (5, 4)]

    Structured arrays are sorted lexically by ``argsort``:

    >>> x = np.array([(1,9), (5,4), (1,0), (4,4), (3,0), (4,2), (4,1)],
    ...              dtype=np.dtype([('x', int), ('y', int)]))

    >>> np.argsort(x) # or np.argsort(x, order=('x', 'y'))
    array([2, 0, 4, 6, 5, 3, 1])
    """
def may_share_memory(*args, **kwargs) -> typing.Any:
    """
    may_share_memory(a, b, /, max_work=None)

    Determine if two arrays might share memory

    A return of True does not necessarily mean that the two arrays
    share any element.  It just means that they *might*.

    Only the memory bounds of a and b are checked by default.

    Parameters
    ----------
    a, b : ndarray
        Input arrays
    max_work : int, optional
        Effort to spend on solving the overlap problem.  See
        `shares_memory` for details.  Default for ``may_share_memory``
        is to do a bounds check.

    Returns
    -------
    out : bool

    See Also
    --------
    shares_memory

    Examples
    --------
    >>> np.may_share_memory(np.array([1,2]), np.array([5,8,9]))
    False
    >>> x = np.zeros([3, 4])
    >>> np.may_share_memory(x[:,0], x[:,1])
    True
    """
def min_scalar_type(*args, **kwargs) -> typing.Any:
    """
    min_scalar_type(a, /)

    For scalar ``a``, returns the data type with the smallest size
    and smallest scalar kind which can hold its value.  For non-scalar
    array ``a``, returns the vector's dtype unmodified.

    Floating point values are not demoted to integers,
    and complex values are not demoted to floats.

    Parameters
    ----------
    a : scalar or array_like
        The value whose minimal data type is to be found.

    Returns
    -------
    out : dtype
        The minimal data type.

    Notes
    -----
    .. versionadded:: 1.6.0

    See Also
    --------
    result_type, promote_types, dtype, can_cast

    Examples
    --------
    >>> np.min_scalar_type(10)
    dtype('uint8')

    >>> np.min_scalar_type(-260)
    dtype('int16')

    >>> np.min_scalar_type(3.1)
    dtype('float16')

    >>> np.min_scalar_type(1e50)
    dtype('float64')

    >>> np.min_scalar_type(np.arange(4,dtype='f8'))
    dtype('float64')
    """
def nested_iters(*args, **kwargs) -> typing.Any:
    """
    Create nditers for use in nested loops

    Create a tuple of `nditer` objects which iterate in nested loops over
    different axes of the op argument. The first iterator is used in the
    outermost loop, the last in the innermost loop. Advancing one will change
    the subsequent iterators to point at its new element.

    Parameters
    ----------
    op : ndarray or sequence of array_like
        The array(s) to iterate over.

    axes : list of list of int
        Each item is used as an "op_axes" argument to an nditer

    flags, op_flags, op_dtypes, order, casting, buffersize (optional)
        See `nditer` parameters of the same name

    Returns
    -------
    iters : tuple of nditer
        An nditer for each item in `axes`, outermost first

    See Also
    --------
    nditer

    Examples
    --------

    Basic usage. Note how y is the "flattened" version of
    [a[:, 0, :], a[:, 1, 0], a[:, 2, :]] since we specified
    the first iter's axes as [1]

    >>> a = np.arange(12).reshape(2, 3, 2)
    >>> i, j = np.nested_iters(a, [[1], [0, 2]], flags=["multi_index"])
    >>> for x in i:
    ...      print(i.multi_index)
    ...      for y in j:
    ...          print('', j.multi_index, y)
    (0,)
     (0, 0) 0
     (0, 1) 1
     (1, 0) 6
     (1, 1) 7
    (1,)
     (0, 0) 2
     (0, 1) 3
     (1, 0) 8
     (1, 1) 9
    (2,)
     (0, 0) 4
     (0, 1) 5
     (1, 0) 10
     (1, 1) 11
    """
def normalize_axis_index(*args, **kwargs) -> typing.Any:
    """
    Normalizes an axis index, `axis`, such that is a valid positive index into
    the shape of array with `ndim` dimensions. Raises an AxisError with an
    appropriate message if this is not possible.

    Used internally by all axis-checking logic.

    .. versionadded:: 1.13.0

    Parameters
    ----------
    axis : int
        The un-normalized index of the axis. Can be negative
    ndim : int
        The number of dimensions of the array that `axis` should be normalized
        against
    msg_prefix : str
        A prefix to put before the message, typically the name of the argument

    Returns
    -------
    normalized_axis : int
        The normalized axis index, such that `0 <= normalized_axis < ndim`

    Raises
    ------
    AxisError
        If the axis index is invalid, when `-ndim <= axis < ndim` is false.

    Examples
    --------
    >>> normalize_axis_index(0, ndim=3)
    0
    >>> normalize_axis_index(1, ndim=3)
    1
    >>> normalize_axis_index(-1, ndim=3)
    2

    >>> normalize_axis_index(3, ndim=3)
    Traceback (most recent call last):
    ...
    AxisError: axis 3 is out of bounds for array of dimension 3
    >>> normalize_axis_index(-4, ndim=3, msg_prefix='axes_arg')
    Traceback (most recent call last):
    ...
    AxisError: axes_arg: axis -4 is out of bounds for array of dimension 3
    """
def packbits(*args, **kwargs) -> typing.Any:
    """
    packbits(a, /, axis=None, bitorder='big')

    Packs the elements of a binary-valued array into bits in a uint8 array.

    The result is padded to full bytes by inserting zero bits at the end.

    Parameters
    ----------
    a : array_like
        An array of integers or booleans whose elements should be packed to
        bits.
    axis : int, optional
        The dimension over which bit-packing is done.
        ``None`` implies packing the flattened array.
    bitorder : {'big', 'little'}, optional
        The order of the input bits. 'big' will mimic bin(val),
        ``[0, 0, 0, 0, 0, 0, 1, 1] => 3 = 0b00000011``, 'little' will
        reverse the order so ``[1, 1, 0, 0, 0, 0, 0, 0] => 3``.
        Defaults to 'big'.

        .. versionadded:: 1.17.0

    Returns
    -------
    packed : ndarray
        Array of type uint8 whose elements represent bits corresponding to the
        logical (0 or nonzero) value of the input elements. The shape of
        `packed` has the same number of dimensions as the input (unless `axis`
        is None, in which case the output is 1-D).

    See Also
    --------
    unpackbits: Unpacks elements of a uint8 array into a binary-valued output
                array.

    Examples
    --------
    >>> a = np.array([[[1,0,1],
    ...                [0,1,0]],
    ...               [[1,1,0],
    ...                [0,0,1]]])
    >>> b = np.packbits(a, axis=-1)
    >>> b
    array([[[160],
            [ 64]],
           [[192],
            [ 32]]], dtype=uint8)

    Note that in binary 160 = 1010 0000, 64 = 0100 0000, 192 = 1100 0000,
    and 32 = 0010 0000.
    """
def promote_types(*args, **kwargs) -> typing.Any:
    """
    Returns the data type with the smallest size and smallest scalar
    kind to which both ``type1`` and ``type2`` may be safely cast.
    The returned data type is always considered "canonical", this mainly
    means that the promoted dtype will always be in native byte order.

    This function is symmetric, but rarely associative.

    Parameters
    ----------
    type1 : dtype or dtype specifier
        First data type.
    type2 : dtype or dtype specifier
        Second data type.

    Returns
    -------
    out : dtype
        The promoted data type.

    Notes
    -----
    Please see `numpy.result_type` for additional information about promotion.

    .. versionadded:: 1.6.0

    Starting in NumPy 1.9, promote_types function now returns a valid string
    length when given an integer or float dtype as one argument and a string
    dtype as another argument. Previously it always returned the input string
    dtype, even if it wasn't long enough to store the max integer/float value
    converted to a string.

    .. versionchanged:: 1.23.0

    NumPy now supports promotion for more structured dtypes.  It will now
    remove unnecessary padding from a structure dtype and promote included
    fields individually.

    See Also
    --------
    result_type, dtype, can_cast

    Examples
    --------
    >>> np.promote_types('f4', 'f8')
    dtype('float64')

    >>> np.promote_types('i8', 'f4')
    dtype('float64')

    >>> np.promote_types('>i8', '<c8')
    dtype('complex128')

    >>> np.promote_types('i4', 'S8')
    dtype('S11')

    An example of a non-associative case:

    >>> p = np.promote_types
    >>> p('S', p('i1', 'u1'))
    dtype('S6')
    >>> p(p('S', 'i1'), 'u1')
    dtype('S4')
    """
def putmask(*args, **kwargs) -> typing.Any:
    """
    putmask(a, mask, values)

    Changes elements of an array based on conditional and input values.

    Sets ``a.flat[n] = values[n]`` for each n where ``mask.flat[n]==True``.

    If `values` is not the same size as `a` and `mask` then it will repeat.
    This gives behavior different from ``a[mask] = values``.

    Parameters
    ----------
    a : ndarray
        Target array.
    mask : array_like
        Boolean mask array. It has to be the same shape as `a`.
    values : array_like
        Values to put into `a` where `mask` is True. If `values` is smaller
        than `a` it will be repeated.

    See Also
    --------
    place, put, take, copyto

    Examples
    --------
    >>> x = np.arange(6).reshape(2, 3)
    >>> np.putmask(x, x>2, x**2)
    >>> x
    array([[ 0,  1,  2],
           [ 9, 16, 25]])

    If `values` is smaller than `a` it is repeated:

    >>> x = np.arange(5)
    >>> np.putmask(x, x>1, [-33, -44])
    >>> x
    array([  0,   1, -33, -44, -33])
    """
def ravel_multi_index(*args, **kwargs) -> typing.Any:
    """
    ravel_multi_index(multi_index, dims, mode='raise', order='C')

    Converts a tuple of index arrays into an array of flat
    indices, applying boundary modes to the multi-index.

    Parameters
    ----------
    multi_index : tuple of array_like
        A tuple of integer arrays, one array for each dimension.
    dims : tuple of ints
        The shape of array into which the indices from ``multi_index`` apply.
    mode : {'raise', 'wrap', 'clip'}, optional
        Specifies how out-of-bounds indices are handled.  Can specify
        either one mode or a tuple of modes, one mode per index.

        * 'raise' -- raise an error (default)
        * 'wrap' -- wrap around
        * 'clip' -- clip to the range

        In 'clip' mode, a negative index which would normally
        wrap will clip to 0 instead.
    order : {'C', 'F'}, optional
        Determines whether the multi-index should be viewed as
        indexing in row-major (C-style) or column-major
        (Fortran-style) order.

    Returns
    -------
    raveled_indices : ndarray
        An array of indices into the flattened version of an array
        of dimensions ``dims``.

    See Also
    --------
    unravel_index

    Notes
    -----
    .. versionadded:: 1.6.0

    Examples
    --------
    >>> arr = np.array([[3,6,6],[4,5,1]])
    >>> np.ravel_multi_index(arr, (7,6))
    array([22, 41, 37])
    >>> np.ravel_multi_index(arr, (7,6), order='F')
    array([31, 41, 13])
    >>> np.ravel_multi_index(arr, (4,6), mode='clip')
    array([22, 23, 19])
    >>> np.ravel_multi_index(arr, (4,4), mode=('clip','wrap'))
    array([12, 13, 13])

    >>> np.ravel_multi_index((3,1,4,1), (6,7,8,9))
    1621
    """
def result_type(*args, **kwargs) -> typing.Any:
    """
    result_type(*arrays_and_dtypes)

    Returns the type that results from applying the NumPy
    type promotion rules to the arguments.

    Type promotion in NumPy works similarly to the rules in languages
    like C++, with some slight differences.  When both scalars and
    arrays are used, the array's type takes precedence and the actual value
    of the scalar is taken into account.

    For example, calculating 3*a, where a is an array of 32-bit floats,
    intuitively should result in a 32-bit float output.  If the 3 is a
    32-bit integer, the NumPy rules indicate it can't convert losslessly
    into a 32-bit float, so a 64-bit float should be the result type.
    By examining the value of the constant, '3', we see that it fits in
    an 8-bit integer, which can be cast losslessly into the 32-bit float.

    Parameters
    ----------
    arrays_and_dtypes : list of arrays and dtypes
        The operands of some operation whose result type is needed.

    Returns
    -------
    out : dtype
        The result type.

    See also
    --------
    dtype, promote_types, min_scalar_type, can_cast

    Notes
    -----
    .. versionadded:: 1.6.0

    The specific algorithm used is as follows.

    Categories are determined by first checking which of boolean,
    integer (int/uint), or floating point (float/complex) the maximum
    kind of all the arrays and the scalars are.

    If there are only scalars or the maximum category of the scalars
    is higher than the maximum category of the arrays,
    the data types are combined with :func:`promote_types`
    to produce the return value.

    Otherwise, `min_scalar_type` is called on each scalar, and
    the resulting data types are all combined with :func:`promote_types`
    to produce the return value.

    The set of int values is not a subset of the uint values for types
    with the same number of bits, something not reflected in
    :func:`min_scalar_type`, but handled as a special case in `result_type`.

    Examples
    --------
    >>> np.result_type(3, np.arange(7, dtype='i1'))
    dtype('int8')

    >>> np.result_type('i4', 'c8')
    dtype('complex128')

    >>> np.result_type(3.0, -2)
    dtype('float64')
    """
def scalar(*args, **kwargs) -> typing.Any:
    """
    Return a new scalar array of the given type initialized with obj.

    This function is meant mainly for pickle support. `dtype` must be a
    valid data-type descriptor. If `dtype` corresponds to an object
    descriptor, then `obj` can be any object, otherwise `obj` must be a
    string. If `obj` is not given, it will be interpreted as None for object
    type and as zeros for all other types.
    """
def set_datetimeparse_function(*args, **kwargs) -> typing.Any:
    pass
def set_legacy_print_mode(*args, **kwargs) -> typing.Any:
    pass
def set_numeric_ops(*args, **kwargs) -> typing.Any:
    """
    Set numerical operators for array objects.

    .. deprecated:: 1.16

        For the general case, use :c:func:`PyUFunc_ReplaceLoopBySignature`.
        For ndarray subclasses, define the ``__array_ufunc__`` method and
        override the relevant ufunc.

    Parameters
    ----------
    op1, op2, ... : callable
        Each ``op = func`` pair describes an operator to be replaced.
        For example, ``add = lambda x, y: np.add(x, y) % 5`` would replace
        addition by modulus 5 addition.

    Returns
    -------
    saved_ops : list of callables
        A list of all operators, stored before making replacements.

    Notes
    -----
    .. warning::
       Use with care!  Incorrect usage may lead to memory errors.

    A function replacing an operator cannot make use of that operator.
    For example, when replacing add, you may not use ``+``.  Instead,
    directly call ufuncs.

    Examples
    --------
    >>> def add_mod5(x, y):
    ...     return np.add(x, y) % 5
    ...
    >>> old_funcs = np.set_numeric_ops(add=add_mod5)

    >>> x = np.arange(12).reshape((3, 4))
    >>> x + x
    array([[0, 2, 4, 1],
           [3, 0, 2, 4],
           [1, 3, 0, 2]])

    >>> ignore = np.set_numeric_ops(**old_funcs) # restore operators
    """
def set_string_function(*args, **kwargs) -> typing.Any:
    """
    Internal method to set a function to be used when pretty printing arrays.
    """
def set_typeDict(*args, **kwargs) -> typing.Any:
    """
    Set the internal dictionary that can look up an array type using a
    registered code.
    """
def seterrobj(*args, **kwargs) -> typing.Any:
    """
    Set the object that defines floating-point error handling.

    The error object contains all information that defines the error handling
    behavior in NumPy. `seterrobj` is used internally by the other
    functions that set error handling behavior (`seterr`, `seterrcall`).

    Parameters
    ----------
    errobj : list
        The error object, a list containing three elements:
        [internal numpy buffer size, error mask, error callback function].

        The error mask is a single integer that holds the treatment information
        on all four floating point errors. The information for each error type
        is contained in three bits of the integer. If we print it in base 8, we
        can see what treatment is set for "invalid", "under", "over", and
        "divide" (in that order). The printed string can be interpreted with

        * 0 : 'ignore'
        * 1 : 'warn'
        * 2 : 'raise'
        * 3 : 'call'
        * 4 : 'print'
        * 5 : 'log'

    See Also
    --------
    geterrobj, seterr, geterr, seterrcall, geterrcall
    getbufsize, setbufsize

    Notes
    -----
    For complete documentation of the types of floating-point exceptions and
    treatment options, see `seterr`.

    Examples
    --------
    >>> old_errobj = np.geterrobj()  # first get the defaults
    >>> old_errobj
    [8192, 521, None]

    >>> def err_handler(type, flag):
    ...     print("Floating point error (%s), with flag %s" % (type, flag))
    ...
    >>> new_errobj = [20000, 12, err_handler]
    >>> np.seterrobj(new_errobj)
    >>> np.base_repr(12, 8)  # int for divide=4 ('print') and over=1 ('warn')
    '14'
    >>> np.geterr()
    {'over': 'warn', 'divide': 'print', 'invalid': 'ignore', 'under': 'ignore'}
    >>> np.geterrcall() is err_handler
    True
    """
def shares_memory(*args, **kwargs) -> typing.Any:
    """
    shares_memory(a, b, /, max_work=None)

    Determine if two arrays share memory.

    .. warning::

       This function can be exponentially slow for some inputs, unless
       `max_work` is set to a finite number or ``MAY_SHARE_BOUNDS``.
       If in doubt, use `numpy.may_share_memory` instead.

    Parameters
    ----------
    a, b : ndarray
        Input arrays
    max_work : int, optional
        Effort to spend on solving the overlap problem (maximum number
        of candidate solutions to consider). The following special
        values are recognized:

        max_work=MAY_SHARE_EXACT  (default)
            The problem is solved exactly. In this case, the function returns
            True only if there is an element shared between the arrays. Finding
            the exact solution may take extremely long in some cases.
        max_work=MAY_SHARE_BOUNDS
            Only the memory bounds of a and b are checked.

    Raises
    ------
    numpy.exceptions.TooHardError
        Exceeded max_work.

    Returns
    -------
    out : bool

    See Also
    --------
    may_share_memory

    Examples
    --------
    >>> x = np.array([1, 2, 3, 4])
    >>> np.shares_memory(x, np.array([5, 6, 7]))
    False
    >>> np.shares_memory(x[::2], x)
    True
    >>> np.shares_memory(x[::2], x[1::2])
    False

    Checking whether two arrays share memory is NP-complete, and
    runtime may increase exponentially in the number of
    dimensions. Hence, `max_work` should generally be set to a finite
    number, as it is possible to construct examples that take
    extremely long to run:

    >>> from numpy.lib.stride_tricks import as_strided
    >>> x = np.zeros([192163377], dtype=np.int8)
    >>> x1 = as_strided(x, strides=(36674, 61119, 85569), shape=(1049, 1049, 1049))
    >>> x2 = as_strided(x[64023025:], strides=(12223, 12224, 1), shape=(1049, 1049, 1))
    >>> np.shares_memory(x1, x2, max_work=1000)
    Traceback (most recent call last):
    ...
    numpy.exceptions.TooHardError: Exceeded max_work

    Running ``np.shares_memory(x1, x2)`` without `max_work` set takes
    around 1 minute for this case. It is possible to find problems
    that take still significantly longer.
    """
def unpackbits(*args, **kwargs) -> typing.Any:
    """
    unpackbits(a, /, axis=None, count=None, bitorder='big')

    Unpacks elements of a uint8 array into a binary-valued output array.

    Each element of `a` represents a bit-field that should be unpacked
    into a binary-valued output array. The shape of the output array is
    either 1-D (if `axis` is ``None``) or the same shape as the input
    array with unpacking done along the axis specified.

    Parameters
    ----------
    a : ndarray, uint8 type
       Input array.
    axis : int, optional
        The dimension over which bit-unpacking is done.
        ``None`` implies unpacking the flattened array.
    count : int or None, optional
        The number of elements to unpack along `axis`, provided as a way
        of undoing the effect of packing a size that is not a multiple
        of eight. A non-negative number means to only unpack `count`
        bits. A negative number means to trim off that many bits from
        the end. ``None`` means to unpack the entire array (the
        default). Counts larger than the available number of bits will
        add zero padding to the output. Negative counts must not
        exceed the available number of bits.

        .. versionadded:: 1.17.0

    bitorder : {'big', 'little'}, optional
        The order of the returned bits. 'big' will mimic bin(val),
        ``3 = 0b00000011 => [0, 0, 0, 0, 0, 0, 1, 1]``, 'little' will reverse
        the order to ``[1, 1, 0, 0, 0, 0, 0, 0]``.
        Defaults to 'big'.

        .. versionadded:: 1.17.0

    Returns
    -------
    unpacked : ndarray, uint8 type
       The elements are binary-valued (0 or 1).

    See Also
    --------
    packbits : Packs the elements of a binary-valued array into bits in
               a uint8 array.

    Examples
    --------
    >>> a = np.array([[2], [7], [23]], dtype=np.uint8)
    >>> a
    array([[ 2],
           [ 7],
           [23]], dtype=uint8)
    >>> b = np.unpackbits(a, axis=1)
    >>> b
    array([[0, 0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 1, 1, 1],
           [0, 0, 0, 1, 0, 1, 1, 1]], dtype=uint8)
    >>> c = np.unpackbits(a, axis=1, count=-3)
    >>> c
    array([[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0]], dtype=uint8)

    >>> p = np.packbits(b, axis=0)
    >>> np.unpackbits(p, axis=0)
    array([[0, 0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 1, 1, 1],
           [0, 0, 0, 1, 0, 1, 1, 1],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]], dtype=uint8)
    >>> np.array_equal(b, np.unpackbits(p, axis=0, count=b.shape[0]))
    True
    """
def unravel_index(*args, **kwargs) -> typing.Any:
    """
    unravel_index(indices, shape, order='C')

    Converts a flat index or array of flat indices into a tuple
    of coordinate arrays.

    Parameters
    ----------
    indices : array_like
        An integer array whose elements are indices into the flattened
        version of an array of dimensions ``shape``. Before version 1.6.0,
        this function accepted just one index value.
    shape : tuple of ints
        The shape of the array to use for unraveling ``indices``.

        .. versionchanged:: 1.16.0
            Renamed from ``dims`` to ``shape``.

    order : {'C', 'F'}, optional
        Determines whether the indices should be viewed as indexing in
        row-major (C-style) or column-major (Fortran-style) order.

        .. versionadded:: 1.6.0

    Returns
    -------
    unraveled_coords : tuple of ndarray
        Each array in the tuple has the same shape as the ``indices``
        array.

    See Also
    --------
    ravel_multi_index

    Examples
    --------
    >>> np.unravel_index([22, 41, 37], (7,6))
    (array([3, 6, 6]), array([4, 5, 1]))
    >>> np.unravel_index([31, 41, 13], (7,6), order='F')
    (array([3, 6, 6]), array([4, 5, 1]))

    >>> np.unravel_index(1621, (6,7,8,9))
    (3, 1, 4, 1)
    """
def vdot(*args, **kwargs) -> typing.Any:
    """
    vdot(a, b, /)

    Return the dot product of two vectors.

    The vdot(`a`, `b`) function handles complex numbers differently than
    dot(`a`, `b`).  If the first argument is complex the complex conjugate
    of the first argument is used for the calculation of the dot product.

    Note that `vdot` handles multidimensional arrays differently than `dot`:
    it does *not* perform a matrix product, but flattens input arguments
    to 1-D vectors first. Consequently, it should only be used for vectors.

    Parameters
    ----------
    a : array_like
        If `a` is complex the complex conjugate is taken before calculation
        of the dot product.
    b : array_like
        Second argument to the dot product.

    Returns
    -------
    output : ndarray
        Dot product of `a` and `b`.  Can be an int, float, or
        complex depending on the types of `a` and `b`.

    See Also
    --------
    dot : Return the dot product without using the complex conjugate of the
          first argument.

    Examples
    --------
    >>> a = np.array([1+2j,3+4j])
    >>> b = np.array([5+6j,7+8j])
    >>> np.vdot(a, b)
    (70-8j)
    >>> np.vdot(b, a)
    (70+8j)

    Note that higher-dimensional arrays are flattened!

    >>> a = np.array([[1, 4], [5, 6]])
    >>> b = np.array([[4, 1], [2, 2]])
    >>> np.vdot(a, b)
    30
    >>> np.vdot(b, a)
    30
    >>> 1*4 + 4*1 + 5*2 + 6*2
    30
    """
def where(*args, **kwargs) -> typing.Any:
    """
    where(condition, [x, y], /)

    Return elements chosen from `x` or `y` depending on `condition`.

    .. note::
        When only `condition` is provided, this function is a shorthand for
        ``np.asarray(condition).nonzero()``. Using `nonzero` directly should be
        preferred, as it behaves correctly for subclasses. The rest of this
        documentation covers only the case where all three arguments are
        provided.

    Parameters
    ----------
    condition : array_like, bool
        Where True, yield `x`, otherwise yield `y`.
    x, y : array_like
        Values from which to choose. `x`, `y` and `condition` need to be
        broadcastable to some shape.

    Returns
    -------
    out : ndarray
        An array with elements from `x` where `condition` is True, and elements
        from `y` elsewhere.

    See Also
    --------
    choose
    nonzero : The function that is called when x and y are omitted

    Notes
    -----
    If all the arrays are 1-D, `where` is equivalent to::

        [xv if c else yv
         for c, xv, yv in zip(condition, x, y)]

    Examples
    --------
    >>> a = np.arange(10)
    >>> a
    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    >>> np.where(a < 5, a, 10*a)
    array([ 0,  1,  2,  3,  4, 50, 60, 70, 80, 90])

    This can be used on multidimensional arrays too:

    >>> np.where([[True, False], [True, True]],
    ...          [[1, 2], [3, 4]],
    ...          [[9, 8], [7, 6]])
    array([[1, 8],
           [3, 4]])

    The shapes of x, y, and the condition are broadcast together:

    >>> x, y = np.ogrid[:3, :4]
    >>> np.where(x < y, x, 10 + y)  # both x and 10+y are broadcast
    array([[10,  0,  0,  0],
           [10, 11,  1,  1],
           [10, 11, 12,  2]])

    >>> a = np.array([[0, 1, 2],
    ...               [0, 2, 4],
    ...               [0, 3, 6]])
    >>> np.where(a < 4, a, -1)  # -1 is broadcast
    array([[ 0,  1,  2],
           [ 0,  2, -1],
           [ 0,  3, -1]])
    """
def zeros(*args, **kwargs) -> typing.Any:
    """
    Return a new array of given shape and type, filled with zeros.

    Parameters
    ----------
    shape : int or tuple of ints
        Shape of the new array, e.g., ``(2, 3)`` or ``2``.
    dtype : data-type, optional
        The desired data-type for the array, e.g., `numpy.int8`.  Default is
        `numpy.float64`.
    order : {'C', 'F'}, optional, default: 'C'
        Whether to store multi-dimensional data in row-major
        (C-style) or column-major (Fortran-style) order in
        memory.
    like : array_like, optional
        Reference object to allow the creation of arrays which are not
        NumPy arrays. If an array-like passed in as ``like`` supports
        the ``__array_function__`` protocol, the result will be defined
        by it. In this case, it ensures the creation of an array object
        compatible with that passed in via this argument.

        .. versionadded:: 1.20.0

    Returns
    -------
    out : ndarray
        Array of zeros with the given shape, dtype, and order.

    See Also
    --------
    zeros_like : Return an array of zeros with shape and type of input.
    empty : Return a new uninitialized array.
    ones : Return a new array setting values to one.
    full : Return a new array of given shape filled with value.

    Examples
    --------
    >>> np.zeros(5)
    array([ 0.,  0.,  0.,  0.,  0.])

    >>> np.zeros((5,), dtype=int)
    array([0, 0, 0, 0, 0])

    >>> np.zeros((2, 1))
    array([[ 0.],
           [ 0.]])

    >>> s = (2,2)
    >>> np.zeros(s)
    array([[ 0.,  0.],
           [ 0.,  0.]])

    >>> np.zeros((2,), dtype=[('x', 'i4'), ('y', 'i4')]) # custom dtype
    array([(0, 0), (0, 0)],
          dtype=[('x', '<i4'), ('y', '<i4')])
    """
ALLOW_THREADS = 1
BUFSIZE = 8192
CLIP = 0
DATETIMEUNITS: typing.Any  # PyCapsule()
ERR_CALL = 3
ERR_DEFAULT = 521
ERR_IGNORE = 0
ERR_LOG = 5
ERR_PRINT = 4
ERR_RAISE = 2
ERR_WARN = 1
FLOATING_POINT_SUPPORT = 1
FPE_DIVIDEBYZERO = 1
FPE_INVALID = 8
FPE_OVERFLOW = 2
FPE_UNDERFLOW = 4
ITEM_HASOBJECT = 1
ITEM_IS_POINTER = 4
LIST_PICKLE = 2
MAXDIMS = 32
MAY_SHARE_BOUNDS = 0
MAY_SHARE_EXACT = -1
NAN: float # value = nan
NEEDS_INIT = 8
NEEDS_PYAPI = 16
NINF: float # value = -inf
NZERO = -0.0
PINF: float # value = inf
PZERO = 0.0
RAISE = 2
SHIFT_DIVIDEBYZERO = 0
SHIFT_INVALID = 9
SHIFT_OVERFLOW = 3
SHIFT_UNDERFLOW = 6
UFUNC_BUFSIZE_DEFAULT = 8192
UFUNC_PYVALS_NAME = 'UFUNC_PYVALS'
USE_GETITEM = 32
USE_SETITEM = 64
WRAP = 1
_ARRAY_API: typing.Any  # PyCapsule()
_UFUNC_API: typing.Any  # PyCapsule()
__cpu_baseline__ = ['SSE', 'SSE2', 'SSE3']
__cpu_dispatch__ = ['SSSE3', 'SSE41', 'POPCNT', 'SSE42', 'AVX', 'F16C', 'FMA3', 'AVX2', 'AVX512F', 'AVX512CD', 'AVX512_KNL', 'AVX512_KNM', 'AVX512_SKX', 'AVX512_CLX', 'AVX512_CNL', 'AVX512_ICL']
__cpu_features__ = {'MMX': True, 'SSE': True, 'SSE2': True, 'SSE3': True, 'SSSE3': True, 'SSE41': True, 'POPCNT': True, 'SSE42': True, 'AVX': True, 'F16C': True, 'XOP': False, 'FMA4': False, 'FMA3': True, 'AVX2': True, 'AVX512F': False, 'AVX512CD': False, 'AVX512ER': False, 'AVX512PF': False, 'AVX5124FMAPS': False, 'AVX5124VNNIW': False, 'AVX512VPOPCNTDQ': False, 'AVX512VL': False, 'AVX512BW': False, 'AVX512DQ': False, 'AVX512VNNI': False, 'AVX512IFMA': False, 'AVX512VBMI': False, 'AVX512VBMI2': False, 'AVX512BITALG': False, 'AVX512FP16': False, 'AVX512_KNL': False, 'AVX512_KNM': False, 'AVX512_SKX': False, 'AVX512_CLX': False, 'AVX512_CNL': False, 'AVX512_ICL': False, 'AVX512_SPR': False, 'VSX': False, 'VSX2': False, 'VSX3': False, 'VSX4': False, 'VX': False, 'VXE': False, 'VXE2': False, 'NEON': False, 'NEON_FP16': False, 'NEON_VFPV4': False, 'ASIMD': False, 'FPHP': False, 'ASIMDHP': False, 'ASIMDDP': False, 'ASIMDFHM': False}
__version__ = '3.1'
_arg: numpy.ufunc # value = <ufunc '_arg'>
_flagdict = {'OWNDATA': 4, 'O': 4, 'FORTRAN': 2, 'F': 2, 'CONTIGUOUS': 1, 'C': 1, 'ALIGNED': 256, 'A': 256, 'WRITEBACKIFCOPY': 8192, 'X': 8192, 'WRITEABLE': 1024, 'W': 1024, 'C_CONTIGUOUS': 1, 'F_CONTIGUOUS': 2}
_ones_like: numpy.ufunc # value = <ufunc '_ones_like'>
absolute: numpy.ufunc # value = <ufunc 'absolute'>
add: numpy.ufunc # value = <ufunc 'add'>
arccos: numpy.ufunc # value = <ufunc 'arccos'>
arccosh: numpy.ufunc # value = <ufunc 'arccosh'>
arcsin: numpy.ufunc # value = <ufunc 'arcsin'>
arcsinh: numpy.ufunc # value = <ufunc 'arcsinh'>
arctan: numpy.ufunc # value = <ufunc 'arctan'>
arctan2: numpy.ufunc # value = <ufunc 'arctan2'>
arctanh: numpy.ufunc # value = <ufunc 'arctanh'>
bitwise_and: numpy.ufunc # value = <ufunc 'bitwise_and'>
bitwise_or: numpy.ufunc # value = <ufunc 'bitwise_or'>
bitwise_xor: numpy.ufunc # value = <ufunc 'bitwise_xor'>
cbrt: numpy.ufunc # value = <ufunc 'cbrt'>
ceil: numpy.ufunc # value = <ufunc 'ceil'>
clip: numpy.ufunc # value = <ufunc 'clip'>
conj: numpy.ufunc # value = <ufunc 'conjugate'>
conjugate: numpy.ufunc # value = <ufunc 'conjugate'>
copysign: numpy.ufunc # value = <ufunc 'copysign'>
cos: numpy.ufunc # value = <ufunc 'cos'>
cosh: numpy.ufunc # value = <ufunc 'cosh'>
deg2rad: numpy.ufunc # value = <ufunc 'deg2rad'>
degrees: numpy.ufunc # value = <ufunc 'degrees'>
divide: numpy.ufunc # value = <ufunc 'divide'>
divmod: numpy.ufunc # value = <ufunc 'divmod'>
e = 2.718281828459045
equal: numpy.ufunc # value = <ufunc 'equal'>
euler_gamma = 0.5772156649015329
exp: numpy.ufunc # value = <ufunc 'exp'>
exp2: numpy.ufunc # value = <ufunc 'exp2'>
expm1: numpy.ufunc # value = <ufunc 'expm1'>
fabs: numpy.ufunc # value = <ufunc 'fabs'>
float_power: numpy.ufunc # value = <ufunc 'float_power'>
floor: numpy.ufunc # value = <ufunc 'floor'>
floor_divide: numpy.ufunc # value = <ufunc 'floor_divide'>
fmax: numpy.ufunc # value = <ufunc 'fmax'>
fmin: numpy.ufunc # value = <ufunc 'fmin'>
fmod: numpy.ufunc # value = <ufunc 'fmod'>
frexp: numpy.ufunc # value = <ufunc 'frexp'>
gcd: numpy.ufunc # value = <ufunc 'gcd'>
greater: numpy.ufunc # value = <ufunc 'greater'>
greater_equal: numpy.ufunc # value = <ufunc 'greater_equal'>
heaviside: numpy.ufunc # value = <ufunc 'heaviside'>
hypot: numpy.ufunc # value = <ufunc 'hypot'>
invert: numpy.ufunc # value = <ufunc 'invert'>
isfinite: numpy.ufunc # value = <ufunc 'isfinite'>
isinf: numpy.ufunc # value = <ufunc 'isinf'>
isnan: numpy.ufunc # value = <ufunc 'isnan'>
isnat: numpy.ufunc # value = <ufunc 'isnat'>
lcm: numpy.ufunc # value = <ufunc 'lcm'>
ldexp: numpy.ufunc # value = <ufunc 'ldexp'>
left_shift: numpy.ufunc # value = <ufunc 'left_shift'>
less: numpy.ufunc # value = <ufunc 'less'>
less_equal: numpy.ufunc # value = <ufunc 'less_equal'>
log: numpy.ufunc # value = <ufunc 'log'>
log10: numpy.ufunc # value = <ufunc 'log10'>
log1p: numpy.ufunc # value = <ufunc 'log1p'>
log2: numpy.ufunc # value = <ufunc 'log2'>
logaddexp: numpy.ufunc # value = <ufunc 'logaddexp'>
logaddexp2: numpy.ufunc # value = <ufunc 'logaddexp2'>
logical_and: numpy.ufunc # value = <ufunc 'logical_and'>
logical_not: numpy.ufunc # value = <ufunc 'logical_not'>
logical_or: numpy.ufunc # value = <ufunc 'logical_or'>
logical_xor: numpy.ufunc # value = <ufunc 'logical_xor'>
matmul: numpy.ufunc # value = <ufunc 'matmul'>
maximum: numpy.ufunc # value = <ufunc 'maximum'>
minimum: numpy.ufunc # value = <ufunc 'minimum'>
mod: numpy.ufunc # value = <ufunc 'remainder'>
modf: numpy.ufunc # value = <ufunc 'modf'>
multiply: numpy.ufunc # value = <ufunc 'multiply'>
negative: numpy.ufunc # value = <ufunc 'negative'>
nextafter: numpy.ufunc # value = <ufunc 'nextafter'>
not_equal: numpy.ufunc # value = <ufunc 'not_equal'>
pi = 3.141592653589793
positive: numpy.ufunc # value = <ufunc 'positive'>
power: numpy.ufunc # value = <ufunc 'power'>
rad2deg: numpy.ufunc # value = <ufunc 'rad2deg'>
radians: numpy.ufunc # value = <ufunc 'radians'>
reciprocal: numpy.ufunc # value = <ufunc 'reciprocal'>
remainder: numpy.ufunc # value = <ufunc 'remainder'>
right_shift: numpy.ufunc # value = <ufunc 'right_shift'>
rint: numpy.ufunc # value = <ufunc 'rint'>
sign: numpy.ufunc # value = <ufunc 'sign'>
signbit: numpy.ufunc # value = <ufunc 'signbit'>
sin: numpy.ufunc # value = <ufunc 'sin'>
sinh: numpy.ufunc # value = <ufunc 'sinh'>
spacing: numpy.ufunc # value = <ufunc 'spacing'>
sqrt: numpy.ufunc # value = <ufunc 'sqrt'>
square: numpy.ufunc # value = <ufunc 'square'>
subtract: numpy.ufunc # value = <ufunc 'subtract'>
tan: numpy.ufunc # value = <ufunc 'tan'>
tanh: numpy.ufunc # value = <ufunc 'tanh'>
tracemalloc_domain = 389047
true_divide: numpy.ufunc # value = <ufunc 'divide'>
trunc: numpy.ufunc # value = <ufunc 'trunc'>
typeinfo: dict # value = {'BOOL': numpy.core.multiarray.typeinforanged(char='?', num=0, bits=8, alignment=1, max=1, min=0, type=<class 'numpy.bool_'>), 'BYTE': numpy.core.multiarray.typeinforanged(char='b', num=1, bits=8, alignment=1, max=127, min=-128, type=<class 'numpy.int8'>), 'UBYTE': numpy.core.multiarray.typeinforanged(char='B', num=2, bits=8, alignment=1, max=255, min=0, type=<class 'numpy.uint8'>), 'SHORT': numpy.core.multiarray.typeinforanged(char='h', num=3, bits=16, alignment=2, max=32767, min=-32768, type=<class 'numpy.int16'>), 'USHORT': numpy.core.multiarray.typeinforanged(char='H', num=4, bits=16, alignment=2, max=65535, min=0, type=<class 'numpy.uint16'>), 'INT': numpy.core.multiarray.typeinforanged(char='i', num=5, bits=32, alignment=4, max=2147483647, min=-2147483648, type=<class 'numpy.int32'>), 'UINT': numpy.core.multiarray.typeinforanged(char='I', num=6, bits=32, alignment=4, max=4294967295, min=0, type=<class 'numpy.uint32'>), 'INTP': numpy.core.multiarray.typeinforanged(char='p', num=7, bits=64, alignment=8, max=9223372036854775807, min=-9223372036854775808, type=<class 'numpy.int64'>), 'UINTP': numpy.core.multiarray.typeinforanged(char='P', num=8, bits=64, alignment=8, max=18446744073709551615, min=0, type=<class 'numpy.uint64'>), 'LONG': numpy.core.multiarray.typeinforanged(char='l', num=7, bits=64, alignment=8, max=9223372036854775807, min=-9223372036854775808, type=<class 'numpy.int64'>), 'ULONG': numpy.core.multiarray.typeinforanged(char='L', num=8, bits=64, alignment=8, max=18446744073709551615, min=0, type=<class 'numpy.uint64'>), 'LONGLONG': numpy.core.multiarray.typeinforanged(char='q', num=9, bits=64, alignment=8, max=9223372036854775807, min=-9223372036854775808, type=<class 'numpy.longlong'>), 'ULONGLONG': numpy.core.multiarray.typeinforanged(char='Q', num=10, bits=64, alignment=8, max=18446744073709551615, min=0, type=<class 'numpy.ulonglong'>), 'HALF': numpy.core.multiarray.typeinfo(char='e', num=23, bits=16, alignment=2, type=<class 'numpy.float16'>), 'FLOAT': numpy.core.multiarray.typeinfo(char='f', num=11, bits=32, alignment=4, type=<class 'numpy.float32'>), 'DOUBLE': numpy.core.multiarray.typeinfo(char='d', num=12, bits=64, alignment=8, type=<class 'numpy.float64'>), 'LONGDOUBLE': numpy.core.multiarray.typeinfo(char='g', num=13, bits=128, alignment=16, type=<class 'numpy.longdouble'>), 'CFLOAT': numpy.core.multiarray.typeinfo(char='F', num=14, bits=64, alignment=4, type=<class 'numpy.complex64'>), 'CDOUBLE': numpy.core.multiarray.typeinfo(char='D', num=15, bits=128, alignment=8, type=<class 'numpy.complex128'>), 'CLONGDOUBLE': numpy.core.multiarray.typeinfo(char='G', num=16, bits=256, alignment=16, type=<class 'numpy.clongdouble'>), 'OBJECT': numpy.core.multiarray.typeinfo(char='O', num=17, bits=64, alignment=8, type=<class 'numpy.object_'>), 'STRING': numpy.core.multiarray.typeinfo(char='S', num=18, bits=0, alignment=1, type=<class 'numpy.bytes_'>), 'UNICODE': numpy.core.multiarray.typeinfo(char='U', num=19, bits=0, alignment=4, type=<class 'numpy.str_'>), 'VOID': numpy.core.multiarray.typeinfo(char='V', num=20, bits=0, alignment=1, type=<class 'numpy.void'>), 'DATETIME': numpy.core.multiarray.typeinforanged(char='M', num=21, bits=64, alignment=8, max=9223372036854775807, min=-9223372036854775808, type=<class 'numpy.datetime64'>), 'TIMEDELTA': numpy.core.multiarray.typeinforanged(char='m', num=22, bits=64, alignment=8, max=9223372036854775807, min=-9223372036854775808, type=<class 'numpy.timedelta64'>), 'Generic': <class 'numpy.generic'>, 'Number': <class 'numpy.number'>, 'Integer': <class 'numpy.integer'>, 'Inexact': <class 'numpy.inexact'>, 'SignedInteger': <class 'numpy.signedinteger'>, 'UnsignedInteger': <class 'numpy.unsignedinteger'>, 'Floating': <class 'numpy.floating'>, 'ComplexFloating': <class 'numpy.complexfloating'>, 'Flexible': <class 'numpy.flexible'>, 'Character': <class 'numpy.character'>}
error = Exception
