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
    RationalLikeMixedSCU,
    RationalLikeMixedT,
    RationalLikeMixedU,
    RationalLikeProperties,
)

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
def rational_like_func(arg: RationalLikeMixedU):
    assert isinstance(arg, RationalLikeMixedT), f"{arg!r}"


@beartype
def rational_like_func_t(arg: RationalLikeMixedSCU):
    assert isinstance(arg, RationalLikeMixedT), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_rational_like() -> None:
    bool_val: RationalLikeProperties = True
    int_val: RationalLikeProperties = -273
    frac_val: RationalLikeProperties = Fraction(-27315, 100)
    test_int_enum: RationalLikeProperties = TestIntEnum.ZERO
    test_int_flag: RationalLikeProperties = TestIntFlag.B
    nw_val: RationalLikeProperties = Numberwang(-273)
    nwd_val: RationalLikeProperties = NumberwangDerived(-273)
    nwr_val: RationalLikeProperties = NumberwangRegistered(-273)

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

    for bad_val in (
        -273.15,
        complex(-273.15),
        Decimal("-273.15"),
        TestFlag.B,
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
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
        TestFlag.B,
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
    uint8_val: RationalLikeProperties = numpy.uint8(2)
    uint16_val: RationalLikeProperties = numpy.uint16(273)
    uint32_val: RationalLikeProperties = numpy.uint32(273)
    uint64_val: RationalLikeProperties = numpy.uint64(273)
    int8_val: RationalLikeProperties = numpy.int8(-2)
    int16_val: RationalLikeProperties = numpy.int16(-273)
    int32_val: RationalLikeProperties = numpy.int32(-273)
    int64_val: RationalLikeProperties = numpy.int64(-273)

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
    float16_val: RationalLikeProperties = numpy.float16(-1.8)
    float32_val: RationalLikeProperties = numpy.float32(-273.15)
    float64_val: RationalLikeProperties = numpy.float64(-273.15)
    float128_val: RationalLikeProperties = numpy.float128(-273.15)
    csingle_val: RationalLikeProperties = numpy.csingle(-273.15)
    cdouble_val: RationalLikeProperties = numpy.cdouble(-273.15)
    clongdouble_val: RationalLikeProperties = numpy.clongdouble(-273.15)

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
    integral_val: RationalLikeProperties = sympy.Integer(-273)
    rational_val: RationalLikeProperties = sympy.Rational(-27315, 100)

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
    sym_float: RationalLikeProperties = sympy.Float(-273.15)
    sym_sym: RationalLikeProperties = sympy.symbols("x")

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