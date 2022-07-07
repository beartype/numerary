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

import pytest
from beartype import beartype, roar
from beartype.typing import cast

from numerary.types import SupportsIntegralOps, SupportsIntegralPow

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
def supports_integral_ops_func(arg: SupportsIntegralOps):
    assert isinstance(arg, SupportsIntegralOps), f"{arg!r}"


@beartype
def supports_integral_pow_func(arg: SupportsIntegralPow):
    assert isinstance(arg, SupportsIntegralPow), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_integral_ops_pow() -> None:
    bool_val: SupportsIntegralOps = True
    int_val: SupportsIntegralOps = -273
    test_int_enum: SupportsIntegralOps = TestIntEnum.ZERO
    test_int_flag: SupportsIntegralOps = TestIntFlag.B
    nw_val: SupportsIntegralOps = Numberwang(-273)
    nwd_val: SupportsIntegralOps = NumberwangDerived(-273)
    nwr_val: SupportsIntegralOps = NumberwangRegistered(-273)
    _: SupportsIntegralPow
    _ = True
    _ = -273
    _ = TestIntEnum.ZERO
    _ = TestIntFlag.B
    _ = Numberwang(-273)
    _ = NumberwangDerived(-273)
    _ = NumberwangRegistered(-273)

    for good_val in (
        bool_val,
        int_val,
        test_int_enum,
        test_int_flag,
        nw_val,
        nwd_val,
        nwr_val,
    ):
        assert isinstance(good_val, SupportsIntegralOps), f"{good_val!r}"
        assert good_val >> 0 == good_val, f"{good_val!r}"
        assert good_val << 0 == good_val, f"{good_val!r}"
        assert good_val & 0 == 0, f"{good_val!r}"
        assert good_val | 0 == good_val, f"{good_val!r}"
        assert isinstance(good_val, SupportsIntegralPow), f"{good_val!r}"
        assert good_val**1 == good_val, f"{good_val!r}"

    float_bad_val: SupportsIntegralOps = -273.15  # type: ignore [assignment]
    complex_bad_val: SupportsIntegralOps = complex(-273.15)  # type: ignore [assignment]
    frac_bad_val: SupportsIntegralOps = Fraction(-27315, 100)  # type: ignore [assignment]
    dec_bad_val: SupportsIntegralOps = Decimal("-273.15")  # type: ignore [assignment]
    wn_bad_val: SupportsIntegralOps = Wangernumb(-273.15)  # type: ignore [assignment]
    wnd_bad_val: SupportsIntegralOps = WangernumbDerived(-273.15)  # type: ignore [assignment]
    wnr_bad_val: SupportsIntegralOps = WangernumbRegistered(-273.15)  # type: ignore [assignment]
    # TODO(posita): These should not validate
    _ = -273.15
    _ = complex(-273.15)
    _ = Fraction(-27315, 100)  # type: ignore [assignment]
    _ = Decimal("-273.15")
    _ = Wangernumb(-273.15)  # type: ignore [assignment]
    _ = WangernumbDerived(-273.15)  # type: ignore [assignment]
    _ = WangernumbRegistered(-273.15)  # type: ignore [assignment]

    for bad_val in (
        float_bad_val,
        complex_bad_val,
        frac_bad_val,
        dec_bad_val,
        wn_bad_val,
        wnd_bad_val,
        wnr_bad_val,
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsIntegralOps), f"{bad_val!r}"


def test_supports_integral_ops_pow_beartype() -> None:
    for good_val in (
        True,
        -273,
        TestIntEnum.ZERO,
        TestIntFlag.B,
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
    ):
        supports_integral_ops_func(cast(SupportsIntegralOps, good_val))
        supports_integral_pow_func(cast(SupportsIntegralPow, good_val))

    for bad_val in (
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func(cast(SupportsIntegralOps, bad_val))


def test_supports_integral_ops_pow_numpy() -> None:
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

    uint8_val: SupportsIntegralOps = numpy.uint8(2)
    uint16_val: SupportsIntegralOps = numpy.uint16(273)
    uint32_val: SupportsIntegralOps = numpy.uint32(273)
    uint64_val: SupportsIntegralOps = numpy.uint64(273)
    int8_val: SupportsIntegralOps = numpy.int8(-2)
    int16_val: SupportsIntegralOps = numpy.int16(-273)
    int32_val: SupportsIntegralOps = numpy.int32(-273)
    int64_val: SupportsIntegralOps = numpy.int64(-273)

    for good_val in (
        uint8_val,
        uint16_val,
        uint32_val,
        uint64_val,
        int8_val,
        int16_val,
        int32_val,
        int64_val,
    ):
        assert isinstance(good_val, SupportsIntegralOps), f"{good_val!r}"

        # I have no idea why numpy.uint64 is special in this regard
        if isinstance(good_val, numpy.uint64):
            assert good_val >> type(good_val)(0) == good_val, f"{good_val!r}"
            assert good_val << type(good_val)(0) == good_val, f"{good_val!r}"
            assert good_val & type(good_val)(0) == type(good_val)(0), f"{good_val!r}"
            assert good_val | type(good_val)(0) == good_val, f"{good_val!r}"
        else:
            assert good_val >> 0 == good_val, f"{good_val!r}"
            assert good_val << 0 == good_val, f"{good_val!r}"
            assert good_val & 0 == 0, f"{good_val!r}"
            assert good_val | 0 == good_val, f"{good_val!r}"

        assert isinstance(good_val, SupportsIntegralPow), f"{good_val!r}"
        assert good_val**1 == good_val, f"{good_val!r}"

    for bad_val in (
        numpy.float16(-1.8),
        numpy.float32(-273.15),
        numpy.float64(-273.15),
        numpy.float128(-273.15),
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, SupportsIntegralOps), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsIntegralPow), f"{bad_val!r}"


def test_supports_integral_ops_pow_numpy_beartype() -> None:
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
    ):
        supports_integral_ops_func(cast(SupportsIntegralOps, good_val))
        supports_integral_pow_func(cast(SupportsIntegralPow, good_val))

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
            supports_integral_ops_func(cast(SupportsIntegralOps, bad_val))


def test_supports_integral_ops_pow_sympy() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    integral_val: SupportsIntegralOps = sympy.Integer(-273)
    _: SupportsIntegralPow
    _ = sympy.Integer(-273)

    for good_val in (integral_val,):
        assert isinstance(good_val, SupportsIntegralOps), f"{good_val!r}"
        assert good_val >> 0 == good_val, f"{good_val!r}"
        assert good_val << 0 == good_val, f"{good_val!r}"
        assert good_val & 0 == 0, f"{good_val!r}"
        assert good_val | 0 == good_val, f"{good_val!r}"
        assert isinstance(good_val, SupportsIntegralPow), f"{good_val!r}"
        assert good_val**1 == good_val, f"{good_val!r}"

    # TODO(posita): These should not validate
    rational_val: SupportsIntegralOps = sympy.Rational(-27315, 100)
    sym_val: SupportsIntegralOps = sympy.symbols("x")
    _ = sympy.Float(-273.15)
    _ = sympy.Rational(-27315, 100)
    _ = sympy.symbols("x")

    for lying_val in (sym_val,):
        assert not isinstance(lying_val, SupportsIntegralOps), f"{lying_val!r}"

        # Relationals have, but don't implement this function
        with pytest.raises(Exception):  # TypeError or beartype.roar.BeartypeException
            lying_val << 0

    for bad_val in (
        sympy.Float(-273.15),
        rational_val,
    ):
        assert not isinstance(bad_val, SupportsIntegralOps), f"{bad_val!r}"


def test_supports_integral_ops_pow_sympy_beartype() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    for good_val in (sympy.Integer(-273),):
        supports_integral_ops_func(cast(SupportsIntegralOps, good_val))
        supports_integral_pow_func(cast(SupportsIntegralPow, good_val))

    for lying_val in (sympy.symbols("x"),):
        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func(cast(SupportsIntegralOps, lying_val))

    for bad_val in (
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_integral_ops_func(cast(SupportsIntegralOps, bad_val))
