# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

import math
from decimal import Decimal
from fractions import Fraction
from typing import cast

import pytest

from numerary.bt import beartype
from numerary.types import (
    RationalLike,
    RationalLikeMixedSCU,
    RationalLikeMixedT,
    RationalLikeMixedU,
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
def rational_like_func(arg: RationalLikeMixedU):
    assert isinstance(arg, RationalLikeMixedT), f"{arg!r}"


@beartype
def rational_like_func_t(arg: RationalLikeMixedSCU):
    assert isinstance(arg, RationalLikeMixedT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_rational_like() -> None:
    bool_val: RationalLike = True
    int_val: RationalLike = -273
    frac_val: RationalLike = Fraction(-27315, 100)
    test_int_enum: RationalLike = TestIntEnum.ZERO
    test_int_flag: RationalLike = TestIntFlag.B
    nw_val: RationalLike = Numberwang(-273)
    nwd_val: RationalLike = NumberwangDerived(-273)
    nwr_val: RationalLike = NumberwangRegistered(-273)

    for good_val in (
        bool_val,
        int_val,
        frac_val,
        test_int_enum,
        test_int_flag,
        nw_val,
        nwd_val,
        nwr_val,
    ):
        assert isinstance(good_val, RationalLikeMixedT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"
        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"
        assert math.trunc(good_val), f"{good_val!r}"
        assert math.floor(good_val), f"{good_val!r}"
        assert math.ceil(good_val), f"{good_val!r}"
        assert good_val.numerator, f"{good_val!r}"
        assert good_val.denominator, f"{good_val!r}"

    float_bad_val: RationalLike = -273.15  # type: ignore [assignment]
    complex_bad_val: RationalLike = complex(-273.15)  # type: ignore [assignment]
    dec_bad_val: RationalLike = Decimal("-273.15")  # type: ignore [assignment]
    wn_bad_val: RationalLike = Wangernumb(-273.15)  # type: ignore [assignment]
    wnd_bad_val: RationalLike = WangernumbDerived(-273.15)  # type: ignore [assignment]
    wnr_bad_val: RationalLike = WangernumbRegistered(-273.15)  # type: ignore [assignment]

    for bad_val in (
        float_bad_val,
        complex_bad_val,
        dec_bad_val,
        wn_bad_val,
        wnd_bad_val,
        wnr_bad_val,
        "-273",
    ):
        assert not isinstance(bad_val, RationalLikeMixedT), f"{bad_val!r}"


def test_rational_like_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        Fraction(-27315, 100),
        TestIntEnum.ZERO,
        TestIntFlag.B,
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
    ):
        rational_like_func(cast(RationalLikeMixedU, good_val))
        rational_like_func_t(cast(RationalLikeMixedSCU, good_val))

    for bad_val in (
        -273.15,
        complex(-273.15),
        Decimal("-273.15"),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
        "-273",
    ):
        with pytest.raises(roar.BeartypeException):
            rational_like_func(cast(RationalLikeMixedU, bad_val))

        with pytest.raises(roar.BeartypeException):
            rational_like_func_t(cast(RationalLikeMixedSCU, bad_val))


def test_rational_like_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: RationalLike = numpy.uint8(2)
    uint16_val: RationalLike = numpy.uint16(273)
    uint32_val: RationalLike = numpy.uint32(273)
    uint64_val: RationalLike = numpy.uint64(273)
    int8_val: RationalLike = numpy.int8(-2)
    int16_val: RationalLike = numpy.int16(-273)
    int32_val: RationalLike = numpy.int32(-273)
    int64_val: RationalLike = numpy.int64(-273)

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
        assert isinstance(good_val, RationalLikeMixedT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"
        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"
        assert good_val.numerator, f"{good_val!r}"
        assert good_val.denominator, f"{good_val!r}"

    # TODO(posita): These should not validate
    float16_val: RationalLike = numpy.float16(-1.8)
    float32_val: RationalLike = numpy.float32(-273.15)
    float64_val: RationalLike = numpy.float64(-273.15)
    float128_val: RationalLike = numpy.float128(-273.15)
    csingle_val: RationalLike = numpy.csingle(-273.15)
    cdouble_val: RationalLike = numpy.cdouble(-273.15)
    clongdouble_val: RationalLike = numpy.clongdouble(-273.15)

    for bad_val in (
        float16_val,
        float32_val,
        float64_val,
        float128_val,
        csingle_val,
        cdouble_val,
        clongdouble_val,
    ):
        assert not isinstance(bad_val, RationalLikeMixedT), f"{bad_val!r}"


def test_rational_like_numpy_beartype() -> None:
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
    ):
        rational_like_func(cast(RationalLikeMixedU, good_val))
        rational_like_func_t(cast(RationalLikeMixedSCU, good_val))

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
            rational_like_func(cast(RationalLikeMixedU, bad_val))

        with pytest.raises(roar.BeartypeException):
            rational_like_func_t(cast(RationalLikeMixedSCU, bad_val))


def test_rational_like_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    integral_val: RationalLike = sympy.Integer(-273)
    rational_val: RationalLike = sympy.Rational(-27315, 100)

    for good_val in (
        integral_val,
        rational_val,
    ):
        assert isinstance(good_val, RationalLikeMixedT), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"
        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"
        assert math.trunc(good_val), f"{good_val!r}"
        assert math.floor(good_val), f"{good_val!r}"
        assert math.ceil(good_val), f"{good_val!r}"
        assert good_val.numerator, f"{good_val!r}"
        assert good_val.denominator, f"{good_val!r}"

    # TODO(posita): These should not validate
    sym_float: RationalLike = sympy.Float(-273.15)
    sym_sym: RationalLike = sympy.symbols("x")

    for bad_val in (
        sym_float,
        sym_sym,
    ):
        assert not isinstance(bad_val, RationalLikeMixedT), f"{bad_val!r}"


def test_rational_like_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Rational(-27315, 100),
        sympy.Integer(-273),
    ):
        rational_like_func(cast(RationalLikeMixedU, good_val))
        rational_like_func_t(cast(RationalLikeMixedSCU, good_val))

    for bad_val in (
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        with pytest.raises(roar.BeartypeException):
            rational_like_func(cast(RationalLikeMixedU, bad_val))

        with pytest.raises(roar.BeartypeException):
            rational_like_func_t(cast(RationalLikeMixedSCU, bad_val))
