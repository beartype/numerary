<!---
  Copyright and other protections apply. Please see the accompanying LICENSE file for
  rights and restrictions governing use of this software. All rights not expressly
  waived or licensed are reserved. If that file is missing or appears to be modified
  from its original, then please contact the author before viewing or using this
  software in any capacity.

  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  !!!!!!!!!!!!!!! IMPORTANT: READ THIS BEFORE EDITING! !!!!!!!!!!!!!!!
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  Please keep each sentence on its own unwrapped line.
  It looks like crap in a text editor, but it has no effect on rendering, and it allows much more useful diffs.
  Thank you!
-->

This story may feel familiar.
If it does, you are in good company.
Your pain is my pain.
May it motivate us to grow and adapt.

## The calculation function—An allegory

We have a simple vision.
We want to define an API that works with *reals* (not just ``float``s), performs a calculation, and returns *integers* (not just ``int``s).

``` python
>>> def deep_thought(arg):
...   from time import sleep
...   sleep(7_500_000 * 365.24219265 * 24 * 60 * 60)  # doctest: +SKIP
...   assert arg != 0 and arg ** 0 == 1
...   return 42

```

### Native primitives

We want to tell the world how to call it and what to expect in return, so we annotate it:

``` python
>>> def deep_thought_typed(arg: float) -> int:
...   assert arg != 0 and arg ** 0 == 1
...   return 42

```

So simple!
We’re done, right?
Not quite.
We find that the runtime works well, but we’re Mypy errors.

``` python
>>> deep_thought_typed(1.0)  # this is fine ...
42
>>> from fractions import Fraction
>>> deep_thought_typed(Fraction(1, 2))  # type: ignore [arg-type]  # ... but this fails
42

```

Without the ``# type: ignore``, we get:

```
…: error: Argument 1 to "deep_thought_typed" has incompatible type "Fraction"; expected "float"
```

### Numeric tower

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
What could be simpler?
It appears a small tweak is all that is required!

``` python
>>> def deep_thought_towered(arg: Real) -> Integral:
...   assert arg != 0 and arg ** 0 == 1
...   return 42  # type: ignore [return-value]  # now this fails

```

Without the ``# type: ignore``, we get:

```
…: error: Incompatible return value type (got "int", expected "Integral")
```

Hold the phone.
``isinstance(42, Integral)`` was ``True``, was it not?
This is starting to get confusing.

### Erm … we mean native primitives *or* the numeric tower?

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
>>> deep_thought_crumbling(Decimal("0.123"))  # type: ignore [arg-type]  # fail
42

```

Without the ``# type: ignore``, we get:

```
…: error: Argument 1 to "deep_thought_crumbling" has incompatible type "Decimal"; expected "Union[float, Real]"
```

### Native primitives, the numeric tower, or other things that define all the methods, but didn’t (or couldn’t) register in the numeric tower for some reason

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

### Protocols!

*Can* we fix this with protocols?
The standard library provides [some simple precedents](https://docs.python.org/3/library/typing.html#protocols).

``` python
>>> try:
...   from typing import Protocol, runtime_checkable
... except ImportError:
...   from typing_extensions import Protocol, runtime_checkable  # type: ignore [misc]
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
>>> require_rational(1.0)  # type: ignore [arg-type]
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

### Puh … ROH … tih … *caaahhhlllz* … !

Let’s see how they perform.
First, let’s get a baseline.

``` python
--8<-- "docs/perf_rational_baseline.out"
```

<details>
<summary>Source: <a href="https://github.com/posita/numerary/blob/latest/docs/perf_rational_baseline.ipy"><code>perf_rational_baseline.ipy</code></a></summary>

``` python
--8<-- "docs/perf_rational_baseline.ipy"
```
</details>

Now let’s compare that with our two-property protocol.

``` python
--8<-- "docs/perf_rational_protocol.out"
```

<details>
<summary>Source: <a href="https://github.com/posita/numerary/blob/latest/docs/perf_rational_protocol.ipy"><code>perf_rational_protocol.ipy</code></a></summary>

``` python
--8<-- "docs/perf_rational_protocol.ipy"
```
</details>

That’s *forty times* slower. 😶
And that’s just with a two-property protocol.
How much worse would it be if we had enumerated all the dunder methods? 😰

``` python
--8<-- "docs/perf_rational_big_protocol.out"
```

<details>
<summary>Source: <a href="https://github.com/posita/numerary/blob/latest/docs/perf_rational_big_protocol.ipy"><code>perf_rational_big_protocol.ipy</code></a></summary>

``` python
--8<-- "docs/perf_rational_big_protocol.ipy"
```
</details>

Over. Four. Hundred. Times. Slower.
And that’s not even *all* the methods!

![Holy moly!](https://c.tenor.com/DZrc0EXTCLgAAAAM/holy-mother-forking-shirt-balls-oh-my-god.gif)

You know what?
Never mind that.
Where there’s a will, there’s a way.
Note to self, “Solve the performance problems with protocols later, but we’re *definitely* onto something!”

### Lies! Upon lies! Upon lies! All the way down!

Let’s do another one.
Real numbers have comparisons that complex ones don’t.
That seems as good a place as any to tackle next.

``` python
>>> try:
...   from typing import Protocol, runtime_checkable
... except ImportError:
...   from typing_extensions import Protocol, runtime_checkable  # type: ignore [misc]

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
>>> require_real(complex(0))  # type: ignore [arg-type]  # should go ka-boom!

```

Where was the ka-boom?
[There was *supposed* to be an earth-shattering ka-boom!](https://youtu.be/t9wmWZbr_wQ)
Mypy spotted the error.
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
>>> complex(0).__le__  # type: ignore [operator]
<...method...complex...>

```

What the shit?
Do they work?

``` python
>>> complex(0) <= complex(0)  # type: ignore [operator]
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

## What do we do?!

Okay.
Can we still work with any of this shit *and* have type-checking?
Let’s try.
Because *somebody* 🤬ing has to.
