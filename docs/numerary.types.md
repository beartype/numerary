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

# ``#!python numerary.types`` package reference

!!! warning "Experimental"

    This package is an attempt to ease compatibility between Python’s numbers and types.
    If that sounds like it shouldn’t be a thing, you won’t get any argument out of me.
    Anyhoo, this package should be considered experimental.
    I am working toward stability as quickly as possible, but be warned that future release may introduce incompatibilities or remove this package altogether.
    [Feedback, suggestions, and contributions](contrib.md) are desperately appreciated.

In addition to the following protocols and helper functions, ``numerary.types`` also resolves importing ``Annotated``, ``Protocol``, and ``runtime_checkable`` from the best available source.
This can be helpful if you need to support Python versions prior to 3.9, but don’t want to take a runtime dependency on ``typing_extensions`` unless needed.
Instead of doing this all over the place …

``` python
try:
  from typing import Annotated, Protocol, runtime_checkable
except ImportError:
  from typing_extensions import Annotated, Protocol, runtime_checkable
```

… you can do this instead …

``` python
from numerary.types import Annotated, Protocol, runtime_checkable
```

Bang.
Done.

Further, if you want to opportunistically take advantage of [``beartype``](https://pypi.org/project/beartype/) without imposing a strict runtime dependency, you can do this:

``` python
from numerary.bt import beartype  # will resolve to the identity decorator if beartype is unavailable at runtime
```

::: numerary.types
    rendering:
      show_if_no_docstring: false
      show_root_heading: false
      show_root_toc_entry: false
    selection:
      members:
        - "CachingProtocolMeta"
        - "RationalLikeProperties"
        - "RationalLikeMethods"
        - "SupportsAbs"
        - "SupportsComplex"
        - "SupportsFloat"
        - "SupportsInt"
        - "SupportsIndex"
        - "SupportsRound"
        - "SupportsConjugate"
        - "SupportsRealImag"
        - "SupportsTrunc"
        - "SupportsFloor"
        - "SupportsCeil"
        - "SupportsDivmod"
        - "SupportsNumeratorDenominatorProperties"
        - "SupportsNumeratorDenominatorMethods"
        - "SupportsComplexOps"
        - "SupportsComplexPow"
        - "SupportsRealOps"
        - "SupportsIntegralOps"
        - "SupportsIntegralPow"
        - "trunc"
        - "floor"
        - "ceil"
        - "numerator"
        - "denominator"

<!---
  See <https://github.com/mkdocstrings/mkdocstrings/issues/333>
-->
::: numerary.types
    rendering:
      show_if_no_docstring: true
      show_root_heading: false
      show_root_toc_entry: false
    selection:
      members:
        - "RationalLikeMixedT"
        - "RationalLikeMixedU"
        - "_SupportsAbs"
        - "_SupportsComplex"
        - "_SupportsFloat"
        - "_SupportsInt"
        - "_SupportsIndex"
        - "_SupportsRound"
        - "_SupportsConjugate"
        - "_SupportsRealImag"
        - "_SupportsTrunc"
        - "_SupportsFloor"
        - "_SupportsCeil"
        - "_SupportsDivmod"
        - "_SupportsNumeratorDenominatorProperties"
        - "_SupportsNumeratorDenominatorMethods"
        - "SupportsNumeratorDenominatorMixedT"
        - "SupportsNumeratorDenominatorMixedU"
        - "_SupportsComplexOps"
        - "_SupportsComplexPow"
        - "_SupportsRealOps"
        - "_SupportsIntegralOps"
        - "_SupportsIntegralPow"
