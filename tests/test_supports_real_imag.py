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
from numerary.types import SupportsRealImag, SupportsRealImagSCU

from .numberwang import (
    Numberwang,
    NumberwangDerived,
    NumberwangRegistered,
    TestFlag,
    TestIntEnum,
    TestIntFlag,
    Wangernumb,
    WangernumbDerived,
    WangernumbRegistered,
)

__all__ = ()


# ---- Functions -----------------------------------------------------------------------


@beartype
def supports_real_imag_func(arg: SupportsRealImag):
    assert isinstance(arg, SupportsRealImag), f"{arg!r}"


@beartype
def supports_real_imag_func_t(arg: SupportsRealImagSCU):
    assert isinstance(arg, SupportsRealImag), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_real_imag() -> None:
    bool_val: SupportsRealImag = True
    int_val: SupportsRealImag = -273
    float_val: SupportsRealImag = -273.15
    frac_val: SupportsRealImag = Fraction(-27315, 100)
    dec_val: SupportsRealImag = Decimal("-273.15")
    test_int_enum: SupportsRealImag = TestIntEnum.ZERO
    test_int_flag: SupportsRealImag = TestIntFlag.B
    # These have inherited this interface by deriving from number tower ABCs
    nwd_val: SupportsRealImag = NumberwangDerived(-273)
    wnd_val: SupportsRealImag = WangernumbDerived(-273.15)

    for good_val in (
        bool_val,
        int_val,
        float_val,
        frac_val,
        dec_val,
        test_int_enum,
        test_int_flag,
        nwd_val,
        wnd_val,
    ):
        assert isinstance(good_val, SupportsRealImag), f"{good_val!r}"
        assert hasattr(good_val, "real"), f"{good_val!r}"
        assert hasattr(good_val, "imag"), f"{good_val!r}"

    for bad_val in (
        TestFlag.B,
        Numberwang(-273),
        NumberwangRegistered(-273),
        Wangernumb(-273.15),
        WangernumbRegistered(-273.15),
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsRealImag), f"{bad_val!r}"


def test_supports_real_imag_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        TestIntEnum.ZERO,
        TestIntFlag.B,
        # These have inherited this interface by deriving from number tower ABCs
        NumberwangDerived(-273),
        WangernumbDerived(-273.15),
    ):
        supports_real_imag_func(cast(SupportsRealImag, good_val))
        supports_real_imag_func_t(cast(SupportsRealImagSCU, good_val))

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func(cast(SupportsRealImag, lying_val))

        with pytest.raises(AssertionError):  # gets past beartype
            supports_real_imag_func_t(cast(SupportsRealImagSCU, lying_val))

    for bad_val in (
        TestFlag.B,
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func(cast(SupportsRealImag, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func_t(cast(SupportsRealImagSCU, bad_val))


def test_supports_real_imag_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: SupportsRealImag = numpy.uint8(2)
    uint16_val: SupportsRealImag = numpy.uint16(273)
    uint32_val: SupportsRealImag = numpy.uint32(273)
    uint64_val: SupportsRealImag = numpy.uint64(273)
    int8_val: SupportsRealImag = numpy.int8(-2)
    int16_val: SupportsRealImag = numpy.int16(-273)
    int32_val: SupportsRealImag = numpy.int32(-273)
    int64_val: SupportsRealImag = numpy.int64(-273)
    float16_val: SupportsRealImag = numpy.float16(-1.8)
    float32_val: SupportsRealImag = numpy.float32(-273.15)
    float64_val: SupportsRealImag = numpy.float64(-273.15)
    float128_val: SupportsRealImag = numpy.float128(-273.15)
    csingle_val: SupportsRealImag = numpy.float32(-273.15)
    cdouble_val: SupportsRealImag = numpy.float64(-273.15)
    clongdouble_val: SupportsRealImag = numpy.float128(-273.15)

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
        csingle_val,
        cdouble_val,
        clongdouble_val,
    ):
        assert isinstance(good_val, SupportsRealImag), f"{good_val!r}"
        assert hasattr(good_val, "real"), f"{good_val!r}"
        assert hasattr(good_val, "imag"), f"{good_val!r}"


def test_supports_real_imag_numpy_beartype() -> None:
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
        supports_real_imag_func(cast(SupportsRealImag, good_val))
        supports_real_imag_func_t(cast(SupportsRealImagSCU, good_val))


def test_supports_real_imag_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    # TODO(posita): These should not validate
    integer_val: SupportsRealImag = sympy.Integer(-273)
    rational_val: SupportsRealImag = sympy.Rational(-27315, 100)
    float_val: SupportsRealImag = sympy.Float(-273.15)
    sym_val: SupportsRealImag = sympy.symbols("x")

    for bad_val in (
        integer_val,
        rational_val,
        float_val,
        sym_val,
    ):
        assert not isinstance(bad_val, SupportsRealImag), f"{bad_val!r}"


def test_supports_real_imag_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        sympy.Integer(-273),
        sympy.Rational(-27315, 100),
        sympy.Float(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func(cast(SupportsRealImag, lying_val))

        with pytest.raises(AssertionError):  # gets past beartype
            supports_real_imag_func_t(cast(SupportsRealImagSCU, lying_val))

    for bad_val in (sympy.symbols("x"),):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func(cast(SupportsRealImag, bad_val))

        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func_t(cast(SupportsRealImagSCU, bad_val))
