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
[![Version](https://img.shields.io/pypi/v/numerary/0.0.4.svg)](https://pypi.org/project/numerary/0.0.4/)
[![Development Stage](https://img.shields.io/pypi/status/numerary/0.0.4.svg)](https://pypi.org/project/numerary/0.0.4/)
[![License](https://img.shields.io/pypi/l/numerary/0.0.4.svg)](https://github.com/me-shaon/GLWTPL/blob/master/NSFW_LICENSE)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/numerary/0.0.4.svg)](https://pypi.org/project/numerary/0.0.4/)
[![Supported Python Implementations](https://img.shields.io/pypi/implementation/numerary/0.0.4.svg)](https://pypi.org/project/numerary/0.0.4/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Bear-ified™](https://raw.githubusercontent.com/beartype/beartype-assets/main/badge/bear-ified.svg)](https://beartype.rtfd.io/)

Are you defining a numeric interface that should work with more than just ``int``s and ``float``s?
Are you annotating that interface for documentation *and* type checking?
Were you excited by [PEP 3141](https://www.python.org/dev/peps/pep-3141/)’s glitz and gloss promising a clean, straightforward number type definition mechanism, only to learn the hard way—after many hours of searching, tweaking, hacking, and testing ever more convoluted code, again and again—that you could’t actually make it work with Python’s type checking system?
Do you now wonder whether numbers were something new to computing in general because nothing else would explain such a gaping hole in a programming language so popular with the STEM crowd that has been around since the early 1990s?
Does the number [3186](https://github.com/python/mypy/issues/3186) haunt you in your dreams?
Do you find yourself shouting to no one in particular, “There *has* to be a better way?”

Well I’m here to tell you there ain’t.
But until there is, there’s …

# *``numerary`` - Now with Protocol Power™*

That’s right!

For a hopefully limited time, you too can benefit from someone else’s deranged work-arounds for the enormous chasms in Python that lie between the esoteric fields of computation that are “typing” and “numbers” instead of having to develop your own ~~out of sheer desperation~~ *from first principles*!

``numerary`` is a pure-Python codified rant for signaling that your interface is usable with non-native numeric primitives[^1] without breaking type checking.
If you’re thinking that you shouldn’t need a 🤬ing library for that, *you’re right*.

[^1]:

    You know, *super* weird, off-the-wall shit, like members of the [numeric tower](https://docs.python.org/3/library/numbers.html), or [standard library primitives that remain *non*-members for some 🤬ed up reason](https://docs.python.org/3/library/decimal.html), or [legitimate non-members because they predate PEP 3141 and conforming would amount to breaking changes](https://trac.sagemath.org/ticket/28234), or—I don’t know—oodles of libraries and applications that have been around for literally decades that bring huge value to vast scientific and mathematic audiences, but whose number primitives break type checking if one abides by the ubiquitous bum steer, “I don’t have any experience trying to do what you’re doing, but just use ``float``, bro.”

    Because, hey, *🤬* numbers!
    Am I right?

``numerary`` should enjoy no audience.
It should not exist.
Yet here we are.
Its author gauges its success by how quickly it can be deleted as superfluous.
(I’m looking at you, maintainers.)

``numerary`` is licensed under the [GLWTS License](https://github.com/me-shaon/GLWTPL/blob/master/NSFW_LICENSE) (NSFW version *only*) and comes with absolutely zero warranty for any purpose whatsoever.
See the accompanying ``LICENSE`` file for details.
It should be considered experimental for now, but should settle down quickly.
See the [release notes](https://posita.github.io/numerary/0.0/notes/) for a summary of version-to-version changes.
Source code is [available on GitHub](https://github.com/posita/numerary).

If you find it lacking in any way, please don’t hesitate to [bring it to my attention](https://posita.github.io/numerary/0.0/contrib/).

## Customers [![``numerary``-encumbered!](https://raw.githubusercontent.com/posita/numerary/v0.0.4/docs/numerary-encumbered.svg)](https://posita.github.io/numerary/)

* [``dyce``](https://pypi.org/project/dycelib/) - a pure-Python library for modeling arbitrarily complex dice mechanics and ~~mother~~ *birthing code base* 🙄 of ``numerary``!
* The next one could be _you_! 👋

Do you have a project that suffers problems made slightly less annoying by ``numerary``?
[Let me know](https://posita.github.io/numerary/0.0/contrib/#filing-issues), and I’ll promote it here!

And don’t forget to do your part in perpetuating gratuitous badge-ification!

``` markdown
<!-- Markdown -->
As of version 0.4.1, ``dyce`` is
[![numerary-encumbered](https://raw.githubusercontent.com/posita/numerary/master/docs/numerary-encumbered.svg)][numerary-encumbered]!
[numerary-encumbered]: https://posita.github.io/numerary/ "numerary-encumbered!"
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

## The calculation function, an allegory

We have a simple vision.
We want to define an API that works with *reals* (not just ``float``s), performs a calculation, and returns *integers* (not just ``int``s).

``` python
>>> from time import sleep
>>> def deep_thought(arg):
...   sleep(7_500_000 * 365.24219265 * 24 * 60 * 60)  # doctest: +SKIP
...   assert arg != 0 and arg ** 0 == 1
...   return 42

```

We want to tell the world how to call it and what to expect in return, so we annotate it:

``` python
>>> def deep_thought_typed(arg: float) -> int:
...   assert arg != 0 and arg ** 0 == 1
...   return 42

```

So simple!
We’re done, right?
Not quite.
We find that the runtime works well, but we’re getting type checking errors.

``` python
>>> deep_thought_typed(1.0)  # this is fine ...
42
>>> from fractions import Fraction
>>> deep_thought_typed(Fraction(1, 2))  # type: ignore  # ... but this fails
42

```

Without the ``# type: ignore``, we get:

```
…: error: Argument 1 to "deep_thought_typed" has incompatible type "Fraction"; expected "float"
```

With a little research, we learn about *the [numeric tower](https://docs.python.org/3/library/numbers.html) [cue angelic singing]*.
Surely, it has the answer!
Both ``float`` and ``Fraction`` are ``Real``s.
Let’s test that to make sure.

``` python
>>> from numbers import Integral, Real
>>> isinstance(42, Integral)
True
>>> isinstance(1.0, Real)
True
>>> isinstance(Fraction(1, 2), Real)
True

```

Huzzah!
What could be simpler!
A small tweak is all that is required.

``` python
>>> def deep_thought_towered(arg: Real) -> Integral:
...   assert arg != 0 and arg ** 0 == 1
...   return 42  # type: ignore  # now this fails

```

Without the ``# type: ignore``, we get:

```
…: error: Incompatible return value type (got "int", expected "Integral")
```

Hold the phone.
``isinstance(42, Integral)`` was ``True``, was it not?
This is starting to get confusing.

``` python
>>> from typing import Union
>>> IntegralT = Union[int, Integral]
>>> RealT = Union[float, Real]
>>> def deep_thought_crumbling(arg: RealT) -> IntegralT:
...   assert arg != 0 and arg ** 0 == 1
...   return 42

```

Well, that was *odd*, but such warts are a small price to pay.
All is right in the world again!

``` python
>>> deep_thought_crumbling(1.0)
42
>>> deep_thought_crumbling(Fraction(1, 2))
42
>>> from decimal import Decimal
>>> deep_thought_crumbling(Decimal("0.123"))  # type: ignore  # fails
42

```

Without the ``# type: ignore``, we get:

```
…: error: Argument 1 to "deep_thought_crumbling" has incompatible type "Decimal"; expected "Union[float, Real]"
```

Oh, come *on*!

``` python
>>> RealAndDecimalT = Union[float, Real, Decimal]
>>> def deep_thought_toppled(arg: RealAndDecimalT) -> IntegralT:
...   assert arg != 0 and arg ** 0 == 1
...   return 42
>>> deep_thought_toppled(Decimal("0.123"))
42

```

🤬 me.
If we have to engage in these kinds of gymnastics just to reach escape velocity from the standard library, how the heck are we supposed to survive contact with numeric implementations we haven’t even heard of yet?!
We can’t enumerate them *all*!

For many years, the numeric tower was declared a “dead end” by maintainers.
Unsurprisingly, many longstanding library authors didn’t see much benefit to conforming to its API.
Adoption has grown, but we can’t rely on it.

What *should* we rely on, then?
Surely the exalted few who have steered us *away* from one thing are prepared to steer us *toward* something else, no?
Sadly, the apparent attitude of many seems to be, “Something, something, protocols? Meh. I don’t know. We’ll figure it out later.”

*Can* we fix this with protocols?
The standard library provides [some simple precedents](https://docs.python.org/3/library/typing.html#protocols).

``` python
>>> try:
...   from typing import Protocol, runtime_checkable
... except ImportError:
...   from typing_extensions import Protocol, runtime_checkable  # type: ignore
>>> from typing import Iterable, Union
>>> @runtime_checkable
... class SupportsNumeratorDenominator(Protocol):
...   __slots__: Union[str, Iterable[str]] = ()
...   @property
...   def numerator(self) -> int: pass
...   @property
...   def denominator(self) -> int: pass
>>> def require_rational(arg: SupportsNumeratorDenominator) -> None:
...   assert isinstance(arg, SupportsNumeratorDenominator)
>>> require_rational(1)
>>> require_rational(Fraction(1, 2))
>>> require_rational(1.0)  # type: ignore
Traceback (most recent call last):
  ...
AssertionError

```

Without the ``# type: ignore``, we get:

```
…: error: Argument 1 to "require_rational" has incompatible type "float"; expected "SupportsNumeratorDenominator"
…: note: "float" is missing following "SupportsNumeratorDenominator" protocol members:
…: note:     denominator, numerator
```

Oh.
My.
Godetia.
Could this be it?
Have we stumbled into the promised land?

Let’s see how they perform.
First, let’s get a baseline.

``` python
In [13]: %timeit -r10 isinstance(val, Rational)
326 ns ± 1.26 ns per loop (mean ± std. dev. of 10 runs, 1000000 loops each)

In [14]: val = Fraction(1, 2)

In [15]: %timeit -r10 isinstance(val, Rational)
329 ns ± 1.87 ns per loop (mean ± std. dev. of 10 runs, 1000000 loops each)

In [16]: val = 1.0

In [17]: %timeit -r10 isinstance(val, Rational)
351 ns ± 1.29 ns per loop (mean ± std. dev. of 10 runs, 1000000 loops each)
```

Now let’s compare that with our two-property protocol.

``` python
In [21]: val = 1

In [22]: %timeit -r10 isinstance(val, SupportsNumeratorDenominator)
12.2 µs ± 203 ns per loop (mean ± std. dev. of 10 runs, 100000 loops each)

In [23]: val = Fraction(1, 2)

In [24]: %timeit -r10 isinstance(val, SupportsNumeratorDenominator)
12.3 µs ± 62 ns per loop (mean ± std. dev. of 10 runs, 100000 loops each)

In [25]: val = 1.0

In [26]: %timeit -r10 isinstance(val, SupportsNumeratorDenominator)
12.4 µs ± 97.8 ns per loop (mean ± std. dev. of 10 runs, 100000 loops each)
```

That’s *forty times* slower. 😶
And that’s just with a two-property protocol.
How much worse would it be if we had enumerated all the dunder methods? 😰

You know what?
Never mind that.
Where there’s a will, there’s a way.
Note to self, “Solve the performance problems with protocols later, but we’re *definitely* onto something!”

Let’s do another one.
Real numbers have comparisons that complex ones don’t.
That seems as good a place as any to tackle next.

``` python
>>> try:
...   from typing import Protocol, runtime_checkable
... except ImportError:
...   from typing_extensions import Protocol, runtime_checkable  # type: ignore
>>> from abc import abstractmethod
>>> from typing import Any, Iterable, Union
>>> @runtime_checkable
... class SupportsRealComparisons(Protocol):
...   __slots__: Union[str, Iterable[str]] = ()
...   @abstractmethod
...   def __lt__(self, other: Any) -> bool: pass
...   @abstractmethod
...   def __le__(self, other: Any) -> bool: pass
...   @abstractmethod
...   def __ge__(self, other: Any) -> bool: pass
...   @abstractmethod
...   def __gt__(self, other: Any) -> bool: pass
>>> def require_real(arg: SupportsRealComparisons) -> None:
...   assert isinstance(arg, SupportsRealComparisons)
>>> require_real(1)
>>> require_real(Fraction(1, 2))
>>> require_real(1.0)
>>> require_real(complex(0))  # type: ignore  # should go ka-boom!

```

Where was the ka-boom?
[There was *supposed* to be an earth-shattering ka-boom!](https://youtu.be/t9wmWZbr_wQ)
Type checking spotted the error.
Without the ``# type: ignore``, we get:

```
…: error: Argument 1 to "require_real" has incompatible type "complex"; expected "SupportsRealComparisons"
```

So what gives?
Why does our protocol think a ``complex`` has comparisons at runtime?
It’s a complex number and complex numbers don’t have those.
The [standard library says so](https://docs.python.org/3/library/numbers.html#the-numeric-tower)!

``` python
>>> from numbers import Complex
>>> isinstance(complex(0), Complex)
True
>>> hasattr(Complex, "__le__")
True
>>> complex(0).__le__  # type: ignore
<...method...complex...>

```

What the shit?
Do they work?

``` python
>>> complex(0) <= complex(0)  # type: ignore
Traceback (most recent call last):
  ...
TypeError: '<=' not supported between instances of 'complex' and 'complex'

```

Wait.
Complex numbers implement comparisons *in complete contradiction to the documentation* just to return ``NotImplemented``?!
🤬 *off*!

How does Mypy know?
Because the type definitions for [``complex``](https://github.com/python/typeshed/blob/f4143c40e85db42dc98549e09329e196668395ee/stdlib/builtins.pyi#L304-L331) and [``Complex``](https://github.com/python/typeshed/blob/f4143c40e85db42dc98549e09329e196668395ee/stdlib/numbers.pyi#L11-L45) are lies that conveniently omit mention of those methods.

!!! quote

    “When it becomes serious, you have to lie.”

    —Jean-Claude Juncker

Do you see?!
Do you see now why we can’t have nice things?!
I mean, I get *casting* as a rare case, but who builds *sophisticated deception tooling* into the very fabric a type definition mechanism to claim that non-compliant native primitives comply?
How can you trust *anything* anymore?!
Shouldn’t that be a pretty strong hint that maybe you should step back and rethink your approach?

Astute readers may note [``beartype``](https://pypi.org/project/beartype/) could help restore Truth for us.

``` python
from beartype import beartype
from beartype.vale import Is
from typing import Annotated
SupportsRealComparisonsNotComplexLies = Annotated[
  SupportsRealComparisons, Is[lambda arg: not isinstance(arg, complex)]
]
@beartype
def require_real(arg: SupportsRealComparisonsNotComplexLies) -> None:
  assert isinstance(arg, SupportsRealComparisonsNotComplexLies)
```

That’s because Bear is hip to the scene.
Bear is *down*.
Bear knows what’s what.
If you have a typing problem, if no one else can help, and if you can find them[^2], maybe you can hire the Bear-Team.

[^2]:

    That should be easy
    I just gave you the [link](https://pypi.org/project/beartype/).
    *Twice*.

I digress.

Okay.
Can we still work with any of this shit *and* have type checking?
Dunno.
Let’s try.
Because *somebody* 🤬ing has to.

## A taste

``numerary`` strives to define composable, *efficient* protocols that one can use to construct numeric requirements.
It expands on the [``Supports`` pattern](https://docs.python.org/3/library/typing.html#protocols ) used in the standard library.

For example, ``numerary.types.SupportsIntegralOps`` is a [``@typing.runtime_checkable``](https://docs.python.org/3/library/typing.html#typing.runtime_checkable) protocol that approximates the binary operators introduced by [``numbers.Integral``](https://docs.python.org/3/library/numbers.html#numbers.Integral).

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
>>> shift_right_one(Fraction(1, 2))  # type: ignore  # properly caught by Mypy
Traceback (most recent call last):
  ...
AssertionError

```

!!! note

    Until 1.9, ``sympy.core.numbers.Integer`` [lacked the requisite bitwise operators](https://github.com/sympy/sympy/issues/19311).
    ``numerary`` catches that!
    The above properly results in both a type checking error as well as a runtime failure for [SymPy](https://www.sympy.org/) versions prior to 1.9.

By default, [protocols frustrate runtime type checking performance](https://bugs.python.org/issue30505).
``numerary`` applies two distinct, layered optimization strategies:

1. Cached ``__instancecheck__`` results for ``numerary``-defined protocols; and
2. Short-circuit type enumerations.

### Cached ``__instancecheck__`` results

It caches, so it’s faster.
[Bang. Done.](https://youtu.be/cCmNYP1k12w)
(NSFW warning.
Although, in retrospect, that warning probably should have been presented more prominently and earlier in this diatribe.)

*TODO(@posita): Describe how this works.*

### Short-circuit type enumerations

If the interface is to be used most often with native types (``int``s, ``float``s, ``bool``s) or those registered with the numeric tower, there is an optimization to be had at runtime by short-circuiting protocol type checking.
These come in two flavors.

1. ``…SCU`` objects which are ``Union``s for compliant types.
2. ``…SCT`` tuples, which are identical to the corresponding ``Union`` arguments. These are useful for runtime checks (e.g., as the second argument to ``isinstance``).

For example, for the aforementioned ``SupportsIntegralOps``, ``numerary`` defines two additional interfaces (some details and safeguards omitted).

``` python
SupportsIntegralOpsSCU = Union[int, bool, Integral, SupportsIntegralOps]
SupportsIntegralOpsSCT = (int, bool, Integral, SupportsIntegralOps)
```

``` python
>>> from numerary.types import SupportsIntegralOpsSCU  # for type annotations
>>> from numerary.types import SupportsIntegralOpsSCT  # for runtime checking
>>> def shift_left_one(arg: SupportsIntegralOpsSCU) -> SupportsIntegralOpsSCU:
...   assert isinstance(arg, SupportsIntegralOpsSCT)
...   return arg << 1
>>> shift_left_one(1)
2
>>> shift_left_one(sympify("1"))
2
>>> shift_left_one(Fraction(1, 2))  # type: ignore
Traceback (most recent call last):
  ...
AssertionError

```

Why two?
Because you can’t do this:

``` python
isinstance(1, Union[int, Integral])  # syntax error
```

And because Mypy is confused by this[^3]:

[^3]:

    Even though the syntax is legal and [``beartype``](https://pypi.org/project/beartype/) gladly does the right thing by treating the tuple literal as a ``Union``.
    Not sure if this is a bug or a feature, but my vote is for feature.

``` python
def my_func(arg: (int, Integral)):  # Mypy "syntax" error
  pass
```

So Python needs one thing for ``isinstance`` checks, and Mypy needs an entirely separate thing for annotations.
Yay. 😒

Does the ``Union`` provide *any* benefit?
Yes.
Because *[``beartype``](https://pypi.org/project/beartype/)*.
``beartype`` is *awesome*.
Its author is even *awesomer*.
More generally, runtime checkers that inspect and enforce annotations face problems similar to ``isinstance``.
Defining a ``Union`` provides an annotation analog for short-circuiting.

### Limitations

There are some downsides, though.
(Aren’t there always?)

#### Short-circuiting is too trusting

Short-circuiting trusts numeric tower registrations.
But sometimes, out there in the real world, implementations *lie*.

Consider:

``` python
>>> from numerary.types import SupportsRealImag, SupportsRealImagSCT
>>> hasattr(Integral, "real") and hasattr(Integral, "imag")
True
>>> one = sympify("1")
>>> isinstance(one, Integral)
True
>>> hasattr(one, "real") or hasattr(one, "imag")  # somebody's tellin' stories
False
>>> isinstance(one, SupportsRealImag)  # detects the lie
False
>>> isinstance(one, SupportsRealImagSCT)  # trusts the registration
True

```

#### Protocols lose fidelity at runtime

At runtime, protocols match *names*, not *signatures*.
More specifically, [``SupportsNumeratorDenominatorProperties``](https://posita.github.io/numerary/0.0/numerary.types/#numerary.types.SupportsNumeratorDenominatorProperties)’s  ``numerator`` and ``denominator`` *properties* will match [``sage.rings.integer.Integer``](https://doc.sagemath.org/html/en/reference/rings_standard/sage/rings/integer.html#sage.rings.integer.Integer)’s similarly named *[functions](https://trac.sagemath.org/ticket/28234)*.
In other words, ``isinstance(sage_integer, SupportsNumeratorDenominatorProperties)`` will return ``True``.
Further, if the short-circuiting approach is used, because ``sage.rings.integer.Integer`` registers itself with the numeric tower, this *may*[^4] not be caught by Mypy.

[^4]:

    I say *may* because I don’t really know how Sage’s number registrations work.

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
>>> sage_rational1: SupportsNumeratorDenominatorProperties = SageLikeRational(29, 3)  # type: ignore  # Mypy catches this
>>> isinstance(sage_rational1, SupportsNumeratorDenominatorProperties)  # isinstance does not
True
>>> sage_rational1.numerator
<...method...numerator...>
>>> frac.numerator
29

```

To combat this particular situation, ``numerary`` provides the [``SupportsNumeratorDenominatorMethods``](https://posita.github.io/numerary/0.0/numerary.types/#numerary.types.SupportsNumeratorDenominatorMethods) protocol and the [``numerator``](https://posita.github.io/numerary/0.0/numerary.types/#numerary.types.numerator) and [``denominator``](https://posita.github.io/numerary/0.0/numerary.types/#numerary.types.denominator) helper functions.

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

The ``SupportsNumeratorDenominator*`` primitives provide the basis for the analogous [``numerary.types.RationalLike*`` primitives](https://posita.github.io/numerary/0.0/numerary.types/#numerary.types.RationalLikeMethods), which *should* provide sufficient (if idiosyncratic) coverage for dealing with (seemingly mis-appropriately named) rationals.

### Shut up and take my money!

If all you deal with are integrals and reals, and what you want is arithmetic operator compatibility, but don’t do a ton of runtime checking, this should probably get you most of where you likely want to go:

``` python
>>> from numerary import IntegralLike, RealLike
>>> def deeper_thot(arg: RealLike) -> IntegralLike:
...   assert arg != 0 and arg ** 0 == 1
...   return arg // arg + 42

```

If your performance requirements demand them, consider the short-circuiting versions.

``` python
>>> from numerary import (
...   IntegralLikeSCT, IntegralLikeSCU,
...   RealLikeSCT, RealLikeSCU,
... )
>>> # ...

```

More examples coming soon.
I *promise*!
No, really.
Not a PEP promise.
A *real* one.
✌️😊

## License

``numerary`` is licensed under the [GLWTS License](https://github.com/me-shaon/GLWTPL/blob/master/NSFW_LICENSE) (NSFW version *only*).
See the included [``LICENSE``](https://posita.github.io/numerary/0.0/license/) file for details.
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

If you use ``beartype`` for type checking your code that interacts with ``numerary``, but don’t want ``numerary`` to use it internally (e.g., for performance reasons), set the ``NUMERARY_BEARTYPE`` environment variable to a falsy[^5] value before ``numerary`` is loaded.

[^5]:

    I.E., one of: ``0``, ``off``, ``f``, ``false``, and ``no``.

See the [hacking quick-start](https://posita.github.io/numerary/0.0/contrib/#hacking-quick-start) for additional development and testing dependencies.
