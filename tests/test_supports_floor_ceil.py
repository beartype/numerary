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
from numerary.types import (
    SupportsCeil,
    SupportsCeilSCU,
    SupportsFloor,
    SupportsFloorSCU,
    ceil,
    floor,
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
def supports_floor_func(arg: SupportsFloor):
    assert isinstance(arg, SupportsFloor), f"{arg!r}"


@beartype
def supports_floor_func_t(arg: SupportsFloorSCU):
    assert isinstance(arg, SupportsFloor), f"{arg!r}"


@beartype
def supports_ceil_func(arg: SupportsCeil):
    assert isinstance(arg, SupportsCeil), f"{arg!r}"


@beartype
def supports_ceil_func_t(arg: SupportsCeilSCU):
    assert isinstance(arg, SupportsCeil), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_floor_ceil() -> None:
    bool_val: SupportsFloor = True
    int_val: SupportsFloor = -273
    frac_val: SupportsFloor = Fraction(-27315, 100)
    dec_val: SupportsFloor = Decimal("-273.15")
    nw_val: SupportsFloor = Numberwang(-273)
    nwd_val: SupportsFloor = NumberwangDerived(-273)
    nwr_val: SupportsFloor = NumberwangRegistered(-273)
    wn_val: SupportsFloor = Wangernumb(-273.15)
    wnd_val: SupportsFloor = WangernumbDerived(-273.15)
    wnr_val: SupportsFloor = WangernumbRegistered(-273.15)
    _: SupportsCeil
    _ = True
    _ = -273
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
        frac_val,
        dec_val,
        nw_val,
        nwd_val,
        nwr_val,
        wn_val,
        wnd_val,
        wnr_val,
    ):
        assert isinstance(good_val, SupportsFloor), f"{good_val!r}"
        assert floor(good_val), f"{good_val!r}"
        assert isinstance(good_val, SupportsCeil), f"{good_val!r}"
        assert ceil(good_val), f"{good_val!r}"

    for bad_val in (
        complex(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsFloor), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsCeil), f"{bad_val!r}"


@pytest.mark.skipif(sys.version_info < (3, 9), reason="requires Python >=3.9")
def test_floor_ceil_float() -> None:
    if sys.version_info >= (3, 9):
        float_val: SupportsFloor = -273.15
        _: SupportsCeil
        _ = -273.15

        for good_val in (float_val,):
            assert isinstance(good_val, SupportsFloor), f"{good_val!r}"
            assert floor(good_val), f"{good_val!r}"
            assert isinstance(good_val, SupportsCeil), f"{good_val!r}"
            assert ceil(good_val), f"{good_val!r}"


def test_floor_ceil_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
    ):
        supports_floor_func(cast(SupportsFloor, good_val))
        supports_floor_func_t(cast(SupportsFloorSCU, good_val))
        supports_ceil_func(cast(SupportsCeil, good_val))
        supports_ceil_func_t(cast(SupportsCeilSCU, good_val))

    for bad_val in (
        complex(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_floor_func(cast(SupportsFloor, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_floor_func_t(cast(SupportsFloorSCU, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_ceil_func(cast(SupportsCeil, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_ceil_func_t(cast(SupportsCeilSCU, bad_val))


def test_floor_ceil_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsFloor = numpy.uint8(2)
    uint16_val: SupportsFloor = numpy.uint16(273)
    uint32_val: SupportsFloor = numpy.uint32(273)
    uint64_val: SupportsFloor = numpy.uint64(273)
    int8_val: SupportsFloor = numpy.int8(-2)
    int16_val: SupportsFloor = numpy.int16(-273)
    int32_val: SupportsFloor = numpy.int32(-273)
    int64_val: SupportsFloor = numpy.int64(-273)
    float16_val: SupportsFloor = numpy.float16(-1.8)
    float32_val: SupportsFloor = numpy.float32(-273.15)
    float64_val: SupportsFloor = numpy.float64(-273.15)
    float128_val: SupportsFloor = numpy.float128(-273.15)
    _: SupportsCeil
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
        assert isinstance(good_val, SupportsFloor), f"{good_val!r}"
        assert floor(good_val), f"{good_val!r}"
        assert isinstance(good_val, SupportsCeil), f"{good_val!r}"
        assert ceil(good_val), f"{good_val!r}"

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, SupportsFloor), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsCeil), f"{bad_val!r}"


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
        supports_floor_func(cast(SupportsFloor, good_val))
        supports_ceil_func(cast(SupportsCeil, good_val))

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_floor_func(cast(SupportsFloor, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_floor_func_t(cast(SupportsFloorSCU, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_ceil_func(cast(SupportsCeil, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_ceil_func_t(cast(SupportsCeilSCU, bad_val))


def test_floor_ceil_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    integer_val: SupportsFloor = sympy.Integer(-273)
    rational_val: SupportsFloor = sympy.Rational(-27315, 100)
    float_val: SupportsFloor = sympy.Float(-273.15)
    symbol_val: SupportsFloor = sympy.symbols("x")
    _: SupportsCeil
    _ = sympy.Integer(-273)
    _ = sympy.Rational(-27315, 100)
    _ = sympy.Float(-273.15)
    _ = sympy.symbols("x")

    for good_val in (
        integer_val,
        rational_val,
        float_val,
    ):
        assert isinstance(good_val, SupportsFloor), f"{good_val!r}"
        assert floor(good_val), f"{good_val!r}"
        assert isinstance(good_val, SupportsCeil), f"{good_val!r}"
        assert ceil(good_val), f"{good_val!r}"

    for bad_val in (symbol_val,):
        assert not isinstance(bad_val, SupportsFloor), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsCeil), f"{bad_val!r}"


def test_floor_ceil_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
    ):
        supports_floor_func(cast(SupportsFloor, good_val))
        supports_floor_func_t(cast(SupportsFloorSCU, good_val))
        supports_ceil_func(cast(SupportsCeil, good_val))
        supports_ceil_func_t(cast(SupportsCeilSCU, good_val))

    for bad_val in (sympy.symbols("x"),):
        with pytest.raises(roar.BeartypeException):
            supports_floor_func(cast(SupportsFloor, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_floor_func_t(cast(SupportsFloorSCU, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_ceil_func(cast(SupportsCeil, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_ceil_func_t(cast(SupportsCeilSCU, bad_val))
