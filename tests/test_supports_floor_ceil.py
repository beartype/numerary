# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

import sys
from decimal import Decimal
from fractions import Fraction
from typing import cast

import pytest

from numerary.bt import beartype
from numerary.types import SupportsFloorCeil, SupportsFloorCeilSCU, ceil, floor

from .numberwang import (
    Numberwang,
    NumberwangDerived,
    NumberwangRegistered,
    TestFlag,
    TestIntEnum,
    TestIntFlag,
    Wangernumb,
    WangernumbDerived,
    WangernumbRegistered,
)

__all__ = ()


# ---- Functions -----------------------------------------------------------------------


@beartype
def supports_floor_ceil_func(arg: SupportsFloorCeil):
    assert isinstance(arg, SupportsFloorCeil), f"{arg!r}"


@beartype
def supports_floor_ceil_func_t(arg: SupportsFloorCeilSCU):
    assert isinstance(arg, SupportsFloorCeil), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_floor_ceil() -> None:
    bool_val: SupportsFloorCeil = True
    int_val: SupportsFloorCeil = -273
    frac_val: SupportsFloorCeil = Fraction(-27315, 100)
    dec_val: SupportsFloorCeil = Decimal("-273.15")
    test_int_enum: SupportsFloorCeil = TestIntEnum.ZERO
    test_int_flag: SupportsFloorCeil = TestIntFlag.B
    nw_val: SupportsFloorCeil = Numberwang(-273)
    nwd_val: SupportsFloorCeil = NumberwangDerived(-273)
    nwr_val: SupportsFloorCeil = NumberwangRegistered(-273)
    wn_val: SupportsFloorCeil = Wangernumb(-273.15)
    wnd_val: SupportsFloorCeil = WangernumbDerived(-273.15)
    wnr_val: SupportsFloorCeil = WangernumbRegistered(-273.15)

    for good_val in (
        bool_val,
        int_val,
        frac_val,
        dec_val,
        test_int_enum,
        test_int_flag,
        nw_val,
        nwd_val,
        nwr_val,
        wn_val,
        wnd_val,
        wnr_val,
    ):
        assert isinstance(good_val, SupportsFloorCeil), f"{good_val!r}"
        assert floor(good_val), f"{good_val!r}"
        assert ceil(good_val), f"{good_val!r}"

    complex_bad_val: SupportsFloorCeil = complex(-273.15)  # type: ignore [assignment]
    test_flag_bad_val: SupportsFloorCeil = TestFlag.B  # type: ignore [assignment]

    for bad_val in (
        complex_bad_val,
        test_flag_bad_val,
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsFloorCeil), f"{bad_val!r}"


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires Python >=3.9")
def test_floor_ceil_float() -> None:
    if sys.version_info >= (3, 9):
        float_val: SupportsFloorCeil = -273.15

        for good_val in (float_val,):
            assert isinstance(good_val, SupportsFloorCeil), f"{good_val!r}"
            assert floor(good_val), f"{good_val!r}"
            assert ceil(good_val), f"{good_val!r}"


def test_floor_ceil_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        Fraction(-27315, 100),
        Decimal("-273.15"),
        TestIntEnum.ZERO,
        TestIntFlag.B,
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
    ):
        supports_floor_ceil_func(cast(SupportsFloorCeil, good_val))
        supports_floor_ceil_func_t(cast(SupportsFloorCeilSCU, good_val))

    for bad_val in (
        complex(-273.15),
        TestFlag.B,
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_floor_ceil_func(cast(SupportsFloorCeil, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_floor_ceil_func_t(cast(SupportsFloorCeilSCU, bad_val))


def test_floor_ceil_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsFloorCeil = numpy.uint8(2)
    uint16_val: SupportsFloorCeil = numpy.uint16(273)
    uint32_val: SupportsFloorCeil = numpy.uint32(273)
    uint64_val: SupportsFloorCeil = numpy.uint64(273)
    int8_val: SupportsFloorCeil = numpy.int8(-2)
    int16_val: SupportsFloorCeil = numpy.int16(-273)
    int32_val: SupportsFloorCeil = numpy.int32(-273)
    int64_val: SupportsFloorCeil = numpy.int64(-273)
    float16_val: SupportsFloorCeil = numpy.float16(-1.8)
    float32_val: SupportsFloorCeil = numpy.float32(-273.15)
    float64_val: SupportsFloorCeil = numpy.float64(-273.15)
    float128_val: SupportsFloorCeil = numpy.float128(-273.15)

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
    ):
        assert isinstance(good_val, SupportsFloorCeil), f"{good_val!r}"
        assert floor(good_val), f"{good_val!r}"
        assert ceil(good_val), f"{good_val!r}"

    # TODO(posita): These should not validate
    csingle_val: SupportsFloorCeil = numpy.csingle(-273.15)
    cdouble_val: SupportsFloorCeil = numpy.cdouble(-273.15)
    clongdouble_val: SupportsFloorCeil = numpy.clongdouble(-273.15)

    for bad_val in (
        csingle_val,
        cdouble_val,
        clongdouble_val,
    ):
        assert not isinstance(bad_val, SupportsFloorCeil), f"{bad_val!r}"


def test_floor_ceil_numpy_beartype() -> None:
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
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
    ):
        supports_floor_ceil_func(cast(SupportsFloorCeil, good_val))

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_floor_ceil_func(cast(SupportsFloorCeil, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_floor_ceil_func_t(cast(SupportsFloorCeilSCU, bad_val))


def test_floor_ceil_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    integer_val: SupportsFloorCeil = sympy.Integer(-273)
    rational_val: SupportsFloorCeil = sympy.Rational(-27315, 100)
    float_val: SupportsFloorCeil = sympy.Float(-273.15)

    for good_val in (
        integer_val,
        rational_val,
        float_val,
    ):
        assert isinstance(good_val, SupportsFloorCeil), f"{good_val!r}"
        assert floor(good_val), f"{good_val!r}"
        assert ceil(good_val), f"{good_val!r}"

    # TODO(posita): These should not validate
    sym_val: SupportsFloorCeil = sympy.symbols("x")

    for bad_val in (sym_val,):
        assert not isinstance(bad_val, SupportsFloorCeil), f"{bad_val!r}"


def test_floor_ceil_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
    ):
        supports_floor_ceil_func(cast(SupportsFloorCeil, good_val))
        supports_floor_ceil_func_t(cast(SupportsFloorCeilSCU, good_val))

    for bad_val in (sympy.symbols("x"),):
        with pytest.raises(roar.BeartypeException):
            supports_floor_ceil_func(cast(SupportsFloorCeil, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_floor_ceil_func_t(cast(SupportsFloorCeilSCU, bad_val))
