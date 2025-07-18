from __future__ import annotations
import numpy.random._mt19937
import typing
import numpy
import numpy.random.bit_generator
import operator
_Shape = typing.Tuple[int, ...]

__all__ = [
    "MT19937"
]


class MT19937(numpy.random.bit_generator.BitGenerator):
    """
    MT19937(seed=None)

    Container for the Mersenne Twister pseudo-random number generator.

    Parameters
    ----------
    seed : {None, int, array_like[ints], SeedSequence}, optional
        A seed to initialize the `BitGenerator`. If None, then fresh,
        unpredictable entropy will be pulled from the OS. If an ``int`` or
        ``array_like[ints]`` is passed, then it will be passed to
        `SeedSequence` to derive the initial `BitGenerator` state. One may also
        pass in a `SeedSequence` instance.

    Attributes
    ----------
    lock: threading.Lock
        Lock instance that is shared so that the same bit git generator can
        be used in multiple Generators without corrupting the state. Code that
        generates values from a bit generator should hold the bit generator's
        lock.

    Notes
    -----
    ``MT19937`` provides a capsule containing function pointers that produce
    doubles, and unsigned 32 and 64- bit integers [1]_. These are not
    directly consumable in Python and must be consumed by a ``Generator``
    or similar object that supports low-level access.

    The Python stdlib module "random" also contains a Mersenne Twister
    pseudo-random number generator.

    **State and Seeding**

    The ``MT19937`` state vector consists of a 624-element array of
    32-bit unsigned integers plus a single integer value between 0 and 624
    that indexes the current position within the main array.

    The input seed is processed by `SeedSequence` to fill the whole state. The
    first element is reset such that only its most significant bit is set.

    **Parallel Features**

    The preferred way to use a BitGenerator in parallel applications is to use
    the `SeedSequence.spawn` method to obtain entropy values, and to use these
    to generate new BitGenerators:

    >>> from numpy.random import Generator, MT19937, SeedSequence
    >>> sg = SeedSequence(1234)
    >>> rg = [Generator(MT19937(s)) for s in sg.spawn(10)]

    Another method is to use `MT19937.jumped` which advances the state as-if
    :math:`2^{128}` random numbers have been generated ([1]_, [2]_). This
    allows the original sequence to be split so that distinct segments can be
    used in each worker process. All generators should be chained to ensure
    that the segments come from the same sequence.

    >>> from numpy.random import Generator, MT19937, SeedSequence
    >>> sg = SeedSequence(1234)
    >>> bit_generator = MT19937(sg)
    >>> rg = []
    >>> for _ in range(10):
    ...    rg.append(Generator(bit_generator))
    ...    # Chain the BitGenerators
    ...    bit_generator = bit_generator.jumped()

    **Compatibility Guarantee**

    ``MT19937`` makes a guarantee that a fixed seed will always produce
    the same random integer stream.

    References
    ----------
    .. [1] Hiroshi Haramoto, Makoto Matsumoto, and Pierre L'Ecuyer, "A Fast
        Jump Ahead Algorithm for Linear Recurrences in a Polynomial Space",
        Sequences and Their Applications - SETA, 290--298, 2008.
    .. [2] Hiroshi Haramoto, Makoto Matsumoto, Takuji Nishimura, François
        Panneton, Pierre L'Ecuyer, "Efficient Jump Ahead for F2-Linear
        Random Number Generators", INFORMS JOURNAL ON COMPUTING, Vol. 20,
        No. 3, Summer 2008, pp. 385-390.
    """
    @staticmethod
    def _legacy_seeding(*args, **kwargs) -> typing.Any: 
        """
        _legacy_seeding(seed)

        Seed the generator in a backward compatible way. For modern
        applications, creating a new instance is preferable. Calling this
        overrides self._seed_seq

        Parameters
        ----------
        seed : {None, int, array_like}
            Random seed initializing the pseudo-random number generator.
            Can be an integer in [0, 2**32-1], array of integers in
            [0, 2**32-1], a `SeedSequence, or ``None``. If `seed`
            is ``None``, then fresh, unpredictable entropy will be pulled from
            the OS.

        Raises
        ------
        ValueError
            If seed values are out of range for the PRNG.
        """
    @staticmethod
    def jumped(*args, **kwargs) -> typing.Any: 
        """
        jumped(jumps=1)

        Returns a new bit generator with the state jumped

        The state of the returned bit generator is jumped as-if
        2**(128 * jumps) random numbers have been generated.

        Parameters
        ----------
        jumps : integer, positive
            Number of times to jump the state of the bit generator returned

        Returns
        -------
        bit_generator : MT19937
            New instance of generator jumped iter times

        Notes
        -----
        The jump step is computed using a modified version of Matsumoto's
        implementation of Horner's method. The step polynomial is precomputed
        to perform 2**128 steps. The jumped state has been verified to match
        the state produced using Matsumoto's original code.

        References
        ----------
        .. [1] Matsumoto, M, Generating multiple disjoint streams of
           pseudorandom number sequences.  Accessed on: May 6, 2020.
           http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/JUMP/
        .. [2] Hiroshi Haramoto, Makoto Matsumoto, Takuji Nishimura, François
           Panneton, Pierre L'Ecuyer, "Efficient Jump Ahead for F2-Linear
           Random Number Generators", INFORMS JOURNAL ON COMPUTING, Vol. 20,
           No. 3, Summer 2008, pp. 385-390.
        """
    __pyx_vtable__: typing.Any  # PyCapsule()
    state: getset_descriptor # value = <attribute 'state' of 'numpy.random._mt19937.MT19937' objects>
    pass
__all__ = ['MT19937']
__test__ = {}
np = numpy
operator = operator
