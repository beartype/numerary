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

from numerary import RealLike
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
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

    uint8_val = numpy.uint8(2)
    assert isinstance(uint8_val, RealLike)
    uint16_val = numpy.uint16(273)
    assert isinstance(uint16_val, RealLike)
    uint32_val = numpy.uint32(273)
    assert isinstance(uint32_val, RealLike)
    uint64_val = numpy.uint64(273)
    assert isinstance(uint64_val, RealLike)
    int8_val = numpy.int8(-2)
    assert isinstance(int8_val, RealLike)
    int16_val = numpy.int16(-273)
    assert isinstance(int16_val, RealLike)
    int32_val = numpy.int32(-273)
    assert isinstance(int32_val, RealLike)
    int64_val = numpy.int64(-273)
    assert isinstance(int64_val, RealLike)
    float16_val = numpy.float16(-1.8)
    assert isinstance(float16_val, RealLike)
    float32_val = numpy.float32(-273.15)
    assert isinstance(float32_val, RealLike)
    float64_val = numpy.float64(-273.15)
    assert isinstance(float64_val, RealLike)
    float128_val = numpy.float128(-273.15)
    assert isinstance(float128_val, RealLike)

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

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, RealLike), f"{bad_val!r}"


def test_real_like_numpy_beartype() -> None:
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
        real_like_func(cast(RealLike, good_val))

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            real_like_func(cast(RealLike, bad_val))


def test_real_like_sympy() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

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
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    for good_val in (
        sympy.Integer(-273),
        sympy.Rational(-27315, 100),
        sympy.Float(-273.15),
        sympy.symbols("x"),
    ):
        real_like_func(cast(RealLike, good_val))
