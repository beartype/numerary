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

from numerary import RealLike
from numerary.bt import beartype
from numerary.types import __ceil__, __floor__, __trunc__

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
def real_like_func(arg: RealLike):
    assert isinstance(arg, RealLike), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_real_like() -> None:
    bool_val: RealLike = True
    int_val: RealLike = -273
    float_val: RealLike = -273.15
    frac_val: RealLike = Fraction(-27315, 100)
    dec_val: RealLike = Decimal("-273.15")
    test_int_enum: RealLike = TestIntEnum.ZERO
    test_int_flag: RealLike = TestIntFlag.B
    nw_val: RealLike = Numberwang(-273)
    nwd_val: RealLike = NumberwangDerived(-273)
    nwr_val: RealLike = NumberwangRegistered(-273)
    wn_val: RealLike = Wangernumb(-273.15)
    wnd_val: RealLike = WangernumbDerived(-273.15)
    wnr_val: RealLike = WangernumbRegistered(-273.15)

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
        assert isinstance(good_val, RealLike), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val**1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"
        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"
        assert __trunc__(good_val), f"{good_val!r}"
        assert __floor__(good_val), f"{good_val!r}"
        assert __ceil__(good_val), f"{good_val!r}"

    complex_bad_val: RealLike = complex(-273.15)  # type: ignore [assignment]

    for bad_val in (
        complex_bad_val,
        "-273.15",
    ):
        assert not isinstance(bad_val, RealLike), f"{bad_val!r}"


def test_real_like_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

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
        real_like_func(cast(RealLike, good_val))

    for bad_val in (
        complex(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            real_like_func(cast(RealLike, bad_val))


def test_real_like_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")
    uint8_val: RealLike = numpy.uint8(2)
    uint16_val: RealLike = numpy.uint16(273)
    uint32_val: RealLike = numpy.uint32(273)
    uint64_val: RealLike = numpy.uint64(273)
    int8_val: RealLike = numpy.int8(-2)
    int16_val: RealLike = numpy.int16(-273)
    int32_val: RealLike = numpy.int32(-273)
    int64_val: RealLike = numpy.int64(-273)
    float16_val: RealLike = numpy.float16(-1.8)
    float32_val: RealLike = numpy.float32(-273.15)
    float64_val: RealLike = numpy.float64(-273.15)
    float128_val: RealLike = numpy.float128(-273.15)

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
        assert isinstance(good_val, RealLike), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val**1 == good_val, f"{good_val!r}"

        # numpy.uint*.__neg__ means something different than what we're testing for
        if not isinstance(
            good_val,
            (numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64),
        ):
            assert 0 - good_val == -good_val, f"{good_val!r}"

        assert good_val - 1 < good_val, f"{good_val!r}"
        assert good_val - 1 <= good_val, f"{good_val!r}"
        assert good_val >= good_val - 1, f"{good_val!r}"
        assert good_val > good_val - 1, f"{good_val!r}"

    # TODO(posita): These should not validate
    csingle_val: RealLike = numpy.csingle(-273.15)
    cdouble_val: RealLike = numpy.cdouble(-273.15)
    clongdouble_val: RealLike = numpy.clongdouble(-273.15)

    for bad_val in (
        csingle_val,
        cdouble_val,
        clongdouble_val,
    ):
        assert not isinstance(bad_val, RealLike), f"{bad_val!r}"


def test_real_like_numpy_beartype() -> None:
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
        real_like_func(cast(RealLike, good_val))

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            real_like_func(cast(RealLike, bad_val))


def test_real_like_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    integer_val: RealLike = sympy.Integer(-273)
    rational_val: RealLike = sympy.Rational(-27315, 100)
    float_val: RealLike = sympy.Float(-273.15)
    sym_val: RealLike = sympy.symbols("x")

    for good_val in (
        integer_val,
        rational_val,
        float_val,
        sym_val,
    ):
        assert isinstance(good_val, RealLike), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert good_val**1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"

        # Symbolic relationals can't be reduced to a boolean or truncated
        if isinstance(good_val, sympy.Symbol):
            good_val - 1 < good_val
            good_val - 1 <= good_val
            good_val >= good_val - 1
            good_val > good_val - 1
        else:
            assert good_val - 1 < good_val, f"{good_val!r}"
            assert good_val - 1 <= good_val, f"{good_val!r}"
            assert good_val >= good_val - 1, f"{good_val!r}"
            assert good_val > good_val - 1, f"{good_val!r}"
            assert __trunc__(good_val), f"{good_val!r}"
            assert __floor__(good_val), f"{good_val!r}"
            assert __ceil__(good_val), f"{good_val!r}"


def test_real_like_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires sympy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Rational(-27315, 100),
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        real_like_func(cast(RealLike, good_val))
