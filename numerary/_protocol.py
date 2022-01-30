# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

import sys
from abc import abstractmethod
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Dict, Iterable, Set, Tuple, Type, TypeVar, Union

__all__ = ("CachingProtocolMeta",)


# ---- Types ---------------------------------------------------------------------------


_T_co = TypeVar("_T_co", covariant=True)
_TT = TypeVar("_TT", bound="type")

if sys.version_info >= (3, 8):
    from typing import _get_protocol_attrs  # type: ignore [attr-defined]
    from typing import (
        Protocol,
        SupportsAbs,
        SupportsComplex,
        SupportsFloat,
        SupportsIndex,
        SupportsInt,
        SupportsRound,
        runtime_checkable,
    )
else:
    from typing_extensions import Protocol, _get_protocol_attrs, runtime_checkable

    @runtime_checkable
    class SupportsAbs(Protocol[_T_co]):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __abs__(self) -> _T_co:
            pass

    @runtime_checkable
    class SupportsComplex(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __complex__(self) -> complex:
            pass

    @runtime_checkable
    class SupportsFloat(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __float__(self) -> float:
            pass

    @runtime_checkable
    class SupportsIndex(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __index__(self) -> int:
            pass

    @runtime_checkable
    class SupportsInt(Protocol):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __int__(self) -> int:
            pass

    @runtime_checkable
    class SupportsRound(Protocol[_T_co]):
        __slots__: Union[str, Iterable[str]] = ()

        @abstractmethod
        def __round__(self, ndigits: int = 0) -> _T_co:
            pass


if TYPE_CHECKING:
    # Warning: Deep typing voodoo ahead. See
    # <https://github.com/python/mypy/issues/11614>.
    from abc import ABCMeta as _ProtocolMeta
else:
    _ProtocolMeta = type(Protocol)


class _CachingProtocolMeta(_ProtocolMeta):
    r"""
    TODO
    """

    _abc_inst_check_cache: Dict[Type, bool]

    def __new__(
        mcls: Type[_TT],
        name: str,
        bases: Tuple[Type, ...],
        namespace: Dict[str, Any],
        **kw: Any,
    ) -> _TT:
        # See <https://github.com/python/mypy/issues/9282>
        cls = super().__new__(mcls, name, bases, namespace, **kw)  # type: ignore [misc]

        # This is required because, despite deriving from typing.Protocol, our
        # redefinition below gets its _is_protocol class member set to False. It being
        # True is required for compatibility with @runtime_checkable. So we lie to tell
        # the truth.
        cls._is_protocol = True

        # Prefixing this class member with "_abc_" is necessary to prevent it from being
        # considered part of the Protocol. (See
        # <https://github.com/python/cpython/blob/main/Lib/typing.py>.)
        cls._abc_inst_check_cache = {}

        return cls

    def __instancecheck__(cls, inst: Any) -> bool:
        try:
            # This has to stay *super* tight! Even adding a mere assertion can add ~50%
            # to the best case runtime!
            return cls._abc_inst_check_cache[type(inst)]
        except KeyError:
            # If you're going to do *anything*, do it here. Don't touch the rest of this
            # method if you can avoid it.
            inst_t = type(inst)
            bases_pass_muster = True

            for base in cls.__bases__:
                # TODO(posita): Checking names seems off to me. Is there a better way?
                if base is cls or base.__name__ in ("Protocol", "Generic", "object"):
                    continue

                if not isinstance(inst, base):
                    bases_pass_muster = False
                    break

            cls._abc_inst_check_cache[
                inst_t
            ] = bases_pass_muster and cls._check_only_my_attrs(inst)

            return cls._abc_inst_check_cache[inst_t]

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


class CachingProtocolMeta(_CachingProtocolMeta):
    r"""
    Stand-in for ``#!python typing.Protocol``’s base class that caches results of
    ``#!python __instancecheck__``, (which is otherwise [really 🤬ing
    expensive](https://github.com/python/mypy/issues/3186#issuecomment-885718629)).
    (When this was introduced, it resulted in about a 5× performance increase for
    [``dyce``](https://github.com/posita/dyce)’s unit tests, which was the only
    benchmark I had at the time.) The downside is that this will yield unpredictable
    results for objects whose methods don’t stem from any type (e.g., are assembled at
    runtime). I don’t know of any real-world case where that would be true. We’ll jump
    off that bridge when we come to it.

    Note that one can make an existing protocol a caching protocol through inheritance,
    but in order to be ``@runtime_checkable``, the parent protocol also has to be
    ``@runtime_checkable``.

    ``` python
    >>> from abc import abstractmethod
    >>> from numerary.types import Protocol, runtime_checkable

    >>> @runtime_checkable
    ... class _MyProtocol(Protocol):  # plain vanilla protocol
    ...   @abstractmethod
    ...   def myfunc(self, arg: int) -> str:
    ...     pass

    >>> @runtime_checkable  # redundant, but useful for documentation
    ... class MyProtocol(
    ...   _MyProtocol,
    ...   Protocol,
    ...   metaclass=CachingProtocolMeta,  # caching version
    ... ):
    ...   pass

    >>> class MyImplementation:
    ...   def myfunc(self, arg: int) -> str:
    ...     return str(arg * -2 + 5)

    >>> my_thing: MyProtocol = MyImplementation()
    >>> isinstance(my_thing, MyProtocol)
    True

    ```
    """

    _abc_inst_check_cache_overridden: Dict[Type, bool]
    _abc_inst_check_cache_listeners: Set[CachingProtocolMeta]

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
        cls._abc_inst_check_cache_overridden = defaultdict(bool)  # defaults to False
        cls._abc_inst_check_cache_listeners = set()

        for base in bases:
            if hasattr(base, "_abc_inst_check_cache_listeners"):
                base._abc_inst_check_cache_listeners.add(cls)

        return cls

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
        ...   def spam(self) -> str:
        ...     pass

        >>> class NoSpam:
        ...   pass

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
        ...   def ham(self) -> str:
        ...     pass

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

    def _dirty_for(cls, inst_t: Type) -> None:
        for inheriting_cls in cls._abc_inst_check_cache_listeners:
            if (
                inst_t in inheriting_cls._abc_inst_check_cache
                and not inheriting_cls._abc_inst_check_cache_overridden[inst_t]
            ):
                del inheriting_cls._abc_inst_check_cache[inst_t]
                del inheriting_cls._abc_inst_check_cache_overridden[inst_t]
