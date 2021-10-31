# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

import math
import operator
from typing import Callable, Tuple, TypeVar

from .numberwang import (
    Numberwang,
    NumberwangDerived,
    NumberwangRegistered,
    Wangernumb,
    WangernumbDerived,
    WangernumbRegistered,
)

__all__ = ()


# ---- Types ---------------------------------------------------------------------------


_T_co = TypeVar("_T_co", covariant=True)
_UnaryOperatorT = Callable[[_T_co], _T_co]
_BinaryOperatorT = Callable[[_T_co, _T_co], _T_co]


# ---- Data ----------------------------------------------------------------------------


BINOPS_REAL: Tuple[_BinaryOperatorT, ...] = (
    operator.__add__,
    operator.__eq__,
    operator.__floordiv__,
    operator.__ge__,
    operator.__gt__,
    operator.__le__,
    operator.__lt__,
    operator.__mod__,
    operator.__mul__,
    operator.__ne__,
    operator.__pow__,
    operator.__sub__,
    operator.__truediv__,
)

BINOPS_INTEGRAL: Tuple[_BinaryOperatorT, ...] = (
    operator.__and__,
    operator.__lshift__,
    operator.__or__,
    operator.__rshift__,
    operator.__xor__,
)

UNOPS_REAL: Tuple[_UnaryOperatorT, ...] = (
    int,
    round,
    math.ceil,
    math.floor,
    math.trunc,
    operator.__abs__,
    operator.__neg__,
    operator.__pos__,
)

UNOPS_REAL_DERIVED: Tuple[_UnaryOperatorT, ...] = UNOPS_REAL + (
    complex,
    float,
)

UNOPS_INTEGRAL: Tuple[_UnaryOperatorT, ...] = (operator.__invert__,)

UNOPS_INTEGRAL_DERIVED: Tuple[_UnaryOperatorT, ...] = UNOPS_INTEGRAL + (
    operator.__index__,
)

# ---- Tests ---------------------------------------------------------------------------


def test_numberwang_binops() -> None:
    for binop in BINOPS_REAL + BINOPS_INTEGRAL:
        assert binop(Numberwang(-273), Numberwang(42)) == binop(
            -273, 42
        ), f"op: {binop}"


def test_numberwang_unops() -> None:
    for unop in UNOPS_REAL + UNOPS_INTEGRAL:
        assert unop(Numberwang(-273)) == unop(-273), f"op: {unop}"


def test_numberwang_registered_binops() -> None:
    for binop in BINOPS_REAL + BINOPS_INTEGRAL:
        assert binop(NumberwangRegistered(-273), NumberwangRegistered(42)) == binop(
            -273, 42
        ), f"op: {binop}"


def test_numberwang_registered_unops() -> None:
    for unop in UNOPS_REAL + UNOPS_INTEGRAL:
        assert unop(NumberwangRegistered(-273)) == unop(-273), f"op: {unop}"


def test_numberwang_derived_binops() -> None:
    for binop in BINOPS_REAL + BINOPS_INTEGRAL:
        assert binop(NumberwangDerived(-273), NumberwangDerived(42)) == binop(
            -273, 42
        ), f"op: {binop}"


def test_numberwang_derived_unops() -> None:
    for unop in UNOPS_REAL_DERIVED + UNOPS_INTEGRAL_DERIVED:
        assert unop(NumberwangDerived(-273)) == unop(-273), f"op: {unop}"


def test_wangernum_binops() -> None:
    for binop in BINOPS_REAL:
        assert binop(Wangernumb(-273.15), Wangernumb(1.618)) == binop(
            -273.15, 1.618
        ), f"op: {binop}"


def test_wangernum_unops() -> None:
    for unop in UNOPS_REAL:
        assert unop(Wangernumb(-273.15)) == unop(-273.15), f"op: {unop}"


def test_wangernum_registered_binops() -> None:
    for binop in BINOPS_REAL:
        assert binop(
            WangernumbRegistered(-273.15), WangernumbRegistered(1.618)
        ) == binop(-273.15, 1.618), f"op: {binop}"


def test_wangernum_registered_unops() -> None:
    for unop in UNOPS_REAL:
        assert unop(WangernumbRegistered(-273.15)) == unop(-273.15), f"op: {unop}"


def test_wangernum_derived_binops() -> None:
    for binop in BINOPS_REAL:
        assert binop(WangernumbDerived(-273.15), WangernumbDerived(1.618)) == binop(
            -273.15, 1.618
        ), f"op: {binop}"


def test_wangernum_derived_unops() -> None:
    for unop in UNOPS_REAL_DERIVED:
        assert unop(WangernumbDerived(-273.15)) == unop(-273.15), f"op: {unop}"
