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
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

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
    from typing import _get_protocol_attrs  # type: ignore [attr-defined]
    from typing import Protocol
    from typing import SupportsAbs as _SupportsAbs
    from typing import SupportsComplex as _SupportsComplex
    from typing import SupportsFloat as _SupportsFloat
    from typing import SupportsIndex as _SupportsIndex
    from typing import SupportsInt as _SupportsInt
    from typing import SupportsRound as _SupportsRound
    from typing import runtime_checkable
else:
    from typing_extensions import Protocol, _get_protocol_attrs, runtime_checkable

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


def _bases_pass_muster_gen(cls: CachingProtocolMeta, inst: Any) -> Iterator[bool]:
    for base in cls.__bases__:
        if base is cls or base.__name__ in ("Protocol", "Generic", "object"):
            continue

        yield isinstance(inst, base)


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
        cls = super().__new__(mcls, name, bases, namespace, **kw)  # type: ignore [misc]
        # Prefixing this class member with "_abc_" is necessary to prevent it from being
        # considered part of the Protocol. (See
        # <https://github.com/python/cpython/blob/main/Lib/typing.py>.)
        cache: Dict[Type, bool] = {}
        cls._abc_inst_check_cache = cache
        overridden: Dict[Type, bool] = {}
        cls._abc_inst_check_cache_overridden = overridden
        listeners: Set[CachingProtocolMeta] = set()
        cls._abc_inst_check_cache_listeners = listeners

        for base in bases:
            if hasattr(base, "_abc_inst_check_cache_listeners"):
                base._abc_inst_check_cache_listeners.add(cls)

        return cls

    def __instancecheck__(cls, inst: Any) -> bool:
        # This has to stay *super* tight! Even adding a mere assertion can add ~50% to
        # the best case runtime!
        inst_t = type(inst)

        if inst_t not in cls._abc_inst_check_cache:
            # If you're going to do *anything*, do it here. Don't touch the rest of this
            # method if you can avoid it.
            cls._abc_inst_check_cache[inst_t] = all(
                _bases_pass_muster_gen(cls, inst)
            ) and cls._check_only_my_attrs(inst)
            cls._abc_inst_check_cache_overridden[inst_t] = False

        return cls._abc_inst_check_cache[inst_t]

    def includes(cls, inst_t: Type) -> None:
        r"""
        Registers *inst_t* as supporting the interface in the runtime type-checking cache.
        This overrides any prior cached value.

        ``` python
        >>> from abc import abstractmethod
        >>> from numerary.types import CachingProtocolMeta, Protocol, runtime_checkable
        >>> @runtime_checkable
        ... class SupportsSpam(
        ...   Protocol,
        ...   metaclass=CachingProtocolMeta
        ... ):
        ...   @abstractmethod
        ...   def spam(self) -> str: pass
        >>> class NoSpam: pass
        >>> isinstance(NoSpam(), SupportsSpam)
        False
        >>> SupportsSpam.includes(NoSpam)
        >>> isinstance(NoSpam(), SupportsSpam)
        True

        ```

        !!! note

            This does not affect static type-checking.

            ``` python
            >>> my_spam: SupportsSpam = NoSpam()  # type: ignore [assignment]  # still generates a Mypy warning

            ```
        """
        cls._abc_inst_check_cache[inst_t] = True
        cls._abc_inst_check_cache_overridden[inst_t] = True
        cls._dirty_for(inst_t)

    def excludes(cls, inst_t: Type) -> None:
        r"""
        Registers *inst_t* as supporting the interface in the runtime type-checking cache.
        This overrides any prior cached value.

        ``` python
        >>> from abc import abstractmethod
        >>> from numerary.types import CachingProtocolMeta, Protocol, runtime_checkable
        >>> @runtime_checkable
        ... class SupportsHam(
        ...   Protocol,
        ...   metaclass=CachingProtocolMeta
        ... ):
        ...   @abstractmethod
        ...   def ham(self) -> str: pass
        >>> class NoHam:
        ...   def ham(self) -> str:
        ...     raise NotImplementedError
        >>> isinstance(NoHam(), SupportsHam)
        True
        >>> SupportsHam.excludes(NoHam)
        >>> isinstance(NoHam(), SupportsHam)
        False

        ```

        !!! note

            This does not affect static type-checking.

            ``` python
            >>> my_ham: SupportsHam = NoHam()  # does *not* generate a Mypy warning

            ```
        """
        cls._abc_inst_check_cache[inst_t] = False
        cls._abc_inst_check_cache_overridden[inst_t] = True
        cls._dirty_for(inst_t)

    def reset_for(cls, inst_t: Type) -> None:
        r"""
        Clears any cached instance check for *inst_t*.
        """
        if inst_t in cls._abc_inst_check_cache:
            del cls._abc_inst_check_cache[inst_t]
            del cls._abc_inst_check_cache_overridden[inst_t]
            cls._dirty_for(inst_t)

    def _check_only_my_attrs(cls, inst: Any) -> bool:
        attrs = set(cls.__dict__)
        attrs.update(cls.__dict__.get("__annotations__", {}))
        attrs.intersection_update(_get_protocol_attrs(cls))

        for attr in attrs:
            if not hasattr(inst, attr):
                return False
            elif callable(getattr(cls, attr, None)) and getattr(inst, attr) is None:
                return False

        return True

    def _dirty_for(cls, inst_t: Type) -> None:
        for inheriting_cls in cls._abc_inst_check_cache_listeners:
            if (
                inst_t in inheriting_cls._abc_inst_check_cache
                and not inheriting_cls._abc_inst_check_cache_overridden[inst_t]
            ):
                del inheriting_cls._abc_inst_check_cache[inst_t]
                del inheriting_cls._abc_inst_check_cache_overridden[inst_t]


def _assert_isinstance(*num_ts: type, target_t: type) -> None:
    for num_t in num_ts:
        assert isinstance(num_t(0), target_t), f"{num_t!r}, {target_t!r}"


@runtime_checkable
class SupportsAbs(
    _SupportsAbs[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching version of the ``#!python typing.SupportsAbs`` ABC defining the
    [``__abs__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__abs__) with a
    covariant return value.
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsAbs)
SupportsAbsSCU = Union[int, float, bool, Complex, SupportsAbs]
SupportsAbsSCT = SupportsAbs


@runtime_checkable
class SupportsComplex(
    _SupportsComplex,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching version of the ``#!python typing.SupportsComplex`` ABC defining the
    [``__complex__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__complex__).
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(Decimal, Fraction, target_t=SupportsComplex)
SupportsComplexSCU = Union[Complex, SupportsComplex]
SupportsComplexSCT = SupportsComplex


@runtime_checkable
class SupportsFloat(
    _SupportsFloat,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching version of the ``#!python typing.SupportsFloat`` ABC defining the
    [``__float__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__float__).
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsFloat)
SupportsFloatSCU = Union[int, float, bool, Real, SupportsFloat]
SupportsFloatSCT = SupportsFloat


@runtime_checkable
class SupportsInt(
    _SupportsInt,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching version of the ``#!python typing.SupportsInt`` ABC defining the
    [``__int__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__int__).
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, target_t=SupportsInt)
SupportsIntSCU = Union[int, float, bool, Integral, SupportsInt]
SupportsIntSCT = SupportsInt


@runtime_checkable
class SupportsIndex(
    _SupportsIndex,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching version of the ``#!python typing.SupportsIndex`` ABC defining the
    [``__index__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__index__).
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, target_t=SupportsIndex)
SupportsIndexSCU = Union[int, bool, Integral, SupportsIndex]
SupportsIndexSCT = SupportsIndex


@runtime_checkable
class SupportsRound(
    _SupportsRound[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching version of the ``#!python typing.SupportsRound`` ABC defining the
    [``__round__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__round__) with a
    covariant return value.
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRound)
SupportsRoundSCU = Union[int, float, bool, Real, SupportsRound]
SupportsRoundSCT = SupportsRound


@runtime_checkable
class _SupportsConjugate(Protocol):
    r"""
    The raw, non-caching version of
    [``SupportsConjugate``][numerary.types.SupportsConjugate].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def conjugate(self) -> Any:
        pass


@runtime_checkable
class SupportsConjugate(
    _SupportsConjugate,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the [``conjugate``
    method](https://docs.python.org/3/library/numbers.html#numbers.Complex.conjugate).

    ([``_SupportsConjugate``][numerary.types._SupportsConjugate] is the raw, non-caching
    version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(
    int, float, bool, complex, Decimal, Fraction, target_t=SupportsConjugate
)
SupportsConjugateSCU = Union[int, float, bool, complex, Complex, SupportsConjugate]
SupportsConjugateSCT = SupportsConjugate


@runtime_checkable
class _SupportsRealImag(Protocol):
    r"""
    The raw, non-caching version of
    [``SupportsRealImag``][numerary.types.SupportsRealImag].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @property
    def real(self) -> Any:
        pass

    @property
    def imag(self) -> Any:
        pass


@runtime_checkable
class SupportsRealImag(
    _SupportsRealImag,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the
    [``real``](https://docs.python.org/3/library/numbers.html#numbers.Complex.real) and
    [``imag``](https://docs.python.org/3/library/numbers.html#numbers.Complex.imag)
    properties.

    ([``_SupportsRealImag``][numerary.types._SupportsRealImag] is the raw, non-caching
    version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRealImag)
SupportsRealImagSCU = Union[int, float, bool, Complex, SupportsRealImag]
SupportsRealImagSCT = SupportsRealImag


@runtime_checkable
class _SupportsTrunc(Protocol):
    r"""
    The raw, non-caching version of [``SupportsTrunc``][numerary.types.SupportsTrunc].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __trunc__(self) -> int:
        pass


@runtime_checkable
class SupportsTrunc(
    _SupportsTrunc,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the [``__trunc__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__trunc__).

    See also the [``trunc`` helper function][numerary.types.trunc].

    ([``_SupportsTrunc``][numerary.types._SupportsTrunc] is the raw, non-caching version
    that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, float, Decimal, Fraction, target_t=SupportsTrunc)
SupportsTruncSCU = Union[int, float, bool, Real, SupportsTrunc]
SupportsTruncSCT = SupportsTrunc


@runtime_checkable
class _SupportsFloor(Protocol):
    r"""
    The raw, non-caching version of [``SupportsFloor``][numerary.types.SupportsFloor].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __floor__(self) -> int:
        pass


@runtime_checkable
class SupportsFloor(
    _SupportsFloor,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the [``__floor__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__floor__).

    See also the [``floor`` helper function][numerary.types.floor].

    ([``_SupportsFloor``][numerary.types._SupportsFloor] is the raw, non-caching version
    that defines the actual methods.)

    !!! note

        This is of limited value for Python versions prior to 3.9, since ``#!python
        float.__floor__`` was not defined. If support for those environments is
        important, consider using [``SupportsFloat``][numerary.types.SupportsFloat]
        instead.
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, Decimal, Fraction, target_t=SupportsFloor)

if sys.version_info >= (3, 9):
    _assert_isinstance(float, target_t=SupportsFloor)

SupportsFloorSCU = Union[int, float, bool, Real, SupportsFloor]
SupportsFloorSCT = SupportsFloor


@runtime_checkable
class _SupportsCeil(Protocol):
    r"""
    The raw, non-caching version of [``SupportsCeil``][numerary.types.SupportsCeil].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __ceil__(self) -> int:
        pass


@runtime_checkable
class SupportsCeil(
    _SupportsCeil,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the [``__ceil__``
    method](https://docs.python.org/3/reference/datamodel.html#object.__ceil__).

    ([``_SupportsCeil``][numerary.types._SupportsCeil] is the raw, non-caching version
    that defines the actual methods.)

    See also the [``ceil`` helper function][numerary.types.ceil].

    !!! note

        This is of limited value for Python versions prior to 3.9, since ``#!python
        float.__ceil__`` was not defined. If support for those environments is
        important, consider using [``SupportsFloat``][numerary.types.SupportsFloat]
        instead, since that is what ``#!python math.ceil`` expects.
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, Decimal, Fraction, target_t=SupportsCeil)

if sys.version_info >= (3, 9):
    _assert_isinstance(float, target_t=SupportsCeil)

SupportsCeilSCU = Union[int, float, bool, Real, SupportsCeil]
SupportsCeilSCT = SupportsCeil


@runtime_checkable
class _SupportsDivmod(Protocol[_T_co]):
    r"""
    The raw, non-caching version of [``SupportsDivmod``][numerary.types.SupportsDivmod].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __divmod__(self, other: Any) -> Tuple[_T_co, _T_co]:
        pass

    @abstractmethod
    def __rdivmod__(self, other: Any) -> Tuple[_T_co, _T_co]:
        pass


@runtime_checkable
class SupportsDivmod(
    _SupportsDivmod[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the
    [``__divmod__``](https://docs.python.org/3/reference/datamodel.html#object.__divmod__)
    and
    [``__rdivmod__``](https://docs.python.org/3/reference/datamodel.html#object.__rdivmod__)
    methods. Each returns a 2-tuple of covariants.

    ([``_SupportsDivmod``][numerary.types._SupportsDivmod] is the raw, non-caching
    version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, float, Decimal, Fraction, target_t=SupportsDivmod)
SupportsDivmodSCU = Union[int, float, bool, Real, SupportsDivmod]
SupportsDivmodSCT = SupportsDivmod


@runtime_checkable
class _SupportsNumeratorDenominatorProperties(Protocol):
    r"""
    The raw, non-caching version of
    [``SupportsNumeratorDenominatorProperties``][numerary.types.SupportsNumeratorDenominatorProperties].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @property
    def numerator(self) -> int:
        pass

    @property
    def denominator(self) -> int:
        pass


@runtime_checkable
class SupportsNumeratorDenominatorProperties(
    _SupportsNumeratorDenominatorProperties,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the
    [``numerator``](https://docs.python.org/3/library/numbers.html#numbers.Rational.numerator)
    and
    [``denominator``](https://docs.python.org/3/library/numbers.html#numbers.Rational.denominator)
    properties.

    ([``_SupportsNumeratorDenominatorProperties``][numerary.types._SupportsNumeratorDenominatorProperties]
    is the raw, non-caching version that defines the actual properties.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, Fraction, target_t=SupportsNumeratorDenominatorProperties)
SupportsNumeratorDenominatorPropertiesSCU = Union[
    int,
    bool,
    Rational,
    SupportsNumeratorDenominatorProperties,
]
SupportsNumeratorDenominatorPropertiesSCT = SupportsNumeratorDenominatorProperties


@runtime_checkable
class _SupportsNumeratorDenominatorMethods(Protocol):
    r"""
    The raw, non-caching version of
    [``SupportsNumeratorDenominatorMethods``][numerary.types.SupportsNumeratorDenominatorMethods].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def numerator(self) -> SupportsInt:
        pass

    @abstractmethod
    def denominator(self) -> SupportsInt:
        pass


@runtime_checkable
class SupportsNumeratorDenominatorMethods(
    _SupportsNumeratorDenominatorMethods,
    Protocol,
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining ``#!python numerator`` and ``#!python denominator`` methods.
    Each returns a [``SupportsInt``][numerary.types.SupportsInt].

    ([``_SupportsNumeratorDenominatorMethods``][numerary.types._SupportsNumeratorDenominatorMethods]
    is the raw, non-caching version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


# See <https://github.com/mkdocstrings/mkdocstrings/issues/333>
SupportsNumeratorDenominatorMixedU = Union[
    SupportsNumeratorDenominatorProperties,
    SupportsNumeratorDenominatorMethods,
]
fr"""
{SupportsNumeratorDenominatorMixedU!r}
"""
SupportsNumeratorDenominatorMixedT = (
    SupportsNumeratorDenominatorProperties,
    SupportsNumeratorDenominatorMethods,
)
fr"""
{SupportsNumeratorDenominatorMixedT!r}
"""
assert SupportsNumeratorDenominatorMixedU.__args__ == SupportsNumeratorDenominatorMixedT  # type: ignore [attr-defined]

SupportsNumeratorDenominatorMixedSCU = Union[
    SupportsNumeratorDenominatorPropertiesSCU,
    SupportsNumeratorDenominatorMethods,
]
SupportsNumeratorDenominatorMixedSCT = SupportsNumeratorDenominatorMixedT


@runtime_checkable
class _SupportsComplexOps(Protocol[_T_co]):
    r"""
    The raw, non-caching version of
    [``SupportsComplexOps``][numerary.types.SupportsComplexOps].
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


@runtime_checkable
class SupportsComplexOps(
    _SupportsComplexOps[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the [``Complex`` operator
    methods](https://docs.python.org/3/library/numbers.html#numbers.Complex) with
    covariant return values.

    ([``_SupportsComplexOps``][numerary.types._SupportsComplexOps] is the raw,
    non-caching version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsComplexOps)
SupportsComplexOpsSCU = Union[int, float, bool, Complex, SupportsComplexOps]
SupportsComplexOpsSCT = SupportsComplexOps


@runtime_checkable
class _SupportsComplexPow(Protocol[_T_co]):
    r"""
    The raw, non-caching version of
    [``SupportsComplexPow``][numerary.types.SupportsComplexPow].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __pow__(self, exponent: Any) -> _T_co:
        pass

    @abstractmethod
    def __rpow__(self, exponent: Any) -> _T_co:
        pass


@runtime_checkable
class SupportsComplexPow(
    _SupportsComplexPow[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the ``#!python Complex`` (i.e., non-modulo) versions of the
    [``__pow__``](https://docs.python.org/3/reference/datamodel.html#object.__pow__) and
    [``__rpow__``](https://docs.python.org/3/reference/datamodel.html#object.__rpow__),
    each with a covariant return value.

    ([``_SupportsComplexPow``][numerary.types._SupportsComplexPow] is the raw,
    non-caching version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsComplexPow)
SupportsComplexPowSCU = Union[int, float, bool, Complex, SupportsComplexPow]
SupportsComplexPowSCT = SupportsComplexPow


@runtime_checkable
class _SupportsRealOps(Protocol[_T_co]):
    r"""
    The raw, non-caching version of
    [``SupportsRealOps``][numerary.types.SupportsRealOps].
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


@runtime_checkable
class SupportsRealOps(
    _SupportsRealOps[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the [``Real`` operator
    methods](https://docs.python.org/3/library/numbers.html#numbers.Real) with covariant
    return values.

    ([``_SupportsRealOps``][numerary.types._SupportsRealOps] is the raw, non-caching
    version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, float, bool, Decimal, Fraction, target_t=SupportsRealOps)
SupportsRealOpsSCU = Union[int, float, bool, Real, SupportsRealOps]
SupportsRealOpsSCT = SupportsRealOps


@runtime_checkable
class _SupportsIntegralOps(Protocol[_T_co]):
    r"""
    The raw, non-caching version of
    [``SupportsIntegralOps``][numerary.types.SupportsIntegralOps].
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


@runtime_checkable
class SupportsIntegralOps(
    _SupportsIntegralOps[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the [``Integral`` operator
    methods](https://docs.python.org/3/library/numbers.html#numbers.Real) with covariant
    return values.

    ([``_SupportsIntegralOps``][numerary.types._SupportsIntegralOps] is the raw,
    non-caching version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, target_t=SupportsIntegralOps)
SupportsIntegralOpsSCU = Union[int, bool, Integral, SupportsIntegralOps]
SupportsIntegralOpsSCT = SupportsIntegralOps


@runtime_checkable
class _SupportsIntegralPow(Protocol[_T_co]):
    r"""
    The raw, non-caching version of
    [``SupportsIntegralPow``][numerary.types.SupportsIntegralPow].
    """
    __slots__: Union[str, Iterable[str]] = ()

    @abstractmethod
    def __pow__(self, exponent: Any, modulus: Optional[Any] = None) -> _T_co:
        pass

    @abstractmethod
    def __rpow__(self, exponent: Any, modulus: Optional[Any] = None) -> _T_co:
        pass


@runtime_checkable
class SupportsIntegralPow(
    _SupportsIntegralPow[_T_co],
    Protocol[_T_co],
    metaclass=CachingProtocolMeta,
):
    r"""
    A caching ABC defining the ``#!python Integral`` (i.e., modulo) versions of the
    [``__pow__``](https://docs.python.org/3/reference/datamodel.html#object.__pow__) and
    [``__rpow__``](https://docs.python.org/3/reference/datamodel.html#object.__rpow__),
    each with a covariant return value.

    ([``_SupportsIntegralPow``][numerary.types._SupportsIntegralPow] is the raw,
    non-caching version that defines the actual methods.)
    """
    __slots__: Union[str, Iterable[str]] = ()


_assert_isinstance(int, bool, target_t=SupportsIntegralPow)
SupportsIntegralPowSCU = Union[int, bool, Integral, SupportsIntegralPow]
SupportsIntegralPowSCT = SupportsIntegralPow


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
    A caching ABC that defines a core set of operations for interacting with reals. It
    is a composition of:

    * [``SupportsAbs``][numerary.types.SupportsAbs]
    * [``SupportsFloat``][numerary.types.SupportsFloat]
    * [``SupportsRealOps``][numerary.types.SupportsRealOps]
    * [``SupportsComplexOps``][numerary.types.SupportsComplexOps]
    * [``SupportsComplexPow``][numerary.types.SupportsComplexPow]

    This is a practically useful, but incomplete list. To enforce equivalence to
    ``#!python numbers.Real``, one would also need:

    * [``SupportsComplex``][numerary.types.SupportsComplex]
    * [``SupportsConjugate``][numerary.types.SupportsConjugate]
    * [``SupportsRealImag``][numerary.types.SupportsRealImag]
    * [``SupportsRound``][numerary.types.SupportsRound]
    * [``SupportsTrunc``][numerary.types.SupportsTrunc]
    * [``SupportsFloor``][numerary.types.SupportsFloor]
    * [``SupportsCeil``][numerary.types.SupportsCeil]
    * [``SupportsDivmod``][numerary.types.SupportsDivmod]
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
RealLikeSCT = RealLike


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
    A caching ABC that defines a core set of operations for interacting with rationals.
    It is a composition of:

    * [``SupportsAbs``][numerary.types.SupportsAbs]
    * [``SupportsFloat``][numerary.types.SupportsFloat]
    * [``SupportsNumeratorDenominatorProperties``][numerary.types.SupportsNumeratorDenominatorProperties]
    * [``SupportsRealOps``][numerary.types.SupportsRealOps]
    * [``SupportsComplexOps``][numerary.types.SupportsComplexOps]
    * [``SupportsComplexPow``][numerary.types.SupportsComplexPow]

    This is a practically useful, but incomplete list. To enforce equivalence to
    ``#!python numbers.Rational``, one would also need:

    * [``SupportsComplex``][numerary.types.SupportsComplex]
    * [``SupportsConjugate``][numerary.types.SupportsConjugate]
    * [``SupportsRealImag``][numerary.types.SupportsRealImag]
    * [``SupportsRound``][numerary.types.SupportsRound]
    * [``SupportsTrunc``][numerary.types.SupportsTrunc]
    * [``SupportsFloor``][numerary.types.SupportsFloor]
    * [``SupportsCeil``][numerary.types.SupportsCeil]
    * [``SupportsDivmod``][numerary.types.SupportsDivmod]
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
RationalLikePropertiesSCT = RationalLikeProperties


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
    A caching ABC that defines a core set of operations for interacting with rationals.
    It is identical to
    [``RationalLikeProperties``][numerary.types.RationalLikeProperties] with one
    important exception. Instead of
    [``SupportsNumeratorDenominatorProperties``][numerary.types.SupportsNumeratorDenominatorProperties],
    this protocol provides
    [``SupportsNumeratorDenominatorMethods``][numerary.types.SupportsNumeratorDenominatorMethods].

    This is probably not very useful on its own, but is important to the construction of
    [``RationalLikeMixedU``][numerary.types.RationalLikeMixedU] and
    [``RationalLikeMixedT``][numerary.types.RationalLikeMixedT].
    """
    __slots__: Union[str, Iterable[str]] = ()

    # Must be able to instantiate it
    @abstractmethod
    def __init__(self, *args: Any, **kw: Any):
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass


# See <https://github.com/mkdocstrings/mkdocstrings/issues/333>
RationalLikeMixedU = Union[RationalLikeProperties, RationalLikeMethods]
fr"""
{RationalLikeMixedU!r}
"""
RationalLikeMixedT = (RationalLikeProperties, RationalLikeMethods)
fr"""
{RationalLikeMixedT!r}
"""
assert RationalLikeMixedU.__args__ == RationalLikeMixedT  # type: ignore [attr-defined]
assert RationalLikeMethods.__doc__
RationalLikeMethods.__doc__ += fr"""

    ``` python
    RationalLikeMixedU = {RationalLikeMixedU!r}
    RationalLikeMixedT = ({", ".join(cls.__name__ for cls in  RationalLikeMixedT)})
    ```
"""

RationalLikeMixedSCU = Union[
    RationalLikePropertiesSCU,
    RationalLikeMethods,
]
RationalLikeMixedSCT = RationalLikeMixedT


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
    A caching ABC that defines a core set of operations for interacting with integrals.
    It is a composition of:

    * [``SupportsAbs``][numerary.types.SupportsAbs]
    * [``SupportsFloat``][numerary.types.SupportsFloat]
    * [``SupportsIndex``][numerary.types.SupportsIndex]
    * [``SupportsInt``][numerary.types.SupportsInt]
    * [``SupportsIntegralOps``][numerary.types.SupportsIntegralOps]
    * [``SupportsIntegralPow``][numerary.types.SupportsIntegralPow]
    * [``SupportsRealOps``][numerary.types.SupportsRealOps]
    * [``SupportsComplexOps``][numerary.types.SupportsComplexOps]

    This is a practically useful, but incomplete list. To enforce equivalence to
    ``#!python numbers.Integral``, one would also need:

    * [``SupportsComplex``][numerary.types.SupportsComplex]
    * [``SupportsConjugate``][numerary.types.SupportsConjugate]
    * [``SupportsRealImag``][numerary.types.SupportsRealImag]
    * [``SupportsRound``][numerary.types.SupportsRound]
    * [``SupportsTrunc``][numerary.types.SupportsTrunc]
    * [``SupportsFloor``][numerary.types.SupportsFloor]
    * [``SupportsCeil``][numerary.types.SupportsCeil]
    * [``SupportsDivmod``][numerary.types.SupportsDivmod]
    * [``SupportsNumeratorDenominatorProperties``][numerary.types.SupportsNumeratorDenominatorProperties]
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
IntegralLikeSCT = IntegralLike


# ---- Functions -----------------------------------------------------------------------


@beartype
def ceil(operand: Union[SupportsFloat, SupportsCeil]):
    r"""
    Helper function that wraps ``math.ceil``.

    ``` python
    >>> from numerary.types import SupportsCeil, SupportsFloat, ceil
    >>> my_ceil: SupportsCeil
    >>> my_ceil = 1
    >>> ceil(my_ceil)
    1
    >>> from fractions import Fraction
    >>> my_ceil = Fraction(1, 2)
    >>> ceil(my_ceil)
    1
    >>> my_ceil_float: SupportsFloat = 1.2
    >>> ceil(my_ceil_float)
    2

    ```
    """
    return math.ceil(operand)  # type: ignore [arg-type]


@beartype
def floor(operand: Union[SupportsFloat, SupportsFloor]):
    r"""
    Helper function that wraps ``math.floor``.

    ``` python
    >>> from numerary.types import SupportsFloat, SupportsFloor, floor
    >>> my_floor: SupportsFloor
    >>> my_floor = 1
    >>> floor(my_floor)
    1
    >>> from fractions import Fraction
    >>> my_floor = Fraction(1, 2)
    >>> floor(my_floor)
    0
    >>> my_floor_float: SupportsFloat = 1.2
    >>> floor(my_floor_float)
    1

    ```
    """
    return math.floor(operand)  # type: ignore [arg-type]


@beartype
def trunc(operand: Union[SupportsFloat, SupportsTrunc]):
    r"""
    Helper function that wraps ``math.trunc``.

    ``` python
    >>> from numerary.types import SupportsFloat, SupportsTrunc, trunc
    >>> my_trunc: SupportsTrunc
    >>> my_trunc = 1
    >>> trunc(my_trunc)
    1
    >>> from fractions import Fraction
    >>> my_trunc = Fraction(1, 2)
    >>> trunc(my_trunc)
    0
    >>> my_trunc_float: SupportsFloat = 1.2
    >>> trunc(my_trunc_float)
    1

    ```
    """
    return math.trunc(operand)  # type: ignore [arg-type]


@beartype
def numerator(operand: SupportsNumeratorDenominatorMixedU):
    r"""
    Helper function that extracts the numerator from *operand* including resolving
    non-compliant rational implementations that implement ``numerator`` as a method
    rather than a property.

    ``` python
    >>> from fractions import Fraction
    >>> from numerary.types import numerator
    >>> numerator(Fraction(22, 7))
    22

    ```

    See
    [SupportsNumeratorDenominatorProperties][numerary.types.SupportsNumeratorDenominatorProperties]
    and
    [SupportsNumeratorDenominatorMethods][numerary.types.SupportsNumeratorDenominatorMethods].
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
    Helper function that extracts the denominator from *operand* including resolving
    non-compliant rational implementations that implement ``denominator`` as a method
    rather than a property.

    ``` python
    >>> from fractions import Fraction
    >>> from numerary.types import denominator
    >>> denominator(Fraction(22, 7))
    7

    ```

    See
    [SupportsNumeratorDenominatorProperties][numerary.types.SupportsNumeratorDenominatorProperties]
    and
    [SupportsNumeratorDenominatorMethods][numerary.types.SupportsNumeratorDenominatorMethods].
    """
    if hasattr(operand, "denominator"):
        if callable(operand.denominator):
            return operand.denominator()
        else:
            return operand.denominator
    else:
        raise TypeError(f"{operand!r} has no denominator")


# ---- Initialization ------------------------------------------------------------------


# Prior to Python 3.9, floats didn't have explicit __floor__ or __ceil__ methods; they
# were "directly" supported in math.floor and math.ceil, respectively, so the pure
# protocol approach thinks they're not supported
SupportsFloor.includes(float)
SupportsCeil.includes(float)

# complex defines these methods, but only to raise exceptions
SupportsDivmod.excludes(complex)
SupportsRealOps.excludes(complex)

try:
    import numpy

    for t in (
        numpy.uint8,
        numpy.uint16,
        numpy.uint32,
        numpy.uint64,
        numpy.int8,
        numpy.int16,
        numpy.int32,
        numpy.int64,
    ):
        SupportsFloor.includes(t)
        SupportsCeil.includes(t)

    for t in (
        numpy.float16,
        numpy.float32,
        numpy.float64,
        numpy.float128,
    ):
        SupportsFloor.includes(t)
        SupportsCeil.includes(t)
        SupportsIntegralOps.excludes(t)
        SupportsIntegralPow.excludes(t)

    # numpy complex types define these methods, but only to raise exceptions
    for t in (
        numpy.csingle,
        numpy.cdouble,
        numpy.clongdouble,
    ):
        SupportsDivmod.excludes(t)
        SupportsRealOps.excludes(t)
        SupportsIntegralOps.excludes(t)
        SupportsIntegralPow.excludes(t)
except ImportError:
    pass

try:
    import sympy.core.symbol

    SupportsTrunc.excludes(sympy.core.symbol.Symbol)
    SupportsIntegralOps.excludes(sympy.core.symbol.Symbol)
    SupportsIntegralPow.excludes(sympy.core.symbol.Symbol)
except ImportError:
    pass
