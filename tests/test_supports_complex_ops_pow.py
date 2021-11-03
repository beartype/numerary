# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import cast

import pytest

from numerary.bt import beartype
from numerary.types import (
    SupportsComplexOps,
    SupportsComplexOpsSCT,
    SupportsComplexOpsSCU,
    SupportsComplexPow,
    SupportsComplexPowSCT,
    SupportsComplexPowSCU,
)

from .numberwang import (
    Numberwang,
    NumberwangDerived,
    NumberwangRegistered,
    Wangernumb,
    WangernumbDerived,
    WangernumbRegistered,
)

__all__ = ()


# ---- Functions -----------------------------------------------------------------------


@beartype
def ops_func(arg: SupportsComplexOps):
    assert isinstance(arg, SupportsComplexOps), f"{arg!r}"


@beartype
def ops_func_t(arg: SupportsComplexOpsSCU):
    assert isinstance(arg, SupportsComplexOpsSCT), f"{arg!r}"


@beartype
def pow_func(arg: SupportsComplexPow):
    assert isinstance(arg, SupportsComplexPow), f"{arg!r}"


@beartype
def pow_func_t(arg: SupportsComplexPowSCU):
    assert isinstance(arg, SupportsComplexPowSCT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_complex_ops_pow() -> None:
    bool_val: SupportsComplexOps = True
    int_val: SupportsComplexOps = -273
    float_val: SupportsComplexOps = -273.15
    complex_val: SupportsComplexOps = complex(-273.15)
    frac_val: SupportsComplexOps = Fraction(-27315, 100)
    dec_val: SupportsComplexOps = Decimal("-273.15")
    nw_val: SupportsComplexOps = Numberwang(-273)
    nwd_val: SupportsComplexOps = NumberwangDerived(-273)
    nwr_val: SupportsComplexOps = NumberwangRegistered(-273)
    wn_val: SupportsComplexOps = Wangernumb(-273.15)
    wnd_val: SupportsComplexOps = WangernumbDerived(-273.15)
    wnr_val: SupportsComplexOps = WangernumbRegistered(-273.15)
    _: SupportsComplexPow
    _ = True
    _ = -273
    _ = -273.15
    _ = complex(-273.15)
    _ = Fraction(-27315, 100)
    _ = Decimal("-273.15")
    _ = Numberwang(-273)
    _ = NumberwangDerived(-273)
    _ = NumberwangRegistered(-273)
    _ = Wangernumb(-273.15)
    _ = WangernumbDerived(-273.15)
    _ = WangernumbRegistered(-273.15)

    for good_val in (
        bool_val,
        int_val,
        float_val,
        complex_val,
        frac_val,
        dec_val,
        nw_val,
        nwd_val,
        nwr_val,
        wn_val,
        wnd_val,
        wnr_val,
    ):
        assert isinstance(good_val, SupportsComplexOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexOpsSCT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPow), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPowSCT), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"

    for bad_val in ("-273.15",):
        assert not isinstance(bad_val, SupportsComplexOps), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsComplexOpsSCT), f"{bad_val!r}"


def test_supports_complex_ops_pow_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
    ):
        ops_func(cast(SupportsComplexOps, good_val))
        ops_func_t(cast(SupportsComplexOpsSCU, good_val))
        pow_func(cast(SupportsComplexPow, good_val))
        pow_func_t(cast(SupportsComplexPowSCU, good_val))

    for bad_val in ("-273.15",):
        with pytest.raises(roar.BeartypeException):
            ops_func(cast(SupportsComplexOps, bad_val))

        with pytest.raises(roar.BeartypeException):
            ops_func_t(cast(SupportsComplexOpsSCU, bad_val))

        with pytest.raises(roar.BeartypeException):
            pow_func(cast(SupportsComplexPow, bad_val))

        with pytest.raises(roar.BeartypeException):
            pow_func_t(cast(SupportsComplexPowSCU, bad_val))


def test_supports_complex_ops_pow_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsComplexOps = numpy.uint8(2)
    uint16_val: SupportsComplexOps = numpy.uint16(273)
    uint32_val: SupportsComplexOps = numpy.uint32(273)
    uint64_val: SupportsComplexOps = numpy.uint64(273)
    int8_val: SupportsComplexOps = numpy.int8(-2)
    int16_val: SupportsComplexOps = numpy.int16(-273)
    int32_val: SupportsComplexOps = numpy.int32(-273)
    int64_val: SupportsComplexOps = numpy.int64(-273)
    float16_val: SupportsComplexOps = numpy.float16(-1.8)
    float32_val: SupportsComplexOps = numpy.float32(-273.15)
    float64_val: SupportsComplexOps = numpy.float64(-273.15)
    float128_val: SupportsComplexOps = numpy.float128(-273.15)
    csingle_val: SupportsComplexOps = numpy.float32(-273.15)
    cdouble_val: SupportsComplexOps = numpy.float64(-273.15)
    clongdouble_val: SupportsComplexOps = numpy.float128(-273.15)
    _: SupportsComplexPow
    _ = numpy.uint8(2)
    _ = numpy.uint16(273)
    _ = numpy.uint32(273)
    _ = numpy.uint64(273)
    _ = numpy.int8(-2)
    _ = numpy.int16(-273)
    _ = numpy.int32(-273)
    _ = numpy.int64(-273)
    _ = numpy.float16(-1.8)
    _ = numpy.float32(-273.15)
    _ = numpy.float64(-273.15)
    _ = numpy.float128(-273.15)
    _ = numpy.float32(-273.15)
    _ = numpy.float64(-273.15)
    _ = numpy.float128(-273.15)

    for good_val in (
        uint8_val,
        uint16_val,
        uint32_val,
        uint64_val,
        int8_val,
        int16_val,
        int32_val,
        int64_val,
        float16_val,
        float32_val,
        float64_val,
        float128_val,
        csingle_val,
        cdouble_val,
        clongdouble_val,
    ):
        assert isinstance(good_val, SupportsComplexOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexOpsSCT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"

        # numpy.uint*.__neg__ means something different than what we're testing for
        if not isinstance(
            good_val,
            (numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64),
        ):
            assert 0 - good_val == -good_val, f"{good_val!r}"

        assert isinstance(good_val, SupportsComplexPow), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPowSCT), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"


def test_supports_complex_ops_pow_numpy_beartype() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        numpy.uint8(2),
        numpy.uint16(273),
        numpy.uint32(273),
        numpy.uint64(273),
        numpy.int8(-2),
        numpy.int16(-273),
        numpy.int32(-273),
        numpy.int64(-273),
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        ops_func(cast(SupportsComplexOps, good_val))
        ops_func_t(cast(SupportsComplexOpsSCU, good_val))
        pow_func(cast(SupportsComplexPow, good_val))
        pow_func_t(cast(SupportsComplexPowSCU, good_val))


def test_supports_complex_ops_pow_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    integer_val: SupportsComplexOps = sympy.Integer(-273)
    rational_val: SupportsComplexOps = sympy.Rational(-27315, 100)
    float_val: SupportsComplexOps = sympy.Float(-273.15)
    # sym_val: SupportsComplexOps = (sympy.symbols("x"),)
    _: SupportsComplexPow
    _ = sympy.Integer(-273)
    _ = sympy.Rational(-27315, 100)
    _ = sympy.Float(-273.15)
    # _ = (sympy.symbols("x"),)

    for good_val in (
        integer_val,
        rational_val,
        float_val,
        # TODO(posita): Can we fix this?
        # sym_val,
    ):
        assert isinstance(good_val, SupportsComplexOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexOpsSCT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"

        assert isinstance(good_val, SupportsComplexPow), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPowSCT), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"


def test_supports_complex_ops_pow_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        ops_func(cast(SupportsComplexOps, good_val))
        ops_func_t(cast(SupportsComplexOpsSCU, good_val))
        pow_func(cast(SupportsComplexPow, good_val))
        pow_func_t(cast(SupportsComplexPowSCU, good_val))
