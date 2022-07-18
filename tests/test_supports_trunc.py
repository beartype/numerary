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
from beartype import beartype

from numerary.types import SupportsTrunc, __trunc__

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
def supports_trunc_func(arg: SupportsTrunc):
    assert isinstance(arg, SupportsTrunc), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_trunc() -> None:
    bool_val: SupportsTrunc = True
    int_val: SupportsTrunc = -273
    float_val: SupportsTrunc = -273.15
    frac_val: SupportsTrunc = Fraction(-27315, 100)
    dec_val: SupportsTrunc = Decimal("-273.15")
    test_int_enum: SupportsTrunc = TestIntEnum.ZERO
    test_int_flag: SupportsTrunc = TestIntFlag.B
    nw_val: SupportsTrunc = Numberwang(-273)
    nwd_val: SupportsTrunc = NumberwangDerived(-273)
    nwr_val: SupportsTrunc = NumberwangRegistered(-273)
    wn_val: SupportsTrunc = Wangernumb(-273.15)
    wnd_val: SupportsTrunc = WangernumbDerived(-273.15)
    wnr_val: SupportsTrunc = WangernumbRegistered(-273.15)

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
        assert isinstance(good_val, SupportsTrunc), f"{good_val!r}"
        assert __trunc__(good_val), f"{good_val!r}"

    complex_bad_val: SupportsTrunc = complex(-273.15)  # type: ignore [assignment]

    for bad_val in (
        complex_bad_val,
        "-273.15",
    ):
        assert not isinstance(bad_val, SupportsTrunc), f"{bad_val!r}"


def test_trunc_beartype() -> None:
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
        supports_trunc_func(cast(SupportsTrunc, good_val))

    for bad_val in (
        complex(-273.15),
        "-273.15",
    ):
        with pytest.raises(roar.BeartypeException):
            supports_trunc_func(cast(SupportsTrunc, bad_val))


def test_trunc_numpy() -> None:
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

    float64_val: SupportsTrunc = numpy.float64(-273.15)

    # numpy.float64 seems to have a closer relationship to the native float than the
    # other numpy.float* types
    for good_val in (float64_val,):
        assert isinstance(good_val, SupportsTrunc), f"{good_val!r}"
        assert __trunc__(good_val), f"{good_val!r}"

    # TODO(posita): These should not validate
    float16_val: SupportsTrunc = numpy.float16(-1.8)
    float32_val: SupportsTrunc = numpy.float32(-273.15)
    float128_val: SupportsTrunc = numpy.float128(-273.15)

    for bad_val in (
        numpy.uint8(2),
        numpy.uint16(273),
        numpy.uint32(273),
        numpy.uint64(273),
        numpy.int8(-2),
        numpy.int16(-273),
        numpy.int32(-273),
        numpy.int64(-273),
        float16_val,
        float32_val,
        float128_val,
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        assert not isinstance(bad_val, SupportsTrunc), f"{bad_val!r}"


def test_trunc_numpy_beartype() -> None:
    pytest.importorskip("numpy", reason="requires numpy")
    import numpy

    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    # numpy.float64 seems to have a closer relationship to the native float than the
    # other numpy.float* types
    for good_val in (numpy.float64(-273.15),):
        supports_trunc_func(cast(SupportsTrunc, good_val))

    for lying_val in (
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
        numpy.float128(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_trunc_func(cast(SupportsTrunc, lying_val))

    for bad_val in (
        numpy.csingle(-273.15),
        numpy.cdouble(-273.15),
        numpy.clongdouble(-273.15),
    ):
        with pytest.raises(roar.BeartypeException):
            supports_trunc_func(cast(SupportsTrunc, bad_val))


def test_trunc_sympy() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    integer_val: SupportsTrunc = sympy.Integer(-273)
    rational_val: SupportsTrunc = sympy.Rational(-27315, 100)
    float_val: SupportsTrunc = sympy.Float(-273.15)

    for good_val in (
        integer_val,
        rational_val,
        float_val,
    ):
        assert isinstance(good_val, SupportsTrunc), f"{good_val!r}"
        assert __trunc__(good_val), f"{good_val!r}"

    # TODO(posita): These should not validate
    sym_val: SupportsTrunc = sympy.symbols("x")

    for lying_val in (sym_val,):
        assert not isinstance(lying_val, SupportsTrunc), f"{lying_val!r}"

        # Relationals have, but don't implement this function
        with pytest.raises(Exception):  # TypeError or beartype.roar.BeartypeException
            __trunc__(lying_val)


def test_trunc_sympy_beartype() -> None:
    pytest.importorskip("sympy", reason="requires sympy")
    import sympy

    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Rational(-27315, 100),
        sympy.Float(-273.15),
    ):
        supports_trunc_func(cast(SupportsTrunc, good_val))

    for lying_val in (sympy.symbols("x"),):
        supports_trunc_func(cast(SupportsTrunc, good_val))
