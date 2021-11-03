# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

from decimal import Decimal
from math import ceil, floor, trunc
from numbers import Integral, Real
from operator import (
    __abs__,
    __add__,
    __and__,
    __eq__,
    __floordiv__,
    __ge__,
    __gt__,
    __invert__,
    __le__,
    __lshift__,
    __lt__,
    __mod__,
    __mul__,
    __ne__,
    __neg__,
    __or__,
    __pos__,
    __pow__,
    __rshift__,
    __sub__,
    __truediv__,
    __xor__,
)
from typing import Iterable, Optional, Union, overload

from numerary.bt import beartype
from numerary.types import SupportsIntSCU

__all__ = (
    "Numberwang",
    "NumberwangDerived",
    "NumberwangRegistered",
    "Wangernumb",
    "WangernumbDerived",
    "WangernumbRegistered",
)


# ---- Types ---------------------------------------------------------------------------


_IntegralT = Union[int, "NumberwangBase", Integral]
_RealT = Union[float, "Wangernumb", Real]


# ---- Classes -------------------------------------------------------------------------


class NumberwangBase:
    __slots__: Union[str, Iterable[str]] = ("val",)

    @beartype
    def __init__(self, arg: SupportsIntSCU = 0):
        self.val: int = int(arg)

    @beartype
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.val})"

    @beartype
    def __lt__(self, other) -> bool:
        return __lt__(self.val, other)

    @beartype
    def __le__(self, other) -> bool:
        return __le__(self.val, other)

    @beartype
    def __eq__(self, other) -> bool:
        return __eq__(self.val, other)

    @beartype
    def __ne__(self, other) -> bool:
        return __ne__(self.val, other)

    @beartype
    def __ge__(self, other) -> bool:
        return __ge__(self.val, other)

    @beartype
    def __gt__(self, other) -> bool:
        return __gt__(self.val, other)

    @beartype
    def __hash__(self) -> int:
        return hash((type(self).__name__, self.val))

    @overload
    def __add__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __add__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __add__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __add__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__add__(self.val, other))
        elif isinstance(other, float):
            val = __add__(self.val, other)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __add__(self.val, other)

    @overload
    def __radd__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __radd__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __radd__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __radd__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__add__(other, self.val))
        elif isinstance(other, float):
            val = __add__(other, self.val)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __add__(other, self.val)

    @overload
    def __sub__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __sub__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __sub__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __sub__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__sub__(self.val, other))
        elif isinstance(other, float):
            val = __sub__(self.val, other)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __sub__(self.val, other)

    @overload
    def __rsub__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __rsub__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rsub__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rsub__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__sub__(other, self.val))
        elif isinstance(other, float):
            val = __sub__(other, self.val)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __sub__(other, self.val)

    @overload
    def __mul__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __mul__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __mul__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __mul__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__mul__(self.val, other))
        elif isinstance(other, float):
            val = __mul__(self.val, other)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __mul__(self.val, other)

    @overload
    def __rmul__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __rmul__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rmul__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rmul__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__mul__(other, self.val))
        elif isinstance(other, float):
            val = __mul__(other, self.val)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __mul__(other, self.val)

    @overload
    def __truediv__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __truediv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __truediv__(self, other):
        if isinstance(other, (float, NumberwangBase, Wangernumb, Real)):
            val = __truediv__(self.val, other)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __truediv__(self.val, other)

    @overload
    def __rtruediv__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rtruediv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rtruediv__(self, other):
        if isinstance(other, (float, NumberwangBase, Wangernumb, Real)):
            val = __truediv__(other, self.val)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __truediv__(other, self.val)

    @overload
    def __floordiv__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __floordiv__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __floordiv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __floordiv__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__floordiv__(self.val, other))
        elif isinstance(other, float):
            val = __floordiv__(self.val, other)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __floordiv__(self.val, other)

    @overload
    def __rfloordiv__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __rfloordiv__(self, other: _RealT) -> _RealT:  # type: ignore
        ...

    @overload
    def __rfloordiv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rfloordiv__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__floordiv__(other, self.val))
        elif isinstance(other, float):
            val = __floordiv__(other, self.val)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __floordiv__(other, self.val)

    @overload
    def __mod__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __mod__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __mod__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __mod__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__mod__(self.val, other))
        elif isinstance(other, float):
            val = __mod__(self.val, other)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __mod__(self.val, other)

    @overload
    def __rmod__(self, other: _IntegralT) -> _IntegralT:  # type: ignore
        ...

    @overload
    def __rmod__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rmod__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rmod__(self, other):
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__mod__(other, self.val))
        elif isinstance(other, float):
            val = __mod__(other, self.val)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return __mod__(other, self.val)

    @overload
    def __pow__(  # type: ignore
        self, other: _IntegralT, modulo: Optional[_IntegralT] = None
    ) -> _IntegralT:
        ...

    @overload
    def __pow__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __pow__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __pow__(self, other, modulo=None):
        if isinstance(other, (NumberwangBase, Integral)):
            return type(self)(pow(self.val, int(other), modulo))
        elif isinstance(other, float):
            val = pow(self.val, float(other), modulo)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return pow(self.val, other, modulo)

    @overload
    def __rpow__(  # type: ignore
        self, other: _IntegralT, modulo: Optional[_IntegralT] = None
    ) -> _IntegralT:
        ...

    @overload
    def __rpow__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rpow__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rpow__(self, other, modulo=None):
        if isinstance(other, (NumberwangBase, Integral)):
            return type(self)(pow(int(other), self.val, modulo))
        elif isinstance(other, float):
            val = pow(float(other), self.val, modulo)

            if isinstance(self, NumberwangDerived):
                return WangernumbDerived(val)
            elif isinstance(self, NumberwangRegistered):
                return WangernumbRegistered(val)
            else:
                return Wangernumb(val)
        else:
            return pow(other, self.val, modulo)

    @beartype
    def __lshift__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__lshift__(self.val, int(other)))
        elif isinstance(other, Integral):
            return __lshift__(self.val, other)
        else:
            return NotImplemented

    @beartype
    def __rlshift__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__lshift__(int(other), self.val))
        elif isinstance(other, Integral):
            return __lshift__(other, self.val)
        else:
            return NotImplemented

    @beartype
    def __rshift__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__rshift__(self.val, other))
        elif isinstance(other, Integral):
            return __rshift__(self.val, other)
        else:
            return NotImplemented

    @beartype
    def __rrshift__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__rshift__(other, self.val))
        elif isinstance(other, Integral):
            return __rshift__(other, self.val)
        else:
            return NotImplemented

    @beartype
    def __and__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__and__(self.val, other))
        elif isinstance(other, Integral):
            return __and__(self.val, other)
        else:
            return NotImplemented

    @beartype
    def __rand__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__and__(other, self.val))
        elif isinstance(other, Integral):
            return __and__(other, self.val)
        else:
            return NotImplemented

    @beartype
    def __xor__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__xor__(self.val, other))
        elif isinstance(other, Integral):
            return __xor__(self.val, other)
        else:
            return NotImplemented

    @beartype
    def __rxor__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__xor__(other, self.val))
        elif isinstance(other, Integral):
            return __xor__(other, self.val)
        else:
            return NotImplemented

    @beartype
    def __or__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__or__(self.val, other))
        elif isinstance(other, Integral):
            return __or__(self.val, other)
        else:
            return NotImplemented

    @beartype
    def __ror__(self, other: _IntegralT) -> _IntegralT:
        if isinstance(other, (int, NumberwangBase)):
            return type(self)(__or__(other, self.val))
        elif isinstance(other, Integral):
            return __or__(other, self.val)
        else:
            return NotImplemented

    @beartype
    def __neg__(self) -> NumberwangBase:
        return type(self)(__neg__(self.val))

    @beartype
    def __pos__(self) -> NumberwangBase:
        return type(self)(__pos__(self.val))

    @beartype
    def __abs__(self) -> NumberwangBase:
        return type(self)(__abs__(self.val))

    @beartype
    def __invert__(self) -> NumberwangBase:
        return type(self)(__invert__(self.val))

    @beartype
    def __int__(self) -> int:
        return self.val

    @beartype
    def __round__(self, ndigits: Optional[_IntegralT] = None) -> int:
        if ndigits is None:
            return round(self.val)
        else:
            return round(self.val, int(ndigits))

    @beartype
    def __trunc__(self) -> int:
        return trunc(self.val)

    @beartype
    def __floor__(self) -> int:
        return floor(self.val)

    @beartype
    def __ceil__(self) -> int:
        return ceil(self.val)

    @property
    def numerator(self) -> int:
        return self.val

    @property
    def denominator(self) -> int:
        return 1


assert not issubclass(NumberwangBase, Real)
assert not issubclass(NumberwangBase, Integral)


class Numberwang(NumberwangBase):
    __slots__: Union[str, Iterable[str]] = ()

    @beartype
    def __float__(self) -> float:
        return float(int(self))

    @beartype
    def __index__(self) -> int:
        return int(self)


assert not issubclass(Numberwang, Real)
assert not issubclass(Numberwang, Integral)


class NumberwangRegistered(Numberwang):
    __slots__: Union[str, Iterable[str]] = ()


assert not issubclass(NumberwangRegistered, Real)
assert not issubclass(NumberwangRegistered, Integral)

Integral.register(NumberwangRegistered)
assert issubclass(NumberwangRegistered, Real)
assert issubclass(NumberwangRegistered, Integral)


class NumberwangDerived(NumberwangBase, Integral):  # type: ignore
    __slots__: Union[str, Iterable[str]] = ()


assert issubclass(NumberwangDerived, Real)
assert issubclass(NumberwangDerived, Integral)

assert not issubclass(NumberwangBase, Real)
assert not issubclass(NumberwangBase, Integral)
assert not issubclass(Numberwang, Real)
assert not issubclass(Numberwang, Integral)


class Wangernumb:
    __slots__: Union[str, Iterable[str]] = ("val",)

    @beartype
    def __init__(self, arg: _RealT = 0):
        self.val = float(arg)

    @beartype
    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.val})"

    @beartype
    def __lt__(self, other: _RealT) -> bool:
        return __lt__(self.val, other)

    @beartype
    def __le__(self, other: _RealT) -> bool:
        return __le__(self.val, other)

    @beartype
    def __eq__(self, other) -> bool:
        return __eq__(self.val, other)

    @beartype
    def __ne__(self, other) -> bool:
        return __ne__(self.val, other)

    @beartype
    def __ge__(self, other: _RealT) -> bool:
        return __ge__(self.val, other)

    @beartype
    def __gt__(self, other: _RealT) -> bool:
        return __gt__(self.val, other)

    @beartype
    def __hash__(self) -> int:
        return hash(self.val)

    @overload
    def __add__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __add__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __add__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__add__(self.val, other))
        else:
            return __add__(self.val, other)

    @overload
    def __radd__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __radd__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __radd__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__add__(other, self.val))
        else:
            return __add__(other, self.val)

    @overload
    def __sub__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __sub__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __sub__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__sub__(self.val, other))
        else:
            return __sub__(self.val, other)

    @overload
    def __rsub__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rsub__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rsub__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__sub__(other, self.val))
        else:
            return __sub__(other, self.val)

    @overload
    def __mul__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __mul__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __mul__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__mul__(self.val, other))
        else:
            return __mul__(self.val, other)

    @overload
    def __rmul__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rmul__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rmul__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__mul__(other, self.val))
        else:
            return __mul__(other, self.val)

    @overload
    def __truediv__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __truediv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __truediv__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__truediv__(self.val, other))
        else:
            return __truediv__(self.val, other)

    @overload
    def __rtruediv__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rtruediv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rtruediv__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__truediv__(other, self.val))
        else:
            return __truediv__(other, self.val)

    @overload
    def __floordiv__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __floordiv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __floordiv__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__floordiv__(self.val, other))
        else:
            return __floordiv__(self.val, other)

    @overload
    def __rfloordiv__(self, other: _RealT) -> _RealT:  # type: ignore
        ...

    @overload
    def __rfloordiv__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rfloordiv__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__floordiv__(other, self.val))
        else:
            return __floordiv__(other, self.val)

    @overload
    def __mod__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __mod__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __mod__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__mod__(self.val, other))
        else:
            return __mod__(self.val, other)

    @overload
    def __rmod__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rmod__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rmod__(self, other):
        if isinstance(other, (float, Wangernumb)):
            return type(self)(__mod__(other, self.val))
        else:
            return __mod__(other, self.val)

    @overload
    def __pow__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __pow__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __pow__(self, other):
        val = __pow__(self.val, other)

        if isinstance(val, Real):
            return type(self)(val)
        else:
            return val

    @overload
    def __rpow__(self, other: _RealT) -> _RealT:
        ...

    @overload
    def __rpow__(self, other: Decimal) -> Decimal:
        ...

    @beartype
    def __rpow__(self, other):
        val = __pow__(other, self.val)

        if isinstance(val, Real):
            return type(self)(val)
        else:
            return val

    @beartype
    def __neg__(self) -> Wangernumb:
        return type(self)(__neg__(self.val))

    @beartype
    def __pos__(self) -> Wangernumb:
        return type(self)(__pos__(self.val))

    @beartype
    def __abs__(self) -> Wangernumb:
        return type(self)(__abs__(self.val))

    @beartype
    def __float__(self) -> float:
        return self.val

    @overload
    def __round__(self) -> int:
        ...

    @overload
    def __round__(self, ndigits: _IntegralT) -> float:
        ...

    @beartype
    def __round__(self, ndigits: Optional[_IntegralT] = None) -> Union[int, float]:
        if ndigits is None:
            return round(self.val)
        else:
            return round(self.val, int(ndigits))

    @beartype
    def __trunc__(self) -> int:
        return trunc(self.val)

    @beartype
    def __floor__(self) -> int:
        return floor(self.val)

    @beartype
    def __ceil__(self) -> int:
        return ceil(self.val)


assert not issubclass(Wangernumb, Real)


class WangernumbRegistered(Wangernumb):
    __slots__: Union[str, Iterable[str]] = ()


assert not issubclass(WangernumbRegistered, Real)

Real.register(WangernumbRegistered)
assert issubclass(WangernumbRegistered, Real)


class WangernumbDerived(Wangernumb, Real):  # type: ignore
    __slots__: Union[str, Iterable[str]] = ()


assert issubclass(WangernumbDerived, Real)

assert not issubclass(Wangernumb, Real)
