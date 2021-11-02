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

from numerary.bt import beartype
from numerary.types import RationalLike, RationalLikeSCT, RationalLikeSCU

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
def func(arg: RationalLike):
    assert isinstance(arg, RationalLike), f"{arg!r}"


@beartype
def func_t(arg: RationalLikeSCU):
    assert isinstance(arg, RationalLikeSCT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_rational_like() -> None:
    for good_val in (
        True,
        -273,
        Fraction(-27315, 100),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
    ):
        assert isinstance(good_val, RationalLike), f"{good_val!r}"
        assert isinstance(good_val, RationalLikeSCT), f"{good_val!r}"
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
        assert good_val.numerator, f"{good_val!r}"
        assert good_val.denominator, f"{good_val!r}"

    for bad_val in (
        -273.15,
        complex(-273.15),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273",
    ):
        assert not isinstance(bad_val, RationalLike), f"{bad_val!r}"
        assert not isinstance(bad_val, RationalLikeSCT), f"{bad_val!r}"


def test_rational_like_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        Fraction(-27315, 100),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
    ):
        func(cast(RationalLike, good_val))
        func_t(cast(RationalLikeSCU, good_val))

    for bad_val in (
        -273.15,
        complex(-273.15),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273",
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(RationalLike, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(RationalLikeSCU, bad_val))


def test_rational_like_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")

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
        assert isinstance(good_val, RationalLike), f"{good_val!r}"
        assert isinstance(good_val, RationalLikeSCT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"
        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"
        assert good_val.numerator, f"{good_val!r}"
        assert good_val.denominator, f"{good_val!r}"

    for bad_val in (
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, RationalLike), f"{bad_val!r}"
        assert not isinstance(bad_val, RationalLikeSCT), f"{bad_val!r}"


def test_rational_like_numpy_beartype() -> None:
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
        func(cast(RationalLike, good_val))
        func_t(cast(RationalLikeSCU, good_val))

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
            func(cast(RationalLike, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(RationalLikeSCU, bad_val))


def test_rational_like_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")

    for good_val in (
        sympy.Rational(-27315, 100),
        sympy.Integer(-273),
    ):
        assert isinstance(good_val, RationalLike), f"{good_val!r}"
        assert isinstance(good_val, RationalLikeSCT), f"{good_val!r}"
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
        assert good_val.numerator, f"{good_val!r}"
        assert good_val.denominator, f"{good_val!r}"

    for bad_val in (
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        assert not isinstance(bad_val, RationalLike), f"{bad_val!r}"
        assert not isinstance(bad_val, RationalLikeSCT), f"{bad_val!r}"


def test_rational_like_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Rational(-27315, 100),
        sympy.Integer(-273),
    ):
        func(cast(RationalLike, good_val))
        func_t(cast(RationalLikeSCU, good_val))

    for bad_val in (
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(RationalLike, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(RationalLikeSCU, bad_val))
