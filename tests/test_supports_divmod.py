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
from numerary.types import SupportsDivmod, SupportsDivmodSCT, SupportsDivmodSCU

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
def func_t(arg: SupportsDivmodSCU):
    assert isinstance(arg, SupportsDivmodSCT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_divmod() -> None:
    bool_val: SupportsDivmod = True
    int_val: SupportsDivmod = -273
    float_val: SupportsDivmod = -273.15
    frac_val: SupportsDivmod = Fraction(-27315, 100)
    dec_val: SupportsDivmod = Decimal("-273.15")
    # These have inherited this interface by deriving from number tower ABCs
    nwd_val: SupportsDivmod = NumberwangDerived(-273)
    wnd_val: SupportsDivmod = WangernumbDerived(-273.15)

    for good_val in (
        bool_val,
        int_val,
        float_val,
        frac_val,
        dec_val,
        nwd_val,
        wnd_val,
    ):
        assert isinstance(good_val, SupportsDivmod), f"{good_val!r}"
        assert isinstance(good_val, SupportsDivmodSCT), f"{good_val!r}"
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
        assert isinstance(lying_val, SupportsDivmodSCT), f"{lying_val!r}"

    for bad_val in (
        # TODO(posita): fix this
        # complex(-273.15),
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsDivmod), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsDivmodSCT), f"{bad_val!r}"


def test_supports_divmod_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        Fraction(-27315, 100),
        Decimal("-273.15"),
        # These have inherited this interface by deriving from number tower ABCs
        NumberwangDerived(-273),
        WangernumbDerived(-273.15),
    ):
        func(cast(SupportsDivmod, good_val))
        func_t(cast(SupportsDivmodSCU, good_val))

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsDivmod, lying_val))

        func_t(cast(SupportsDivmodSCU, lying_val))

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
            func_t(cast(SupportsDivmodSCU, bad_val))


def test_supports_divmod_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsDivmod = numpy.uint8(2)
    uint16_val: SupportsDivmod = numpy.uint16(273)
    uint32_val: SupportsDivmod = numpy.uint32(273)
    uint64_val: SupportsDivmod = numpy.uint64(273)
    int8_val: SupportsDivmod = numpy.int8(-2)
    int16_val: SupportsDivmod = numpy.int16(-273)
    int32_val: SupportsDivmod = numpy.int32(-273)
    int64_val: SupportsDivmod = numpy.int64(-273)
    float16_val: SupportsDivmod = numpy.float16(-1.8)
    float32_val: SupportsDivmod = numpy.float32(-273.15)
    float64_val: SupportsDivmod = numpy.float64(-273.15)
    float128_val: SupportsDivmod = numpy.float128(-273.15)

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
        assert isinstance(good_val, SupportsDivmod), f"{good_val!r}"
        assert isinstance(good_val, SupportsDivmodSCT), f"{good_val!r}"
        assert divmod(good_val, good_val), f"{good_val!r}"

    for bad_val in (
        # TODO(posita): fix these
        # numpy.csingle(-273.15),
        # numpy.cdouble(-273.15),
        # numpy.clongdouble(-273.15),
        "-273.15",  # TODO(posita): remove me
    ):
        assert not isinstance(bad_val, SupportsDivmod), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsDivmodSCT), f"{bad_val!r}"


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
        func_t(cast(SupportsDivmodSCU, good_val))

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
            func_t(cast(SupportsDivmodSCU, bad_val))


def test_supports_divmod_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    integer_val: SupportsDivmod = sympy.Integer(-273)
    rational_val: SupportsDivmod = sympy.Rational(-27315, 100)
    float_val: SupportsDivmod = sympy.Float(-273.15)
    # sym_val: SupportsDivmod = (sympy.symbols("x"),)

    for good_val in (
        integer_val,
        rational_val,
        float_val,
        # TODO(posita): Can we fix this?
        # sym_val,
    ):
        assert isinstance(good_val, SupportsDivmod), f"{good_val!r}"
        assert isinstance(good_val, SupportsDivmodSCT), f"{good_val!r}"

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
        func_t(cast(SupportsDivmodSCU, good_val))
