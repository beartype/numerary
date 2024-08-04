# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

import os
from typing import TYPE_CHECKING, TypeVar

__all__ = ("beartype",)


# ---- Types ---------------------------------------------------------------------------


_T = TypeVar("_T")


# ---- Functions -----------------------------------------------------------------------


def identity(__: _T) -> _T:
    return __


# ---- Initialization ------------------------------------------------------------------


_NUMERARY_BEARTYPE = os.environ.get("NUMERARY_BEARTYPE", "no")
_truthy = ("on", "t", "true", "yes")
_falsy = ("off", "f", "false", "no")
_use_beartype_internally: bool

try:
    _use_beartype_internally = bool(int(_NUMERARY_BEARTYPE))
except ValueError:
    if _NUMERARY_BEARTYPE.lower() in _truthy:
        _use_beartype_internally = True
    elif _NUMERARY_BEARTYPE.lower() in _falsy:
        _use_beartype_internally = False
    else:
        raise EnvironmentError(
            f"""unrecognized value ({_NUMERARY_BEARTYPE}) for NUMERARY_BEARTYPE environment variable (should be "{'", "'.join(_truthy + _falsy)}", or an integer)"""
        )

if TYPE_CHECKING or not _use_beartype_internally:
    beartype = identity
else:
    from beartype import beartype as _beartype

    beartype = _beartype
