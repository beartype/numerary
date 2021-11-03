# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

import math
import sys
from abc import abstractmethod
from decimal import Decimal
from fractions import Fraction
from numbers import Complex, Integral, Rational, Real
from typing import Any, Dict, Iterable, Optional, Tuple, Type, TypeVar, Union

from .bt import beartype

__all__ = (
    "IntegralLike",
    "IntegralLikeSCU",
    "IntegralLikeSCT",
    "RealLike",
    "RealLikeSCU",
    "RealLikeSCT",
)


# ---- Types ---------------------------------------------------------------------------


_T_co = TypeVar("_T_co", covariant=True)
_TT = TypeVar("_TT", bound="type")

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated  # noqa: F401

if sys.version_info >= (3, 8):
    from typing import Protocol
    from typing import SupportsAbs as _SupportsAbs
    from typing import SupportsComplex as _SupportsComplex
    from typing import SupportsFloat as _SupportsFloat
    from typing import SupportsIndex as _SupportsIndex
    from typing import SupportsInt as _SupportsInt
    from typing import SupportsRound as _SupportsRound
    from typing import runtime_checkable
else:
    from typing_extensions import Protocol, runtime_checkable

    @runtime_checkable
    class _SupportsAbs(Protocol[_T_co]):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __abs__(self) -> _T_co:
            pass

    @runtime_checkable
    class _SupportsComplex(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __complex__(self) -> complex:
            pass

    @runtime_checkable
    class _SupportsFloat(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __float__(self) -> float:
            pass

    @runtime_checkable
    class _SupportsIndex(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __index__(self) -> int:
            pass

    @runtime_checkable
    class _SupportsInt(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __int__(self) -> int:
            pass

    @runtime_checkable
    class _SupportsRound(Protocol[_T_co]):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __round__(self, ndigits: int = 0) -> _T_co:
            pass


_ProtocolMeta: Any = type(Protocol)


class CachingProtocolMeta(_ProtocolMeta):
    """
    Stand-in for ``#!python Protocol``’s base class that caches results of ``#!python
    __instancecheck__``, (which is otherwise [really 🤬ing
    expensive](https://github.com/python/mypy/issues/3186#issuecomment-885718629)).
    (When this was introduced, it resulted in about a 5× performance increase for
    [``dyce``](https://github.com/posita/dyce)’s unit tests, which was the only
    benchmark I had at the time.) The downside is that this will yield unpredictable
    results for objects whose methods don’t stem from any type (e.g., are assembled at
    runtime). I don’t know of any real-world case where that would be true. We’ll jump
    off that bridge when we come to it.
    """

    def __new__(
        mcls: Type[_TT],
        name: str,
        bases: Tuple[Type, ...],
        namespace: Dict[str, Any],
        **kw: Any,
    ) -> _TT:
        # See <https://github.com/python/mypy/issues/9282>
        cls = super().__new__(mcls, name, bases, namespace, **kw)  # type: ignore
        # Prefixing this class member with "_abc_" is necessary to prevent it from being
        # considered part of the Protocol. (See
        # <https://github.com/python/cpython/blob/main/Lib/typing.py>.)
        cache: Dict[Tuple[type, type], bool] = {}
        cls._abc_inst_check_cache = cache

        return cls

    def __instancecheck__(self, inst: Any) -> bool:
        inst_t = type(inst)

        if (self, inst_t) not in self._abc_inst_check_cache:
            self._abc_inst_check_cache[self, inst_t] = super().__instancecheck__(inst)

        return self._abc_inst_check_cache[self, inst_t]


def _assert_isinstance(*num_ts: type, target_t: type) -> None:
    for num_t in num_ts:
        assert isinstance(num_t(0), target_t), f"{num_t!r}, {target_t!r}"


@runtime_checkable
class SupportsAbs(
    _SupportsAbs[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsAbs.__doc__ = _SupportsAbs.__doc__
_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsAbs)
SupportsAbsSCU = Union[int, float, bool, Complex, SupportsAbs]
SupportsAbsSCT = (int, float, bool, Complex, SupportsAbs)
assert SupportsAbsSCU.__args__ == SupportsAbsSCT  # type: ignore


@runtime_checkable
class SupportsComplex(
    _SupportsComplex,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsComplex.__doc__ = _SupportsComplex.__doc__
_assert_isinstance(Decimal, Fraction, target_t=SupportsComplex)
SupportsComplexSCU = Union[Complex, SupportsComplex]
SupportsComplexSCT = (Complex, SupportsComplex)
assert SupportsComplexSCU.__args__ == SupportsComplexSCT  # type: ignore


@runtime_checkable
class SupportsFloat(
    _SupportsFloat,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsFloat.__doc__ = _SupportsFloat.__doc__
_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsFloat)
SupportsFloatSCU = Union[int, float, bool, Real, SupportsFloat]
SupportsFloatSCT = (int, float, bool, Real, SupportsFloat)
assert SupportsFloatSCU.__args__ == SupportsFloatSCT  # type: ignore


@runtime_checkable
class SupportsInt(
    _SupportsInt,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsInt.__doc__ = _SupportsInt.__doc__
_assert_isinstance(int, float, bool, target_t=SupportsInt)
SupportsIntSCU = Union[int, float, bool, Integral, SupportsInt]
SupportsIntSCT = (int, float, bool, Integral, SupportsInt)
assert SupportsIntSCU.__args__ == SupportsIntSCT  # type: ignore


@runtime_checkable
class SupportsIndex(
    _SupportsIndex,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsIndex.__doc__ = _SupportsIndex.__doc__
_assert_isinstance(int, bool, target_t=SupportsIndex)
SupportsIndexSCU = Union[int, bool, Integral, SupportsIndex]
SupportsIndexSCT = (int, bool, Integral, SupportsIndex)
assert SupportsIndexSCU.__args__ == SupportsIndexSCT  # type: ignore


@runtime_checkable
class SupportsRound(
    _SupportsRound[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsRound.__doc__ = _SupportsRound.__doc__
_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRound)
SupportsRoundSCU = Union[int, float, bool, Real, SupportsRound]
SupportsRoundSCT = (int, float, bool, Real, SupportsRound)
assert SupportsRoundSCU.__args__ == SupportsRoundSCT  # type: ignore


@runtime_checkable
class SupportsConjugate(
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def conjugate(self) -> Any:
        pass


_assert_isinstance(
    int, float, bool, complex, Decimal, Fraction, target_t=SupportsConjugate
)
SupportsConjugateSCU = Union[int, float, bool, complex, Complex, SupportsConjugate]
SupportsConjugateSCT = (int, float, bool, complex, Complex, SupportsConjugate)
assert SupportsConjugateSCU.__args__ == SupportsConjugateSCT  # type: ignore


@runtime_checkable
class SupportsRealImag(
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @property
    def real(self) -> Any:
        pass

    @property
    def imag(self) -> Any:
        pass


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRealImag)
SupportsRealImagSCU = Union[int, float, bool, Complex, SupportsRealImag]
SupportsRealImagSCT = (int, float, bool, Complex, SupportsRealImag)
assert SupportsRealImagSCU.__args__ == SupportsRealImagSCT  # type: ignore


@runtime_checkable
class SupportsTrunc(
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __trunc__(self) -> int:
        pass


_assert_isinstance(int, bool, float, Decimal, Fraction, target_t=SupportsTrunc)
SupportsTruncSCU = Union[int, float, bool, Real, SupportsTrunc]
SupportsTruncSCT = (int, float, bool, Real, SupportsTrunc)
assert SupportsTruncSCU.__args__ == SupportsTruncSCT  # type: ignore


@runtime_checkable
class SupportsFloor(
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __floor__(self) -> int:
        pass


_assert_isinstance(int, bool, Decimal, Fraction, target_t=SupportsFloor)

if sys.version_info >= (3, 9):
    _assert_isinstance(float, target_t=SupportsFloor)

SupportsFloorSCU = Union[int, float, bool, Real, SupportsFloor]
SupportsFloorSCT = (int, float, bool, Real, SupportsFloor)
assert SupportsFloorSCU.__args__ == SupportsFloorSCT  # type: ignore


@runtime_checkable
class SupportsCeil(
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __ceil__(self) -> int:
        pass


_assert_isinstance(int, bool, Decimal, Fraction, target_t=SupportsCeil)

if sys.version_info >= (3, 9):
    _assert_isinstance(float, target_t=SupportsCeil)

SupportsCeilSCU = Union[int, float, bool, Real, SupportsCeil]
SupportsCeilSCT = (int, float, bool, Real, SupportsCeil)
assert SupportsCeilSCU.__args__ == SupportsCeilSCT  # type: ignore


@runtime_checkable
class SupportsDivmod(
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __divmod__(self, other: Any) -> Tuple[_T_co, _T_co]:
        pass

    @abstractmethod
    def __rdivmod__(self, other: Any) -> Tuple[_T_co, _T_co]:
        pass


_assert_isinstance(int, bool, float, Decimal, Fraction, target_t=SupportsDivmod)
SupportsDivmodSCU = Union[int, float, bool, Real, SupportsDivmod]
SupportsDivmodSCT = (int, float, bool, Real, SupportsDivmod)
assert SupportsDivmodSCU.__args__ == SupportsDivmodSCT  # type: ignore


@runtime_checkable
class SupportsNumeratorDenominatorProperties(
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @property
    def numerator(self) -> int:
        pass

    @property
    def denominator(self) -> int:
        pass


_assert_isinstance(int, bool, Fraction, target_t=SupportsNumeratorDenominatorProperties)
SupportsNumeratorDenominatorPropertiesSCU = Union[
    int,
    bool,
    Rational,
    SupportsNumeratorDenominatorProperties,
]
SupportsNumeratorDenominatorPropertiesSCT = (
    int,
    bool,
    Rational,
    SupportsNumeratorDenominatorProperties,
)
assert SupportsNumeratorDenominatorPropertiesSCU.__args__ == SupportsNumeratorDenominatorPropertiesSCT  # type: ignore


@runtime_checkable
class SupportsNumeratorDenominatorMethods(
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def numerator(self) -> SupportsInt:
        pass

    @abstractmethod
    def denominator(self) -> SupportsInt:
        pass


SupportsNumeratorDenominatorMixedU = Union[
    SupportsNumeratorDenominatorProperties,
    SupportsNumeratorDenominatorMethods,
]
SupportsNumeratorDenominatorMixedT = (
    SupportsNumeratorDenominatorProperties,
    SupportsNumeratorDenominatorMethods,
)
assert SupportsNumeratorDenominatorMixedU.__args__ == SupportsNumeratorDenominatorMixedT  # type: ignore

SupportsNumeratorDenominatorMixedSCU = Union[
    SupportsNumeratorDenominatorPropertiesSCU,
    SupportsNumeratorDenominatorMethods,
]
SupportsNumeratorDenominatorMixedSCT = SupportsNumeratorDenominatorPropertiesSCT + (
    SupportsNumeratorDenominatorMethods,
)
assert SupportsNumeratorDenominatorMixedSCU.__args__ == SupportsNumeratorDenominatorMixedSCT  # type: ignore


@runtime_checkable
class SupportsComplexOps(
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __add__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __radd__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __sub__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rsub__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __mul__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rmul__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __truediv__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rtruediv__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __neg__(self) -> _T_co:
        pass

    @abstractmethod
    def __pos__(self) -> _T_co:
        pass


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsComplexOps)
SupportsComplexOpsSCU = Union[int, float, bool, Complex, SupportsComplexOps]
SupportsComplexOpsSCT = (int, float, bool, Complex, SupportsComplexOps)
assert SupportsComplexOpsSCU.__args__ == SupportsComplexOpsSCT  # type: ignore


@runtime_checkable
class SupportsComplexPow(
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __pow__(self, exponent: Any) -> _T_co:
        pass

    @abstractmethod
    def __rpow__(self, exponent: Any) -> _T_co:
        pass


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsComplexPow)
SupportsComplexPowSCU = Union[int, float, bool, Complex, SupportsComplexPow]
SupportsComplexPowSCT = (int, float, bool, Complex, SupportsComplexPow)
assert SupportsComplexPowSCU.__args__ == SupportsComplexPowSCT  # type: ignore


@runtime_checkable
class SupportsRealOps(
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __lt__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __le__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __ge__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __gt__(self, other: Any) -> bool:
        pass

    @abstractmethod
    def __floordiv__(self, other: Any) -> Any:  # TODO(posita): should be int
        pass

    @abstractmethod
    def __rfloordiv__(self, other: Any) -> Any:  # TODO(posita): should be int
        pass

    @abstractmethod
    def __mod__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rmod__(self, other: Any) -> _T_co:
        pass


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRealOps)
SupportsRealOpsSCU = Union[int, float, bool, Real, SupportsRealOps]
SupportsRealOpsSCT = (int, float, bool, Real, SupportsRealOps)
assert SupportsRealOpsSCU.__args__ == SupportsRealOpsSCT  # type: ignore


@runtime_checkable
class SupportsIntegralOps(
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __lshift__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rlshift__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rshift__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rrshift__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __and__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rand__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __xor__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __rxor__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __or__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __ror__(self, other: Any) -> _T_co:
        pass

    @abstractmethod
    def __invert__(self) -> _T_co:
        pass


_assert_isinstance(int, bool, target_t=SupportsIntegralOps)
SupportsIntegralOpsSCU = Union[int, bool, Integral, SupportsIntegralOps]
SupportsIntegralOpsSCT = (int, bool, Integral, SupportsIntegralOps)
assert SupportsIntegralOpsSCU.__args__ == SupportsIntegralOpsSCT  # type: ignore


@runtime_checkable
class SupportsIntegralPow(
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __pow__(self, exponent: Any, modulus: Optional[Any] = None) -> _T_co:
        pass

    @abstractmethod
    def __rpow__(self, exponent: Any, modulus: Optional[Any] = None) -> _T_co:
        pass


_assert_isinstance(int, bool, target_t=SupportsIntegralPow)
SupportsIntegralPowSCU = Union[int, bool, Integral, SupportsIntegralPow]
SupportsIntegralPowSCT = (int, bool, Integral, SupportsIntegralPow)
assert SupportsIntegralPowSCU.__args__ == SupportsIntegralPowSCT  # type: ignore


@runtime_checkable
class RealLike(
    SupportsAbs[_T_co],
    SupportsFloat,
    SupportsRealOps[_T_co],
    SupportsComplexOps[_T_co],
    SupportsComplexPow[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    # Must be able to instantiate it
    @abstractmethod
    def __init__(self, *args: Any, **kw: Any):
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=RealLike)
RealLikeSCU = Union[int, float, bool, Real, RealLike]
RealLikeSCT = (int, float, bool, Real, RealLike)
assert RealLikeSCU.__args__ == RealLikeSCT  # type: ignore


@runtime_checkable
class RationalLikeProperties(
    SupportsAbs[_T_co],
    SupportsFloat,
    SupportsNumeratorDenominatorProperties,
    SupportsRealOps[_T_co],
    SupportsComplexOps[_T_co],
    SupportsComplexPow[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    # Must be able to instantiate it
    @abstractmethod
    def __init__(self, *args: Any, **kw: Any):
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


_assert_isinstance(int, bool, Fraction, target_t=RationalLikeProperties)
RationalLikePropertiesSCU = Union[
    int,
    bool,
    Rational,
    RationalLikeProperties,
]
RationalLikePropertiesSCT = (
    int,
    bool,
    Rational,
    RationalLikeProperties,
)
assert RationalLikePropertiesSCU.__args__ == RationalLikePropertiesSCT  # type: ignore


@runtime_checkable
class RationalLikeMethods(
    SupportsAbs[_T_co],
    SupportsFloat,
    SupportsNumeratorDenominatorMethods,
    SupportsRealOps[_T_co],
    SupportsComplexOps[_T_co],
    SupportsComplexPow[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    # Must be able to instantiate it
    @abstractmethod
    def __init__(self, *args: Any, **kw: Any):
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


RationalLikeMixedU = Union[RationalLikeProperties, RationalLikeMethods]
RationalLikeMixedT = (RationalLikeProperties, RationalLikeMethods)
RationalLikeMixedSCU = Union[
    RationalLikePropertiesSCU,
    RationalLikeMethods,
]
RationalLikeMixedSCT = RationalLikePropertiesSCT + (RationalLikeMethods,)
assert RationalLikeMixedSCU.__args__ == RationalLikeMixedSCT  # type: ignore


@runtime_checkable
class IntegralLike(
    SupportsAbs[_T_co],
    SupportsFloat,
    SupportsIndex,
    SupportsInt,
    SupportsIntegralOps[_T_co],
    SupportsIntegralPow[_T_co],
    SupportsRealOps[_T_co],
    SupportsComplexOps[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    # Must be able to instantiate it
    @abstractmethod
    def __init__(self, *args: Any, **kw: Any):
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


_assert_isinstance(int, bool, target_t=IntegralLike)
IntegralLikeSCU = Union[int, bool, Integral, IntegralLike]
IntegralLikeSCT = (int, bool, Integral, IntegralLike)
assert IntegralLikeSCU.__args__ == IntegralLikeSCT  # type: ignore


# ---- Functions -----------------------------------------------------------------------


@beartype
def ceil(operand: SupportsCeil):
    r"""
    TODO(posita): Document this!
    """
    assert isinstance(operand, SupportsFloat)

    return math.ceil(operand)


@beartype
def floor(operand: SupportsFloor):
    r"""
    TODO(posita): Document this!
    """
    assert isinstance(operand, SupportsFloat)

    return math.floor(operand)


@beartype
def trunc(operand: SupportsTrunc):
    r"""
    TODO(posita): Document this!
    """
    assert isinstance(operand, SupportsFloat)

    return math.trunc(operand)


@beartype
def numerator(operand: SupportsNumeratorDenominatorMixedU):
    r"""
    TODO(posita): Document this!
    """
    if hasattr(operand, "numerator"):
        if callable(operand.numerator):
            return operand.numerator()
        else:
            return operand.numerator
    else:
        raise TypeError(f"{operand!r} has no numerator")


@beartype
def denominator(operand: SupportsNumeratorDenominatorMixedU):
    r"""
    TODO(posita): Document this!
    """
    if hasattr(operand, "denominator"):
        if callable(operand.denominator):
            return operand.denominator()
        else:
            return operand.denominator
    else:
        raise TypeError(f"{operand!r} has no denominator")
