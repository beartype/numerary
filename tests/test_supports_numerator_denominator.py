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

from numerary import denominator, numerator
from numerary.bt import beartype
from numerary.types import (
    SupportsNumeratorDenominator,
    SupportsNumeratorDenominatorT,
    SupportsNumeratorDenominatorTs,
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


# ---- Classes -------------------------------------------------------------------------


class SageMathLikeFraction(Fraction):
    r"""
    Hack to emulate a rational similar to Sage’s implementation, where the numerator and
    denominator are exposed via methods, not properties.

    Sage’s rational implementation predates PEP 3141. Unfortunately, fixing this in Sage
    would be a breaking change. (See [this
    issue](https://trac.sagemath.org/ticket/28234) for more details.
    """

    def denominator(self) -> int:
        return Fraction.denominator.fget(self)  # type: ignore

    def numerator(self) -> int:
        return Fraction.numerator.fget(self)  # type: ignore


# ---- Functions -----------------------------------------------------------------------


@beartype
def func(arg: SupportsNumeratorDenominator):
    assert isinstance(arg, SupportsNumeratorDenominator), f"{arg!r}"


@beartype
def func_t(arg: SupportsNumeratorDenominatorT):
    assert isinstance(arg, SupportsNumeratorDenominatorTs), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_numerator_denominator() -> None:
    for good_val in (
        True,
        -273,
        Fraction(-27315, 100),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
        SageMathLikeFraction(-27315, 100),
    ):
        assert isinstance(good_val, SupportsNumeratorDenominator), f"{good_val!r}"
        assert isinstance(good_val, SupportsNumeratorDenominatorTs), f"{good_val!r}"
        assert numerator(good_val), f"{good_val!r}"
        assert denominator(good_val), f"{good_val!r}"

    for bad_val in (
        -273.15,
        complex(-273.15),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273",
    ):
        assert not isinstance(bad_val, SupportsNumeratorDenominator), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsNumeratorDenominatorTs), f"{bad_val!r}"


def test_numerator_denominator_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        Fraction(-27315, 100),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
        SageMathLikeFraction(-27315, 100),
    ):
        func(cast(SupportsNumeratorDenominator, good_val))
        func_t(cast(SupportsNumeratorDenominatorT, good_val))

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
            func(cast(SupportsNumeratorDenominator, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsNumeratorDenominatorT, bad_val))


def test_numerator_denominator_numpy() -> None:
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
        assert isinstance(good_val, SupportsNumeratorDenominator), f"{good_val!r}"
        assert isinstance(good_val, SupportsNumeratorDenominatorTs), f"{good_val!r}"
        assert numerator(good_val), f"{good_val!r}"
        assert denominator(good_val), f"{good_val!r}"

    for bad_val in (
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, SupportsNumeratorDenominator), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsNumeratorDenominatorTs), f"{bad_val!r}"


def test_numerator_denominator_numpy_beartype() -> None:
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
        func(cast(SupportsNumeratorDenominator, good_val))
        func_t(cast(SupportsNumeratorDenominatorT, good_val))

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
            func(cast(SupportsNumeratorDenominator, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsNumeratorDenominatorT, bad_val))


def test_numerator_denominator_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")

    for good_val in (
        sympy.Rational(-27315, 100),
        sympy.Integer(-273),
    ):
        assert isinstance(good_val, SupportsNumeratorDenominator), f"{good_val!r}"
        assert isinstance(good_val, SupportsNumeratorDenominatorTs), f"{good_val!r}"
        assert numerator(good_val), f"{good_val!r}"
        assert denominator(good_val), f"{good_val!r}"

    for bad_val in (
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        assert not isinstance(bad_val, SupportsNumeratorDenominator), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsNumeratorDenominatorTs), f"{bad_val!r}"


def test_numerator_denominator_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Rational(-27315, 100),
        sympy.Integer(-273),
    ):
        func(cast(SupportsNumeratorDenominator, good_val))
        func_t(cast(SupportsNumeratorDenominatorT, good_val))

    for bad_val in (
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsNumeratorDenominator, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsNumeratorDenominatorT, bad_val))
