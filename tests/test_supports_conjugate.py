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
from numerary.types import SupportsConjugate, SupportsConjugateSCT, SupportsConjugateSCU

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
def func(arg: SupportsConjugate):
    assert isinstance(arg, SupportsConjugate), f"{arg!r}"


@beartype
def func_t(arg: SupportsConjugateSCU):
    assert isinstance(arg, SupportsConjugateSCT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_conjugate() -> None:
    for good_val in (
        True,
        -273,
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        # These have inherited this interface by deriving from number tower ABCs
        NumberwangDerived(-273),
        WangernumbDerived(-273.15),
    ):
        assert isinstance(good_val, SupportsConjugate), f"{good_val!r}"
        assert isinstance(good_val, SupportsConjugateSCT), f"{good_val!r}"
        assert good_val.conjugate(), f"{good_val!r}"

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        # The pure protocol approach catches this
        assert not isinstance(lying_val, SupportsConjugate), f"{lying_val!r}"

        # The short-circuiting approach does not
        assert isinstance(lying_val, SupportsConjugateSCT), f"{lying_val!r}"

    for bad_val in (
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsConjugate), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsConjugateSCT), f"{bad_val!r}"


def test_supports_conjugate_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        # These have inherited this interface by deriving from number tower ABCs
        NumberwangDerived(-273),
        WangernumbDerived(-273.15),
    ):
        func(cast(SupportsConjugate, good_val))
        func_t(cast(SupportsConjugateSCU, good_val))

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsConjugate, lying_val))

        func_t(cast(SupportsConjugateSCU, lying_val))

    for bad_val in (
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsConjugate, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsConjugateSCU, bad_val))


def test_supports_conjugate_numpy() -> None:
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
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert isinstance(good_val, SupportsConjugate), f"{good_val!r}"
        assert isinstance(good_val, SupportsConjugateSCT), f"{good_val!r}"
        assert good_val.conjugate(), f"{good_val!r}"


def test_supports_conjugate_numpy_beartype() -> None:
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
        func(cast(SupportsConjugate, good_val))
        func_t(cast(SupportsConjugateSCU, good_val))


def test_supports_conjugate_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        assert isinstance(good_val, SupportsConjugate), f"{good_val!r}"
        assert isinstance(good_val, SupportsConjugateSCT), f"{good_val!r}"
        assert good_val.conjugate(), f"{good_val!r}"


def test_supports_conjugate_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        func(cast(SupportsConjugate, good_val))
        func_t(cast(SupportsConjugateSCU, good_val))
