"""Runtime Adapter — canonical bridge between Runtime and Contracts.

The Runtime Adapter is the only layer authorized to know both
the Python Runtime and the Canonical Contracts simultaneously.

It translates Runtime entities, results, errors, and events into
the canonical formats defined in @ascend/contracts and ARCH-0026.

This layer contains zero business logic — it is a translation layer only.
"""

from .runtime_adapter import RuntimeAdapter

__all__ = ["RuntimeAdapter"]
