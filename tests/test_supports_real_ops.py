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
from numerary.types import SupportsRealOps, SupportsRealOpsSCT, SupportsRealOpsSCU

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
def func(arg: SupportsRealOps):
    assert isinstance(arg, SupportsRealOps), f"{arg!r}"


@beartype
def func_t(arg: SupportsRealOpsSCU):
    assert isinstance(arg, SupportsRealOpsSCT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_real_ops() -> None:
    bool_val: SupportsRealOps = True
    int_val: SupportsRealOps = -273
    float_val: SupportsRealOps = -273.15
    frac_val: SupportsRealOps = Fraction(-27315, 100)
    dec_val: SupportsRealOps = Decimal("-273.15")
    nw_val: SupportsRealOps = Numberwang(-273)
    nwd_val: SupportsRealOps = NumberwangDerived(-273)
    nwr_val: SupportsRealOps = NumberwangRegistered(-273)
    wn_val: SupportsRealOps = Wangernumb(-273.15)
    wnd_val: SupportsRealOps = WangernumbDerived(-273.15)
    wnr_val: SupportsRealOps = WangernumbRegistered(-273.15)

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
        assert isinstance(good_val, SupportsRealOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsRealOpsSCT), f"{good_val!r}"
        assert good_val <= good_val, f"{good_val!r}"
        assert good_val >= good_val, f"{good_val!r}"

    for bad_val in (
        # TODO(posita): fix this
        # complex(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsRealOps), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsRealOpsSCT), f"{bad_val!r}"


def test_supports_real_ops_beartype() -> None:
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
        func(cast(SupportsRealOps, good_val))
        func_t(cast(SupportsRealOpsSCU, good_val))

    for bad_val in (
        # TODO(posita): fix this
        # complex(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsRealOps, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsRealOpsSCU, bad_val))


def test_supports_real_ops_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsRealOps = numpy.uint8(2)
    uint16_val: SupportsRealOps = numpy.uint16(273)
    uint32_val: SupportsRealOps = numpy.uint32(273)
    uint64_val: SupportsRealOps = numpy.uint64(273)
    int8_val: SupportsRealOps = numpy.int8(-2)
    int16_val: SupportsRealOps = numpy.int16(-273)
    int32_val: SupportsRealOps = numpy.int32(-273)
    int64_val: SupportsRealOps = numpy.int64(-273)
    float16_val: SupportsRealOps = numpy.float16(-1.8)
    float32_val: SupportsRealOps = numpy.float32(-273.15)
    float64_val: SupportsRealOps = numpy.float64(-273.15)
    float128_val: SupportsRealOps = numpy.float128(-273.15)

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
        assert isinstance(good_val, SupportsRealOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsRealOpsSCT), f"{good_val!r}"
        assert good_val <= good_val, f"{good_val!r}"
        assert good_val >= good_val, f"{good_val!r}"

    for bad_val in (
        # TODO(posita): fix these
        # numpy.csingle(-273.15),
        # numpy.cdouble(-273.15),
        # numpy.clongdouble(-273.15),
        "-273.15",  # TODO(posita): remove me
    ):
        assert not isinstance(bad_val, SupportsRealOps), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsRealOpsSCT), f"{bad_val!r}"


def test_supports_real_ops_numpy_beartype() -> None:
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
        func(cast(SupportsRealOps, good_val))
        func_t(cast(SupportsRealOpsSCU, good_val))

    for bad_val in (
        # TODO(posita): fix these
        # numpy.csingle(-273.15),
        # numpy.cdouble(-273.15),
        # numpy.clongdouble(-273.15),
        "-273.15",  # TODO(posita): remove me
    ):
        with pytest.raises(roar.BeartypeException):
            func(cast(SupportsRealOps, bad_val))

        with pytest.raises(roar.BeartypeException):
            func_t(cast(SupportsRealOpsSCU, bad_val))


def test_supports_real_ops_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    integer_val: SupportsRealOps = sympy.Integer(-273)
    rational_val: SupportsRealOps = sympy.Rational(-27315, 100)
    float_val: SupportsRealOps = sympy.Float(-273.15)
    sym_val: SupportsRealOps = sympy.symbols("x")

    for good_val in (
        integer_val,
        rational_val,
        float_val,
        sym_val,
    ):
        assert isinstance(good_val, SupportsRealOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsRealOpsSCT), f"{good_val!r}"

        # Symbolic relationals can't be reduced to a boolean
        if isinstance(good_val, sympy.core.symbol.Symbol):
            good_val <= good_val
            good_val >= good_val
        else:
            assert good_val <= good_val, f"{good_val!r}"
            assert good_val >= good_val, f"{good_val!r}"


def test_supports_real_ops_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        func(cast(SupportsRealOps, good_val))
        func_t(cast(SupportsRealOpsSCU, good_val))
