# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from decimal import Decimal
from fractions import Fraction
from typing import cast

import pytest
from beartype import beartype, roar

from numerary.types import SupportsConjugate

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
def supports_conjugate_func(arg: SupportsConjugate):
    assert isinstance(arg, SupportsConjugate), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_conjugate() -> None:
    bool_val: SupportsConjugate = True
    int_val: SupportsConjugate = -273
    float_val: SupportsConjugate = -273.15
    complex_val: SupportsConjugate = complex(-273.15)
    frac_val: SupportsConjugate = Fraction(-27315, 100)
    dec_val: SupportsConjugate = Decimal("-273.15")
    test_int_enum: SupportsConjugate = TestIntEnum.ZERO
    test_int_flag: SupportsConjugate = TestIntFlag.B
    # These have inherited this interface by deriving from number tower ABCs
    nwd_val: SupportsConjugate = NumberwangDerived(-273)
    wnd_val: SupportsConjugate = WangernumbDerived(-273.15)

    for good_val in (
        bool_val,
        int_val,
        float_val,
        complex_val,
        frac_val,
        dec_val,
        test_int_enum,
        test_int_flag,
        nwd_val,
        wnd_val,
    ):
        assert isinstance(good_val, SupportsConjugate), f"{good_val!r}"
        assert good_val.conjugate(), f"{good_val!r}"

    nw_bad_val: SupportsConjugate = Numberwang(-273)  # type: ignore [assignment]
    nwr_bad_val: SupportsConjugate = NumberwangRegistered(-273)  # type: ignore [assignment]
    wn_bad_val: SupportsConjugate = Wangernumb(-273.15)  # type: ignore [assignment]
    wnr_bad_val: SupportsConjugate = WangernumbRegistered(-273.15)  # type: ignore [assignment]

    for bad_val in (
        nw_bad_val,
        nwr_bad_val,
        wn_bad_val,
        wnr_bad_val,
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsConjugate), f"{bad_val!r}"


def test_supports_conjugate_beartype() -> None:
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
        supports_conjugate_func(cast(SupportsConjugate, good_val))

    for bad_val in (
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_conjugate_func(cast(SupportsConjugate, bad_val))

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_conjugate_func(cast(SupportsConjugate, lying_val))


def test_supports_conjugate_numpy() -> None:
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

    uint8_val: SupportsConjugate = numpy.uint8(2)
    uint16_val: SupportsConjugate = numpy.uint16(273)
    uint32_val: SupportsConjugate = numpy.uint32(273)
    uint64_val: SupportsConjugate = numpy.uint64(273)
    int8_val: SupportsConjugate = numpy.int8(-2)
    int16_val: SupportsConjugate = numpy.int16(-273)
    int32_val: SupportsConjugate = numpy.int32(-273)
    int64_val: SupportsConjugate = numpy.int64(-273)
    float16_val: SupportsConjugate = numpy.float16(-1.8)
    float32_val: SupportsConjugate = numpy.float32(-273.15)
    float64_val: SupportsConjugate = numpy.float64(-273.15)
    float128_val: SupportsConjugate = numpy.float128(-273.15)
    csingle_val: SupportsConjugate = numpy.float32(-273.15)
    cdouble_val: SupportsConjugate = numpy.float64(-273.15)
    clongdouble_val: SupportsConjugate = numpy.float128(-273.15)

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
        assert isinstance(good_val, SupportsConjugate), f"{good_val!r}"
        assert good_val.conjugate(), f"{good_val!r}"


def test_supports_conjugate_numpy_beartype() -> None:
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
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        supports_conjugate_func(cast(SupportsConjugate, good_val))


def test_supports_conjugate_sympy() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    integer_val: SupportsConjugate = sympy.Integer(-273)
    rational_val: SupportsConjugate = sympy.Rational(-27315, 100)
    float_val: SupportsConjugate = sympy.Float(-273.15)
    sym_val: SupportsConjugate = sympy.symbols("x")

    for good_val in (
        integer_val,
        rational_val,
        float_val,
        sym_val,
    ):
        assert isinstance(good_val, SupportsConjugate), f"{good_val!r}"
        assert good_val.conjugate(), f"{good_val!r}"


def test_supports_conjugate_sympy_beartype() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        supports_conjugate_func(cast(SupportsConjugate, good_val))
