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
from beartype import beartype, roar

from numerary.types import SupportsRealOps

from .numberwang import (
    Numberwang,
    NumberwangDerived,
    NumberwangRegistered,
    TestIntEnum,
    TestIntFlag,
    Wangernumb,
    WangernumbDerived,
    WangernumbRegistered,
)

__all__ = ()


# ---- Functions -----------------------------------------------------------------------


@beartype
def supports_real_ops_func(arg: SupportsRealOps):
    assert isinstance(arg, SupportsRealOps), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_real_ops() -> None:
    bool_val: SupportsRealOps = True
    int_val: SupportsRealOps = -273
    float_val: SupportsRealOps = -273.15
    frac_val: SupportsRealOps = Fraction(-27315, 100)
    dec_val: SupportsRealOps = Decimal("-273.15")
    test_int_enum: SupportsRealOps = TestIntEnum.ZERO
    test_int_flag: SupportsRealOps = TestIntFlag.B
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
        test_int_enum,
        test_int_flag,
        nw_val,
        nwd_val,
        nwr_val,
        wn_val,
        wnd_val,
        wnr_val,
    ):
        assert isinstance(good_val, SupportsRealOps), f"{good_val!r}"
        assert good_val <= good_val, f"{good_val!r}"
        assert good_val >= good_val, f"{good_val!r}"

    complex_bad_val: SupportsRealOps = complex(-273.15)  # type: ignore [assignment]

    for bad_val in (
        complex_bad_val,
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsRealOps), f"{bad_val!r}"


def test_supports_real_ops_beartype() -> None:
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
        supports_real_ops_func(cast(SupportsRealOps, good_val))

    for bad_val in (
        complex(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_ops_func(cast(SupportsRealOps, bad_val))


def test_supports_real_ops_numpy() -> None:
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

    uint8_val = numpy.uint8(2)
    assert isinstance(uint8_val, SupportsRealOps)
    uint16_val = numpy.uint16(273)
    assert isinstance(uint16_val, SupportsRealOps)
    uint32_val = numpy.uint32(273)
    assert isinstance(uint32_val, SupportsRealOps)
    uint64_val = numpy.uint64(273)
    assert isinstance(uint64_val, SupportsRealOps)
    int8_val = numpy.int8(-2)
    assert isinstance(int8_val, SupportsRealOps)
    int16_val = numpy.int16(-273)
    assert isinstance(int16_val, SupportsRealOps)
    int32_val = numpy.int32(-273)
    assert isinstance(int32_val, SupportsRealOps)
    int64_val = numpy.int64(-273)
    assert isinstance(int64_val, SupportsRealOps)
    float16_val = numpy.float16(-1.8)
    assert isinstance(float16_val, SupportsRealOps)
    float32_val = numpy.float32(-273.15)
    assert isinstance(float32_val, SupportsRealOps)
    float64_val = numpy.float64(-273.15)
    assert isinstance(float64_val, SupportsRealOps)
    float128_val = numpy.float128(-273.15)
    assert isinstance(float128_val, SupportsRealOps)

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
        assert good_val <= good_val, f"{good_val!r}"
        assert good_val >= good_val, f"{good_val!r}"

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, SupportsRealOps), f"{bad_val!r}"


def test_supports_real_ops_numpy_beartype() -> None:
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

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
        supports_real_ops_func(cast(SupportsRealOps, good_val))

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_ops_func(cast(SupportsRealOps, bad_val))


def test_supports_real_ops_sympy() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

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

        # Symbolic relationals can't be reduced to a boolean
        if isinstance(good_val, sympy.Symbol):
            good_val <= good_val
            good_val >= good_val
        else:
            assert good_val <= good_val, f"{good_val!r}"
            assert good_val >= good_val, f"{good_val!r}"


def test_supports_real_ops_sympy_beartype() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        supports_real_ops_func(cast(SupportsRealOps, good_val))
