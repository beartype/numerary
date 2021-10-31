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
from numerary.types import (
    SupportsComplexOps,
    SupportsComplexOpsT,
    SupportsComplexOpsTs,
    SupportsComplexPow,
    SupportsComplexPowT,
    SupportsComplexPowTs,
)

from .numberwang import (
    Numberwang,
    NumberwangDerived,
    NumberwangRegistered,
    Wangernumb,
    WangernumbDerived,
    WangernumbRegistered,
)

__all__ = ()


# ---- Functions -----------------------------------------------------------------------


@beartype
def ops_func(arg: SupportsComplexOps):
    assert isinstance(arg, SupportsComplexOps), f"{arg!r}"


@beartype
def ops_func_t(arg: SupportsComplexOpsT):
    assert isinstance(arg, SupportsComplexOpsTs), f"{arg!r}"


@beartype
def pow_func(arg: SupportsComplexPow):
    assert isinstance(arg, SupportsComplexPow), f"{arg!r}"


@beartype
def pow_func_t(arg: SupportsComplexPowT):
    assert isinstance(arg, SupportsComplexPowTs), f"{arg!r}"


# ---- Tests ---------------------------------------------------------------------------


def test_supports_complex_ops_pow() -> None:
    for good_val in (
        True,
        -273,
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
    ):
        assert isinstance(good_val, SupportsComplexOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexOpsTs), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPow), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPowTs), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"

    for bad_val in ("-273.15",):
        assert not isinstance(bad_val, SupportsComplexOps), f"{bad_val!r}"
        assert not isinstance(bad_val, SupportsComplexOpsTs), f"{bad_val!r}"


def test_supports_complex_ops_pow_beartype() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        True,
        -273,
        -273.15,
        complex(-273.15),
        Fraction(-27315, 100),
        Decimal("-273.15"),
        Numberwang(-273),
        NumberwangDerived(-273),
        NumberwangRegistered(-273),
        Wangernumb(-273.15),
        WangernumbDerived(-273.15),
        WangernumbRegistered(-273.15),
    ):
        ops_func(cast(SupportsComplexOps, good_val))
        ops_func_t(cast(SupportsComplexOpsT, good_val))
        pow_func(cast(SupportsComplexPow, good_val))
        pow_func_t(cast(SupportsComplexPowT, good_val))

    for bad_val in ("-273.15",):
        with pytest.raises(roar.BeartypeException):
            ops_func(cast(SupportsComplexOps, bad_val))

        with pytest.raises(roar.BeartypeException):
            ops_func_t(cast(SupportsComplexOpsT, bad_val))

        with pytest.raises(roar.BeartypeException):
            pow_func(cast(SupportsComplexPow, bad_val))

        with pytest.raises(roar.BeartypeException):
            pow_func_t(cast(SupportsComplexPowT, bad_val))


def test_supports_complex_ops_pow_numpy() -> None:
    numpy = pytest.importorskip("numpy", reason="requires numpy")

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
        assert isinstance(good_val, SupportsComplexOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexOpsTs), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"

        # numpy.uint*.__neg__ means something different than what we're testing for
        if not isinstance(
            good_val,
            (numpy.uint8, numpy.uint16, numpy.uint32, numpy.uint64),
        ):
            assert 0 - good_val == -good_val, f"{good_val!r}"

        assert isinstance(good_val, SupportsComplexPow), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPowTs), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"


def test_supports_complex_ops_pow_numpy_beartype() -> None:
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
        ops_func(cast(SupportsComplexOps, good_val))
        ops_func_t(cast(SupportsComplexOpsT, good_val))
        pow_func(cast(SupportsComplexPow, good_val))
        pow_func_t(cast(SupportsComplexPowT, good_val))


def test_supports_complex_ops_pow_sympy() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        assert isinstance(good_val, SupportsComplexOps), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexOpsTs), f"{good_val!r}"
        assert good_val + 0 == good_val, f"{good_val!r}"
        assert good_val - 0 == good_val, f"{good_val!r}"
        assert good_val * 1 == good_val, f"{good_val!r}"
        assert good_val / 1 == good_val, f"{good_val!r}"
        assert 0 - good_val == -good_val, f"{good_val!r}"

        assert isinstance(good_val, SupportsComplexPow), f"{good_val!r}"
        assert isinstance(good_val, SupportsComplexPowTs), f"{good_val!r}"
        assert good_val ** 1 == good_val, f"{good_val!r}"


def test_supports_complex_ops_pow_sympy_beartype() -> None:
    sympy = pytest.importorskip("sympy", reason="requires numpy")
    pytest.importorskip("beartype.roar", reason="requires beartype")

    for good_val in (
        sympy.Integer(-273),
        sympy.Float(-273.15),
        sympy.Rational(-27315, 100),
        sympy.symbols("x"),
    ):
        ops_func(cast(SupportsComplexOps, good_val))
        ops_func_t(cast(SupportsComplexOpsT, good_val))
        pow_func(cast(SupportsComplexPow, good_val))
        pow_func_t(cast(SupportsComplexPowT, good_val))
