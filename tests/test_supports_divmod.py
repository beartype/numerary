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
from numerary.types import SupportsDivmod, SupportsDivmodT, SupportsDivmodTs

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
def func(arg: SupportsDivmod):
    assert isinstance(arg, SupportsDivmod), f"{arg!r}"


@beartype
def func_t(arg: SupportsDivmodT):
    assert isinstance(arg, SupportsDivmodTs), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_divmod() -> None:
    for good_val in (
        True,
        -273,
        -273.15,
        Fraction(-27315, 100),
        Decimal("-273.15"),
        NumberwangDerived(-273),
        WangernumbDerived(-273.15),
    ):
        assert isinstance(good_val, SupportsDivmod), f"{good_val!r}"
        assert isinstance(good_val, SupportsDivmodTs), f"{good_val!r}"
        assert divmod(good_val, good_val), f"{good_val!r}"

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        # The pure protocol approach catches this
        assert not isinstance(lying_val, SupportsDivmod), f"{lying_val!r}"

        # The short-circuiting approach does not
        assert isinstance(lying_val, SupportsDivmodTs), f"{lying_val!r}"

    for bad_val in (
        # TODO(posita): fix this
        # complex(-273.15),
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsDivmod), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsDivmodTs), f"{bad_val!r}"


def test_supports_divmod_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        Fraction(-27315, 100),
        Decimal("-273.15"),
        NumberwangDerived(-273),
        WangernumbDerived(-273.15),
    ):
        func(cast(SupportsDivmod, good_val))
        func_t(cast(SupportsDivmodT, good_val))

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsDivmod, lying_val))

        func_t(cast(SupportsDivmodT, lying_val))

    for bad_val in (
        # TODO(posita): fix this
        # complex(-273.15),
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsDivmod, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsDivmodT, bad_val))


def test_supports_divmod_numpy() -> None:
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
    ):
        assert isinstance(good_val, SupportsDivmod), f"{good_val!r}"
        assert isinstance(good_val, SupportsDivmodTs), f"{good_val!r}"
        assert divmod(good_val, good_val), f"{good_val!r}"

    for bad_val in (
        # TODO(posita): fix these
        # numpy.csingle(-273.15),
        # numpy.cdouble(-273.15),
        # numpy.clongdouble(-273.15),
        "-273.15",  # TODO(posita): remove me
    ):
        assert not isinstance(bad_val, SupportsDivmod), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsDivmodTs), f"{bad_val!r}"


def test_supports_divmod_numpy_beartype() -> None:
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
        func(cast(SupportsDivmod, good_val))
        func_t(cast(SupportsDivmodT, good_val))

    for bad_val in (
        # TODO(posita): fix these
        # numpy.csingle(-273.15),
        # numpy.cdouble(-273.15),
        # numpy.clongdouble(-273.15),
        "-273.15",  # TODO(posita): remove me
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsDivmod, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsDivmodT, bad_val))


def test_supports_divmod_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        assert isinstance(good_val, SupportsDivmod), f"{good_val!r}"
        assert isinstance(good_val, SupportsDivmodTs), f"{good_val!r}"

        # Symbolic relationals can't be reduced to a boolean
        if isinstance(good_val, sympy.core.symbol.Symbol):
            assert divmod(good_val, good_val), f"{good_val!r}"
        else:
            assert divmod(good_val, good_val), f"{good_val!r}"


def test_supports_divmod_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        func(cast(SupportsDivmod, good_val))
        func_t(cast(SupportsDivmodT, good_val))
