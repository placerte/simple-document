"""Public API for simdoc."""

from ._errors import SimDocError
from .doc import Doc

__all__ = ["Doc", "SimDocError"]
