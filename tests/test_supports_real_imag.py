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

from numerary.types import (
    SupportsRealImag,
    SupportsRealImagAsMethod,
    SupportsRealImagMixedT,
    SupportsRealImagMixedU,
    imag,
    real,
)

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
def supports_real_imag_func(arg: SupportsRealImagMixedU):
    assert isinstance(arg, SupportsRealImagMixedT), f"{arg!r}"


@beartype
def supports_real_imag_properties_func(arg: SupportsRealImag):
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
        assert isinstance(good_val, SupportsRealImagMixedT), f"{good_val!r}"
        assert real(good_val) is not None, f"{good_val!r}"
        assert imag(good_val) is not None, f"{good_val!r}"

    nw_bad_val: SupportsRealImagMixedU = Numberwang(-273)  # type: ignore [assignment]
    nwr_bad_val: SupportsRealImagMixedU = NumberwangRegistered(-273)  # type: ignore [assignment]
    wn_bad_val: SupportsRealImagMixedU = Wangernumb(-273.15)  # type: ignore [assignment]
    wnr_bad_val: SupportsRealImagMixedU = WangernumbRegistered(-273.15)  # type: ignore [assignment]

    for bad_val in (
        nw_bad_val,
        nwr_bad_val,
        wn_bad_val,
        wnr_bad_val,
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsRealImagMixedT), f"{bad_val!r}"


def test_supports_real_imag_beartype() -> None:
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
        supports_real_imag_func(cast(SupportsRealImagMixedU, good_val))

    for bad_val in (
        Numberwang(-273),
        Wangernumb(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func(cast(SupportsRealImagMixedU, bad_val))

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        NumberwangRegistered(-273),
        WangernumbRegistered(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_func(cast(SupportsRealImagMixedU, lying_val))


def test_supports_real_imag_numpy() -> None:
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

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
        assert isinstance(good_val, SupportsRealImagMixedT), f"{good_val!r}"
        assert real(good_val) is not None, f"{good_val!r}"
        assert imag(good_val) is not None, f"{good_val!r}"


def test_supports_real_imag_numpy_beartype() -> None:
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
        supports_real_imag_func(cast(SupportsRealImagMixedU, good_val))


def test_supports_real_imag_sympy() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    integer_val: SupportsRealImagAsMethod = sympy.Integer(-273)
    rational_val: SupportsRealImagAsMethod = sympy.Rational(-27315, 100)
    float_val: SupportsRealImagAsMethod = sympy.Float(-273.15)
    sym_val: SupportsRealImagAsMethod = sympy.symbols("x")

    for good_val in (
        integer_val,
        rational_val,
        float_val,
        sym_val,
    ):
        assert isinstance(good_val, SupportsRealImagMixedT), f"{good_val!r}"
        assert real(good_val) is not None, f"{good_val!r}"
        assert imag(good_val) is not None, f"{good_val!r}"


def test_supports_real_imag_sympy_beartype() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    for good_val in (
        sympy.Integer(-273),
        sympy.Rational(-27315, 100),
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        supports_real_imag_func(cast(SupportsRealImagMixedU, good_val))


def test_supports_real_imag_sympy_false_positives() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    # TODO(posita): These should not validate
    integer_val: SupportsRealImag = sympy.Integer(-273)
    rational_val: SupportsRealImag = sympy.Rational(-27315, 100)
    sym_val: SupportsRealImag = sympy.symbols("x")

    for bad_val in (
        integer_val,
        rational_val,
        sympy.Float(-273.15),
        sym_val,
    ):
        assert not isinstance(bad_val, SupportsRealImag), f"{bad_val!r}"


def test_supports_real_imag_sympy_beartype_false_positives() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    for lying_val in (
        # These have lied about supporting this interface when they registered
        # themselves in the number tower
        sympy.Integer(-273),
        sympy.Rational(-27315, 100),
        sympy.Float(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_properties_func(cast(SupportsRealImag, lying_val))

    for bad_val in (sympy.symbols("x"),):
        with pytest.raises(roar.BeartypeException):
            supports_real_imag_properties_func(cast(SupportsRealImag, bad_val))
