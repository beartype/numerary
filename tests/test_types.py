# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

from typing import Tuple

import pytest

from numerary import IntegralLikeT, RealLikeT
from numerary.bt import beartype

__all__ = ()


# ---- Tests ---------------------------------------------------------------------------


def test_beartype_detection() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")

    @beartype
    def _real_like_identity(arg: RealLikeT) -> RealLikeT:
        return arg

    with pytest.raises(roar.BeartypeException):
        _real_like_identity("-273")  # type: ignore

    @beartype
    def _lies_all_lies(arg: RealLikeT) -> Tuple[str]:
        return (arg,)  # type: ignore

    with pytest.raises(roar.BeartypeException):
        _lies_all_lies(-273)


def test_beartype_validators() -> None:
    roar = pytest.importorskip("beartype.roar", reason="requires beartype")
    from beartype.vale import Is

    from numerary.types import Annotated

    NonZero = Annotated[IntegralLikeT, Is[lambda x: x != 0]]

    @beartype
    def _divide_it(n: IntegralLikeT, d: NonZero) -> RealLikeT:
        return n / d

    with pytest.raises(roar.BeartypeException):
        _divide_it(0, 0)

    with pytest.raises(roar.BeartypeException):
        _divide_it(0, "1")  # type: ignore

    If = Annotated[
        Tuple[str, ...],
        Is[
            lambda x: x
            == (
                "If you can dream—and not make dreams your master;",
                "If you can think—and not make thoughts your aim;",
            )
        ],
    ]

    @beartype
    def _if(lines: If) -> Tuple[str, ...]:
        return (
            "If you can meet with Triumph and Disaster",
            "And treat those two impostors just the same;",
        )

    with pytest.raises(roar.BeartypeException):
        _if(())
