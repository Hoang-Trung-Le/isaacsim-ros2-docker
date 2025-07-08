from __future__ import annotations
import numpy.linalg._umath_linalg
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "cholesky_lo",
    "det",
    "eig",
    "eigh_lo",
    "eigh_up",
    "eigvals",
    "eigvalsh_lo",
    "eigvalsh_up",
    "inv",
    "lstsq_m",
    "lstsq_n",
    "qr_complete",
    "qr_r_raw_m",
    "qr_r_raw_n",
    "qr_reduced",
    "slogdet",
    "solve",
    "solve1",
    "svd_m",
    "svd_m_f",
    "svd_m_s",
    "svd_n",
    "svd_n_f",
    "svd_n_s"
]


__version__ = '0.1.5'
_ilp64 = True
cholesky_lo: numpy.ufunc # value = <ufunc 'cholesky_lo'>
det: numpy.ufunc # value = <ufunc 'det'>
eig: numpy.ufunc # value = <ufunc 'eig'>
eigh_lo: numpy.ufunc # value = <ufunc 'eigh_lo'>
eigh_up: numpy.ufunc # value = <ufunc 'eigh_up'>
eigvals: numpy.ufunc # value = <ufunc 'eigvals'>
eigvalsh_lo: numpy.ufunc # value = <ufunc 'eigvalsh_lo'>
eigvalsh_up: numpy.ufunc # value = <ufunc 'eigvalsh_up'>
inv: numpy.ufunc # value = <ufunc 'inv'>
lstsq_m: numpy.ufunc # value = <ufunc 'lstsq_m'>
lstsq_n: numpy.ufunc # value = <ufunc 'lstsq_n'>
qr_complete: numpy.ufunc # value = <ufunc 'qr_complete'>
qr_r_raw_m: numpy.ufunc # value = <ufunc 'qr_r_raw_m'>
qr_r_raw_n: numpy.ufunc # value = <ufunc 'qr_r_raw_n'>
qr_reduced: numpy.ufunc # value = <ufunc 'qr_reduced'>
slogdet: numpy.ufunc # value = <ufunc 'slogdet'>
solve: numpy.ufunc # value = <ufunc 'solve'>
solve1: numpy.ufunc # value = <ufunc 'solve1'>
svd_m: numpy.ufunc # value = <ufunc 'svd_m'>
svd_m_f: numpy.ufunc # value = <ufunc 'svd_m_f'>
svd_m_s: numpy.ufunc # value = <ufunc 'svd_m_s'>
svd_n: numpy.ufunc # value = <ufunc 'svd_n'>
svd_n_f: numpy.ufunc # value = <ufunc 'svd_n_f'>
svd_n_s: numpy.ufunc # value = <ufunc 'svd_n_s'>
