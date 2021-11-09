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
    SupportsIntegralOps,
    SupportsIntegralOpsSCU,
    SupportsIntegralPow,
    SupportsIntegralPowSCU,
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
def supports_integral_ops_func(arg: SupportsIntegralOps):
    assert isinstance(arg, SupportsIntegralOps), f"{arg!r}"


@beartype
def supports_integral_ops_func_t(arg: SupportsIntegralOpsSCU):
    assert isinstance(arg, SupportsIntegralOps), f"{arg!r}"


@beartype
def supports_integral_pow_func(arg: SupportsIntegralPow):
    assert isinstance(arg, SupportsIntegralPow), f"{arg!r}"


@beartype
def supports_integral_pow_func_t(arg: SupportsIntegralPowSCU):
    assert isinstance(arg, SupportsIntegralPow), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_integral_ops_pow() -> None:
    bool_val: SupportsIntegralOps = True
    int_val: SupportsIntegralOps = -273
    nw_val: SupportsIntegralOps = Numberwang(-273)
    nwd_val: SupportsIntegralOps = NumberwangDerived(-273)
    nwr_val: SupportsIntegralOps = NumberwangRegistered(-273)
    _: SupportsIntegralPow
    _ = True
    _ = -273
    _ = Numberwang(-273)
    _ = NumberwangDerived(-273)
    _ = NumberwangRegistered(-273)

    for good_val in (
        bool_val,
        int_val,
        nw_val,
        nwd_val,
        nwr_val,
    ):
        assert isinstance(good_val, SupportsIntegralOps), f"{good_val!r}"
        assert good_val >> 0 == good_val, f"{good_val!r}"
        assert good_val << 0 == good_val, f"{good_val!r}"
        assert good_val & 0 == 0, f"{good_val!r}"
        assert good_val | 0 == good_val, f"{good_val!r}"
        assert isinstance(good_val, SupportsIntegralPow), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"

    for bad_val in (
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsIntegralOps), f"{bad_val!r}"


def test_supports_integral_ops_pow_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
    ):
        supports_integral_ops_func(cast(SupportsIntegralOps, good_val))
        supports_integral_ops_func_t(cast(SupportsIntegralOpsSCU, good_val))
        supports_integral_pow_func(cast(SupportsIntegralPow, good_val))
        supports_integral_pow_func_t(cast(SupportsIntegralPowSCU, good_val))

    for bad_val in (
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func(cast(SupportsIntegralOps, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func_t(cast(SupportsIntegralOpsSCU, bad_val))


def test_supports_integral_ops_pow_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsIntegralOps = numpy.uint8(2)
    uint16_val: SupportsIntegralOps = numpy.uint16(273)
    uint32_val: SupportsIntegralOps = numpy.uint32(273)
    uint64_val: SupportsIntegralOps = numpy.uint64(273)
    int8_val: SupportsIntegralOps = numpy.int8(-2)
    int16_val: SupportsIntegralOps = numpy.int16(-273)
    int32_val: SupportsIntegralOps = numpy.int32(-273)
    int64_val: SupportsIntegralOps = numpy.int64(-273)
    float16_val: SupportsIntegralOps = numpy.float16(-1.8)
    float32_val: SupportsIntegralOps = numpy.float32(-273.15)
    float64_val: SupportsIntegralOps = numpy.float64(-273.15)
    float128_val: SupportsIntegralOps = numpy.float128(-273.15)
    _: SupportsIntegralPow
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
    _ = numpy.csingle(-273.15)
    _ = numpy.cdouble(-273.15)
    _ = numpy.clongdouble(-273.15)

    for good_val in (
        uint8_val,
        uint16_val,
        uint32_val,
        uint64_val,
        int8_val,
        int16_val,
        int32_val,
        int64_val,
    ):
        assert isinstance(good_val, SupportsIntegralOps), f"{good_val!r}"

        # I have no idea why numpy.uint64 is special in this regard
        if isinstance(good_val, numpy.uint64):
            assert good_val >> type(good_val)(0) == good_val, f"{good_val!r}"
            assert good_val << type(good_val)(0) == good_val, f"{good_val!r}"
            assert good_val & type(good_val)(0) == type(good_val)(0), f"{good_val!r}"
            assert good_val | type(good_val)(0) == good_val, f"{good_val!r}"
        else:
            assert good_val >> 0 == good_val, f"{good_val!r}"
            assert good_val << 0 == good_val, f"{good_val!r}"
            assert good_val & 0 == 0, f"{good_val!r}"
            assert good_val | 0 == good_val, f"{good_val!r}"

        assert isinstance(good_val, SupportsIntegralPow), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"

    for bad_val in (
        float16_val,
        float32_val,
        float64_val,
        float128_val,
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, SupportsIntegralOps), f"{bad_val!r}"

        # These have, but don't implement these functions
        with pytest.raises(Exception):  # TypeError or beartype.roar.BeartypeException
            bad_val << 0

        with pytest.raises(Exception):  # TypeError or beartype.roar.BeartypeException
            bad_val >> 0

        with pytest.raises(Exception):  # TypeError or beartype.roar.BeartypeException
            bad_val & 0

        with pytest.raises(Exception):  # TypeError or beartype.roar.BeartypeException
            bad_val | 0

        assert not isinstance(bad_val, SupportsIntegralPow), f"{bad_val!r}"


def test_supports_integral_ops_pow_numpy_beartype() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        numpy.uint8(2),
        numpy.uint16(273),
        numpy.uint32(273),
        numpy.uint64(273),
        numpy.int8(-2),
        numpy.int16(-273),
        numpy.int32(-273),
        numpy.int64(-273),
    ):
        supports_integral_ops_func(cast(SupportsIntegralOps, good_val))
        supports_integral_ops_func_t(cast(SupportsIntegralOpsSCU, good_val))
        supports_integral_pow_func(cast(SupportsIntegralPow, good_val))
        supports_integral_pow_func_t(cast(SupportsIntegralPowSCU, good_val))

    for bad_val in (
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func(cast(SupportsIntegralOps, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func_t(cast(SupportsIntegralOpsSCU, bad_val))


def test_supports_integral_ops_pow_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    integral_val: SupportsIntegralOps = sympy.Integer(-273)
    sym_val: SupportsIntegralOps = sympy.symbols("x")
    _: SupportsIntegralPow
    _ = sympy.Integer(-273)
    _ = sympy.symbols("x")

    for good_val in (integral_val,):
        assert isinstance(good_val, SupportsIntegralOps), f"{good_val!r}"
        assert good_val >> 0 == good_val, f"{good_val!r}"
        assert good_val << 0 == good_val, f"{good_val!r}"
        assert good_val & 0 == 0, f"{good_val!r}"
        assert good_val | 0 == good_val, f"{good_val!r}"
        assert isinstance(good_val, SupportsIntegralPow), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"

    for lying_val in (sym_val,):
        assert not isinstance(lying_val, SupportsIntegralOps), f"{lying_val!r}"

        # Relationals have, but don't implement this function
        with pytest.raises(Exception):  # TypeError or beartype.roar.BeartypeException
            lying_val << 0

    for bad_val in (
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
    ):
        assert not isinstance(bad_val, SupportsIntegralOps), f"{bad_val!r}"


def test_supports_integral_ops_pow_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (sympy.Integer(-273),):
        supports_integral_ops_func(cast(SupportsIntegralOps, good_val))
        supports_integral_ops_func_t(cast(SupportsIntegralOpsSCU, good_val))
        supports_integral_pow_func(cast(SupportsIntegralPow, good_val))
        supports_integral_pow_func_t(cast(SupportsIntegralPowSCU, good_val))

    for lying_val in (sympy.symbols("x"),):
        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func(cast(SupportsIntegralOps, lying_val))

        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func_t(cast(SupportsIntegralOpsSCU, lying_val))

    for bad_val in (
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func(cast(SupportsIntegralOps, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func_t(cast(SupportsIntegralOpsSCU, bad_val))
