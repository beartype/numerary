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
from numerary.types import SupportsTrunc, SupportsTruncSCT, SupportsTruncSCU, trunc

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
def func(arg: SupportsTrunc):
    assert isinstance(arg, SupportsTrunc), f"{arg!r}"


@beartype
def func_t(arg: SupportsTruncSCU):
    assert isinstance(arg, SupportsTruncSCT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_trunc() -> None:
    bool_val: SupportsTrunc = True
    int_val: SupportsTrunc = -273
    float_val: SupportsTrunc = -273.15
    frac_val: SupportsTrunc = Fraction(-27315, 100)
    dec_val: SupportsTrunc = Decimal("-273.15")
    nw_val: SupportsTrunc = Numberwang(-273)
    nwd_val: SupportsTrunc = NumberwangDerived(-273)
    nwr_val: SupportsTrunc = NumberwangRegistered(-273)
    wn_val: SupportsTrunc = Wangernumb(-273.15)
    wnd_val: SupportsTrunc = WangernumbDerived(-273.15)
    wnr_val: SupportsTrunc = WangernumbRegistered(-273.15)

    for good_val in (
        bool_val,
        int_val,
        float_val,
        frac_val,
        dec_val,
        nw_val,
        nwd_val,
        nwr_val,
        wn_val,
        wnd_val,
        wnr_val,
    ):
        assert isinstance(good_val, SupportsTrunc), f"{good_val!r}"
        assert isinstance(good_val, SupportsTruncSCT), f"{good_val!r}"
        assert trunc(good_val), f"{good_val!r}"

    for bad_val in (
        complex(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsTrunc), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsTruncSCT), f"{bad_val!r}"


def test_trunc_beartype() -> None:
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
        func(cast(SupportsTrunc, good_val))
        func_t(cast(SupportsTruncSCU, good_val))

    for bad_val in (
        complex(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsTrunc, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsTruncSCU, bad_val))


def test_trunc_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsTrunc = numpy.uint8(2)
    uint16_val: SupportsTrunc = numpy.uint16(273)
    uint32_val: SupportsTrunc = numpy.uint32(273)
    uint64_val: SupportsTrunc = numpy.uint64(273)
    int8_val: SupportsTrunc = numpy.int8(-2)
    int16_val: SupportsTrunc = numpy.int16(-273)
    int32_val: SupportsTrunc = numpy.int32(-273)
    int64_val: SupportsTrunc = numpy.int64(-273)
    float16_val: SupportsTrunc = numpy.float16(-1.8)
    float32_val: SupportsTrunc = numpy.float32(-273.15)
    float64_val: SupportsTrunc = numpy.float64(-273.15)
    float128_val: SupportsTrunc = numpy.float128(-273.15)

    # numpy.float64 seems to have a closer relationship to the native float than the
    # other numpy.float* types
    for good_val in (float64_val,):
        assert isinstance(good_val, SupportsTrunc), f"{good_val!r}"
        assert isinstance(good_val, SupportsTruncSCT), f"{good_val!r}"
        assert trunc(good_val), f"{good_val!r}"

    for lying_val in (
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
        float128_val,
    ):
        # The pure protocol approach catches this
        assert not isinstance(lying_val, SupportsTrunc), f"{lying_val!r}"

        # The short-circuiting approach does not
        assert isinstance(lying_val, SupportsTruncSCT), f"{lying_val!r}"

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, SupportsTrunc), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsTruncSCT), f"{bad_val!r}"


def test_trunc_numpy_beartype() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    # numpy.float64 seems to have a closer relationship to the native float than the
    # other numpy.float* types
    for good_val in (numpy.float64(-273.15),):
        func(cast(SupportsTrunc, good_val))
        func_t(cast(SupportsTruncSCU, good_val))

    for lying_val in (
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
        numpy.float128(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsTrunc, lying_val))

        func_t(cast(SupportsTruncSCU, lying_val))

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsTrunc, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsTruncSCU, bad_val))


def test_trunc_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    integer_val: SupportsTrunc = sympy.Integer(-273)
    rational_val: SupportsTrunc = sympy.Rational(-27315, 100)
    float_val: SupportsTrunc = sympy.Float(-273.15)
    sym_val: SupportsTrunc = sympy.symbols("x")

    for good_val in (
        integer_val,
        rational_val,
        float_val,
    ):
        assert isinstance(good_val, SupportsTrunc), f"{good_val!r}"
        assert isinstance(good_val, SupportsTruncSCT), f"{good_val!r}"
        assert trunc(good_val), f"{good_val!r}"

    for lying_val in (sym_val,):
        assert isinstance(lying_val, SupportsTrunc), f"{lying_val!r}"
        assert isinstance(lying_val, SupportsTruncSCT), f"{lying_val!r}"

        # Relationals have, but don't implement this function
        # TODO(posita): Can we fix this?
        with pytest.raises(TypeError):
            trunc(lying_val)


def test_trunc_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Rational(-27315, 100),
        sympy.Float(-273.15),
    ):
        func(cast(SupportsTrunc, good_val))
        func_t(cast(SupportsTruncSCU, good_val))

    for lying_val in (sympy.symbols("x"),):
        func(cast(SupportsTrunc, good_val))
        func_t(cast(SupportsTruncSCU, good_val))
