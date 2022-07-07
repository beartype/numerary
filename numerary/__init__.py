# ======================================================================================
# Copyright and other protections apply. Please see the accompanying LICENSE file for
# rights and restrictions governing use of this software. All rights not expressly
# waived or licensed are reserved. If that file is missing or appears to be modified
# from its original, then please contact the author before viewing or using this
# software in any capacity.
# ======================================================================================

from __future__ import annotations

from typing import Tuple, Union

from .types import *  # noqa: F401,F403

__all__ = ()

_VersionT = Union[
    Tuple[int, int, int],
    Tuple[int, int, int, str],
    Tuple[int, int, int, str, str],
    Tuple[int, int, int, str, str, str],
]

__version__: _VersionT
__vers_str__: str

try:
    from ._version import __vers_str__, __version__
except Exception:
    __version__ = (0, 0, 0, "post0", "unknown", "d00000000")
    __vers_str__ = "0.0.0.post0+unknown.d00000000"
