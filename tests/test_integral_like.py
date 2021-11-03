# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction
from typing import cast

import pytest

from numerary import IntegralLike, IntegralLikeSCT, IntegralLikeSCU
from numerary.bt import beartype

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
def func(arg: IntegralLike):
    assert isinstance(arg, IntegralLike)


@beartype
def func_t(arg: IntegralLikeSCU):
    assert isinstance(arg, IntegralLikeSCT)


# ---- Tests ---------------------------------------------------------------------------


def test_integral_like() -> None:
    bool_val: IntegralLike = True
    int_val: IntegralLike = -273
    nw_val: IntegralLike = Numberwang(-273)
    nwd_val: IntegralLike = NumberwangDerived(-273)
    nwr_val: IntegralLike = NumberwangRegistered(-273)

    for good_val in (
        bool_val,
        int_val,
        nw_val,
        nwd_val,
        nwr_val,
    ):
        assert isinstance(good_val, IntegralLike), f"{good_val!r}"
        assert isinstance(good_val, IntegralLikeSCT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"
        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"
        assert math.trunc(good_val), f"{good_val!r}"
        assert math.floor(good_val), f"{good_val!r}"
        assert math.ceil(good_val), f"{good_val!r}"
        assert good_val >> 0 == good_val, f"{good_val!r}"
        assert good_val << 0 == good_val, f"{good_val!r}"
        assert good_val & 0 == 0, f"{good_val!r}"
        assert good_val | 0 == good_val, f"{good_val!r}"

    for bad_val in (
        -273.15,
        Fraction(-27315, 100),
        Decimal("-273.15"),
        complex(-273.15),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273",
    ):
        assert not isinstance(bad_val, IntegralLike), f"{bad_val!r}"
        assert not isinstance(bad_val, IntegralLikeSCT), f"{bad_val!r}"


def test_integral_like_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
    ):
        func(cast(IntegralLike, good_val))
        func_t(cast(IntegralLikeSCU, good_val))

    for bad_val in (
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273",
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(IntegralLike, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(IntegralLikeSCU, bad_val))


def test_integral_like_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: IntegralLike = numpy.uint8(2)
    uint16_val: IntegralLike = numpy.uint16(273)
    uint32_val: IntegralLike = numpy.uint32(273)
    uint64_val: IntegralLike = numpy.uint64(273)
    int8_val: IntegralLike = numpy.int8(-2)
    int16_val: IntegralLike = numpy.int16(-273)
    int32_val: IntegralLike = numpy.int32(-273)
    int64_val: IntegralLike = numpy.int64(-273)

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
        assert isinstance(good_val, IntegralLike), f"{good_val!r}"
        assert isinstance(good_val, IntegralLikeSCT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"

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

    for bad_val in (
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, IntegralLike), f"{bad_val!r}"
        assert not isinstance(bad_val, IntegralLikeSCT), f"{bad_val!r}"


def test_integral_like_numpy_beartype() -> None:
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
        func(cast(IntegralLike, good_val))
        func_t(cast(IntegralLikeSCU, good_val))

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
            func(cast(IntegralLike, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(IntegralLikeSCU, bad_val))


def test_integral_like_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    integral_val: IntegralLike = sympy.Integer(-273)

    for good_val in (integral_val,):
        assert isinstance(good_val, IntegralLike), f"{good_val!r}"
        assert isinstance(good_val, IntegralLikeSCT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"
        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"
        assert math.trunc(good_val), f"{good_val!r}"
        assert math.floor(good_val), f"{good_val!r}"
        assert math.ceil(good_val), f"{good_val!r}"
        assert good_val >> 0 == good_val, f"{good_val!r}"
        assert good_val << 0 == good_val, f"{good_val!r}"
        assert good_val & 0 == 0, f"{good_val!r}"
        assert good_val | 0 == good_val, f"{good_val!r}"

    for bad_val in (
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        # Bitwise operators are not supported by SymPy's symbols
        sympy.symbols("x"),
    ):
        assert not isinstance(bad_val, IntegralLike), f"{bad_val!r}"
        assert not isinstance(bad_val, IntegralLikeSCT), f"{bad_val!r}"


def test_integral_like_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (sympy.Integer(-273),):
        func(cast(IntegralLike, good_val))
        func_t(cast(IntegralLikeSCU, good_val))

    for bad_val in (
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        # Bitwise operators are not supported by SymPy's symbols
        sympy.symbols("x"),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(IntegralLike, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(IntegralLikeSCU, bad_val))
