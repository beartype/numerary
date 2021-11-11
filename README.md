<!---
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !!!!!!!!!!!!!!! IMPORTANT: READ THIS BEFORE EDITING! !!!!!!!!!!!!!!!
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  Please keep each sentence on its own unwrapped line.
  It looks like crap in a text editor, but it has no effect on rendering, and it allows much more useful diffs.
  Thank you!

  WARNING: THIS DOCUMENT MUST BE SELF-CONTAINED.
  ALL LINKS MUST BE ABSOLUTE.
  This file is used on GitHub and PyPi (via setup.cfg).
  There is no guarantee that other docs/resources will be available where this content is displayed.
-->

*Copyright and other protections apply.
Please see the accompanying ``LICENSE`` file for rights and restrictions governing use of this software.
All rights not expressly waived or licensed are reserved.
If that file is missing or appears to be modified from its original, then please contact the author before viewing or using this software in any capacity.*

[![Tests](https://github.com/posita/numerary/actions/workflows/unit-tests.yaml/badge.svg)](https://github.com/posita/numerary/actions/workflows/unit-tests.yaml)
[![Version](https://img.shields.io/pypi/v/numerary/0.1.0.svg)](https://pypi.org/project/numerary/0.1.0/)
[![Development Stage](https://img.shields.io/pypi/status/numerary/0.1.0.svg)](https://pypi.org/project/numerary/0.1.0/)
[![License](https://img.shields.io/pypi/l/numerary/0.1.0.svg)](http://opensource.org/licenses/MIT)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/numerary/0.1.0.svg)](https://pypi.org/project/numerary/0.1.0/)
[![Supported Python Implementations](https://img.shields.io/pypi/implementation/numerary/0.1.0.svg)](https://pypi.org/project/numerary/0.1.0/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Bear-ified™](https://raw.githubusercontent.com/beartype/beartype-assets/main/badge/bear-ified.svg)](https://beartype.rtfd.io/)

Are you defining a numeric interface that should work with more than just ``int``s and ``float``s?
Are you annotating that interface for documentation *and* type-checking?
Were you excited by [PEP 3141](https://www.python.org/dev/peps/pep-3141/)’s glitz and gloss promising a clean, straightforward number type definition mechanism, only to learn the hard way—after many hours of searching, tweaking, hacking, and testing ever more convoluted code, again and again—that you could’t actually make it work with Python’s type-checking system?
Do you now wonder whether numbers were something new to computing in general because nothing else would explain such a gaping hole in a programming language so popular with the STEM crowd that has been around since the early 1990s?
Does the number [3186](https://github.com/python/mypy/issues/3186) haunt you in your dreams?
Do you find yourself shouting to no one in particular, “There *has* to be a better way?”

Well I’m here to tell you there ain’t.
But until there is, there’s …

# *``numerary``—Now with Protocol Power™*

That’s right!

For a hopefully limited time, you too can benefit from someone else’s deranged work-arounds for the enormous chasms in Python that lie between the esoteric fields of computation that are “typing” and “numbers” instead of having to roll your own ~~out of sheer desperation~~ *from first principles*!
If you still have no idea what I’m talking about, [this may help illustrate](https://posita.github.io/numerary/0.1/whytho/).

``numerary`` is a pure-Python codified rant for signaling that your interface is usable with non-native numeric primitives[^1] without breaking type-checking.
More simply, ``numerary`` aspires to a world where numbers and types can work together.

If you’re thinking that you shouldn’t need a 🤬ing library for that, *you’re right*.

[^1]:

    You know, *super* weird, off-the-wall shit, like members of the [numeric tower](https://docs.python.org/3/library/numbers.html), or [standard library primitives that remain *non*-members for some 🤬ed up reason](https://docs.python.org/3/library/decimal.html), or [legitimate non-members because they predate PEP 3141 and conforming would amount to breaking changes](https://trac.sagemath.org/ticket/28234), or—I don’t know—oodles of libraries and applications that have been around for literally decades that bring huge value to vast scientific and mathematic audiences, but whose number primitives break type-checking if one abides by the ubiquitous bum steer, “I don’t have any experience trying to do what you’re doing, but just use ``float``, bro.”

    Because, hey, *🤬* numbers!
    Am I right?

This madness should enjoy no audience.
It should not exist.
Yet here we are.
Its author gauges its success by how quickly it can be forgotten, relegated to the annals of superfluous folly.

``numerary`` is licensed under the [MIT License](https://opensource.org/licenses/MIT).
See the accompanying ``LICENSE`` file for details.
It should be considered experimental for now, but should settle down quickly.
See the [release notes](https://posita.github.io/numerary/0.1/notes/) for a summary of version-to-version changes.
Source code is [available on GitHub](https://github.com/posita/numerary).

If you find it lacking in any way, please don’t hesitate to [bring it to my attention](https://posita.github.io/numerary/0.1/contrib/).

## You had me at, “numbers and types can work together”

``numerary`` strives to define composable, *efficient* protocols that one can use to construct numeric requirements.
If all you deal with are integrals and reals, and what you want is broad arithmetic operator compatibility, this will probably get you where you likely want to go:

``` python
>>> from numerary import IntegralLike, RealLike

>>> def deeper_thot(arg: RealLike) -> IntegralLike:
...   assert arg != 0 and arg ** 0 == 1
...   return arg // arg + 42

```

Beyond default compositions for common use cases, ``numerary`` expands on the [``Supports`` pattern](https://docs.python.org/3/library/typing.html#protocols ) used in the standard library.
For example, ``numerary.types.SupportsIntegralOps`` is a [``@typing.runtime_checkable``](https://docs.python.org/3/library/typing.html#typing.runtime_checkable) protocol that approximates the unary and binary operators introduced by [``numbers.Integral``](https://docs.python.org/3/library/numbers.html#numbers.Integral).

``` python
>>> from numerary.types import SupportsIntegralOps

>>> def shift_right_one(arg: SupportsIntegralOps) -> SupportsIntegralOps:
...   assert isinstance(arg, SupportsIntegralOps)
...   return arg >> 1

>>> shift_right_one(2)
1

>>> from sympy import sympify
>>> two = sympify("2") ; type(two)
<class 'sympy.core.numbers.Integer'>
>>> res = shift_right_one(two) ; res
1
>>> type(res)
<class 'sympy.core.numbers.One'>

>>> from fractions import Fraction
>>> shift_right_one(Fraction(1, 2))  # type: ignore [arg-type]  # properly caught by Mypy
Traceback (most recent call last):
  ...
AssertionError

```

!!! note

    Until 1.9, ``sympy.core.numbers.Integer`` [lacked the requisite bitwise operators](https://github.com/sympy/sympy/issues/19311).
    ``numerary`` catches that!
    The above properly results in both a type-checking error as well as a runtime failure for [SymPy](https://www.sympy.org/) versions prior to 1.9.

 ``numerary``’s ``Supports`` protocols can be composed to refine requirements.
For example, let’s say one wanted to ensure type compatibility with primitives that support both ``__abs__`` and ``__divmod__``.

``` python
>>> from typing import TypeVar
>>> T_co = TypeVar("T_co", covariant=True)
>>> from numerary.types import (
...   CachingProtocolMeta, Protocol, runtime_checkable,
...   SupportsAbs, SupportsDivmod,
... )

>>> @runtime_checkable
... class MyType(
...   SupportsAbs[T_co], SupportsDivmod[T_co],
...   Protocol, metaclass=CachingProtocolMeta,
... ): pass

>>> my_type: MyType

>>> my_type = 3.5
>>> isinstance(my_type, MyType)
True
>>> abs(my_type)
3.5
>>> divmod(my_type, 2)
(1.0, 1.5)

>>> from fractions import Fraction
>>> my_type = Fraction(22, 7)
>>> isinstance(my_type, MyType)
True
>>> abs(my_type)
Fraction(22, 7)
>>> divmod(my_type, 2)
(1, Fraction(8, 7))

>>> from decimal import Decimal
>>> my_type = Decimal("5.2")
>>> isinstance(my_type, MyType)
True
>>> abs(my_type)
Decimal('5.2')
>>> divmod(my_type, 2)
(Decimal('2'), Decimal('1.2'))

>>> my_type = "nope"  # type: ignore [assignment]  # properly caught by Mypy
>>> isinstance(my_type, MyType)
False

```

Remember that scandal where [``complex`` defined exception-throwing comparators it wasn’t supposed to have, which confused runtime protocol checking, and then its type definitions lied about it to cover it up](https://posita.github.io/numerary/0.1/whytho/#lies-upon-lies-upon-lies-all-the-way-down)?
Yeah, that shit ends *here*.

``` python
>>> from numerary.types import SupportsRealOps
>>> isinstance(1.0, SupportsRealOps)  # all good
True
>>> has_real_ops: SupportsRealOps = complex(1)  # type: ignore [assignment]  # properly caught by Mypy
>>> isinstance(complex(1), SupportsRealOps)  # you're not fooling anyone, buddy
False

```

That is because ``numerary`` not only caches runtime protocol evaluations, but allows overriding those evaluations when the default machinery gets it wrong.

``` python
>>> from abc import abstractmethod
>>> from typing import Iterable, Union
>>> from numerary.types import CachingProtocolMeta, Protocol, runtime_checkable

>>> @runtime_checkable
... class SupportsOne(Protocol, metaclass=CachingProtocolMeta):
...   __slots__: Union[str, Iterable[str]] = ()
...   @abstractmethod
...   def one(self) -> int: pass

>>> class Imposter:
...   def one(self) -> str:
...     return "one"

>>> imp: SupportsOne = Imposter()  # type: ignore [assignment]  # properly caught by Mypy
>>> isinstance(imp, SupportsOne)  # fool me once, shame on you ...
True

>>> SupportsOne.excludes(Imposter)
>>> isinstance(imp, SupportsOne)  # ... can't get fooled again
False

```

``numerary`` has default overrides to correct for known oddities with native types (like our old friend, ``complex``) and with popular libraries like [``numpy``](https://numpy.org/) and [``sympy``](https://www.sympy.org/).
Others will be added as they are identified.
If I’ve missed any, or if you would like ``numerary`` to support additional number implementations out of the box, please [let me know](https://posita.github.io/numerary/0.1/contrib/#filing-issues).

## Performance Enhanced Protocols—A *different* kind of “PEP” for your step

By default, [protocols frustrate runtime type-checking performance](https://bugs.python.org/issue30505).

[A lot.](https://posita.github.io/numerary/0.1/whytho/#puh-roh-tih-caaahhhlllz)

``numerary`` applies two distinct, layered optimization strategies:

1. Cached ``__instancecheck__`` results for ``numerary``-defined protocols; and
2. Optional(-ish) short-circuit type enumerations.

### Cached ``__instancecheck__`` results

To understand why ``numerary`` protocols are faster for runtime checks, it helps to understand why non-``numerary`` protocols are so slow.
At runtime (i.e., via ``isinstance``), the [default ``Protocol`` implementation](https://github.com/python/cpython/blob/main/Lib/typing.py) delegates to ``_ProtocolMeta.__instancecheck__`` to perform a crude comparison of an instance’s callable attributes against the protocol’s.
More attributes means more comparisons.
Further, it performs these comparisons … Every. Single. 🤬ing. Time.

Protocols provided by ``numerary`` use instead [``CachingProtocolMeta``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.CachingProtocolMeta) as their meta class.
``CachingProtocolMeta`` derives from ``_ProtocolMeta`` and overrides ``__instancecheck__ `` to cache the default implementation’s results based on instance type.

Conceptually:

``` python
>>> isinstance(1, SupportsIntegralOps)  # first check for an int is delegated to _ProtcolMeta.__instancecheck__
True
>>> isinstance(2, SupportsIntegralOps)  # cached result
True
>>> isinstance(1.0, SupportsIntegralOps)  # the first check for a float is delegated to _ProtcolMeta.__instancecheck__
False
>>> isinstance(2.0, SupportsIntegralOps)  # cached result
False

```

These offer significant performance improvements, especially where protocols define many methods.

``` python
--8<-- "docs/perf_supports_complex.out"
```

<details>
<summary>Source: <a href="https://github.com/posita/numerary/blob/v0.1.0/docs/perf_supports_complex.ipy"><code>perf_supports_complex.ipy</code></a></summary>

``` python
--8<-- "docs/perf_supports_complex.ipy"
```
</details>

### Short-circuit type enumerations

If the interface is to be used most often with native types (``int``s, ``float``s, ``bool``s), an additional optimization may be had at runtime by short-circuiting protocol type-checking.

``…SCU`` objects provide ``Union``s for compliant types.
As one example, for the aforementioned ``SupportsIntegralOps``, ``numerary`` defines an additional interface.

``` python
SupportsIntegralOpsSCU = Union[int, bool, Integral, SupportsIntegralOps]
```

``` python
>>> from numerary.types import SupportsIntegralOpsSCU

>>> def shift_left_one(arg: SupportsIntegralOpsSCU) -> SupportsIntegralOpsSCU:
...   assert isinstance(arg, SupportsIntegralOps)
...   return arg << 1

>>> shift_left_one(1)
2
>>> shift_left_one(sympify("1"))
2
>>> shift_left_one(Fraction(1, 2))  # type: ignore [arg-type]
Traceback (most recent call last):
  ...
AssertionError

```

Where do ``…SCU`` protocols help?
In a word, *[``beartype``](https://pypi.org/project/beartype/)*.
``beartype`` is *awesome*.
Its author is even *awesomer*.[^4]
More generally, runtime checkers that inspect and enforce annotations may benefit from short-circuiting where protocol validation is expensive.

[^4]:

    I acknowledge that the subject of who is awesomer, beartype or the man who made it, is [hotly contested](https://github.com/beartype/beartype/issues/66#issuecomment-960495976).

``Union``s are *also* useful when trying to accommodate non-compliant primitives that fail static type-checking, but will work anyway at runtime.
``float``s in Python versions prior to 3.9 are an excellent example, because they officially lacked ``__floor__`` and ``__ceil__`` methods, but were registered with the numeric tower and worked just fine with ``math.floor`` and ``math.ceil``.

How do ``numerary``’s [``SupportsFloor``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.SupportsFloor) and [``SupportsCeil``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.SupportsCeil) deal with this situation?
Not super well on their own, unfortunately.

``` python
>>> import math
>>> from numerary.types import SupportsFloor

>>> def my_dumb_floor_func(arg: SupportsFloor) -> int:
...   assert isinstance(arg, SupportsFloor)  # will work, even for floats, thanks to default overrides
...   return math.floor(arg)  # type: ignore [arg-type]  # doesn't understand SupportsFloor

>>> my_dumb_floor_func(float(1.2))  # type: ignore [arg-type]  # still results in a Mypy error for Python version <3.9
1

```

``Union``s allow a work-around for the static type-checking issue.

``` python
>>> from numerary.types import SupportsFloor, SupportsFloorSCU, floor
>>> SupportsFloorSCU  # float is included here
typing.Union[int, float, bool, numbers.Real, numerary.types.SupportsFloor]

>>> import sys
>>> def my_floor_func(arg: SupportsFloorSCU) -> int:
...   assert isinstance(arg, SupportsFloor)
...   return floor(arg)

>>> my_floor_func(float(1.2))  # works in 3.7+
1

```

This is largely a contrived example, since ``math.floor`` and ``math.ceil`` happily accept ``SupportsFloat``, but it is useful for illustration.

### Limitations

There are some downsides, though.
(Aren’t there always?)

#### Sometimes protocols are too trusting

Protocols trust numeric tower registrations.
*TODO(@posita): Is this really true?*
But sometimes, out there in the real world, implementations *lie*.

Consider:

``` python
>>> from numbers import Integral
>>> hasattr(Integral, "real") and hasattr(Integral, "imag")
True
>>> import sympy.core.numbers
>>> pants_on_fire = sympy.core.numbers.Integer(1)
>>> isinstance(pants_on_fire, Integral)
True
>>> hasattr(pants_on_fire, "real") or hasattr(pants_on_fire, "imag")  # somebody's tellin' stories
False
>>> from numerary.types import SupportsRealImag
>>> real_imag: SupportsRealImag = pants_on_fire  # fails to detect the lie

```

#### Protocols loses fidelity during runtime checking

At runtime, protocols match *names*, not *signatures*.
For example, [``SupportsNumeratorDenominatorProperties``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.SupportsNumeratorDenominatorProperties)’s  ``numerator`` and ``denominator`` *properties* will match [``sage.rings.integer.Integer``](https://doc.sagemath.org/html/en/reference/rings_standard/sage/rings/integer.html#sage.rings.integer.Integer)’s similarly named *[functions](https://trac.sagemath.org/ticket/28234)*.
In other words, ``isinstance(sage_integer, SupportsNumeratorDenominatorProperties)`` will return ``True``.
Further, if the short-circuiting approach is used, because ``sage.rings.integer.Integer`` registers itself with the numeric tower, this *may*[^5] not be caught by Mypy.

[^5]:

    I say *may* because I don’t really understand how Sage’s number registrations work.

``` python
>>> class SageLikeRational:
...   def __init__(self, numerator: int, denominator: int = 1):
...     self._numerator = numerator
...     self._denominator = denominator
...   def numerator(self) -> int:
...     return self._numerator
...   def denominator(self) -> int:
...     return self._denominator

>>> from numerary.types import SupportsNumeratorDenominatorProperties
>>> frac: SupportsNumeratorDenominatorProperties = Fraction(29, 3)  # no typing error
>>> sage_rational1: SupportsNumeratorDenominatorProperties = SageLikeRational(29, 3)  # type: ignore [assignment]  # Mypy catches this
>>> isinstance(sage_rational1, SupportsNumeratorDenominatorProperties)  # isinstance does not
True
>>> sage_rational1.numerator
<...method...numerator...>
>>> frac.numerator
29

```

Known warts *could* be cured by cache overriding as discussed above.
However, to combat this particular situation, ``numerary`` provides an alternative: the [``SupportsNumeratorDenominatorMethods``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.SupportsNumeratorDenominatorMethods) protocol and the [``numerator``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.numerator) and [``denominator``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.denominator) helper functions.
These allow accommodation of rational implementations like Sage’s that are mostly compliant with the exception of their respective ``numerator`` and ``denominator`` implementations.

``` python
>>> from numerary.types import numerator
>>> numerator(sage_rational1)
29
>>> numerator(frac)
29

>>> from numerary.types import SupportsNumeratorDenominatorMethods, numerator
>>> sage_rational2: SupportsNumeratorDenominatorMethods = SageLikeRational(3, 29)  # no type error
>>> numerator(sage_rational2)
3

```

``numerary`` also defines:

``` python
SupportsNumeratorDenominatorMixedU = Union[
    SupportsNumeratorDenominatorProperties,
    SupportsNumeratorDenominatorMethods,
]
SupportsNumeratorDenominatorMixedT = (
    SupportsNumeratorDenominatorProperties,
    SupportsNumeratorDenominatorMethods,
)
```

``` python
>>> from numerary.types import SupportsNumeratorDenominatorMixedU, numerator
>>> chimera_rational: SupportsNumeratorDenominatorMixedU
>>> chimera_rational = Fraction(29, 3)  # no type error
>>> numerator(chimera_rational)
29
>>> chimera_rational = SageLikeRational(3, 29)  # still no type error
>>> numerator(chimera_rational)
3

```

The ``SupportsNumeratorDenominator*`` primitives provide the basis for analogous [``numerary.types.RationalLike*`` primitives](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.RationalLikeMethods), which *should* provide sufficient (if idiosyncratic) coverage for dealing with (seemingly mis-appropriately named) rationals.

#### Pass-through caching with composition implementation is pretty sketchy

This is really getting into where the sausage is made.
However, in the spirit of full transparency, this must be disclosed.

Let’s say we register an errant implementation as non-compliant.

``` python
>>> from numerary.types import SupportsFloat

>>> class FloatImposter:
...   def __float__(self) -> float:
...     raise NotImplementedError("Haha! JK! @#$% you!")
...   def __int__(self) -> int:
...     return 42

>>> float_imp = FloatImposter()
>>> isinstance(float_imp, SupportsFloat)
True
>>> SupportsFloat.excludes(FloatImposter)
>>> isinstance(float_imp, SupportsFloat)
False

```

For composition to be ergonomic, this registration should be indelible, survive composition, but allow overriding by inheritors.

``` python
>>> from numerary.types import (
...   CachingProtocolMeta, Protocol, runtime_checkable,
...   SupportsInt,
... )

>>> @runtime_checkable
... class MyFloatInt(
...   SupportsFloat, SupportsInt,
...   Protocol, metaclass=CachingProtocolMeta,
... ): pass

>>> isinstance(float_imp, MyFloatInt)  # picks up excludes override from SupportsFloat
False

>>> SupportsFloat.reset_for(FloatImposter)
>>> isinstance(float_imp, SupportsFloat)
True
>>> isinstance(float_imp, MyFloatInt)  # picks up resetting of SupportsFloat override
True

>>> MyFloatInt.excludes(FloatImposter)  # overrides in composition
>>> isinstance(float_imp, MyFloatInt)
False
>>> SupportsFloat.includes(FloatImposter)
>>> isinstance(float_imp, FloatImposter)
True
>>> isinstance(float_imp, MyFloatInt)  # overrides/resets in member protocols are hidden
False

>>> MyFloatInt.reset_for(FloatImposter)  # removes override in composition
>>> isinstance(float_imp, MyFloatInt)  # member protocol is visible again
True
>>> SupportsFloat.excludes(FloatImposter)
>>> isinstance(float_imp, MyFloatInt)
False

```

For this to work under the current implementation, we cannot rely exclusively on the [standard library’s implementation of ``__instancecheck__``](https://github.com/python/cpython/blob/main/Lib/typing.py), since it flattens and inspects all properties (with some proprietary exceptions) of all classes in order of the MRO, not just the current instance.
In lay terms, this means that an ancestor’s ``__instancecheck__`` cache is effectively hidden from its progeny.
Without intervention, that would require one to register exceptions with every inheritor, which would suck.

Overriding the behavior is problematic, because the standard library uses a non-public function called ``_get_protocol_attrs`` to perform its attribute enumeration.

[``CachingProtocolMeta``](https://posita.github.io/numerary/0.1/numerary.types/#numerary.types.CachingProtocolMeta) tries to work around this by importing ``_get_protocol_attrs`` and performing some set arithmetic to limit its evaluation to directly defined attributes, and then delegate ``isinstance`` evaluation to its ``__base__`` classes.
In doing so, it picks up its bases’ then-cached values, but at the cost of re-implementing the attribute check as well as taking a dependency on an implementation detail of the standard library, which creates a fragility.
Further, for post-inheritance updates, ``CachingProtocolMeta`` implements a simplistic publish/subscribe mechanism that dirties non-overridden caches in inheritors when member protocols caches are updated.
These are deliberate compromises.
(See the [implementation](https://github.com/posita/numerary/blob/v0.1.0/numerary/types.py) for details.)

One subtlety is that the implementation deviates from performing checks in MRO order (and may perform redundant checks).
This is probably fine as long as runtime comparisons remain limited to crude checks whether attributes merely exist.
It would likely fail if runtime checking becomes more sophisticated, at which time, this implementation will need to be revisited.
Hopefully by then, we can just delete ``numerary`` as the aspirationally unnecessary hack it is and move on with our lives.

## License

``numerary`` is licensed under the [MIT License](https://opensource.org/licenses/MIT).
See the included [``LICENSE``](https://posita.github.io/numerary/0.1/license/) file for details.
Source code is [available on GitHub](https://github.com/posita/numerary).

## Installation

Installation can be performed via [PyPI](https://pypi.python.org/pypi/numerary/).

``` sh
% pip install numerary
...
```

Alternately, you can download [the source](https://github.com/posita/numerary) and install manually.

``` sh
% git clone https://github.com/posita/numerary.git
...
% cd numerary
% python -m pip install .  # -or- python -c 'from setuptools import setup ; setup()' install .
...
```

### Requirements

``numerary`` requires a relatively modern version of Python:

* [CPython](https://www.python.org/) (3.7+)
* [PyPy](http://pypy.org/) (CPython 3.7+ compatible)

It has the following runtime dependencies:

* [``typing-extensions``](https://pypi.org/project/typing-extensions/) (with Python <3.9)

``numerary`` will opportunistically use the following, if available at runtime:

* [``beartype``](https://pypi.org/project/beartype/) for yummy runtime type-checking goodness (0.8+)
  [![Bear-ified™](https://raw.githubusercontent.com/beartype/beartype-assets/main/badge/bear-ified.svg)](https://beartype.rtfd.io/)

If you use ``beartype`` for type-checking your code that interacts with ``numerary``, but don’t want ``numerary`` to use it internally (e.g., for some strange reason), set the ``NUMERARY_BEARTYPE`` environment variable to a falsy[^6] value before ``numerary`` is loaded.

[^6]:

    I.E., one of: ``0``, ``off``, ``f``, ``false``, and ``no``.

See the [hacking quick-start](https://posita.github.io/numerary/0.1/contrib/#hacking-quick-start) for additional development and testing dependencies.

## Customers [![``numerary``-encumbered](https://raw.githubusercontent.com/posita/numerary/v0.1.0/docs/numerary-encumbered.svg)](https://posita.github.io/numerary/)

* [``dyce``](https://pypi.org/project/dyce/) - a pure-Python library for modeling arbitrarily complex dice mechanics and ~~mother~~ *birthing code base* of ``numerary``!
* The next one could be _you_! 👋

Do you have a project that suffers problems made slightly less annoying by ``numerary``?
[Let me know](https://posita.github.io/numerary/0.1/contrib/#filing-issues), and I’ll promote it here!

And don’t forget to do your part in perpetuating gratuitous badge-ification!

``` markdown
<!-- Markdown -->
As of version 0.4.1, ``dyce`` is
[![numerary-encumbered](https://raw.githubusercontent.com/posita/numerary/master/docs/numerary-encumbered.svg)][numerary-encumbered]!
[numerary-encumbered]: https://posita.github.io/numerary/ "numerary-encumbered"
```

``` rst
..
    reStructuredText - see https://docutils.sourceforge.io/docs/ref/rst/directives.html#image

As of version 0.4.1, ``dyce`` is |numerary-encumbered|!

.. |numerary-encumbered| image:: https://raw.githubusercontent.com/posita/numerary/master/docs/numerary-encumbered.svg
   :align: top
   :target: https://posita.github.io/numerary/
   :alt: numerary-encumbered
```

``` html
<!-- HTML -->
As of version 0.4.1, <code>dyce</code> is <a href="https://posita.github.io/numerary/"><img
  src="https://raw.githubusercontent.com/posita/numerary/master/docs/numerary-encumbered.svg"
  alt="numerary-encumbered"
  style="vertical-align: middle;"></a>!
```
