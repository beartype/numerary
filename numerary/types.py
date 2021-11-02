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
    "IntegralLikeT",
    "IntegralLikeTs",
    "RationalLike",
    "RationalLikeT",
    "RationalLikeTs",
    "RealLike",
    "RealLikeT",
    "RealLikeTs",
    "denominator",
    "numerator",
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
            ...

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
            ...

    @runtime_checkable
    class _SupportsIndex(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __index__(self) -> int:
            ...

    @runtime_checkable
    class _SupportsInt(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __int__(self) -> int:
            ...

    @runtime_checkable
    class _SupportsRound(Protocol[_T_co]):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __round__(self, ndigits: int = 0) -> _T_co:
            ...


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
SupportsAbsT = Union[int, float, bool, Complex, SupportsAbs]
SupportsAbsTs = (int, float, bool, Complex, SupportsAbs)
assert SupportsAbsT.__args__ == SupportsAbsTs  # type: ignore


@runtime_checkable
class SupportsComplex(
    _SupportsComplex,
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsComplex.__doc__ = _SupportsComplex.__doc__
_assert_isinstance(Decimal, Fraction, target_t=SupportsComplex)
SupportsComplexT = Union[Complex, SupportsComplex]
SupportsComplexTs = (Complex, SupportsComplex)
assert SupportsComplexT.__args__ == SupportsComplexTs  # type: ignore


@runtime_checkable
class SupportsFloat(
    _SupportsFloat,
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsFloat.__doc__ = _SupportsFloat.__doc__
_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsFloat)
SupportsFloatT = Union[int, float, bool, Real, SupportsFloat]
SupportsFloatTs = (int, float, bool, Real, SupportsFloat)
assert SupportsFloatT.__args__ == SupportsFloatTs  # type: ignore


@runtime_checkable
class SupportsInt(
    _SupportsInt,
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsInt.__doc__ = _SupportsInt.__doc__
_assert_isinstance(int, float, bool, target_t=SupportsInt)
SupportsIntT = Union[int, float, bool, Integral, SupportsInt]
SupportsIntTs = (int, float, bool, Integral, SupportsInt)
assert SupportsIntT.__args__ == SupportsIntTs  # type: ignore


@runtime_checkable
class SupportsIndex(
    _SupportsIndex,
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsIndex.__doc__ = _SupportsIndex.__doc__
_assert_isinstance(int, bool, target_t=SupportsIndex)
SupportsIndexT = Union[int, bool, Integral, SupportsIndex]
SupportsIndexTs = (int, bool, Integral, SupportsIndex)
assert SupportsIndexT.__args__ == SupportsIndexTs  # type: ignore


@runtime_checkable
class SupportsRound(
    _SupportsRound,
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    __slots__: Union[str, Iterable[str]] = ()


SupportsRound.__doc__ = _SupportsRound.__doc__
_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRound)
SupportsRoundT = Union[int, float, bool, Real, SupportsRound]
SupportsRoundTs = (int, float, bool, Real, SupportsRound)
assert SupportsRoundT.__args__ == SupportsRoundTs  # type: ignore


@runtime_checkable
class SupportsConjugate(Protocol[_T_co], metaclass=CachingProtocolMeta):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def conjugate(self) -> Any:
        ...


_assert_isinstance(
    int, float, bool, complex, Decimal, Fraction, target_t=SupportsConjugate
)
SupportsConjugateT = Union[int, float, bool, complex, Complex, SupportsConjugate]
SupportsConjugateTs = (int, float, bool, complex, Complex, SupportsConjugate)
assert SupportsConjugateT.__args__ == SupportsConjugateTs  # type: ignore


@runtime_checkable
class SupportsRealImag(Protocol[_T_co], metaclass=CachingProtocolMeta):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @property
    def real(self) -> Any:
        ...

    @property
    def imag(self) -> Any:
        ...


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRealImag)
SupportsRealImagT = Union[int, float, bool, Complex, SupportsRealImag]
SupportsRealImagTs = (int, float, bool, Complex, SupportsRealImag)
assert SupportsRealImagT.__args__ == SupportsRealImagTs  # type: ignore


@runtime_checkable
class SupportsTrunc(Protocol[_T_co], metaclass=CachingProtocolMeta):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __trunc__(self) -> int:
        ...


_assert_isinstance(int, bool, float, Decimal, Fraction, target_t=SupportsTrunc)
SupportsTruncT = Union[int, float, bool, Real, SupportsTrunc]
SupportsTruncTs = (int, float, bool, Real, SupportsTrunc)
assert SupportsTruncT.__args__ == SupportsTruncTs  # type: ignore


@runtime_checkable
class SupportsFloor(Protocol[_T_co], metaclass=CachingProtocolMeta):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __floor__(self) -> int:
        ...


_assert_isinstance(int, bool, Decimal, Fraction, target_t=SupportsFloor)

if sys.version_info >= (3, 9):
    _assert_isinstance(float, target_t=SupportsFloor)

SupportsFloorT = Union[int, float, bool, Real, SupportsFloor]
SupportsFloorTs = (int, float, bool, Real, SupportsFloor)
assert SupportsFloorT.__args__ == SupportsFloorTs  # type: ignore


@runtime_checkable
class SupportsCeil(Protocol[_T_co], metaclass=CachingProtocolMeta):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __ceil__(self) -> int:
        ...


_assert_isinstance(int, bool, Decimal, Fraction, target_t=SupportsCeil)

if sys.version_info >= (3, 9):
    _assert_isinstance(float, target_t=SupportsCeil)

SupportsCeilT = Union[int, float, bool, Real, SupportsCeil]
SupportsCeilTs = (int, float, bool, Real, SupportsCeil)
assert SupportsCeilT.__args__ == SupportsCeilTs  # type: ignore


@runtime_checkable
class SupportsDivmod(Protocol[_T_co], metaclass=CachingProtocolMeta):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __divmod__(self, other: Any) -> Tuple[_T_co, _T_co]:
        ...

    @abstractmethod
    def __rdivmod__(self, other: Any) -> Tuple[_T_co, _T_co]:
        ...


_assert_isinstance(int, bool, float, Decimal, Fraction, target_t=SupportsDivmod)
SupportsDivmodT = Union[int, float, bool, Real, SupportsDivmod]
SupportsDivmodTs = (int, float, bool, Real, SupportsDivmod)
assert SupportsDivmodT.__args__ == SupportsDivmodTs  # type: ignore


@runtime_checkable
class SupportsNumeratorDenominator(Protocol[_T_co], metaclass=CachingProtocolMeta):
    r"""
    TODO(posita): Document this!
    """
    __slots__: Union[str, Iterable[str]] = ()

    @property
    def numerator(self) -> int:
        ...

    @property
    def denominator(self) -> int:
        ...


_assert_isinstance(int, bool, Fraction, target_t=SupportsNumeratorDenominator)
SupportsNumeratorDenominatorT = Union[int, bool, Rational, SupportsNumeratorDenominator]
SupportsNumeratorDenominatorTs = (int, bool, Rational, SupportsNumeratorDenominator)
assert SupportsNumeratorDenominatorT.__args__ == SupportsNumeratorDenominatorTs  # type: ignore


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
        ...

    @abstractmethod
    def __radd__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __sub__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rsub__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __mul__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rmul__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __truediv__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rtruediv__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __neg__(self) -> _T_co:
        ...

    @abstractmethod
    def __pos__(self) -> _T_co:
        ...


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsComplexOps)
SupportsComplexOpsT = Union[int, float, bool, Complex, SupportsComplexOps]
SupportsComplexOpsTs = (int, float, bool, Complex, SupportsComplexOps)
assert SupportsComplexOpsT.__args__ == SupportsComplexOpsTs  # type: ignore


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
        ...

    @abstractmethod
    def __rpow__(self, exponent: Any) -> _T_co:
        ...


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsComplexPow)
SupportsComplexPowT = Union[int, float, bool, Complex, SupportsComplexPow]
SupportsComplexPowTs = (int, float, bool, Complex, SupportsComplexPow)
assert SupportsComplexPowT.__args__ == SupportsComplexPowTs  # type: ignore


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
        ...

    @abstractmethod
    def __le__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __ge__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __gt__(self, other: Any) -> bool:
        ...

    @abstractmethod
    def __floordiv__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rfloordiv__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __mod__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rmod__(self, other: Any) -> _T_co:
        ...


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRealOps)
SupportsRealOpsT = Union[int, float, bool, Real, SupportsRealOps]
SupportsRealOpsTs = (int, float, bool, Real, SupportsRealOps)
assert SupportsRealOpsT.__args__ == SupportsRealOpsTs  # type: ignore


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
        ...

    @abstractmethod
    def __rlshift__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rshift__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rrshift__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __and__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rand__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __xor__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __rxor__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __or__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __ror__(self, other: Any) -> _T_co:
        ...

    @abstractmethod
    def __invert__(self) -> _T_co:
        ...


_assert_isinstance(int, bool, target_t=SupportsIntegralOps)
SupportsIntegralOpsT = Union[int, bool, Integral, SupportsIntegralOps]
SupportsIntegralOpsTs = (int, bool, Integral, SupportsIntegralOps)
assert SupportsIntegralOpsT.__args__ == SupportsIntegralOpsTs  # type: ignore


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
        ...

    @abstractmethod
    def __rpow__(self, exponent: Any, modulus: Optional[Any] = None) -> _T_co:
        ...


_assert_isinstance(int, bool, target_t=SupportsIntegralPow)
SupportsIntegralPowT = Union[int, bool, Integral, SupportsIntegralPow]
SupportsIntegralPowTs = (int, bool, Integral, SupportsIntegralPow)
assert SupportsIntegralPowT.__args__ == SupportsIntegralPowTs  # type: ignore


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
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=RealLike)
RealLikeT = Union[int, float, bool, Real, RealLike]
RealLikeTs = (int, float, bool, Real, RealLike)
assert RealLikeT.__args__ == RealLikeTs  # type: ignore


@runtime_checkable
class RationalLike(
    SupportsAbs[_T_co],
    SupportsFloat,
    SupportsNumeratorDenominator[_T_co],
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
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...


_assert_isinstance(int, bool, Fraction, target_t=RationalLike)
RationalLikeT = Union[
    int,
    bool,
    Rational,
    RationalLike,
]
RationalLikeTs = (
    int,
    bool,
    Rational,
    RationalLike,
)
assert RationalLikeT.__args__ == RationalLikeTs  # type: ignore


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
        ...

    @abstractmethod
    def __hash__(self) -> int:
        ...


_assert_isinstance(int, bool, target_t=IntegralLike)
IntegralLikeT = Union[int, bool, Integral, IntegralLike]
IntegralLikeTs = (int, bool, Integral, IntegralLike)
assert IntegralLikeT.__args__ == IntegralLikeTs  # type: ignore


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
def numerator(operand: SupportsNumeratorDenominator):
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
def denominator(operand: SupportsNumeratorDenominator):
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
